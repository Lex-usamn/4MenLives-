const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const cors = require('cors');
const { v4: uuidv4 } = require('uuid');
const mediasoup = require('mediasoup');

const app = express();
const server = http.createServer(app);

// Enable CORS for all routes
app.use(cors({
  origin: "*",
  methods: ["GET", "POST"],
  credentials: true
}));

app.use(express.json());

const io = socketIo(server, {
  cors: {
    origin: "*",
    methods: ["GET", "POST"],
    credentials: true
  }
});

// Mediasoup configuration
const mediaCodecs = [
  {
    kind: 'audio',
    mimeType: 'audio/opus',
    clockRate: 48000,
    channels: 2,
  },
  {
    kind: 'video',
    mimeType: 'video/VP8',
    clockRate: 90000,
    parameters: {
      'x-google-start-bitrate': 1000,
    },
  },
  {
    kind: 'video',
    mimeType: 'video/VP9',
    clockRate: 90000,
    parameters: {
      'profile-id': 2,
      'x-google-start-bitrate': 1000,
    },
  },
  {
    kind: 'video',
    mimeType: 'video/h264',
    clockRate: 90000,
    parameters: {
      'packetization-mode': 1,
      'profile-level-id': '4d0032',
      'level-asymmetry-allowed': 1,
      'x-google-start-bitrate': 1000,
    },
  },
];

// Global variables
let worker;
let router;
let rooms = new Map(); // roomId -> Room
let peers = new Map(); // socketId -> Peer

class Room {
  constructor(roomId) {
    this.id = roomId;
    this.peers = new Map(); // peerId -> Peer
    this.host = null;
  }

  addPeer(peer) {
    this.peers.set(peer.id, peer);
    if (!this.host) {
      this.host = peer.id;
    }
  }

  removePeer(peerId) {
    this.peers.delete(peerId);
    if (this.host === peerId && this.peers.size > 0) {
      this.host = this.peers.keys().next().value;
    }
  }

  getPeers() {
    return Array.from(this.peers.values());
  }
}

class Peer {
  constructor(socketId, roomId, name) {
    this.id = socketId;
    this.roomId = roomId;
    this.name = name;
    this.transports = new Map(); // transportId -> Transport
    this.producers = new Map(); // producerId -> Producer
    this.consumers = new Map(); // consumerId -> Consumer
    this.rtpCapabilities = null;
    this.isHost = false;
    this.connectionQuality = {
      latency: 0,
      packetsLost: 0,
      jitter: 0,
      quality: 'unknown'
    };
  }

  addTransport(transport) {
    this.transports.set(transport.id, transport);
  }

  addProducer(producer) {
    this.producers.set(producer.id, producer);
  }

  addConsumer(consumer) {
    this.consumers.set(consumer.id, consumer);
  }

  removeTransport(transportId) {
    this.transports.delete(transportId);
  }

  removeProducer(producerId) {
    this.producers.delete(producerId);
  }

  removeConsumer(consumerId) {
    this.consumers.delete(consumerId);
  }

  close() {
    // Close all transports
    for (const transport of this.transports.values()) {
      transport.close();
    }
    this.transports.clear();
    this.producers.clear();
    this.consumers.clear();
  }
}

// Initialize Mediasoup
async function initializeMediasoup() {
  try {
    worker = await mediasoup.createWorker({
      logLevel: 'warn',
      rtcMinPort: 10000,
      rtcMaxPort: 10100,
    });

    worker.on('died', () => {
      console.error('Mediasoup worker died, exiting...');
      process.exit(1);
    });

    router = await worker.createRouter({ mediaCodecs });
    console.log('Mediasoup initialized successfully');
  } catch (error) {
    console.error('Failed to initialize Mediasoup:', error);
    process.exit(1);
  }
}

// Socket.IO connection handling
io.on('connection', (socket) => {
  console.log(`Client connected: ${socket.id}`);

  socket.on('join-room', async (data) => {
    try {
      const { roomId, name, guestToken } = data;
      
      // Create or get room
      if (!rooms.has(roomId)) {
        rooms.set(roomId, new Room(roomId));
      }
      
      const room = rooms.get(roomId);
      const peer = new Peer(socket.id, roomId, name);
      
      // Add peer to room and global peers map
      room.addPeer(peer);
      peers.set(socket.id, peer);
      
      // Join socket room
      socket.join(roomId);
      
      console.log(`Peer ${name} joined room ${roomId}`);
      
      // Notify other peers in the room
      socket.to(roomId).emit('peer-joined', {
        peerId: socket.id,
        name: name
      });
      
      // Send current peers to the new peer
      const currentPeers = room.getPeers()
        .filter(p => p.id !== socket.id)
        .map(p => ({ peerId: p.id, name: p.name }));
      
      socket.emit('room-joined', {
        roomId,
        peers: currentPeers,
        routerRtpCapabilities: router.rtpCapabilities
      });
      
    } catch (error) {
      console.error('Error joining room:', error);
      socket.emit('error', { message: 'Failed to join room' });
    }
  });

  socket.on('get-router-rtp-capabilities', (callback) => {
    callback(router.rtpCapabilities);
  });

  socket.on('create-webrtc-transport', async (data, callback) => {
    try {
      const { direction } = data; // 'send' or 'recv'
      const peer = peers.get(socket.id);
      
      if (!peer) {
        callback({ error: 'Peer not found' });
        return;
      }

      const transport = await router.createWebRtcTransport({
        listenIps: [
          {
            ip: '0.0.0.0',
            announcedIp: '127.0.0.1', // Replace with your server's public IP in production
          },
        ],
        enableUdp: true,
        enableTcp: true,
        preferUdp: true,
      });

      transport.on('dtlsstatechange', (dtlsState) => {
        if (dtlsState === 'closed') {
          transport.close();
        }
      });

      peer.addTransport(transport);

      callback({
        id: transport.id,
        iceParameters: transport.iceParameters,
        iceCandidates: transport.iceCandidates,
        dtlsParameters: transport.dtlsParameters,
      });

    } catch (error) {
      console.error('Error creating WebRTC transport:', error);
      callback({ error: 'Failed to create transport' });
    }
  });

  socket.on('connect-transport', async (data, callback) => {
    try {
      const { transportId, dtlsParameters } = data;
      const peer = peers.get(socket.id);
      
      if (!peer) {
        callback({ error: 'Peer not found' });
        return;
      }

      const transport = peer.transports.get(transportId);
      if (!transport) {
        callback({ error: 'Transport not found' });
        return;
      }

      await transport.connect({ dtlsParameters });
      callback({ success: true });

    } catch (error) {
      console.error('Error connecting transport:', error);
      callback({ error: 'Failed to connect transport' });
    }
  });

  socket.on('produce', async (data, callback) => {
    try {
      const { transportId, kind, rtpParameters } = data;
      const peer = peers.get(socket.id);
      
      if (!peer) {
        callback({ error: 'Peer not found' });
        return;
      }

      const transport = peer.transports.get(transportId);
      if (!transport) {
        callback({ error: 'Transport not found' });
        return;
      }

      const producer = await transport.produce({
        kind,
        rtpParameters,
      });

      peer.addProducer(producer);

      producer.on('transportclose', () => {
        producer.close();
        peer.removeProducer(producer.id);
      });

      // Notify other peers about the new producer
      const room = rooms.get(peer.roomId);
      if (room) {
        socket.to(peer.roomId).emit('new-producer', {
          peerId: socket.id,
          producerId: producer.id,
          kind: producer.kind
        });
      }

      callback({ id: producer.id });

    } catch (error) {
      console.error('Error producing:', error);
      callback({ error: 'Failed to produce' });
    }
  });

  socket.on('consume', async (data, callback) => {
    try {
      const { transportId, producerId, rtpCapabilities } = data;
      const peer = peers.get(socket.id);
      
      if (!peer) {
        callback({ error: 'Peer not found' });
        return;
      }

      const transport = peer.transports.get(transportId);
      if (!transport) {
        callback({ error: 'Transport not found' });
        return;
      }

      // Check if we can consume
      if (!router.canConsume({ producerId, rtpCapabilities })) {
        callback({ error: 'Cannot consume' });
        return;
      }

      const consumer = await transport.consume({
        producerId,
        rtpCapabilities,
        paused: true,
      });

      peer.addConsumer(consumer);

      consumer.on('transportclose', () => {
        consumer.close();
        peer.removeConsumer(consumer.id);
      });

      consumer.on('producerclose', () => {
        consumer.close();
        peer.removeConsumer(consumer.id);
        socket.emit('consumer-closed', { consumerId: consumer.id });
      });

      callback({
        id: consumer.id,
        producerId: producerId,
        kind: consumer.kind,
        rtpParameters: consumer.rtpParameters,
      });

    } catch (error) {
      console.error('Error consuming:', error);
      callback({ error: 'Failed to consume' });
    }
  });

  socket.on('resume-consumer', async (data, callback) => {
    try {
      const { consumerId } = data;
      const peer = peers.get(socket.id);
      
      if (!peer) {
        callback({ error: 'Peer not found' });
        return;
      }

      const consumer = peer.consumers.get(consumerId);
      if (!consumer) {
        callback({ error: 'Consumer not found' });
        return;
      }

      await consumer.resume();
      callback({ success: true });

    } catch (error) {
      console.error('Error resuming consumer:', error);
      callback({ error: 'Failed to resume consumer' });
    }
  });

  socket.on('get-stats', async (data, callback) => {
    try {
      const peer = peers.get(socket.id);
      if (!peer) {
        callback({ error: 'Peer not found' });
        return;
      }

      const stats = {};
      
      // Get producer stats
      for (const [id, producer] of peer.producers) {
        stats[`producer-${id}`] = await producer.getStats();
      }
      
      // Get consumer stats
      for (const [id, consumer] of peer.consumers) {
        stats[`consumer-${id}`] = await consumer.getStats();
      }

      callback({ stats });

    } catch (error) {
      console.error('Error getting stats:', error);
      callback({ error: 'Failed to get stats' });
    }
  });

  socket.on('disconnect', () => {
    console.log(`Client disconnected: ${socket.id}`);
    
    const peer = peers.get(socket.id);
    if (peer) {
      // Close peer resources
      peer.close();
      
      // Remove from room
      const room = rooms.get(peer.roomId);
      if (room) {
        room.removePeer(socket.id);
        
        // Notify other peers
        socket.to(peer.roomId).emit('peer-left', {
          peerId: socket.id
        });
        
        // Remove room if empty
        if (room.peers.size === 0) {
          rooms.delete(peer.roomId);
        }
      }
      
      // Remove from global peers map
      peers.delete(socket.id);
    }
  });
});

// REST API endpoints
app.get('/health', (req, res) => {
  res.json({ 
    status: 'ok', 
    rooms: rooms.size, 
    peers: peers.size,
    timestamp: new Date().toISOString()
  });
});

app.get('/rooms', (req, res) => {
  const roomList = Array.from(rooms.entries()).map(([id, room]) => ({
    id,
    peerCount: room.peers.size,
    host: room.host
  }));
  res.json({ rooms: roomList });
});

app.get('/rooms/:roomId', (req, res) => {
  const { roomId } = req.params;
  const room = rooms.get(roomId);
  
  if (!room) {
    return res.status(404).json({ error: 'Room not found' });
  }
  
  const roomData = {
    id: room.id,
    host: room.host,
    peers: room.getPeers().map(peer => ({
      id: peer.id,
      name: peer.name,
      isHost: peer.isHost,
      connectionQuality: peer.connectionQuality
    }))
  };
  
  res.json(roomData);
});

// Guest page route
app.get('/guest/:token', (req, res) => {
  const { token } = req.params;
  
  const guestPageHTML = `
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>4MenLive - Convidado</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
        }
        
        .container {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 40px;
            text-align: center;
            max-width: 500px;
            width: 90%;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }
        
        h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
            background: linear-gradient(45deg, #fff, #f0f0f0);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .subtitle {
            font-size: 1.2rem;
            margin-bottom: 30px;
            opacity: 0.9;
        }
        
        .status {
            background: rgba(255, 255, 255, 0.2);
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
        }
        
        .token {
            font-family: 'Courier New', monospace;
            background: rgba(0, 0, 0, 0.3);
            padding: 10px;
            border-radius: 5px;
            margin: 10px 0;
            word-break: break-all;
        }
        
        .info {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 20px;
            margin-top: 20px;
            text-align: left;
        }
        
        .info h3 {
            margin-bottom: 15px;
            color: #fff;
        }
        
        .info ul {
            list-style: none;
            padding-left: 0;
        }
        
        .info li {
            margin: 8px 0;
            padding-left: 20px;
            position: relative;
        }
        
        .info li:before {
            content: "•";
            color: #4CAF50;
            font-weight: bold;
            position: absolute;
            left: 0;
        }
        
        .footer {
            margin-top: 30px;
            opacity: 0.7;
            font-size: 0.9rem;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>4MenLive</h1>
        <p class="subtitle">Você foi convidado para participar de uma transmissão ao vivo!</p>
        
        <div class="status">
            <h3>🎥 Convite Ativo</h3>
            <p>Token do Convidado:</p>
            <div class="token">${token}</div>
        </div>
        
        <div class="info">
            <h3>📋 Como participar:</h3>
            <ul>
                <li>Este link confirma que você foi convidado</li>
                <li>O host da transmissão irá te conectar durante a live</li>
                <li>Certifique-se de ter uma boa conexão de internet</li>
                <li>Teste sua câmera e microfone antes da transmissão</li>
                <li>Aguarde instruções do host para entrar na live</li>
            </ul>
        </div>
        
        <div class="info">
            <h3>🔧 Requisitos técnicos:</h3>
            <ul>
                <li>Navegador moderno (Chrome, Firefox, Safari, Edge)</li>
                <li>Câmera e microfone funcionando</li>
                <li>Conexão de internet estável (mínimo 5 Mbps)</li>
                <li>Permissões de câmera e microfone habilitadas</li>
            </ul>
        </div>
        
        <div class="footer">
            <p>Powered by 4MenLive Dashboard</p>
            <p>Sistema de streaming multicast profissional</p>
        </div>
    </div>
</body>
</html>
  `;
  
  res.send(guestPageHTML);
});

// Start server
const PORT = process.env.PORT || 3002;

async function startServer() {
  await initializeMediasoup();
  
  server.listen(PORT, '0.0.0.0', () => {
    console.log(`WebRTC server running on port ${PORT}`);
    console.log(`Health check: http://localhost:${PORT}/health`);
  });
}

startServer().catch(console.error);


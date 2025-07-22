# WebRTC Server para Dashboard de Streaming

Este servidor WebRTC implementa um SFU (Selective Forwarding Unit) usando Mediasoup para gerenciar conexões de convidados com baixa latência no dashboard de streaming.

## Funcionalidades

- **SFU (Selective Forwarding Unit)**: Gerencia múltiplas conexões WebRTC de forma eficiente
- **Baixa Latência**: Otimizado para comunicação em tempo real
- **Controle de Qualidade**: Monitoramento de latência, jitter e perda de pacotes
- **Salas Virtuais**: Suporte a múltiplas salas de streaming simultâneas
- **API REST**: Endpoints para monitoramento e controle
- **Socket.IO**: Comunicação em tempo real para sinalização WebRTC

## Arquitetura

### Componentes Principais

1. **Mediasoup Worker**: Processa mídia WebRTC
2. **Router**: Roteamento de streams de mídia
3. **Transports**: Conexões WebRTC individuais
4. **Producers**: Fontes de mídia (câmera, microfone)
5. **Consumers**: Receptores de mídia

### Fluxo de Conexão

1. Cliente se conecta via Socket.IO
2. Entra em uma sala virtual
3. Cria transports WebRTC (send/recv)
4. Produz mídia (vídeo/áudio)
5. Consome mídia de outros peers
6. Monitora qualidade da conexão

## API Endpoints

### Health Check
```
GET /health
```
Retorna status do servidor, número de salas e peers conectados.

### Listar Salas
```
GET /rooms
```
Lista todas as salas ativas com contagem de peers.

### Detalhes da Sala
```
GET /rooms/:roomId
```
Retorna informações detalhadas de uma sala específica.

## Socket.IO Events

### Cliente para Servidor

- `join-room`: Entrar em uma sala
- `create-webrtc-transport`: Criar transport WebRTC
- `connect-transport`: Conectar transport
- `produce`: Iniciar produção de mídia
- `consume`: Consumir mídia de outro peer
- `resume-consumer`: Retomar consumer pausado
- `get-stats`: Obter estatísticas de conexão

### Servidor para Cliente

- `room-joined`: Confirmação de entrada na sala
- `peer-joined`: Novo peer entrou na sala
- `peer-left`: Peer saiu da sala
- `new-producer`: Novo producer disponível
- `consumer-closed`: Consumer foi fechado

## Configuração

### Portas
- **Servidor HTTP**: 3002
- **WebRTC (UDP/TCP)**: 10000-10100

### Codecs Suportados
- **Áudio**: Opus (48kHz, 2 canais)
- **Vídeo**: VP8, VP9, H.264

## Uso

### Iniciar Servidor
```bash
npm start
```

### Teste com Cliente HTML
Abra `client-example.html` no navegador para testar as funcionalidades.

### Integração com Dashboard
O servidor pode ser integrado ao dashboard React através de:
1. Socket.IO client no frontend
2. Mediasoup-client para WebRTC
3. APIs REST para monitoramento

## Monitoramento

### Métricas Coletadas
- Latência RTT
- Perda de pacotes
- Jitter
- Bitrate de vídeo/áudio
- Qualidade da conexão

### Logs
O servidor registra eventos importantes:
- Conexões/desconexões de peers
- Criação/fechamento de transports
- Erros de mídia
- Estatísticas de performance

## Segurança

### Considerações
- Validação de tokens de convidado
- Limitação de peers por sala
- Rate limiting para eventos Socket.IO
- Validação de parâmetros WebRTC

### Produção
Para uso em produção, configure:
- HTTPS/WSS obrigatório
- IP público no `announcedIp`
- Firewall para portas WebRTC
- Certificados SSL válidos

## Integração com OBS Studio

O servidor pode ser integrado ao OBS através de:
1. **Plugin OBS personalizado**: Recebe streams WebRTC diretamente
2. **Virtual Camera**: Expõe streams como câmeras virtuais
3. **RTMP Relay**: Retransmite para servidor RTMP local

## Performance

### Otimizações
- Pool de workers Mediasoup
- Balanceamento de carga entre routers
- Compressão de vídeo adaptativa
- Priorização de tráfego por qualidade

### Limites Recomendados
- **Peers por sala**: 10-15
- **Streams simultâneos**: 30-50
- **Bitrate máximo**: 2 Mbps por peer

## Troubleshooting

### Problemas Comuns
1. **Porta em uso**: Altere a porta no arquivo de configuração
2. **Firewall**: Libere portas 10000-10100 para WebRTC
3. **NAT/STUN**: Configure STUN servers para NAT traversal
4. **Certificados**: Use HTTPS em produção

### Debug
Ative logs detalhados definindo:
```bash
DEBUG=mediasoup* node server.js
```


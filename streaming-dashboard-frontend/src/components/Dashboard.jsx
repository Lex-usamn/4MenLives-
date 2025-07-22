import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { 
  Play, 
  Square, 
  Users, 
  Eye, 
  MessageCircle, 
  Settings, 
  Plus,
  Wifi,
  WifiOff,
  Monitor,
  Video,
  Mic,
  MicOff
} from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts';

const Dashboard = () => {
  const [isStreaming, setIsStreaming] = useState(false);
  const [showSettings, setShowSettings] = useState(false);
  const [showAddGuest, setShowAddGuest] = useState(false);
  const [newGuest, setNewGuest] = useState({ name: '', email: '' });
  const [platforms, setPlatforms] = useState([
    { id: 1, name: 'Twitch', status: 'connected', viewers: 1247, isLive: false, color: 'bg-purple-500' },
    { id: 2, name: 'YouTube', status: 'connected', viewers: 3521, isLive: false, color: 'bg-red-500' },
    { id: 3, name: 'Facebook', status: 'connected', viewers: 892, isLive: false, color: 'bg-blue-500' },
    { id: 4, name: 'TikTok', status: 'disconnected', viewers: 0, isLive: false, color: 'bg-black' },
    { id: 5, name: 'Instagram', status: 'connected', viewers: 654, isLive: false, color: 'bg-pink-500' }
  ]);

  const [guests, setGuests] = useState([
    { id: 1, name: 'João Silva', status: 'connected', latency: 45, quality: 'good', videoEnabled: true, audioEnabled: true },
    { id: 2, name: 'Maria Santos', status: 'connected', latency: 67, quality: 'fair', videoEnabled: true, audioEnabled: false },
    { id: 3, name: 'Pedro Costa', status: 'disconnected', latency: 0, quality: 'unknown', videoEnabled: false, audioEnabled: false }
  ]);

  const [viewerData, setViewerData] = useState([
    { time: '10:00', viewers: 1200 },
    { time: '10:05', viewers: 1350 },
    { time: '10:10', viewers: 1480 },
    { time: '10:15', viewers: 1620 },
    { time: '10:20', viewers: 1750 },
    { time: '10:25', viewers: 1890 },
    { time: '10:30', viewers: 2100 }
  ]);

  const [latencyData, setLatencyData] = useState([
    { name: 'João', latency: 45 },
    { name: 'Maria', latency: 67 },
    { name: 'Pedro', latency: 0 }
  ]);

  const handleStartStream = () => {
    setIsStreaming(true);
    setPlatforms(prev => prev.map(p => 
      p.status === 'connected' ? { ...p, isLive: true } : p
    ));
  };

  const handleStopStream = () => {
    setIsStreaming(false);
    setPlatforms(prev => prev.map(p => ({ ...p, isLive: false })));
  };

  const handleOpenSettings = () => {
    setShowSettings(true);
  };

  const handleCloseSettings = () => {
    setShowSettings(false);
  };

  const handleOpenAddGuest = () => {
    setShowAddGuest(true);
  };

  const handleCloseAddGuest = () => {
    setShowAddGuest(false);
    setNewGuest({ name: '', email: '' });
  };

  const handleAddGuest = () => {
    if (newGuest.name.trim()) {
      const guestId = guests.length + 1;
      const inviteToken = Math.random().toString(36).substring(2, 15);
      const webrtcServerUrl = 'https://3002-inm5a11kid4aihi52iio3-2719d2cf.manusvm.computer';
      const inviteLink = `${webrtcServerUrl}/guest/${inviteToken}`;
      
      const newGuestData = {
        id: guestId,
        name: newGuest.name,
        email: newGuest.email,
        status: 'invited',
        latency: 0,
        quality: 'unknown',
        videoEnabled: false,
        audioEnabled: false,
        inviteToken,
        inviteLink
      };
      
      setGuests(prev => [...prev, newGuestData]);
      
      // Copiar link para clipboard
      navigator.clipboard.writeText(inviteLink).then(() => {
        alert(`Convidado adicionado! Link copiado para clipboard:\n${inviteLink}`);
      });
      
      handleCloseAddGuest();
    }
  };

  const downloadOBSConfig = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`https://vgh0i1coxgyk.manus.space/api/streaming/obs/config`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        const obsConfig = await response.json();
        
        // Adicionar informações específicas para 4MenLive
        const enhancedConfig = {
          ...obsConfig,
          project_name: "4MenLive Dashboard",
          generated_at: new Date().toISOString(),
          user_guide: {
            setup_steps: [
              "1. Abra o OBS Studio",
              "2. Vá em Configurações > Stream",
              "3. Selecione 'Serviço Personalizado'",
              "4. Configure cada plataforma usando as URLs e chaves abaixo",
              "5. Para streaming simultâneo, instale o plugin 'Multiple RTMP outputs'",
              "6. Configure cada output usando os dados fornecidos"
            ],
            multicast_plugin: {
              name: "Multiple RTMP outputs",
              download_url: "https://obsproject.com/forum/resources/multiple-rtmp-outputs-plugin.964/",
              installation: "Baixe e instale o plugin para transmitir simultaneamente"
            }
          },
          guest_integration: {
            webrtc_server: `${window.location.origin.replace(/:\d+/, ':3002')}`,
            instructions: [
              "Para adicionar convidados:",
              "1. Use a aba 'Convidados' no dashboard",
              "2. Clique em 'Convidar Amigo'",
              "3. Envie o link gerado para o convidado",
              "4. No OBS, adicione uma fonte 'Browser Source'",
              "5. Use a URL do convidado como fonte"
            ]
          }
        };

        const dataStr = JSON.stringify(enhancedConfig, null, 2);
        const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr);
        
        const exportFileDefaultName = '4menlive-obs-config.json';
        
        const linkElement = document.createElement('a');
        linkElement.setAttribute('href', dataUri);
        linkElement.setAttribute('download', exportFileDefaultName);
        linkElement.click();
        
        alert('Configuração do OBS baixada com sucesso!\nImporte este arquivo no OBS Studio para configurar o streaming multicast.');
      } else {
        throw new Error('Falha ao obter configurações do servidor');
      }
    } catch (error) {
      console.error('Erro ao baixar configuração OBS:', error);
      alert('Erro ao baixar configurações do OBS. Verifique sua conexão e tente novamente.');
    }
  };

  const totalViewers = platforms.reduce((sum, platform) => sum + platform.viewers, 0);
  const connectedPlatforms = platforms.filter(p => p.status === 'connected').length;
  const connectedGuests = guests.filter(g => g.status === 'connected').length;

  const getQualityColor = (quality) => {
    switch (quality) {
      case 'good': return 'bg-green-500';
      case 'fair': return 'bg-yellow-500';
      case 'poor': return 'bg-red-500';
      default: return 'bg-gray-500';
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 p-6">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Header */}
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
              Dashboard de Streaming
            </h1>
            <p className="text-gray-600 dark:text-gray-400">
              Gerencie suas transmissões simultâneas e convidados
            </p>
          </div>
          <div className="flex gap-3">
            {!isStreaming ? (
              <Button onClick={handleStartStream} className="bg-green-600 hover:bg-green-700">
                <Play className="w-4 h-4 mr-2" />
                Iniciar Stream
              </Button>
            ) : (
              <Button onClick={handleStopStream} variant="destructive">
                <Square className="w-4 h-4 mr-2" />
                Parar Stream
              </Button>
            )}
            <Button variant="outline" onClick={handleOpenSettings}>
              <Settings className="w-4 h-4 mr-2" />
              Configurações
            </Button>
          </div>
        </div>

        {/* Status Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total de Visualizadores</CardTitle>
              <Eye className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{totalViewers.toLocaleString()}</div>
              <p className="text-xs text-muted-foreground">
                +12% desde a última hora
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Plataformas Ativas</CardTitle>
              <Monitor className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{connectedPlatforms}/5</div>
              <p className="text-xs text-muted-foreground">
                {platforms.filter(p => p.isLive).length} transmitindo ao vivo
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Convidados Online</CardTitle>
              <Users className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{connectedGuests}</div>
              <p className="text-xs text-muted-foreground">
                {guests.length} convidados total
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Status do Stream</CardTitle>
              {isStreaming ? (
                <Wifi className="h-4 w-4 text-green-500" />
              ) : (
                <WifiOff className="h-4 w-4 text-gray-400" />
              )}
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {isStreaming ? 'AO VIVO' : 'OFFLINE'}
              </div>
              <p className="text-xs text-muted-foreground">
                {isStreaming ? 'Transmitindo agora' : 'Pronto para transmitir'}
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Main Content */}
        <Tabs defaultValue="platforms" className="space-y-4">
          <TabsList>
            <TabsTrigger value="platforms">Plataformas</TabsTrigger>
            <TabsTrigger value="guests">Convidados</TabsTrigger>
            <TabsTrigger value="analytics">Análises</TabsTrigger>
          </TabsList>

          <TabsContent value="platforms" className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {platforms.map((platform) => (
                <Card key={platform.id} className="relative">
                  <CardHeader>
                    <div className="flex items-center justify-between">
                      <CardTitle className="flex items-center gap-2">
                        <div className={`w-3 h-3 rounded-full ${platform.color}`}></div>
                        {platform.name}
                      </CardTitle>
                      <Badge variant={platform.status === 'connected' ? 'default' : 'secondary'}>
                        {platform.status === 'connected' ? 'Conectado' : 'Desconectado'}
                      </Badge>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-2">
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-muted-foreground">Visualizadores</span>
                        <span className="font-semibold">{platform.viewers.toLocaleString()}</span>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-muted-foreground">Status</span>
                        <Badge variant={platform.isLive ? 'destructive' : 'outline'}>
                          {platform.isLive ? 'AO VIVO' : 'OFFLINE'}
                        </Badge>
                      </div>
                      {platform.isLive && (
                        <div className="mt-2">
                          <div className="flex items-center gap-1 text-red-500">
                            <div className="w-2 h-2 bg-red-500 rounded-full animate-pulse"></div>
                            <span className="text-xs">Transmitindo</span>
                          </div>
                        </div>
                      )}
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </TabsContent>

          <TabsContent value="guests" className="space-y-4">
            <div className="flex justify-between items-center">
              <h3 className="text-lg font-semibold">Gerenciar Convidados</h3>
              <Button onClick={handleOpenAddGuest}>
                <Plus className="w-4 h-4 mr-2" />
                Convidar Amigo
              </Button>
            </div>
            
            <div className="grid gap-4">
              {guests.map((guest) => (
                <Card key={guest.id}>
                  <CardContent className="p-4">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-4">
                        <div className="flex items-center gap-2">
                          <div className={`w-3 h-3 rounded-full ${guest.status === 'connected' ? 'bg-green-500' : 'bg-gray-400'}`}></div>
                          <span className="font-medium">{guest.name}</span>
                        </div>
                        <Badge variant={guest.status === 'connected' ? 'default' : 'secondary'}>
                          {guest.status === 'connected' ? 'Conectado' : 'Desconectado'}
                        </Badge>
                      </div>
                      
                      <div className="flex items-center gap-4">
                        {guest.status === 'connected' && (
                          <>
                            <div className="flex items-center gap-2">
                              <span className="text-sm text-muted-foreground">Latência:</span>
                              <span className="font-mono text-sm">{guest.latency}ms</span>
                              <div className={`w-2 h-2 rounded-full ${getQualityColor(guest.quality)}`}></div>
                            </div>
                            
                            <div className="flex gap-2">
                              <Button
                                size="sm"
                                variant={guest.videoEnabled ? "default" : "outline"}
                              >
                                <Video className="w-4 h-4" />
                              </Button>
                              <Button
                                size="sm"
                                variant={guest.audioEnabled ? "default" : "outline"}
                              >
                                {guest.audioEnabled ? <Mic className="w-4 h-4" /> : <MicOff className="w-4 h-4" />}
                              </Button>
                            </div>
                          </>
                        )}
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </TabsContent>

          <TabsContent value="analytics" className="space-y-4">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle>Visualizadores ao Longo do Tempo</CardTitle>
                  <CardDescription>
                    Número total de visualizadores nas últimas horas
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={300}>
                    <LineChart data={viewerData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="time" />
                      <YAxis />
                      <Tooltip />
                      <Line 
                        type="monotone" 
                        dataKey="viewers" 
                        stroke="#8884d8" 
                        strokeWidth={2}
                        dot={{ fill: '#8884d8' }}
                      />
                    </LineChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Latência dos Convidados</CardTitle>
                  <CardDescription>
                    Latência atual de cada convidado conectado
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={latencyData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="name" />
                      <YAxis />
                      <Tooltip />
                      <Bar dataKey="latency" fill="#82ca9d" />
                    </BarChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>
            </div>
          </TabsContent>
        </Tabs>

        {/* Modal de Configurações */}
        {showSettings && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white dark:bg-gray-800 rounded-lg p-6 w-full max-w-2xl mx-4">
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Configurações</h2>
                <Button variant="ghost" onClick={handleCloseSettings}>
                  ✕
                </Button>
              </div>
              
              <div className="space-y-6">
                <div>
                  <h3 className="text-lg font-semibold mb-4">Configurações de Stream</h3>
                  <div className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium mb-2">Qualidade de Vídeo</label>
                      <select className="w-full p-2 border rounded-md">
                        <option>1080p 60fps</option>
                        <option>1080p 30fps</option>
                        <option>720p 60fps</option>
                        <option>720p 30fps</option>
                      </select>
                    </div>
                    <div>
                      <label className="block text-sm font-medium mb-2">Bitrate</label>
                      <input 
                        type="range" 
                        min="1000" 
                        max="8000" 
                        defaultValue="4000"
                        className="w-full"
                      />
                      <div className="flex justify-between text-sm text-gray-500">
                        <span>1000 kbps</span>
                        <span>8000 kbps</span>
                      </div>
                    </div>
                  </div>
                </div>

                <div>
                  <h3 className="text-lg font-semibold mb-4">Configurações de Áudio</h3>
                  <div className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium mb-2">Qualidade de Áudio</label>
                      <select className="w-full p-2 border rounded-md">
                        <option>320 kbps</option>
                        <option>256 kbps</option>
                        <option>192 kbps</option>
                        <option>128 kbps</option>
                      </select>
                    </div>
                    <div className="flex items-center space-x-2">
                      <input type="checkbox" id="noise-suppression" defaultChecked />
                      <label htmlFor="noise-suppression" className="text-sm">Supressão de ruído</label>
                    </div>
                  </div>
                </div>

                <div>
                  <h3 className="text-lg font-semibold mb-4">Configurações de Plataforma</h3>
                  <div className="space-y-4">
                    <div className="flex items-center space-x-2">
                      <input type="checkbox" id="auto-start" />
                      <label htmlFor="auto-start" className="text-sm">Iniciar automaticamente em todas as plataformas</label>
                    </div>
                    <div className="flex items-center space-x-2">
                      <input type="checkbox" id="notifications" defaultChecked />
                      <label htmlFor="notifications" className="text-sm">Notificações de status</label>
                    </div>
                    <div className="pt-4 border-t">
                      <Button onClick={downloadOBSConfig} variant="outline" className="w-full">
                        📥 Baixar Configurações do OBS
                      </Button>
                      <p className="text-xs text-gray-500 mt-2">
                        Baixe um arquivo de configuração para importar no OBS Studio
                      </p>
                    </div>
                  </div>
                </div>
              </div>

              <div className="flex justify-end gap-3 mt-6">
                <Button variant="outline" onClick={handleCloseSettings}>
                  Cancelar
                </Button>
                <Button onClick={handleCloseSettings}>
                  Salvar Configurações
                </Button>
              </div>
            </div>
          </div>
        )}
        {/* Modal de Adicionar Convidado */}
        {showAddGuest && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white dark:bg-gray-800 rounded-lg p-6 w-full max-w-md mx-4">
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Convidar Amigo</h2>
                <Button variant="ghost" onClick={handleCloseAddGuest}>
                  ✕
                </Button>
              </div>
              
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium mb-2">Nome do Convidado *</label>
                  <input 
                    type="text"
                    value={newGuest.name}
                    onChange={(e) => setNewGuest(prev => ({ ...prev, name: e.target.value }))}
                    placeholder="Digite o nome do convidado"
                    className="w-full p-3 border rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium mb-2">Email (opcional)</label>
                  <input 
                    type="email"
                    value={newGuest.email}
                    onChange={(e) => setNewGuest(prev => ({ ...prev, email: e.target.value }))}
                    placeholder="email@exemplo.com"
                    className="w-full p-3 border rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>

                <div className="bg-blue-50 dark:bg-blue-900/20 p-4 rounded-md">
                  <h4 className="font-medium text-blue-900 dark:text-blue-100 mb-2">Como funciona:</h4>
                  <ul className="text-sm text-blue-800 dark:text-blue-200 space-y-1">
                    <li>• Um link único será gerado para o convidado</li>
                    <li>• O link será copiado automaticamente</li>
                    <li>• Envie o link para seu amigo acessar</li>
                    <li>• Ele poderá se conectar com vídeo e áudio</li>
                  </ul>
                </div>
              </div>

              <div className="flex justify-end gap-3 mt-6">
                <Button variant="outline" onClick={handleCloseAddGuest}>
                  Cancelar
                </Button>
                <Button 
                  onClick={handleAddGuest}
                  disabled={!newGuest.name.trim()}
                  className="bg-green-600 hover:bg-green-700"
                >
                  Gerar Convite
                </Button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;


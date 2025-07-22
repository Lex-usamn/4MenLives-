# Requisitos Técnicos para o Dashboard de Streaming Multicast

## 1. Streaming Simultâneo

### 1.1. Plataformas Suportadas:
- Twitch
- YouTube
- Facebook
- TikTok
- Instagram

### 1.2. Integração com OBS Studio:
- O dashboard deve ser capaz de interagir com o OBS Studio para iniciar/parar streams e possivelmente ajustar configurações.
- Investigar plugins do OBS Studio como "Multiple RTMP Outputs Plugin" ou "Aitum Multistream" para facilitar o envio de streams para múltiplos destinos.
- Considerar a possibilidade de um servidor RTMP local para retransmitir o sinal do OBS para as plataformas, otimizando o uso de recursos.

### 1.3. Gerenciamento de Chaves de Stream e URLs de Ingestão:
- O dashboard deve permitir o armazenamento seguro e o gerenciamento das chaves de stream e URLs de ingestão para cada plataforma.
- Necessidade de autenticação e autorização com as APIs de cada plataforma para obter as informações necessárias.

## 2. Gerenciamento de Conexões de Amigos (Alternativa ao VDO.Ninja)

### 2.1. Requisitos de Baixa Latência e Alta Qualidade:
- A solução deve oferecer baixa latência (preferencialmente abaixo de 500ms) para interações em tempo real.
- A qualidade de áudio e vídeo deve ser configurável e otimizada para streaming.

### 2.2. Tecnologias Potenciais:
- **WebRTC:** É a tecnologia mais promissora para comunicação em tempo real ponto a ponto (P2P) com baixa latência. Deve ser a base para o gerenciamento de conexões de amigos.
- Considerar o uso de um Servidor de Unidade de Mídia (SFU) para gerenciar múltiplas conexões WebRTC e otimizar o tráfego de rede, especialmente para grupos maiores.
- Explorar bibliotecas e frameworks WebRTC para facilitar o desenvolvimento (ex: `simple-peer`, `peerjs`).

### 2.3. Controle de Qualidade e Latência:
- O dashboard deve exibir métricas de latência e qualidade para cada conexão de amigo.
- Possibilidade de ajustar dinamicamente a resolução, taxa de bits e outros parâmetros para otimizar a qualidade e latência com base na largura de banda disponível.

## 3. Dashboard Centralizado

### 3.1. Interface do Usuário:
- Interface intuitiva para monitorar o status de todas as streams simultâneas.
- Exibição de métricas importantes (visualizadores, tempo de stream, etc.) para cada plataforma.
- Controles para iniciar/parar streams, alternar entre cenas do OBS (se possível via API/plugin).

### 3.2. Notificações e Alertas:
- Sistema de notificação para eventos importantes (stream offline, problemas de conexão, etc.).

## 4. APIs das Plataformas (Detalhes Iniciais)

### 4.1. Twitch API:
- **Helix API:** Para obter informações sobre streams, usuários, canais, etc.
- **EventSub:** Para receber notificações em tempo real sobre eventos (ex: novos seguidores, doações).
- **Ingest Endpoints:** Para obter URLs de ingestão e chaves de stream.

### 4.2. YouTube Live Streaming API:
- Para criar, atualizar e gerenciar eventos ao vivo no YouTube.
- Para obter URLs de ingestão e chaves de stream.
- Para interagir com o chat ao vivo.

### 4.3. Facebook Live API (Graph API):
- Para transmitir vídeo ao vivo para perfis, páginas e grupos.
- Para interagir com comentários e reações.
- Requer autenticação e permissões específicas.

### 4.4. TikTok Live Studio API (ou alternativas):
- A TikTok não possui uma API pública de streaming tão robusta quanto as outras plataformas. A integração pode exigir o uso de ferramentas de terceiros ou a emulação do TikTok Live Studio.
- Investigar soluções como `TikTokLive` (Python) ou `TikTok-Live-Connector` (Node.js) para interagir com eventos de live (comentários, presentes).
- A transmissão de vídeo para o TikTok pode depender de chaves RTMP geradas pelo TikTok Live Studio.

### 4.5. Instagram Live Producer:
- O Instagram Live Producer permite transmitir via software de streaming (OBS, Streamlabs) usando uma chave de stream e URL RTMP.
- A API para interagir com o Instagram Live é limitada. O foco será na obtenção da chave de stream e URL RTMP para uso no OBS.

## 5. Considerações de Segurança e Autenticação
- O dashboard deve implementar autenticação segura para proteger as credenciais das plataformas.
- Gerenciamento de tokens de acesso e refresh tokens para as APIs.

## 6. Escalabilidade e Performance
- A arquitetura deve ser escalável para suportar múltiplos usuários e streams simultâneas.
- Otimização de recursos para minimizar o consumo de CPU e largura de banda.


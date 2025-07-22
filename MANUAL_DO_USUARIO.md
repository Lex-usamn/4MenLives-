# 📺 Dashboard de Streaming Multicast - Manual do Usuário

## 🎯 Visão Geral

O Dashboard de Streaming Multicast é uma solução completa para gerenciar transmissões simultâneas em múltiplas plataformas (Twitch, YouTube, Facebook, TikTok, Instagram) com controle avançado de convidados, latência e qualidade, totalmente integrado ao OBS Studio.

## 🚀 Funcionalidades Principais

### ✨ Streaming Multicast
- **Transmissão Simultânea**: Stream para todas as plataformas ao mesmo tempo
- **Controle Centralizado**: Iniciar/parar todas as transmissões com um clique
- **Monitoramento em Tempo Real**: Status, visualizadores e métricas de cada plataforma
- **Configuração Automática**: Geração de configurações para OBS Studio

### 👥 Gerenciamento de Convidados
- **Conexões WebRTC**: Baixa latência superior ao vdo.ninja
- **Controle de Qualidade**: Ajuste dinâmico de resolução e bitrate
- **Monitoramento de Latência**: Métricas em tempo real de cada convidado
- **Convites Seguros**: Tokens únicos para cada participante

### 📊 Análises Avançadas
- **Métricas por Plataforma**: Visualizadores, engajamento, tempo de transmissão
- **Gráficos Interativos**: Histórico de audiência e performance
- **Relatórios Detalhados**: Análise completa das transmissões

## 🛠️ Instalação e Configuração

### Pré-requisitos
- Node.js 20+ instalado
- Python 3.11+ instalado
- OBS Studio (opcional, mas recomendado)

### 1. Configuração do Backend
```bash
cd streaming-dashboard-backend
source venv/bin/activate
pip install -r requirements.txt
python src/main.py
```
**Servidor rodará em**: http://localhost:5002

### 2. Configuração do Frontend
```bash
cd streaming-dashboard-frontend
pnpm install
pnpm run dev
```
**Interface disponível em**: http://localhost:5173

### 3. Servidor WebRTC (Convidados)
```bash
cd webrtc-server
npm install
npm start
```
**Servidor WebRTC em**: http://localhost:3002

## 🔐 Configuração das Plataformas

### Twitch
1. Acesse [Twitch Developers](https://dev.twitch.tv/console)
2. Crie uma nova aplicação
3. Configure OAuth com redirect URI: `http://localhost:5173/auth/twitch`
4. Anote o Client ID e Client Secret

### YouTube
1. Acesse [Google Cloud Console](https://console.cloud.google.com)
2. Ative a YouTube Data API v3
3. Crie credenciais OAuth 2.0
4. Configure redirect URI: `http://localhost:5173/auth/youtube`

### Facebook
1. Acesse [Facebook Developers](https://developers.facebook.com)
2. Crie uma nova aplicação
3. Adicione o produto "Facebook Login"
4. Configure redirect URI: `http://localhost:5173/auth/facebook`

### Instagram
1. Use as mesmas credenciais do Facebook
2. Ative Instagram Basic Display API
3. Configure permissões para live streaming

### TikTok
1. Acesse [TikTok Developers](https://developers.tiktok.com)
2. Crie uma aplicação (API limitada para live)
3. Configure OAuth (funcionalidade limitada)

## 📱 Como Usar o Dashboard

### 1. Login
- Acesse http://localhost:5173
- Use as credenciais padrão: `admin` / `123456`
- Ou registre uma nova conta

### 2. Configurar Plataformas
1. Clique em **"Configurações"**
2. Adicione suas credenciais OAuth para cada plataforma
3. Teste a conexão com cada serviço
4. Ative as plataformas desejadas

### 3. Gerenciar Convidados
1. Vá para a aba **"Convidados"**
2. Clique em **"Convidar Amigo"**
3. Envie o link gerado para seus amigos
4. Monitore latência e qualidade em tempo real
5. Use os controles de áudio/vídeo conforme necessário

### 4. Iniciar Transmissão
1. Configure seu OBS Studio (veja seção específica)
2. No dashboard, clique em **"Iniciar Stream"**
3. Monitore o status de cada plataforma
4. Acompanhe métricas em tempo real na aba **"Análises"**

## 🎥 Integração com OBS Studio

### Configuração Automática
1. No dashboard, vá em **"Configurações"** → **"OBS Config"**
2. Baixe o arquivo de configuração gerado
3. Importe no OBS Studio

### Configuração Manual
Para cada plataforma, configure um output RTMP:

**Twitch:**
- Servidor: `rtmp://live.twitch.tv/app/`
- Chave: Obtida automaticamente via API

**YouTube:**
- Servidor: `rtmp://a.rtmp.youtube.com/live2/`
- Chave: Gerada dinamicamente

**Facebook:**
- Servidor: `rtmps://live-api-s.facebook.com:443/rtmp/`
- Chave: URL dinâmica da API

### Plugin Recomendado
Para streaming simultâneo, instale o plugin **"Multiple RTMP outputs"** no OBS Studio.

## 🔧 Configurações Avançadas

### Qualidade de Stream
- **Resolução**: 1920x1080 (recomendado)
- **FPS**: 30 ou 60 (dependendo da plataforma)
- **Bitrate Vídeo**: 2500-6000 kbps
- **Bitrate Áudio**: 128-320 kbps

### Latência dos Convidados
- **Excelente**: < 50ms
- **Boa**: 50-100ms
- **Aceitável**: 100-200ms
- **Ruim**: > 200ms

### Monitoramento
- Verifique regularmente a aba **"Análises"**
- Monitore a latência dos convidados
- Acompanhe o número de visualizadores por plataforma
- Use os gráficos para otimizar horários de transmissão

## 🚨 Solução de Problemas

### Problemas de Conexão
1. **Plataforma não conecta**: Verifique credenciais OAuth
2. **Stream não inicia**: Confirme configuração RTMP no OBS
3. **Alta latência**: Verifique conexão de internet dos convidados

### Problemas de Performance
1. **CPU alta**: Reduza qualidade de encoding no OBS
2. **Perda de frames**: Ajuste bitrate ou resolução
3. **Áudio dessincronizado**: Verifique configurações de áudio

### Logs e Debug
- Backend: Logs disponíveis no terminal do Flask
- Frontend: Console do navegador (F12)
- WebRTC: Logs no terminal do Node.js

## 📞 APIs Disponíveis

### Streaming
- `GET /api/streaming/platforms` - Lista plataformas
- `GET /api/streaming/status/all` - Status de todas as plataformas
- `POST /api/streaming/multicast/start` - Inicia streaming
- `POST /api/streaming/multicast/stop` - Para streaming

### Convidados
- `GET /api/guests` - Lista convidados
- `POST /api/guests` - Cria convite
- `PUT /api/guests/:id` - Atualiza convidado
- `DELETE /api/guests/:id` - Remove convidado

### Plataformas
- `GET /api/platforms` - Lista plataformas configuradas
- `POST /api/platforms` - Adiciona plataforma
- `PUT /api/platforms/:id` - Atualiza configuração

## 🔒 Segurança

### Autenticação
- JWT tokens com expiração de 24 horas
- Refresh tokens válidos por 30 dias
- Senhas criptografadas com bcrypt

### Dados Sensíveis
- Credenciais OAuth criptografadas no banco
- Tokens de API protegidos
- Comunicação HTTPS recomendada em produção

## 🌐 Deploy em Produção

### Requisitos
- Servidor Linux (Ubuntu 20.04+)
- Nginx como proxy reverso
- Certificado SSL (Let's Encrypt)
- Banco PostgreSQL (recomendado)

### Configuração
1. Configure variáveis de ambiente
2. Use PM2 para gerenciar processos Node.js
3. Configure Nginx para servir arquivos estáticos
4. Implemente backup automático do banco

## 📈 Métricas e Analytics

### Dados Coletados
- Número de visualizadores por plataforma
- Tempo de transmissão
- Latência média dos convidados
- Taxa de perda de pacotes
- Qualidade de conexão

### Relatórios
- Relatórios diários, semanais e mensais
- Comparativo entre plataformas
- Análise de crescimento de audiência
- Métricas de engajamento

## 🎯 Dicas de Uso

### Melhores Práticas
1. **Teste sempre** antes de transmissões importantes
2. **Monitore latência** constantemente durante lives
3. **Use conexão cabeada** sempre que possível
4. **Tenha backup** de internet (4G/5G)
5. **Configure alertas** para problemas técnicos

### Otimização
- Feche aplicações desnecessárias durante streams
- Use SSD para melhor performance
- Configure QoS no roteador para priorizar streaming
- Mantenha drivers de vídeo atualizados

## 📞 Suporte

Para dúvidas ou problemas:
1. Consulte este manual
2. Verifique os logs do sistema
3. Teste com uma plataforma por vez
4. Documente erros para análise

---

**Versão**: 1.0  
**Data**: Julho 2025  
**Compatibilidade**: OBS Studio 29+, Chrome 90+, Firefox 88+


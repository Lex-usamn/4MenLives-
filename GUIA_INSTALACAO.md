# 🚀 Guia de Instalação - Dashboard de Streaming Multicast

## 📋 Pré-requisitos

### Sistema Operacional
- **Linux**: Ubuntu 20.04+ (recomendado)
- **Windows**: Windows 10/11
- **macOS**: macOS 10.15+

### Software Necessário
- **Node.js**: Versão 20.0.0 ou superior
- **Python**: Versão 3.11 ou superior
- **Git**: Para clonar repositórios
- **OBS Studio**: Versão 29+ (opcional)

### Hardware Recomendado
- **CPU**: Intel i5/AMD Ryzen 5 ou superior
- **RAM**: 8GB mínimo, 16GB recomendado
- **Armazenamento**: 10GB livres
- **Internet**: Upload mínimo de 10 Mbps

## 📦 Instalação Completa

### 1. Preparação do Ambiente

#### Ubuntu/Debian
```bash
# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar dependências
sudo apt install -y curl wget git build-essential

# Instalar Node.js 20
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs

# Instalar Python 3.11
sudo apt install -y python3.11 python3.11-venv python3.11-dev

# Instalar pnpm
npm install -g pnpm
```

#### Windows
```powershell
# Instalar via Chocolatey (recomendado)
# Primeiro instale o Chocolatey: https://chocolatey.org/install

choco install nodejs python git -y
npm install -g pnpm
```

#### macOS
```bash
# Instalar via Homebrew
brew install node python@3.11 git
npm install -g pnpm
```

### 2. Download do Projeto

```bash
# Criar diretório do projeto
mkdir ~/streaming-dashboard
cd ~/streaming-dashboard

# Clonar ou baixar os arquivos do projeto
# (Os arquivos já estão disponíveis no sandbox)
```

### 3. Configuração do Backend

```bash
# Navegar para o diretório do backend
cd streaming-dashboard-backend

# Criar ambiente virtual Python
python3.11 -m venv venv

# Ativar ambiente virtual
# Linux/macOS:
source venv/bin/activate
# Windows:
# venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Criar diretório do banco de dados
mkdir -p src/database

# Inicializar banco de dados
python -c "
from src.main import app, db
with app.app_context():
    db.create_all()
    print('Banco de dados criado com sucesso!')
"
```

### 4. Configuração do Frontend

```bash
# Navegar para o diretório do frontend
cd ../streaming-dashboard-frontend

# Instalar dependências
pnpm install

# Criar arquivo de configuração (opcional)
echo "VITE_API_URL=http://localhost:5002" > .env.local
```

### 5. Configuração do Servidor WebRTC

```bash
# Navegar para o diretório WebRTC
cd ../webrtc-server

# Instalar dependências
npm install

# Verificar instalação do Mediasoup
npm run test-mediasoup
```

## 🔧 Configuração das Variáveis de Ambiente

### Backend (.env)
```bash
# Criar arquivo .env no diretório backend
cd streaming-dashboard-backend
cat > .env << EOF
FLASK_ENV=development
SECRET_KEY=sua-chave-secreta-aqui
JWT_SECRET_KEY=sua-jwt-secret-aqui
DATABASE_URL=sqlite:///database/app.db

# Credenciais das plataformas (configure após criar apps)
TWITCH_CLIENT_ID=seu-twitch-client-id
TWITCH_CLIENT_SECRET=seu-twitch-client-secret

YOUTUBE_API_KEY=sua-youtube-api-key
YOUTUBE_CLIENT_ID=seu-youtube-client-id
YOUTUBE_CLIENT_SECRET=seu-youtube-client-secret

FACEBOOK_APP_ID=seu-facebook-app-id
FACEBOOK_APP_SECRET=seu-facebook-app-secret

INSTAGRAM_CLIENT_ID=seu-instagram-client-id
INSTAGRAM_CLIENT_SECRET=seu-instagram-client-secret
EOF
```

### Frontend (.env.local)
```bash
# Criar arquivo .env.local no diretório frontend
cd ../streaming-dashboard-frontend
cat > .env.local << EOF
VITE_API_URL=http://localhost:5002
VITE_WEBRTC_URL=http://localhost:3002
VITE_APP_NAME=Dashboard de Streaming Multicast
EOF
```

### WebRTC (.env)
```bash
# Criar arquivo .env no diretório webrtc-server
cd ../webrtc-server
cat > .env << EOF
PORT=3002
NODE_ENV=development
RTC_MIN_PORT=10000
RTC_MAX_PORT=10100
EOF
```

## 🚀 Inicialização dos Serviços

### Método 1: Manual (Desenvolvimento)

#### Terminal 1 - Backend
```bash
cd streaming-dashboard-backend
source venv/bin/activate
python src/main.py
```

#### Terminal 2 - Frontend
```bash
cd streaming-dashboard-frontend
pnpm run dev
```

#### Terminal 3 - WebRTC
```bash
cd webrtc-server
npm start
```

### Método 2: Script Automatizado

Crie um script `start.sh`:
```bash
#!/bin/bash
echo "🚀 Iniciando Dashboard de Streaming Multicast..."

# Função para matar processos ao sair
cleanup() {
    echo "🛑 Parando serviços..."
    kill $BACKEND_PID $FRONTEND_PID $WEBRTC_PID 2>/dev/null
    exit 0
}
trap cleanup SIGINT SIGTERM

# Iniciar Backend
echo "📡 Iniciando Backend..."
cd streaming-dashboard-backend
source venv/bin/activate
python src/main.py &
BACKEND_PID=$!

# Iniciar WebRTC
echo "🌐 Iniciando Servidor WebRTC..."
cd ../webrtc-server
npm start &
WEBRTC_PID=$!

# Iniciar Frontend
echo "💻 Iniciando Frontend..."
cd ../streaming-dashboard-frontend
pnpm run dev &
FRONTEND_PID=$!

echo "✅ Todos os serviços iniciados!"
echo "📱 Frontend: http://localhost:5173"
echo "🔧 Backend: http://localhost:5002"
echo "📞 WebRTC: http://localhost:3002"
echo ""
echo "Pressione Ctrl+C para parar todos os serviços"

# Aguardar
wait
```

Tornar executável e executar:
```bash
chmod +x start.sh
./start.sh
```

## 🔐 Configuração das Plataformas de Streaming

### 1. Twitch
1. Acesse https://dev.twitch.tv/console
2. Clique em "Register Your Application"
3. Preencha:
   - **Name**: Dashboard Streaming
   - **OAuth Redirect URLs**: `http://localhost:5173/auth/twitch`
   - **Category**: Broadcasting Suite
4. Anote o **Client ID** e **Client Secret**

### 2. YouTube
1. Acesse https://console.cloud.google.com
2. Crie um novo projeto ou selecione existente
3. Ative a "YouTube Data API v3"
4. Vá em "Credenciais" → "Criar Credenciais" → "ID do cliente OAuth 2.0"
5. Configure:
   - **Tipo**: Aplicação da Web
   - **URIs de redirecionamento**: `http://localhost:5173/auth/youtube`
6. Anote o **Client ID** e **Client Secret**

### 3. Facebook/Instagram
1. Acesse https://developers.facebook.com
2. Crie uma nova aplicação
3. Adicione o produto "Facebook Login"
4. Configure:
   - **Valid OAuth Redirect URIs**: `http://localhost:5173/auth/facebook`
5. Para Instagram, ative "Instagram Basic Display"
6. Anote o **App ID** e **App Secret**

### 4. TikTok (Opcional)
1. Acesse https://developers.tiktok.com
2. Crie uma aplicação
3. Configure OAuth (funcionalidade limitada)

## ✅ Verificação da Instalação

### 1. Teste dos Serviços
```bash
# Testar Backend
curl http://localhost:5002/api/users

# Testar WebRTC
curl http://localhost:3002/health

# Testar Frontend (abrir no navegador)
# http://localhost:5173
```

### 2. Teste de Login
1. Acesse http://localhost:5173
2. Use credenciais padrão: `admin` / `123456`
3. Verifique se o dashboard carrega corretamente

### 3. Teste das Plataformas
1. Vá em "Configurações"
2. Adicione credenciais de pelo menos uma plataforma
3. Teste a conexão

## 🐛 Solução de Problemas Comuns

### Erro: "Port already in use"
```bash
# Encontrar processo usando a porta
sudo lsof -i :5002  # ou :5173, :3002

# Matar processo
sudo kill -9 <PID>
```

### Erro: "Module not found"
```bash
# Backend
cd streaming-dashboard-backend
pip install -r requirements.txt

# Frontend
cd streaming-dashboard-frontend
pnpm install

# WebRTC
cd webrtc-server
npm install
```

### Erro: "Permission denied"
```bash
# Dar permissões corretas
chmod +x start.sh
sudo chown -R $USER:$USER ~/streaming-dashboard
```

### Erro: "Database not found"
```bash
cd streaming-dashboard-backend
source venv/bin/activate
python -c "
from src.main import app, db
with app.app_context():
    db.create_all()
"
```

## 📊 Monitoramento

### Logs dos Serviços
```bash
# Backend logs
tail -f streaming-dashboard-backend/logs/app.log

# Frontend logs (console do navegador)
# F12 → Console

# WebRTC logs
tail -f webrtc-server/logs/webrtc.log
```

### Métricas de Sistema
```bash
# CPU e Memória
htop

# Uso de rede
iftop

# Espaço em disco
df -h
```

## 🔄 Atualizações

### Atualizar Dependências
```bash
# Backend
cd streaming-dashboard-backend
source venv/bin/activate
pip install -r requirements.txt --upgrade

# Frontend
cd ../streaming-dashboard-frontend
pnpm update

# WebRTC
cd ../webrtc-server
npm update
```

### Backup do Banco de Dados
```bash
# Criar backup
cp streaming-dashboard-backend/src/database/app.db backup_$(date +%Y%m%d_%H%M%S).db

# Restaurar backup
cp backup_YYYYMMDD_HHMMSS.db streaming-dashboard-backend/src/database/app.db
```

## 🎯 Próximos Passos

Após a instalação bem-sucedida:

1. **Configure as plataformas** com suas credenciais OAuth
2. **Teste o streaming** com OBS Studio
3. **Convide amigos** para testar o sistema WebRTC
4. **Monitore métricas** na aba de análises
5. **Personalize configurações** conforme necessário

## 📞 Suporte

Se encontrar problemas durante a instalação:

1. Verifique os logs de cada serviço
2. Confirme que todas as dependências estão instaladas
3. Teste cada componente individualmente
4. Consulte a seção de solução de problemas

---

**Instalação concluída com sucesso!** 🎉

Acesse http://localhost:5173 para começar a usar o Dashboard de Streaming Multicast.


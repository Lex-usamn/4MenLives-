# Projeto de Arquitetura do Sistema para Dashboard de Streaming Multicast

## 1. Visão Geral da Arquitetura

O dashboard de streaming multicast será uma aplicação web robusta e escalável, projetada para facilitar o gerenciamento de transmissões ao vivo simultâneas em diversas plataformas, bem como o controle de conexões de convidados com baixa latência. A arquitetura proposta adota uma abordagem de microsserviços, permitindo flexibilidade, escalabilidade e manutenção independente dos componentes. Será composta por um frontend interativo, um backend de API para lógica de negócios e integração com serviços externos, e um módulo dedicado para gerenciamento de conexões WebRTC de baixa latência. A integração com o OBS Studio será um ponto central para otimizar o fluxo de trabalho do usuário.

## 2. Componentes do Sistema

### 2.1. Frontend (Interface do Usuário)

O frontend será a camada de interação direta com o usuário, desenvolvida para ser intuitiva e responsiva. Será responsável por:

- **Dashboard de Monitoramento:** Exibição em tempo real do status das transmissões em cada plataforma (online/offline), número de espectadores, duração da live, e métricas de engajamento (comentários, reações).
- **Controles de Streaming:** Botões para iniciar, pausar e parar transmissões. Possibilidade de alternar entre perfis de streaming pré-configurados para diferentes plataformas ou combinações de plataformas.
- **Gerenciamento de Plataformas:** Interface para adicionar, remover e configurar credenciais (chaves de stream, tokens de acesso) para Twitch, YouTube, Facebook, TikTok e Instagram.
- **Gerenciamento de Convidados:** Seção dedicada para convidar amigos, monitorar o status de suas conexões (online/offline, latência, qualidade de vídeo/áudio) e gerenciar suas permissões.
- **Configurações do OBS Studio:** Interface para configurar a integração com o OBS, incluindo a seleção de cenas e perfis de saída, se a API do OBS permitir controle remoto.
- **Notificações e Alertas:** Exibição de alertas em tempo real sobre problemas de conexão, status da live, ou interações importantes (ex: novos seguidores, doações).

**Tecnologias Sugeridas:** React ou Vue.js para o framework, com bibliotecas de gráficos para visualização de dados em tempo real.

### 2.2. Backend (API e Lógica de Negócios)

O backend será o cérebro da aplicação, responsável por orquestrar as operações, gerenciar dados e interagir com as APIs das plataformas de streaming. Será implementado como uma API RESTful e incluirá os seguintes módulos:

- **Módulo de Autenticação e Autorização:** Gerenciamento de usuários, autenticação segura (OAuth 2.0 para plataformas de streaming) e controle de acesso.
- **Módulo de Gerenciamento de Plataformas:** Armazenamento seguro e gerenciamento das credenciais de API para cada plataforma de streaming. Lógica para interagir com as APIs da Twitch, YouTube, Facebook, TikTok e Instagram para iniciar/parar streams, obter métricas e gerenciar eventos.
- **Módulo de Gerenciamento de Streams:** Lógica para coordenar o início e fim de transmissões simultâneas, garantindo que o mesmo conteúdo seja enviado para todas as plataformas selecionadas.
- **Módulo de Dados e Análises:** Coleta e processamento de dados de streaming (visualizadores, chat, etc.) para exibição no dashboard. Armazenamento de dados históricos para análises futuras.
- **Módulo de Notificações:** Envio de notificações em tempo real para o frontend e, opcionalmente, para outros canais (email, SMS) sobre o status das lives.

**Tecnologias Sugeridas:** Python com Flask ou FastAPI para o framework web, PostgreSQL para o banco de dados, Redis para caching e filas de mensagens.

### 2.3. Módulo de Gerenciamento de Conexões (WebRTC)

Este módulo será crucial para a funcionalidade de convidados com baixa latência. Será uma camada separada, otimizada para comunicação em tempo real:

- **Servidor WebRTC (SFU - Selective Forwarding Unit):** Essencial para gerenciar múltiplas conexões de vídeo e áudio entre os participantes. Um SFU encaminha seletivamente os fluxos de mídia, reduzindo a carga de processamento nos clientes e otimizando a largura de banda. Isso é fundamental para garantir baixa latência e alta qualidade em chamadas com vários participantes.
- **Sinalização WebRTC:** Um servidor de sinalização será necessário para coordenar o estabelecimento de conexões peer-to-peer entre os participantes. Isso inclui troca de informações de rede (ICE candidates) e descrições de sessão (SDP).
- **Controle de Qualidade e Latência:** Implementação de lógica para monitorar a qualidade da conexão de cada participante (jitter, perda de pacotes, latência) e ajustar dinamicamente a resolução e taxa de bits para otimizar a experiência.

**Tecnologias Sugeridas:** Node.js com bibliotecas WebRTC (ex: `mediasoup`, `simple-peer`) para o SFU e servidor de sinalização. Alternativamente, considerar serviços de WebRTC gerenciados como Daily.co ou Twilio Programmable Video para simplificar a implementação, embora isso possa adicionar custos e dependências externas.

## 3. Integração com OBS Studio

A integração com o OBS Studio será realizada de duas formas principais:

- **Plugin OBS Studio:** A abordagem mais eficiente é utilizar um plugin do OBS Studio que permita o controle remoto e o envio de múltiplos streams RTMP. O "Multiple RTMP Outputs Plugin" ou o "Aitum Multistream" são candidatos promissores. Este plugin permitiria ao dashboard:
    - Iniciar/parar streams diretamente do OBS.
    - Selecionar perfis de saída e cenas.
    - Obter o status da transmissão (online/offline, bitrate).
- **Servidor RTMP Local (Opcional/Alternativo):** Para maior controle e para evitar a dependência de serviços de retransmissão de terceiros, pode-se configurar um servidor RTMP local (ex: Nginx com módulo RTMP) no mesmo servidor do OBS. O OBS enviaria um único stream para este servidor local, que então retransmitiria para as múltiplas plataformas. Isso centraliza o controle de stream e pode otimizar o uso da largura de banda de upload do usuário.

## 4. Fluxo de Dados e Interações

1. O usuário configura as credenciais das plataformas no frontend, que são enviadas e armazenadas de forma segura no backend.
2. O usuário inicia uma transmissão no OBS Studio, que envia o stream para o servidor RTMP local ou diretamente para as plataformas via plugin OBS.
3. O backend, através das APIs das plataformas, monitora o status das lives e coleta métricas em tempo real.
4. O frontend exibe essas métricas e o status no dashboard.
5. Para convidados, o frontend estabelece conexões WebRTC com o módulo de gerenciamento de conexões. O áudio/vídeo dos convidados é então encaminhado para o OBS Studio (via plugin ou virtual camera) para ser incluído na transmissão principal.
6. O backend gerencia a autenticação e autorização dos convidados, e o módulo WebRTC otimiza a qualidade e latência das conexões.

## 5. Considerações de Segurança

- **Autenticação e Autorização:** Implementar OAuth 2.0 para acesso às APIs das plataformas e JWT (JSON Web Tokens) para autenticação de usuários no dashboard.
- **Armazenamento de Credenciais:** As chaves de stream e tokens de acesso devem ser criptografados e armazenados de forma segura no backend.
- **Segurança da Comunicação:** Utilizar HTTPS para todas as comunicações entre frontend e backend, e DTLS/SRTP para as conexões WebRTC.

## 6. Escalabilidade e Performance

- **Microsserviços:** A arquitetura de microsserviços permite escalar componentes individualmente conforme a demanda.
- **Balanceamento de Carga:** Utilizar balanceadores de carga para distribuir o tráfego entre as instâncias do backend e do servidor WebRTC.
- **Caching:** Implementar caching (Redis) para dados frequentemente acessados para reduzir a carga no banco de dados.
- **Otimização de Mídia:** No módulo WebRTC, otimizar o processamento de vídeo e áudio para minimizar o uso de CPU e largura de banda.

Este projeto de arquitetura serve como um guia inicial. Detalhes de implementação e escolhas de tecnologia específicas serão refinados durante as fases de desenvolvimento.



### 2.4. Banco de Dados

Um banco de dados relacional será utilizado para armazenar informações persistentes do sistema. As principais entidades a serem armazenadas incluem:

- **Usuários:** Informações de autenticação e perfil dos usuários do dashboard.
- **Plataformas de Streaming:** Credenciais de API (tokens de acesso, chaves de stream) para cada plataforma configurada pelo usuário, armazenadas de forma criptografada.
- **Configurações de Stream:** Perfis de streaming definidos pelo usuário, incluindo plataformas de destino, títulos de stream padrão, etc.
- **Dados de Conexão de Convidados:** Informações sobre convidados, histórico de conexões e configurações de qualidade preferenciais.
- **Métricas de Stream:** Dados históricos de visualizadores, duração da live, engajamento, etc., para análises e relatórios.

**Tecnologia Sugerida:** PostgreSQL, devido à sua robustez, escalabilidade e suporte a tipos de dados complexos, além de ser uma escolha comum para aplicações web modernas.

### 2.5. Fila de Mensagens (Opcional, para Escalabilidade)

Para operações assíncronas e para desacoplar componentes, uma fila de mensagens pode ser introduzida. Isso seria útil para:

- **Processamento de Eventos:** Lidar com eventos de API das plataformas de streaming (ex: novos comentários, doações) de forma assíncrona.
- **Tarefas em Segundo Plano:** Executar tarefas demoradas, como processamento de dados de métricas ou transcodificação de vídeo (se aplicável), sem bloquear a resposta da API.

**Tecnologia Sugerida:** Redis (com Pub/Sub) ou RabbitMQ, dependendo da complexidade e volume esperado de mensagens.

## 3. Integração com OBS Studio (Detalhes Adicionais)

Para a integração com o OBS Studio, além dos plugins mencionados, é importante considerar:

- **OBS WebSocket API:** O OBS Studio possui uma API WebSocket que permite o controle remoto e a recuperação de dados em tempo real. O backend pode se conectar a esta API para:
    - Iniciar/parar gravações e transmissões.
    - Alternar entre cenas e fontes.
    - Obter o status de áudio e vídeo.
    - Receber eventos do OBS (ex: mudança de cena, início/fim de stream).
- **Automação de Configuração:** O dashboard pode auxiliar na configuração do OBS, gerando arquivos de perfil ou scripts para automatizar a adição de destinos RTMP para multistreaming.

## 4. Projeto do Sistema de Gerenciamento de Conexões (WebRTC)

O sistema de gerenciamento de conexões para amigos será um componente crítico para a experiência do usuário, focando em baixa latência e alta qualidade. O design incluirá:

- **Servidor de Sinalização:** Um servidor WebSocket simples para troca de mensagens de sinalização (SDP, ICE candidates) entre os pares WebRTC. Este servidor não lida com o fluxo de mídia diretamente, apenas com a coordenação da conexão.
- **Servidor SFU (Selective Forwarding Unit):** Para cenários com mais de dois participantes, um SFU é essencial. Ele recebe os fluxos de mídia de cada participante e os encaminha seletivamente para os outros participantes. Isso evita que cada participante precise enviar seu vídeo para todos os outros, economizando largura de banda e poder de processamento. O SFU também pode realizar transcodificação seletiva para adaptar a qualidade do vídeo às condições de rede de cada receptor.
- **Controle de Qualidade Adaptativo:** Implementar algoritmos para monitorar a largura de banda e a qualidade da rede de cada participante. Com base nessas métricas, o sistema pode ajustar dinamicamente a resolução, taxa de bits e taxa de quadros dos fluxos de vídeo para manter a latência baixa e minimizar interrupções.
- **Integração com OBS:** Os fluxos de vídeo e áudio dos convidados, após serem processados pelo SFU, precisarão ser injetados no OBS Studio. Isso pode ser feito de algumas maneiras:
    - **Virtual Camera/Audio Device:** O SFU pode expor os fluxos como câmeras e dispositivos de áudio virtuais que o OBS pode capturar.
    - **Plugin OBS Personalizado:** Desenvolver um plugin OBS que se conecte ao SFU e receba os fluxos de mídia diretamente, oferecendo maior controle e otimização.
    - **RTMP Ingest:** O SFU pode retransmitir os fluxos dos convidados para um servidor RTMP local que o OBS possa consumir como uma fonte de mídia.

## 5. Fluxo de Dados e Interações (Revisado com Detalhes)

1. **Configuração Inicial:** O usuário autentica o dashboard com suas contas de streaming. O dashboard armazena tokens de acesso e chaves de stream de forma segura no banco de dados.
2. **Início da Transmissão:** O usuário inicia a transmissão no OBS Studio. O OBS, usando um plugin de múltiplas saídas RTMP ou um servidor RTMP local, envia o stream para as plataformas configuradas.
3. **Monitoramento de Stream:** O backend, usando as APIs das plataformas, consulta o status da live (online/offline), número de visualizadores, e dados de chat. Esses dados são enviados para o frontend via WebSocket para atualização em tempo real do dashboard.
4. **Convite de Amigos:** O usuário gera um link de convite no dashboard. Este link contém um token que permite ao amigo se conectar ao sistema WebRTC.
5. **Conexão do Amigo:** O amigo acessa o link, e seu navegador estabelece uma conexão WebRTC com o servidor de sinalização e, em seguida, com o SFU. O áudio e vídeo do amigo são transmitidos para o SFU.
6. **Injeção no OBS:** O SFU encaminha o fluxo de mídia do amigo para o OBS Studio. Isso pode ser feito via um plugin OBS personalizado que captura o fluxo WebRTC, ou o SFU pode retransmitir o fluxo para uma entrada RTMP local que o OBS consome.
7. **Controle de Qualidade:** O SFU e o backend monitoram a latência e a qualidade da conexão de cada amigo, ajustando dinamicamente os parâmetros do stream para otimizar a experiência.
8. **Interação:** O chat das plataformas de streaming é exibido no dashboard, permitindo que o streamer e os amigos interajam com o público. O dashboard pode também permitir que o streamer gerencie os convidados (mutar, remover, etc.).

## 6. Tecnologias e Ferramentas (Consolidação)

- **Frontend:** React.js (ou Vue.js), Chart.js (para gráficos), WebSocket API.
- **Backend:** Python (Flask/FastAPI), PostgreSQL, SQLAlchemy (ORM), Redis (caching/fila de mensagens).
- **WebRTC:** Node.js (para SFU e sinalização), `mediasoup` (SFU), `socket.io` (sinalização).
- **OBS Integration:** OBS WebSocket API, `obs-websocket-py` (Python client), `Multiple RTMP Outputs Plugin` (ou similar).
- **Autenticação:** OAuth 2.0, JWT.
- **Infraestrutura (Sugestão):** Docker (para conteinerização), Kubernetes (para orquestração em larga escala), Nginx (proxy reverso).

Esta seção detalha os componentes e a interação entre eles, fornecendo uma base sólida para a próxima fase de desenvolvimento.


# Guia de Uso: Dashboard de Streaming Multicast

Este guia detalha como utilizar o Dashboard de Streaming Multicast para gerenciar suas transmissões ao vivo simultâneas e convidados. Ele aborda desde o acesso inicial até a configuração do OBS Studio e a integração de convidados.

## 1. Acesso ao Dashboard

Para começar, acesse o Dashboard de Streaming Multicast através da URL:

[https://jfhxwifn.manus.space](https://jfhxwifn.manus.space)

### Credenciais de Acesso:

*   **Usuário/Email:** `admin`
*   **Senha:** `123456`

## 2. Visão Geral do Dashboard

Após o login, você será direcionado para a tela principal do Dashboard. Aqui você encontrará informações essenciais sobre suas transmissões e convidados:

*   **Total de Visualizadores:** Número total de espectadores em todas as plataformas.
*   **Plataformas Ativas:** Quantidade de plataformas conectadas e transmitindo ao vivo.
*   **Convidados Online:** Número de convidados conectados à sua sessão.
*   **Status do Stream:** Indica se você está AO VIVO ou OFFLINE.

Você também verá o status individual de cada plataforma (Twitch, YouTube, Facebook, TikTok, Instagram) com o número de visualizadores e o status de conexão.

## 3. Gerenciamento de Convidados

A funcionalidade de gerenciamento de convidados permite que você adicione amigos à sua transmissão com controle de latência e qualidade.

### 3.1. Convidar um Amigo

1.  No Dashboard principal, clique na aba **"Convidados"**.
2.  Clique no botão **"Convidar Amigo"**.
3.  Uma janela modal será exibida. No campo **"Nome do Convidado"**, digite o nome do seu amigo (obrigatório).
4.  Clique em **"Gerar Convite"**.
5.  Um link único será gerado e copiado automaticamente para a sua área de transferência. Este link é a URL que seu amigo deverá acessar.
6.  Envie este link para o seu amigo. Ele será direcionado para uma página onde poderá se conectar à sua transmissão.

### 3.2. Página do Convidado

Quando seu amigo acessar o link de convite, ele verá uma página com as seguintes informações:

*   **Token de Convidado:** Um identificador único para a sessão dele.
*   **Instruções:** Orientações sobre como se conectar e o que esperar.
*   **Requisitos Técnicos:** Informações sobre navegadores compatíveis e configurações de rede.

Seu amigo precisará permitir o acesso à câmera e ao microfone para participar da transmissão.

## 4. Configuração do OBS Studio para Multicast

Para transmitir para múltiplas plataformas simultaneamente e integrar seus convidados, você precisará configurar o OBS Studio. O Dashboard fornece um arquivo de configuração JSON que simplifica esse processo.

### 4.1. Baixar Configurações do OBS

1.  No Dashboard principal, clique no botão **"Configurações"** (ícone de engrenagem) no canto superior direito.
2.  Na janela de Configurações, role para baixo até a seção **"Configurações de Plataforma"**.
3.  Clique no botão **"📥 Baixar Configurações do OBS"**.
4.  Um arquivo JSON (`4menlive-obs-config-YYYY-MM-DD.json`) será baixado para o seu computador.

### 4.2. Importar Configurações no OBS Studio

1.  Abra o **OBS Studio**.
2.  Vá em **"Arquivo" > "Importar Perfil"**.
3.  Selecione o arquivo JSON que você baixou do Dashboard.
4.  Um novo perfil será criado no OBS com as configurações pré-definidas para multicast.

### 4.3. Configuração Manual no OBS (se necessário)

O arquivo de configuração inclui as URLs RTMP e chaves de stream para cada plataforma. Você pode usá-las para configurar manualmente as saídas de stream no OBS:

1.  No OBS Studio, vá em **"Configurações" > "Stream"**.
2.  Para streaming simultâneo, você precisará do plugin **"Multiple RTMP outputs"**.
    *   **Nome:** Multiple RTMP outputs
    *   **Download:** [https://obsproject.com/forum/resources/multiple-rtmp-outputs-plugin.964/](https://obsproject.com/forum/resources/multiple-rtmp-outputs-plugin.964/)
    *   **Instalação:** Baixe e instale o plugin para habilitar o multicast.
3.  Configure cada plataforma como uma saída separada usando as URLs e chaves fornecidas no arquivo JSON baixado.

**Exemplo de URLs RTMP:**

*   **Twitch:** `rtmp://live.twitch.tv/live/`
*   **YouTube:** `rtmp://a.rtmp.youtube.com/live2/`
*   **Facebook:** `rtmps://live-api-s.facebook.com:443/rtmp/`
*   **Instagram:** `rtmps://live-upload.instagram.com:443/rtmp/`

**Importante:** Substitua `SEU_STREAM_KEY_PLATAFORMA` pela sua chave de stream real de cada plataforma. Você pode encontrar essas chaves no painel de controle de cada plataforma (ex: Twitch Creator Dashboard, YouTube Studio).

## 5. Integração de Convidados no OBS

Para exibir seus convidados na sua transmissão do OBS, você precisará adicioná-los como uma fonte de navegador (Browser Source).

1.  No OBS Studio, na seção **"Fontes"**, clique no botão **"+"**.
2.  Selecione **"Navegador" (Browser Source)**.
3.  Dê um nome à fonte (ex: "Convidado João").
4.  Na janela de propriedades, cole a **URL do link de convite** do seu amigo no campo **"URL"**.
5.  Ajuste a largura e altura conforme necessário (ex: 1920x1080 para tela cheia).
6.  Marque a opção **"Controlar áudio via OBS"** se desejar gerenciar o áudio do convidado diretamente no OBS.
7.  Clique em **"OK"**.

Repita este processo para cada convidado que você deseja adicionar à sua cena. Você pode organizar as fontes de navegador em suas cenas do OBS para criar layouts personalizados.

## 6. Iniciar e Parar a Transmissão

### 6.1. Iniciar Stream

1.  No Dashboard principal, clique no botão **"Iniciar Stream"**.
2.  No OBS Studio, clique em **"Iniciar Transmissão"**.

O Dashboard atualizará o status para **AO VIVO** e começará a exibir métricas em tempo real.

### 6.2. Parar Stream

1.  No Dashboard principal, clique no botão **"Parar Stream"**.
2.  No OBS Studio, clique em **"Parar Transmissão"**.

O Dashboard atualizará o status para **OFFLINE**.

## 7. Análises e Métricas

A aba **"Análises"** no Dashboard fornece gráficos e dados sobre seus visualizadores e latência dos convidados, ajudando você a monitorar o desempenho da sua transmissão.

--- 

Se tiver qualquer dúvida ou precisar de assistência adicional, não hesite em perguntar!


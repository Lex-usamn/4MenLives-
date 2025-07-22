# Guia de Uso: Integração de Convidados com Tokens

Este guia detalha o procedimento completo para utilizar os links de convite gerados pelo Dashboard de Streaming Multicast, tanto para o convidado que irá participar da transmissão quanto para o streamer que irá integrar o convidado no OBS Studio.

## 1. Para o Convidado: Acessando o Link de Convite

Após o streamer gerar um link de convite no Dashboard, ele enviará este link para você. Este link é único e contém um token que identifica sua sessão como convidado.

### 1.1. O que o Convidado Deve Fazer:

1.  **Clique no Link:** Ao receber o link (ex: `https://4menlive.supersamsm.com.br:3002/guest/SEU_TOKEN_UNICO`), clique nele para abrir em seu navegador de internet. Recomenda-se usar navegadores modernos como Google Chrome, Mozilla Firefox ou Microsoft Edge para melhor compatibilidade com WebRTC.

2.  **Permitir Acesso à Câmera e Microfone:** Seu navegador solicitará permissão para acessar sua câmera e microfone. **É crucial que você conceda essas permissões** para que sua imagem e áudio possam ser transmitidos para o streamer.

3.  **Verificar Conexão:** Após conceder as permissões, você será direcionado para uma página de espera ou pré-visualização. Esta página exibirá seu token de convidado e pode mostrar um feedback visual da sua câmera e microfone. Certifique-se de que sua câmera e microfone estão funcionando corretamente.

4.  **Aguardar o Streamer:** Mantenha esta página aberta. O streamer irá integrar sua conexão no OBS Studio. Sua transmissão de áudio e vídeo só será ativa quando o streamer adicionar sua fonte no OBS e iniciar a transmissão.

### 1.2. Dicas para o Convidado:

*   **Ambiente:** Escolha um local bem iluminado e silencioso para sua participação.
*   **Fones de Ouvido:** Use fones de ouvido para evitar eco e melhorar a qualidade do áudio.
*   **Conexão:** Uma conexão de internet estável e rápida é fundamental para uma boa qualidade de transmissão.
*   **Fechamento da Página:** Não feche a página do navegador enquanto estiver participando da transmissão, pois isso encerrará sua conexão.

## 2. Para o Streamer: Integrando o Convidado no OBS Studio

Depois que o convidado acessar o link e estiver aguardando, você precisará adicioná-lo como uma fonte em suas cenas do OBS Studio.

### 2.1. Adicionando o Convidado como Fonte de Navegador (Browser Source):

1.  **Abra o OBS Studio:** Certifique-se de que seu OBS Studio está aberto e pronto para a transmissão.

2.  **Selecione a Cena:** No painel "Cenas" (Scenes), selecione a cena onde você deseja que o convidado apareça. Você pode ter uma cena específica para entrevistas ou uma cena geral onde o convidado será inserido.

3.  **Adicionar Nova Fonte:** No painel "Fontes" (Sources) da cena selecionada, clique no botão **"+"** (Adicionar).

4.  **Escolha "Navegador" (Browser Source):** Na lista de opções, selecione "Navegador".

5.  **Configurar a Fonte do Navegador:** Uma nova janela de propriedades será aberta:
    *   **Criar novo:** Selecione "Criar novo" e dê um nome claro para a fonte, como "Convidado [Nome do Convidado]" (ex: "Convidado João"). Isso ajuda a organizar suas fontes.
    *   **URL:** **Cole o link de convite completo** que você gerou no Dashboard e enviou para o seu convidado (ex: `https://4menlive.supersamsm.com.br:3002/guest/i22429rhd2`). Este é o ponto crucial para a conexão.
    *   **Largura e Altura:** Defina as dimensões da janela do navegador. Se o convidado for ocupar a tela inteira, use a resolução da sua tela (ex: 1920x1080). Se for um layout com múltiplos convidados, ajuste o tamanho para caber no seu design.
    *   **FPS:** Mantenha em "Controlar via OBS" ou defina para 30/60 FPS, dependendo da sua configuração de stream.
    *   **Controlar áudio via OBS:** **Marque esta opção.** Isso permitirá que você gerencie o volume do áudio do convidado diretamente no Mixer de Áudio do OBS, facilitando o controle durante a live.
    *   **CSS Personalizado:** (Opcional) Se você tiver conhecimentos de CSS, pode usar este campo para aplicar estilos adicionais à página do convidado dentro do OBS.

6.  **Clique em "OK":** A fonte de navegador do convidado aparecerá na sua cena. Você pode redimensioná-la e posicioná-la livremente dentro da sua cena, assim como faria com qualquer outra imagem, vídeo ou webcam.

7.  **Repita para Múltiplos Convidados:** Se você tiver mais de um convidado, repita os passos de 3 a 6 para cada um, usando o link de convite único de cada convidado.

### 2.2. Gerenciamento de Áudio e Vídeo no OBS:

*   **Mixer de Áudio:** O áudio de cada convidado aparecerá como uma fonte separada no Mixer de Áudio do OBS. Você pode ajustar o volume individualmente, aplicar filtros (como supressão de ruído) e monitorar os níveis.
*   **Visualização:** Acompanhe a visualização da sua cena no OBS para garantir que a imagem do convidado esteja aparecendo corretamente e que o layout esteja como desejado.

## 3. Considerações Finais

*   **Testes Prévios:** Sempre realize testes com seus convidados antes de iniciar a transmissão ao vivo. Isso ajuda a identificar e resolver problemas de conexão, áudio ou vídeo antecipadamente.
*   **Conexão do Convidado:** Lembre-se que a qualidade da transmissão do convidado dependerá da conexão de internet dele. O sistema ajuda a controlar a latência, mas uma conexão instável por parte do convidado pode afetar a qualidade geral.
*   **Privacidade:** O link do convidado é único para cada sessão. Certifique-se de enviá-lo apenas para a pessoa correta.

Com este procedimento, você poderá integrar facilmente seus convidados em suas transmissões ao vivo, aproveitando a funcionalidade de tokens únicos para um gerenciamento eficiente e controlado. Boa live!


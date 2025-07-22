# Guia de Uso: Integração de Cenas Existentes do OBS com o Dashboard de Streaming Multicast

Se você já possui cenas configuradas no OBS Studio, o processo de integração com o Dashboard de Streaming Multicast é focado em adicionar as saídas de stream para as plataformas e incorporar os convidados como fontes de navegador em suas cenas existentes.

## 1. Configurando Múltiplas Saídas de Stream (Multicast)

Para transmitir para Twitch, YouTube, Facebook, TikTok e Instagram simultaneamente, você precisará do plugin **"Multiple RTMP outputs"** no OBS Studio. Se você ainda não o tem, baixe-o e instale-o:

*   **Nome do Plugin:** Multiple RTMP outputs
*   **Download:** [https://obsproject.com/forum/resources/multiple-rtmp-outputs-plugin.964/](https://obsproject.com/forum/resources/multiple-rtmp-outputs-plugin.964/)

Após a instalação do plugin, siga estes passos para configurar as saídas de stream em suas cenas existentes:

1.  **Baixe o arquivo de configuração do OBS** do seu Dashboard de Streaming Multicast. Este arquivo contém as URLs RTMP e as chaves de stream para cada plataforma. (Consulte a seção "4.1. Baixar Configurações do OBS" no `GUIA_DE_USO.md` para mais detalhes).

2.  No OBS Studio, vá em **"Ferramentas" > "Multiple Output"**.

3.  Na janela do Multiple Output, clique em **"Adicionar nova saída"**.

4.  Para cada plataforma que você deseja transmitir (Twitch, YouTube, Facebook, Instagram, TikTok), configure uma nova saída:
    *   **Nome da Saída:** Dê um nome claro (ex: "Twitch", "YouTube Live").
    *   **Tipo de Serviço:** Selecione "Custom" (Personalizado).
    *   **Servidor RTMP:** Copie a URL RTMP correspondente do arquivo JSON baixado do Dashboard (ex: `rtmp://live.twitch.tv/live/` para Twitch).
    *   **Chave de Stream:** Copie sua chave de stream pessoal para a plataforma específica. **Lembre-se de que o arquivo JSON baixado do Dashboard contém placeholders como `SEU_STREAM_KEY_TWITCH`. Você deve substituí-los pelas suas chaves reais, que podem ser encontradas no painel de controle de cada plataforma.**
    *   **Configurações de Vídeo/Áudio:** Você pode usar as configurações globais do OBS ou ajustar individualmente para cada saída, se necessário. O arquivo JSON baixado também contém configurações recomendadas.

5.  Repita o passo 4 para todas as plataformas que você deseja incluir em sua transmissão simultânea.

6.  Após configurar todas as saídas, você pode iniciar a transmissão para todas elas simultaneamente clicando em **"Iniciar todas as saídas"** no plugin Multiple Output, ou individualmente, conforme sua necessidade.

## 2. Adicionando Convidados como Fontes de Navegador

Para integrar seus convidados em suas cenas existentes do OBS, você os adicionará como fontes de navegador (Browser Source). Certifique-se de já ter gerado os links de convite para seus amigos através do Dashboard. (Consulte a seção "3.1. Convidar um Amigo" no `GUIA_DE_USO.md` para mais detalhes).

1.  No OBS Studio, selecione a **cena** onde você deseja que o convidado apareça.

2.  Na seção **"Fontes"** (Sources) da cena selecionada, clique no botão **"+"**.

3.  Selecione **"Navegador" (Browser Source)** na lista de opções.

4.  Na janela que se abre:
    *   **Criar novo:** Selecione "Criar novo" e dê um nome claro para a fonte (ex: "Convidado João", "Webcam Maria").
    *   **URL:** Cole o **link de convite único** que você gerou no Dashboard para o seu amigo. Este é o link que seu amigo acessará para entrar na sua live.
    *   **Largura e Altura:** Defina as dimensões desejadas para a janela do navegador. Para um convidado em tela cheia, você pode usar a resolução da sua tela (ex: 1920x1080). Para múltiplos convidados, você pode ajustar o tamanho para criar um layout de mosaico.
    *   **FPS:** Mantenha em "Controlar via OBS" ou defina para 30/60 FPS.
    *   **Controlar áudio via OBS:** Marque esta opção se você quiser gerenciar o volume do áudio do convidado diretamente no Mixer de Áudio do OBS.

5.  Clique em **"OK"**.

6.  A fonte de navegador do convidado aparecerá na sua cena. Você pode redimensioná-la e posicioná-la como qualquer outra fonte (imagem, vídeo, webcam) dentro da sua cena.

7.  **Repita** este processo para cada convidado que você deseja incluir em suas cenas.

## 3. Considerações Adicionais

*   **Organização de Cenas:** Você pode criar cenas específicas para diferentes layouts de convidados (ex: "Cena 2 Convidados", "Cena 3 Convidados") e alternar entre elas durante a transmissão.
*   **Áudio:** Certifique-se de que o áudio de cada convidado esteja sendo capturado e mixado corretamente no OBS. Use o Mixer de Áudio para ajustar os níveis.
*   **Testes:** Sempre faça testes com seus convidados antes da transmissão ao vivo para garantir que a conexão, áudio e vídeo estejam funcionando perfeitamente.

Com esses passos, você poderá integrar suas cenas existentes do OBS com o Dashboard de Streaming Multicast, aproveitando todas as funcionalidades de transmissão simultânea e gerenciamento de convidados.


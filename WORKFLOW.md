# TikToks com narração e explicação visual

## Padrão ativo: teruya.dev 3.0

As próximas edições seguem [o padrão teruya.dev](standards/teruya-dev/VIDEO_STANDARD.md), atualizado em 30/10/2026 com o design Markdown enviado: azul #0066CC, branco e cinzas neutros, blocos escuros, SF Pro Display/Text em Semibold/Regular e arredondamentos por função. Todo elemento focal precisa de entrada e saída fluida de bolha pop, com origem e direção ligadas ao significado. Fundos e apoios podem ficar estáticos; o foco assenta para leitura e pode sair por uma camada de destaque sem remover o objeto base. Nas explicações, usar grid sketchbook largo de 216 px, translúcido (7% claro / 6% escuro), como apoio estático. A energia do design clean vem da coreografia: tipografia sincronizada, transformação de componentes e câmera com alvo e retorno, intercaladas com leitura estável. Sobre a gravação do Henrique, todo texto é flutuante, com fundo transparente, incluindo títulos, legendas e CTA; aplicar contorno duplo: branco interno/preto externo sobre fundo escuro e preto interno/branco externo sobre claro. Cada letra das palavras de ênfase tem Elastic Pop-In e Elastic Pop-Out próprios; acentos e posição final são preservados. A legenda de apoio continua discreta. Preencher a câmera por recorte proporcional com foco no rosto, nunca por blur lateral; cortes espaciais não alteram o tempo da gravação. O manual inclui tokens, cinco variantes pop e o par elastic por letra, ficha de cena e receitas ShotCraft rastreáveis. JSONs são especificações, não presets nativos instalados. A primeira edição, sobre fundamentos de AI, mantém sua direção original. O padrão 2.1 foi aplicado ao episódio “Tá vendo essa edição?”, em `projects/artcraft-edicao/`, com receitas ShotCraft, projetos nativos, composição complementar e registros de revisão.

## Direção definida pelo Henrique

Os vídeos serão para TikTok. Henrique aparece nos primeiros segundos e em momentos específicos. Na maior parte do vídeo, sua voz continua narrando enquanto imagens, vídeos de apoio e animações explicam visualmente o que ele está dizendo.

Priorizar FilmCraft e EffectCraft para edição e animação, com VectorCraft para criar os elementos vetoriais. Manter a gravação original intacta e salvar projetos e exportações separadamente.

## Fluxo proposto

### Opção: narração sintética com a própria voz

No desktop Windows, o [estúdio de voz](docs/VOICE.md) acrescenta uma fonte de áudio ao fluxo existente. Criar o roteiro normalmente; cadastrar uma amostra própria e consentida; gerar e escutar o WAV; importar no FilmCraft; então transcrever o arquivo final e alinhar as legendas. A narração em português usa Chatterbox Multilingual V3, com conversão opcional de timbre pelo OpenVoice V2. Não atribuir o resultado somente ao OpenVoice, nem prometer cópia de sotaque, personalidade ou fidelidade sem teste.

O apresentador pode aparecer apenas em trechos reais identificados. Não sincronizar uma gravação antiga da boca com texto sintético novo. Amostras, embeddings e áudios ficam fora do Git. A geração local não publica vídeos e não altera o processo de escrever roteiros. Na CPU, reservar alguns minutos por trecho. Escuta e revisão de pronúncia continuam necessárias.

### Montagem orientada pelo áudio

1. Selecionar a gravação e montar a fala: o áudio determina a duração e a ordem das ideias.
2. Marcar, na linha do tempo, cada ideia, palavra de ênfase, comparação e mudança de assunto.
3. Definir onde o apresentador aparece: abertura, opinião/ênfase pessoal, transição ou fechamento quando fizer sentido. A duração exata depende da gravação.
4. Para os demais trechos, escolher uma explicação visual: imagem de apoio, exemplo real, diagrama, comparação, número ou vetor animado. Cada plano precisa ajudar a entender a fala.
5. Criar vetores no VectorCraft, animar no EffectCraft e montar áudio, imagens, aparições e legendas no FilmCraft.
6. Usar 1080 × 1920 como alvo de entrega; preservar o enquadramento vertical desde a composição. Confirmar a taxa de quadros com o material original. Conferir legibilidade e sobreposição da interface do TikTok na prévia final.

## Avaliação do Video ShotCraft

Análise realizada em 29/10/2026, revisão `5a2e98daade313c4f376120f38427eb19a108e8c`. Foram lidas a documentação, receitas selecionadas, componentes e exemplos de implementação. Depois da análise, Henrique autorizou a instalação: a mesma revisão está instalada como skill global em `~/.codex/skills/video-shotcraft`. `research/video-shotcraft/` continua sendo apenas uma seleção de arquivos de consulta.

**Recomendação: aproveitar como biblioteca de receitas de movimento e composição.** A biblioteca tem 124 cartões; o projeto anuncia 150 exemplos de movimentos. As receitas incluem intenção, parâmetros, tempos, limitações e código Remotion. É material útil para reduzir tentativa e erro na animação.

| Receita | Aplicação em nossos vídeos | Adaptação necessária |
| --- | --- | --- |
| `type-rhythm-sync`, variação `karaoke-fill-sync` | Destacar palavras conforme a voz | Marcar os tempos reais da gravação; revisar quebra de linhas em português |
| `marker-underline-title` | Sublinhar a palavra que concentra a ideia | Aplicar uma ênfase por vez, com traço curto e legível |
| `draw-svg-trace` | Construir setas, diagramas e ícones enquanto são explicados | Desenhar os vetores no VectorCraft e revelar os traços no momento correspondente da fala |
| `before-after-slider-scrub` | Mostrar transformação ou comparação | Usar exemplos reais alinhados e dar tempo para perceber a diferença |
| `list-reveal` | Apresentar etapas ou motivos | Revelar cada item na respectiva frase, em uma composição vertical |
| `crash-zoom-punch` | Apontar um detalhe importante em imagem ou gravação | Usar pontualmente, com imagem em resolução suficiente e alvo claramente definido |

### Integração com ArtCraft

As implementações são componentes React/Remotion. Não encontrei um exportador de projetos ou presets nativos para FilmCraft/EffectCraft na documentação e na estrutura examinadas. A exportação editável documentada é para JianYing, a versão chinesa do CapCut, além do próprio Motion Workbench.

Há dois caminhos de reaproveitamento:

- **Receita recriada no EffectCraft:** traduzir timing, curvas, máscaras, keyframes e camadas. É o caminho preferido para manter os movimentos editáveis na nossa suíte.
- **Trecho renderizado com Remotion:** importar o vídeo resultante no FilmCraft e preservar o projeto Remotion para futuras alterações. Textos e camadas internos não passam a ser editáveis no FilmCraft. Sobreposições exigem testar uma saída com transparência e a importação correspondente.

O template inspecionado está configurado em 1920 × 1080 a 30 fps. Há também coordenadas fixas de 1920/1080 nos exemplos. A adaptação para 9:16 exige recompor posições, tamanhos, quebras de texto e trajetória da câmera; mudar só a resolução não resolve. Tempos expressos em frames precisam ser ajustados se a taxa de quadros mudar.

A orientação original é principalmente para vídeos promocionais de produtos e interfaces. Para este projeto, a voz e o significado da frase devem orientar os cortes e as animações; a batida da música será secundária. Aberturas de marca longas, grades de interfaces pequenas e efeitos intensos repetidos têm menor prioridade.

### Video TalkCraft como referência complementar

O projeto irmão é mais próximo do formato escolhido: recebe roteiro e áudio pronto, organiza planos por momentos da fala e oferece sincronização de palavras, animações e composição de material do apresentador. A documentação descreve também exportação de movimentos isolados com transparência. Essas funcionalidades foram consultadas na documentação, sem teste de execução. A qualidade do alinhamento de voz em português ainda precisa ser validada com uma gravação real.

Não é necessário adotar o fluxo completo de nenhum dos dois projetos para aproveitar suas receitas no ArtCraft.

### Limites observados

- O arquivo de atribuição do ShotCraft aponta alguns áudios antigos sem origem individual confirmada. Selecionar áudio com origem verificável ou usar os nossos próprios arquivos.
- Os demos contêm marcas, textos e materiais de exemplo que precisam ser substituídos.
- A análise de código e documentação não comprova integração automática nem resultado visual já renderizado em 9:16.

## Instalação local

Aplicativos instalados em `/Applications`:

| Aplicativo | Versão | Papel |
| --- | --- | --- |
| ArtCraft Launcher | 0.9.0 | Gerenciar os aplicativos da suíte |
| FilmCraft | 0.14.0 | Montagem, cortes, áudio, legendas e exportação |
| EffectCraft | 0.18.0 | Animação, composição e efeitos |
| VectorCraft | 0.18.0 | Criar e exportar vetores |

Os downloads foram conferidos por SHA-256; os aplicativos passaram pela verificação de assinatura e pela avaliação de notarização do macOS. Metadados FinderInfo do empacotamento foram removidos das cópias de instalação, mantendo as assinaturas originais válidas.

Os três editores abriram, responderam a `ui.inspect` e produziram capturas de tela. EffectCraft precisou de uma segunda inicialização com prazo maior. As três ferramentas CLI também foram verificadas e responderam a `--help`. Depois dessa verificação, foi concluída e entregue a primeira edição com os vídeos do Henrique: `projects/fundamentos-ai/`, com projetos nativos, vetores e exportação vertical de aproximadamente 50,27 s. A direção teruya.dev 2.1 foi aplicada no episódio `projects/artcraft-edicao/`: 49,37 s, 1080 × 1920, 30 fps, Rec.709 e −16 LUFS. O vídeo, as legendas e os editáveis em dois ZIPs foram enviados para `material videos/outputs`; o registro está em `projects/artcraft-edicao/docs/delivery.json`. A revisão independente visual e técnica está concluída; a escuta integral não foi realizada.

As CLIs estão em `tools/artcraft/bin/`. A documentação das versões instaladas está em `tools/artcraft/docs/`; os registros de instalação e verificação ficam em `tools/artcraft/installation.json` e `tools/artcraft/verification/`. Nenhum servidor MCP global foi adicionado. O controle da interface pode ser iniciado apenas durante a edição, conforme os protocolos oficiais salvos localmente.

### Video ShotCraft

Instalado em `~/.codex/skills/video-shotcraft` com o instalador oficial de skills do Codex. As dependências do template Remotion e do Motion Workbench foram instaladas pelos respectivos lockfiles. O Chrome Headless Shell está preparado e compartilhado entre os dois ambientes. O vínculo interno `workbench/demosrc -> ../demos`, que o ZIP transformou em arquivo de texto, foi restaurado.

Verificação concluída: Motion Workbench compilado com sucesso e catálogo de 150 exemplos gerado; imagem de teste do template `AiflPromo`, frame 150 em 960 × 540, renderizada e inspecionada. O resultado fica em `tools/shotcraft/verification/installation-frame.png`. Esta é uma verificação de instalação do template original, não uma adaptação vertical ou um vídeo do Henrique.

A skill fica disponível ao Codex a partir da próxima mensagem. O Video TalkCraft permanece apenas como referência analisada. A ferramenta opcional `uv`, usada pelo ShotCraft para análise de batidas, pode ser preparada quando esse recurso for necessário.

### TikTok Video Skills

Instaladas as quatro skills de `iart-ai/tiktok-video-skills` na revisão `2a775336b5a638cbf8a61dbd785f9a1b649be016`, pelo instalador oficial do Codex, em `~/.codex/skills/`: `short-form-video`, `caption-animation`, `countdown-video` e `lower-thirds`. Cada pasta inclui as referências originais, a licença MIT e uma cópia dos scripts compartilhados da mesma revisão. As skills `tiktok-marketing` e `video-shotcraft` foram preservadas.

Usar `short-form-video` para estrutura e ritmo; `caption-animation` para sincronização de palavras; `lower-thirds` para identificação do apresentador; `countdown-video` quando uma contagem ajudar o conteúdo. As receitas complementam o ShotCraft e a produção no ArtCraft. Seus exemplos em Remotion não são presets nativos de FilmCraft ou EffectCraft.

**O padrão teruya.dev 3.0 orienta a aplicação visual.** Aplicar azul e branco, SF Pro, arredondamentos por função, entradas e saídas de bolha pop nos elementos focais e grid sketchbook translúcido apenas nas explicações. Preservar apoios estáticos e tempo de leitura. Adaptar cores, contornos, sombras, escala e ritmo dos exemplos ao manual; suas sugestões genéricas não substituem a direção definida pelo Henrique. Para narração em português, escolher transcrição multilíngue com tempos reais por palavra, em vez de modelos exclusivos de inglês.

Verificação de instalação: 33 arquivos inventariados, metadados e referências internas conferidos, 12 verificações de sintaxe Bash aprovadas e scripts marcados como executáveis. FFmpeg, FFprobe, Node e npx estão disponíveis. Há Chromium em cache, mas a execução do Playwright e as dependências opcionais de renderização/transcrição serão validadas quando utilizadas. Nenhum vídeo foi renderizado ou alterado nesta instalação. As skills ficam disponíveis na próxima mensagem.

Instalações e materiais citados acima são registros locais históricos e não são versionados. Instruções portáveis dos auxiliares: [guia das skills](skills/README.md). Revisão e hashes dos arquivos: [catálogo fixado](skills/catalog.json).

## Fontes

- [Video ShotCraft e biblioteca](https://github.com/Vincentwei1021/video-shotcraft)
- [TikTok Video Skills — revisão instalada](https://github.com/iart-ai/tiktok-video-skills/tree/2a775336b5a638cbf8a61dbd785f9a1b649be016)
- [Demos e dependências compartilhadas](https://github.com/Vincentwei1021/video-shotcraft/blob/5a2e98daade313c4f376120f38427eb19a108e8c/demos/README.md)
- [Receitas](https://github.com/Vincentwei1021/video-shotcraft/tree/5a2e98daade313c4f376120f38427eb19a108e8c/references/shots)
- [Composição original do template](https://github.com/Vincentwei1021/video-shotcraft/blob/5a2e98daade313c4f376120f38427eb19a108e8c/template/src/Root.tsx)
- [Atribuição dos áudios](https://github.com/Vincentwei1021/video-shotcraft/blob/5a2e98daade313c4f376120f38427eb19a108e8c/assets/audio/ATTRIBUTION.md)
- [Video TalkCraft](https://github.com/Vincentwei1021/video-talkcraft)
- [Orientações criativas do TikTok para anúncios: vertical e área visível](https://ads.tiktok.com/resources/help/article/creative-best-practices)
- [ArtCraft](https://getartcraft.com/)
- [FilmCraft](https://github.com/storytold/filmcraft)
- [EffectCraft](https://github.com/storytold/effectcraft)
- [VectorCraft](https://github.com/storytold/vectorcraft)

### Variante integral 60/40
Quando solicitada, preservar takes inteiros e ordem original. Registrar sourceIn=0, duração em frames e velocidade 1×; comparar duração, mapeamento e transporte de áudio no export. Layout opcional introduzido no adendo 2.1 de 30.10.2026 e refinado pelo padrão ativo 3.0: recorte no rosto, sem blur lateral. Capturas reais condensadas devem ser declaradas; não confundir cursor editorial com captura contínua.

### Ajustes aprovados para os próximos vídeos — 3.0

A integral “Tá vendo toda essa edição?” está aprovada e não deve ser refeita por esta atualização. Usar Elastic Pop-In/Out em cada letra da palavra de ênfase, contorno duplo (branco interno/preto externo no escuro; preto interno/branco externo no claro) em todo texto sobre a câmera e nas ênfases em geral, e recorte cover com prioridade no rosto. Removida a opção anterior de preencher laterais com blur. Preservar os projetos e manuais históricos já entregues.

### Tipografia SF Pro — 3.0

Fonte geral San Francisco/SF Pro: Display nos títulos, ênfases e CTA; Text nas legendas, rótulos, corpo e apoios. Semibold 600 e Regular 400, largura normal. Medir novamente o texto após carregar a fonte; manter tamanho óptico estável no pop. Fonte local do macOS, procedência em `font-source.json`; Inter permanece apenas nos arquivos históricos. A troca não altera os vídeos aprovados.

## Sincronização da documentação

Manter este fluxo, o padrão visual e os registros de skills no [repositório v-deo-editor-artcraft](https://github.com/Henrique-Teruya/v-deo-editor-artcraft). Materiais e outputs permanecem locais ou no Drive; não entram no Git. Seguir [a política do repositório](docs/REPOSITORY.md) após cada atualização autorizada.

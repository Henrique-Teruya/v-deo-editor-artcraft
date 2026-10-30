# teruya.dev — padrão de vídeo 3.0

**Direção:** referência visual fornecida pelo Henrique, azul #0066CC, branco e cinzas neutros, tipografia cinética e entradas/saídas fluidas com bolha pop.

**Definido em:** 29/10/2026. **Escopo:** TikToks narrados, com aparições pontuais do Henrique.

**Atualização 3.0 — 30/10/2026:** SF Pro como fonte geral, mantendo contorno duplo e motion; regras para os próximos vídeos. “Tá vendo toda essa edição?” integral foi aprovado; vídeo, projetos e documentação histórica dessa entrega permanecem inalterados.

**Estado:** especificação para as próximas edições. Os quadros do manual são ilustrações de estados, não uma animação já implementada ou validada nos editores.

## 1. A assinatura

**A fala vira imagem, e a imagem continua a ideia.** Um termo surge no instante em que é dito, ganha posição e passa a integrar o diagrama. A câmera aproxima o detalhe que está sendo explicado e recua para revelar a relação entre as partes. Elementos persistem e se transformam entre planos.

O visual deve ser claro e ter movimento perceptível. Minimalismo significa poucas coisas competindo pela atenção; não significa manter uma tela parada enquanto a narração avança. Liquid motion significa continuidade de posição, escala, largura, máscara e velocidade. A elasticidade permanece discreta nos apoios; palavras de ênfase têm Elastic Pop-In e Elastic Pop-Out por letra, com retorno amortecido e leitura estável. Evitar vidro intenso, gelatina, partículas, brilho constante e tremor como assinatura padrão.

**Design clean, coreografia expressiva.** Como há poucos elementos e pouca decoração, a energia da edição vem de tipografia cinética, entradas/saídas pop, componentes que se reorganizam e movimentos de câmera que revelam relações. A cada nova ideia, planejar uma ação visual perceptível: apresentar, conectar, transformar, aproximar, comparar ou recuperar o conjunto. Alternar esses recursos, em vez de depender apenas de fade ou repetir o mesmo zoom. A ação assenta antes da leitura; o fundo e os apoios podem continuar estáticos. Aumentar a intenção e a variedade do movimento, não a quantidade de objetos simultâneos.

O sistema tem três marcas reconhecíveis:

1. **Palavra → componente:** a palavra principal diminui e passa a identificar um nó do diagrama.
2. **Foco → relação:** aproximar um componente; recuar quando a fala conecta esse componente ao conjunto.
3. **Azul acompanha o raciocínio:** o foco atual fica azul; elementos já explicados permanecem em superfícies neutras claras ou escuras.

Uma transformação principal por vez. Um novo estado visual a cada ideia; 1,5–3 s é um ponto de partida para trechos rápidos, nunca uma obrigação de cortar. Diagramas complexos podem permanecer 4–5 s com atenção guiada. Preservar tempo para ler depois da entrada.

## 2. Identidade visual

### Cor

A linguagem visual vem do [design Markdown enviado pelo Henrique](references/design-reference.md). Ele é a referência criativa deste projeto; suas descrições do site da Apple não foram tratadas como uma auditoria independente. Adotamos a paleta, a hierarquia tipográfica, o espaço e a geometria. Componentes de loja e navegação não são necessários no vídeo. O azul, usado para ação no site de referência, marca o foco narrativo nos nossos diagramas.

| Token | Valor | Uso |
| --- | --- | --- |
| `blue` | `#0066CC` | Palavra ativa, nó em foco e conexões sobre fundo claro |
| `focusBlue` | `#0071E3` | Foco de interação, quando uma interface o exige |
| `blueOnDark` | `#2997FF` | Palavra ou chamada azul sobre bloco escuro |
| `ink` | `#1D1D1F` | Títulos e texto sobre fundo claro |
| `white` | `#FFFFFF` | Fundo predominante; texto sobre azul |
| `canvas` | `#F5F5F7` | Fundo neutro alternativo |
| `surface` | `#FAFAFC` | Superfície pearl |
| `dark` | `#272729` | Blocos escuros de destaque |
| `dark2` / `dark3` | `#2A2A2C` / `#252527` | Variações de superfície escura |
| `muted` | `#333333` | Apoio legível sobre branco ou cinza claro |
| `mutedOnDark` | `#CCCCCC` | Apoio sobre escuro |
| `line` | `#E0E0E0` | Hairline em cartões utilitários |
| `dividerSoft` | `#F0F0F0` | Separação sutil em superfícies claras |

Branco predomina. Alternar branco, cinza #F5F5F7 e blocos #272729 quando houver uma mudança de ideia; a própria superfície faz a divisão. Blocos de ponta a ponta não têm cantos arredondados, borda ou sombra. Azul é o acento único, em variações adequadas ao fundo; não usar azul-claro decorativo nem navy como segunda cor de marca. Não recolorir interfaces reais a ponto de falsear o produto.

Durante o estado de leitura, texto essencial deve atingir contraste mínimo interno de 4,5:1 com o fundo final, considerando opacidade e compressão. Entrada e saída são transitórias; deixar texto nítido e com contraste completo antes do hold. #2997FF fica restrito ao fundo escuro; #0066CC é usado sobre claro ou como preenchimento com texto branco. #7A7A7A, presente na referência para estados desativados, não é a cor de texto essencial. Não usar apenas cor para diferenciar alternativas: combinar nome, posição, forma ou ícone.

### Tipografia

**San Francisco, família SF Pro, é a fonte geral obrigatória.** Usar **SF Pro Display** em títulos, palavras de ênfase e CTA; **SF Pro Text** em legendas, rótulos, corpo e apoio. A variante é a padrão de largura normal, sem Rounded, Compact ou Mono. Inter deixa de ser o padrão e não deve entrar como fallback silencioso.

Títulos, ênfases, rótulos e legendas em **Semibold (600)**; corpo e apoio em **Regular (400)**. Peso 300 apenas em apoio grande e pontual; 700 só em ênfase rara. Tracking dos títulos: ponto de partida -0,01 em; entrelinha do corpo editorial: 1,44. Preservar acentos e manter `teruya.dev` como wordmark textual em Semibold.

Carregar SF Pro antes de medir largura, quebra de linha, chips e âncoras por letra. Em fonte variável, fixar tamanho óptico e largura durante o Elastic Pop; a animação altera a escala do objeto, sem trocar o desenho da fonte a cada frame. Para o vídeo, a escolha Text/Display segue o papel e o tamanho de leitura na tela, não os pixels de exportação isoladamente.

O PDF utiliza a San Francisco instalada no macOS (`/System/Library/Fonts/SFNS.ttf`), com instâncias ópticas Text e Display e pesos Regular/Semibold. O gerador prepara instâncias temporárias e incorpora subconjuntos; os arquivos de fonte Apple não são empacotados como assets redistribuíveis. A procedência fica em `font-source.json`. Os arquivos Inter e sua OFL são mantidos apenas para reproduzir versões históricas.

Valores em pixels na composição 1080 × 1920:

| Papel | Tamanho inicial | Entrelinha | Limite |
| --- | --- | --- | --- |
| Palavra hero | 144–176 | 1,07–1,10 | 1–3 palavras, até 2 linhas |
| Título | 96–120 | 1,07–1,12 | Preferir até 6 palavras |
| Rótulo de diagrama | 48–64 | 1,19–1,24 | Sem abreviação ambígua |
| Legenda | 60–68 | 1,19 | Até 2 linhas, alvo 3–7 palavras por bloco |
| Apoio essencial | ≥40 | 1,2–1,3 | Apenas se legível no celular |

Medir a fonte carregada antes de distribuir palavras ou calcular largura de chips. Se não couber: reescrever texto de apoio, dividir o estado ou quebrar a linha. Não resolver encolhendo tudo. Uma tela reduzida a 360 px de largura deve continuar legível; o teste real no celular decide.

### Contorno duplo obrigatório nas letras

Todo texto sobre a câmera e todas as palavras de ênfase, inclusive nos quadros explicativos, recebem **dois contornos concêntricos nos próprios glifos**. Manter SF Pro Semibold e o preenchimento da paleta; não é necessário trocar de família tipográfica. As duas bordas acompanham cada letra durante sua animação, sem caixa, placa ou fundo atrás do texto.

| Fundo efetivo atrás do texto | Contorno interno, junto ao preenchimento | Contorno externo, por fora do primeiro |
| --- | --- | --- |
| Escuro | **Branco #FFFFFF** | **Preto #000000** |
| Claro | **Preto #000000** | **Branco #FFFFFF** |

A leitura das camadas, do centro para fora, é **preenchimento → branco → preto** no escuro e **preenchimento → preto → branco** no claro. “Por fora” significa expandir o contorno adicional, sem cobrir ou substituir o interno. Não deslocar as cópias do texto: as três camadas usam exatamente os mesmos glifos, kerning, posição e transformação.

Ponto de partida em 1080 × 1920: espessura visível do anel interno `a = clamp(2 px, 0,035 × tamanho da fonte, 6 px)` e do anel externo `b = clamp(1 px, 0,0175 × tamanho da fonte, 3 px)`. O externo é mais fino, para preservar o visual clean. Em legenda de 60 px: aproximadamente 2,1 px + 1,05 px; em palavra hero de 144 px: 5,04 px + 2,52 px. São espessuras visíveis, não larguras de stroke centrado.

**Ordem de desenho:** contorno externo mais largo → contorno interno → preenchimento intacto por cima. Para strokes centrados no mesmo caminho, usar largura `2 × (a + b)` no externo e `2 × a` no interno. Preservar contraformas e acentos; se alguma letra fechar em tamanho pequeno, ajustar as duas espessuras mantendo ambos os anéis. Sombra curta opcional é apenas complementar. Não usar blur, deslocamento de sombra ou halo para simular a segunda borda.

Escolher a combinação pelo fundo na região do texto, não apenas pelo tema geral da cena. Em gravações com áreas mistas, reposicionar primeiro e manter a decisão estável durante a frase; trocar suavemente o par quando a composição revelar outra superfície. Conferir transição, hold e compressão em 360 px. Rótulos comuns fora da câmera, sem função de ênfase, não precisam de contorno por obrigação. Este refinamento substitui a regra anterior de borda única.

### Composição 9:16

Base 1080 × 1920, 30 fps. Traduzir medidas web da referência com fator 3, considerando um layout base de 360 px para vídeo de 1080 px: grade 8 → 24 px; padding de cartão 24 → 72 px; raio utilitário 8 → 24 px, pearl 11 → 33 px e cartão 18 → 54 px. Pílula usa metade da altura; blocos de ponta a ponta usam raio zero. Não aplicar 18 px web literalmente a toda peça de vídeo. No PDF, usar os mesmos papéis geométricos em pontos: 6 / 8,25 / 13,5 pt.

Hairline de cartão: 1 → 3 px no vídeo; conexões essenciais do diagrama permanecem em 4–6 px por legibilidade. Sem sombras decorativas em texto, cartão ou botão, e sem gradientes decorativos. Exceção funcional: sobre a gravação do apresentador, uma sombra curta somente nos glifos pode sustentar a leitura, sem formar fundo ou halo largo. A sombra de referência `3px 5px 30px rgba(0,0,0,.22)` fica restrita a uma imagem de produto apoiada em superfície (equivalente inicial no vídeo: 9 / 15 / 90 px). Blur de fundo só quando uma sobreposição sobre imagem o justifica; nunca como fundo de texto sobre o apresentador. O movimento liquid vem da animação, não de brilho ou vidro decorativo.

Área interna conservadora: **x=96…900, y=200…1520**. Palco de explicação: y=240…1260. Faixa de legendas: y=1340…1520. O espaço entre ambos evita colisões. A margem direita maior acomoda controles. São guias do projeto, não uma garantia oficial da interface TikTok: conferir o overlay atual e a prévia na conta de destino antes de publicar.

Ter no máximo três componentes principais visíveis quando cada um exigir leitura. Revelar grupos maiores em etapas. Evitar seis cartões pequenos preenchendo a tela. Manter o centro óptico próximo de x=498, não necessariamente no centro geométrico do vídeo.

### Fundo de explicação: sketchbook espaçado

Quando a voz estiver **explicando visualmente um conceito**, usar um grid quadrado de sketchbook bem espaçado e translúcido atrás do diagrama. Ele sinaliza um espaço de raciocínio e construção. É um apoio estático, sem chamar mais atenção que palavras, setas ou componentes.

| Parâmetro | Padrão em 1080 × 1920 |
| --- | --- |
| Espaço entre linhas | **216 × 216 px**, cerca de cinco células na largura; faixa de ajuste 180–240 px |
| Espessura | **1,5 px**, ajustável entre 1–2 px após conferir a compressão |
| Sobre branco ou #F5F5F7 | Linhas **#1D1D1F a 7% de opacidade** |
| Sobre #272729 | Linhas **#FFFFFF a 6% de opacidade** |
| Hierarquia | Uma única malha; sem subdivisões, pontos ou eixos mais fortes |
| Ordem de camadas | Fundo sólido → grid → conexões → componentes → texto; legendas em camada de tela |
| Movimento | Sem drift, pulsação ou desenho de linha repetido. Se houver câmera no diagrama, grid e objetos compartilham o mesmo plano do mundo |

As medidas descrevem o estado geral em escala 1. O zoom pode alterar o tamanho aparente das células de forma contínua; não recalcular a densidade a cada frame. Deixar opacidade, espessura e fase do grid estáveis dentro do plano para evitar cintilação. Conferir o render no celular: a malha deve ser percebida ao olhar o fundo e desaparecer da atenção durante a leitura. Manter cartões e placas de legenda com fundo suficiente para não atravessar as letras.

Usar o grid em diagramas, comparações, passos e transformações explicativas. O apresentador em tela cheia, imagens de apoio, interfaces reais e cartelas de chamada podem manter fundo liso; não sobrepor a malha a toda cena por obrigação. Na entrada ou saída do modo explicação, o fundo pode acompanhar a transição da cena com opacidade suave, sem receber bolha pop. A referência de sketchbook não pede textura de papel, borda de caderno, espiral, sujeira ou tremor no traço.

Assets de referência em SVG transparente: [grid claro](assets/backgrounds/sketchbook-grid-light.svg) e [grid escuro](assets/backgrounds/sketchbook-grid-dark.svg). São camadas de fundo reutilizáveis, não animações já integradas ao vídeo.

## 3. Texto que acompanha a voz

### Três camadas com funções distintas

**Legenda de apoio:** cobre toda a fala, em blocos de sentido. #1D1D1F sobre fundo claro; sobre vídeo do apresentador, texto flutuante com fundo totalmente transparente e cor escolhida pelo contraste da gravação, normalmente branco. Destaque #0066CC sobre claro e #2997FF sobre escuro, com contraste conferido. A legenda fica em coordenadas da tela, independente do zoom do diagrama. Entrada e saída usam pop discreto no bloco; o realce segue as palavras sem fazer a linha inteira pular a cada sílaba.

**Ênfase cinética:** 1–3 palavras importantes entram na região principal quando são ditas. Cada letra da palavra de ênfase tem Elastic Pop-In e Elastic Pop-Out próprios; um pop único no contêiner da palavra não atende à regra. Isso é especialmente importante sobre a câmera e também vale para palavras focais nos diagramas. Uma palavra focal por vez, com contorno duplo: branco interno/preto externo sobre escuro, preto interno/branco externo sobre claro. Não repetir toda a legenda em tamanho gigante.

**Texto como objeto:** o termo apresentado vira título, rótulo, chip ou nó. Exemplo: “MODELO” entra como protagonista e se desloca para dentro do chip que continuará no plano. Preservar identidade visual e continuidade do objeto.

Se um título já cobre integralmente uma fala curta e cumpre a função de legenda, a legenda separada pode ser suprimida naquele intervalo. Não omitir outras palavras faladas; a transcrição/SRT permanece integral. Evitar duas frases iguais competindo ao mesmo tempo.

### Texto flutuante sobre o apresentador

**Todo texto sobre a gravação do Henrique deve aparecer sem fundo.** A regra vale para títulos, palavras cinéticas, legendas, identificação, assinatura e CTA. Não usar placas, cartões, pílulas, faixas, preenchimento atrás da palavra ativa, vidro, blur de fundo ou degradê de proteção.

Manter SF Pro, contorno duplo obrigatório nos glifos e sincronização. Palavras de ênfase usam entrada e saída elásticas por letra; a legenda de apoio mantém pop discreto por bloco e realce por palavra. Preferir branco sobre regiões escuras e #1D1D1F sobre regiões claras; o destaque azul acompanha o contraste (#2997FF no escuro, #0066CC no claro). Primeiro ajustar posição e quebra de linha, evitando olhos e boca. Se necessário, admitir apenas sombra curta nos glifos: ponto de partida `0 2px 5px rgba(0,0,0,.55)` em 1080 × 1920, sem halo largo. Conferir leitura em 360 px e no arquivo comprimido.

Quando um cartão explicativo se transforma em CTA sobre o rosto, retirar sua superfície antes da primeira imagem do apresentador e preservar o texto na transformação. Nas máscaras de saída do rosto, adaptar preenchimento e contorno ao fundo revelado (branco interno/preto externo no escuro; preto interno/branco externo no claro). O texto continua flutuante até o fim dessa aparição. Cartões e fundos seguem permitidos nas cenas de explicação, fora da gravação do apresentador.

### Elastic Pop-In e Elastic Pop-Out por letra

Separar a palavra em **grafemas**: letra e acento animam juntos; espaços mantêm o avanço tipográfico sem virar elementos de foco. Cada grafema tem sua própria escala, opacidade, início e saída. Reservar a largura da palavra desde o começo, preservar kerning e baseline e animar a partir da posição final de cada letra. As letras não empurram suas vizinhas durante o pop.

Valores iniciais a 30 fps, a validar no próximo vídeo:

| Fase | Parâmetros próprios teruya.dev |
| --- | --- |
| **Elastic Pop-In** | 12–16 frames por letra; referência de escala **0,55 → 1,08 → 0,98 → 1**; opacidade chega nos primeiros 3–4 frames. Expansão perceptível, pequeno retorno amortecido e assentamento. |
| Cascata de entrada | Atraso inicial de 1 frame entre letras, ajustável; limitar o espalhamento total a 8 frames. A palavra completa deve assentar em até 24 frames como ponto de partida. |
| Leitura | Palavra inteira nítida e estável, pelo menos 18 frames após a última letra assentar; adaptar à fala. |
| **Elastic Pop-Out** | 10–14 frames por letra; referência de escala **1 → 1,06 → 0,55 → 0**; expansão preparatória curta seguida de recolhimento, opacidade cai nos últimos 4–6 frames. |
| Cascata de saída | Atraso inicial de 1 frame, com espalhamento total limitado a 6 frames; saída completa em até 20 frames como ponto de partida. Pode seguir leitura, inverter ou partir do centro conforme a composição. |

A primeira letra começa junto da palavra falada, dentro da janela de antecipação de 0–2 frames. Encurtar o stagger em palavras longas e ajustar a duração ao espaço disponível, preservando a janela de leitura. Se não houver espaço, selecionar uma ênfase mais curta; não acelerar a gravação para acomodar a animação.

Usar interpolação elástica amortecida ou curvas amostradas que preservem esses estados, nunca keyframes lineares secos. Escala isotrópica, sem deformar as letras; deslocamento opcional curto segue o significado, não uma subida vertical automática. Os dois contornos e o preenchimento viajam juntos, inclusive na opacidade; não aplicar springs separados nas bordas. Não duplicar elasticidade no pai e nos filhos. Quando a palavra virar rótulo persistente, assentar as letras, fazer o morph contínuo e executar Pop-Out individual ao retirar definitivamente a palavra.

Este preset próprio substitui o antigo limite de 1,5% **somente nas letras de ênfase**: entrada até 8% e preparação de saída até 6%, com retorno curto e sem pulsação contínua. Legendas de apoio e elementos comuns continuam discretos. Os valores são especificação, não animação já validada; registrar entrada, pico, hold e saída na próxima produção.

### Sincronização

1. Fechar a montagem da voz antes da animação. Alinhar palavras à gravação e revisar a transcrição em português.
2. Registrar `startSec`/`endSec` de cada palavra e seu trecho fonte. Converter para frames na composição: `round(segundos × fps)`.
3. Para palavra enfatizada, início da entrada de 0 a 2 frames antes do início falado. Alvo de revisão: diferença de até 3 frames (100 ms a 30 fps), conferida no áudio. A antecipação não deve revelar a conclusão antes da voz.
4. Blocos de legenda entram pelo sentido da frase. Palavras muito rápidas não recebem entradas individuais completas; usar bloco legível com preenchimento ou realce sincronizado.
5. Guardar leitura após o movimento: mínimo inicial de 18 frames para 1–3 palavras; 30 frames para nomes/listas depois de assentarem. Frases maiores exigem mais tempo. Esses mínimos não substituem leitura real.

Não distribuir palavras por intervalos iguais. Não tratar transcrição automática como alinhamento definitivo. Não inventar uma forma de onda sem relação com o áudio.

## 4. Gramática de movimento

Todos os números abaixo são **defaults próprios teruya.dev**. Receitas ShotCraft preservam seus parâmetros essenciais; diferenças ficam registradas no manifesto. Uma adaptação não deve ser descrita como reprodução exata.

| Movimento próprio | Tempo a 30 fps | Curva / comportamento |
| --- | --- | --- |
| Entrada de texto de apoio / bloco de legenda | 8–12 f / 267–400 ms | Pop 0,94→1,015→1; opacidade 0→1 nos primeiros 3–4 f; origem na palavra |
| Entrada de componente | 16–24 f / 533–800 ms | Pop 0,86–0,92→1,02–1,03→1; posição opcional desde a origem semântica |
| Reorganização / morph | 20–28 f / 667–933 ms | `cubic-bezier(.6,0,.18,1)`; posição, largura e altura compartilham progresso |
| Saída | 8–12 f / 267–400 ms | Desinflar 1→0,90–0,96 e apagar suavemente nos últimos 4–6 f; ou transformar no próximo objeto |
| Foco de câmera | 18–30 f / 600–1000 ms | `cubic-bezier(.55,0,.18,1)`; escala e centro ligados |
| Retorno da câmera | 24–36 f / 800–1200 ms | Mesma família suave; devolver a relação espacial |

A duração muda com a fala; velocidade não deve prejudicar leitura. Converter pela duração em segundos ao mudar fps. Não reaproveitar 24 frames de 30 fps em 60 fps sem ajuste.

**Liquid + bolha pop:** um chip muda a largura medindo a palavra nova; o texto mantém suas proporções. Um contêiner cresce para acomodar ferramentas; seus rótulos acompanham o objeto pai. Uma linha continua para a próxima cena. O pop é expansão isotrópica curta, com uma única ultrapassagem sutil e assentamento. Limite inicial: 1,5% em texto de apoio e 3% em objetos. Exceção explícita: letras de ênfase seguem Elastic Pop-In/Out, com picos de 8%/6% e retorno amortecido. Não esticar glifos, deformar o rosto nem repetir várias oscilações.

**Entrada → ação → leitura → saída.** Escrever esses quatro estados na ficha da cena. A saída pode ser uma transformação útil, não precisa ser sempre fade. Elementos secundários podem acompanhar 2–4 frames depois do principal, sem criar outro foco.

### Regra obrigatória: entrada e saída de todo elemento focal

Todo texto, ícone, cartão, imagem, destaque ou componente que aparece para chamar atenção precisa ter **entrada e saída fluidas planejadas**. O ciclo deve ser perceptível, sem surgir ou desaparecer por um corte acidental. O último elemento também precisa de fechamento: sua saída pode ocupar os últimos frames, depois do tempo de leitura, com o fundo da composição mantido. Objetos que continuam em outra cena fazem uma transição com identidade preservada, registrada como saída/transformação, sem desaparecer e reaparecer.

**A base pode ser estática.** Fundos, superfícies, divisórias, molduras de apoio, rótulos já compreendidos e componentes sem foco podem permanecer imóveis. A obrigação de pop pertence aos elementos focais, não a tudo que está visível. Um elemento focal também fica estático durante a leitura depois de assentar. Não acrescentar drift, pulsação ou movimento ambiente só para manter a tela animada.

Se um objeto estático passa a ser o foco, animar a entrada e a saída da **camada de destaque** ou sua mudança de estado; o objeto base pode continuar no mesmo lugar. Encerrar o foco não exige remover o objeto do diagrama. Registrar na ficha `role: static-support` ou `role: focal`, e se a saída é do objeto, do destaque ou uma transformação contínua.

| Variante própria | Entrada | Saída | Quando usar |
| --- | --- | --- | --- |
| `bubble-pop-center` | 0,88→1,025→1 em 18 f; opacidade em 4 f; centro fixo | 1→0,92 em 10 f; opacidade nos últimos 5 f | Palavra-chave, ícone ou objeto isolado |
| `bubble-pop-origin` | 0,86→1,03→1 em 20 f; vem do ponto de conexão, deslocamento curto de 16–40 px | Retorna ao ponto de origem ou se incorpora ao pai em 12–20 f | Ferramenta que se conecta ao harness |
| `bubble-pop-inline` | 0,94→1,015→1 em 10 f; âncora na palavra, sem mover a linha | 1→0,96 + opacidade em 8 f | Texto de apoio e blocos de legenda; ênfase usa elastic por letra |
| `bubble-pop-replace` | A nova forma emerge enquanto a anterior muda de largura e se recolhe, em 20–28 f | A anterior sai pelo mesmo morph; sem duplicar leitura | Troca de termo ou estado de um chip |
| `bubble-pop-frame` | Moldura/recorte de imagem 0,96→1,01→1 em 18 f, com máscara ou opacidade | Recolhimento do quadro em 10–14 f | Imagem de apoio ou janela do apresentador |

Direções permitidas: centro, esquerda, direita, cima, baixo, diagonal ou ponto de conexão. Escolher pelo vínculo visual: uma peça pode sair do seu pai, uma resposta pode expandir no lugar e uma comparação pode entrar pelo lado correspondente. A direção não é aleatória. A subida vertical deixa de ser o comportamento automático. Nunca aplicar uma deformação de bolha ao rosto; animar o enquadramento ou a máscara.

O pop deve começar junto da palavra e terminar rápido o suficiente para permitir leitura. Não transformar todas as palavras em eventos grandes: legendas têm pop discreto por bloco, enquanto uma palavra-chave por ideia recebe a ênfase principal. Opacidade sozinha não entrega a assinatura pop. Efeitos sonoros permanecem seletivos.

O par `elastic-pop-in-letter` / `elastic-pop-out-letter` é obrigatório nas palavras de ênfase. Os cinco presets de bolha acima continuam disponíveis para componentes e textos de apoio; não substituem o ciclo por letra.

### Como aproveitar o componente enviado

O [componente VerticalCutReveal](references/VerticalCutReveal.reference.tsx) fornece uma referência de spring (`stiffness: 190`, `damping: 22`), segmentação e stagger. Seu código anima `y` de ±100% até zero: ele não implementa escala de bolha nem uma saída independente. Aproveitar a sensação de assentamento e a organização por unidades; adicionar os estados próprios de escala, opacidade, origem e saída descritos acima. `reverse` só muda o sentido vertical no exemplo, não resolve essa gramática.

Usar 190/22 apenas como ponto de partida se o motor suportar spring equivalente; massa, duração, amostragem e resultado visual precisam ser conferidos. Os frames e picos da tabela são o alvo editorial. Para render offline, amostrar o movimento pela timeline e fixar qualquer aleatoriedade; não usar `Math.random()` por render nem depender de `autoStart` no momento da montagem do componente. O stagger padrão de 0,2 s do exemplo deve ser substituído pelos tempos reais das palavras ou por pequenos atrasos de 2–4 frames entre peças relacionadas.

As receitas ShotCraft continuam válidas: seu desenho, câmera ou montagem pode ser a entrada principal, com chegada e saída pop adaptadas. Não empilhar dois springs em pais e filhos, nem substituir o movimento que define uma receita por um pop genérico. Registrar como **adaptação ShotCraft + envelope teruya** quando a assinatura alterar os parâmetros originais.

## 5. Zoom, câmera e apresentador

### Enquadramento da gravação: recorte para preencher

**Nunca preencher as laterais da câmera com blur.** Usar o próprio take em escala proporcional e recortar espacialmente para preencher todo o espaço destinado à câmera, priorizando o rosto falando. A regra vale para tela inteira, 60/40 e qualquer outro layout.

- Ajustar escala em modo cover: `max(largura do quadro / largura da fonte, altura do quadro / altura da fonte)`. Recortar o excedente, sem esticar a imagem.
- Posicionar a janela de recorte a partir do rosto. Preservar olhos, boca, testa e queixo sempre que possível, com pequena margem para o movimento natural. Tronco e cenário podem sair do enquadramento antes do rosto.
- Durante mudanças de layout, interpolar escala e posição de forma contínua e acompanhar o rosto suavemente; não deixar o recorte saltar ou perseguir cada microgesto.
- Não completar largura com cópia desfocada, espelhada ou esticada da gravação. Se o rosto não couber no recorte, ajustar a geometria do painel ou escolher outro enquadramento.
- “Cortar” aqui significa **recorte espacial**, não retirar tempo, pausas ou falas. Regras de continuidade temporal continuam valendo quando o episódio for integral.


Cada zoom responde a uma pergunta: **qual detalhe precisa ser visto agora?** Cada zoom out responde: **qual relação fica clara ao recuperar o conjunto?**

- Aproximação leve de diagrama: escala 1→1,08–1,18 em 18–30 frames.
- Foco em detalhe: 1→1,2–1,4, desde que a resolução, os rótulos e o enquadramento suportem. A escala exata vem do alvo, não de uma obrigação estética.
- Retorno: 1,25→1 em 24–36 frames; manter 18–30 frames de leitura do conjunto ao fim.
- Apresentador: primeiros 2–4 s e momentos de opinião, transição ou conclusão. Alvo flexível de 10–20% de um vídeo de 45–60 s. Não cumprir uma cota à custa da narrativa.
- Reenquadramento do rosto, quando útil: escala 1→1,04–1,08 em ≥18 frames, sem cortar testa, boca ou gestos importantes. Evitar zoom contínuo por toda a fala.

Usar um único transform pai para a câmera do mundo. Definir centro, escala e objeto alvo. Fórmula conceitual: `tela = centroDoViewport + (pontoDoMundo - centroDaCamera) × escala`. Legendas e controles explicativos fixos ficam fora desse grupo. Ao chegar no detalhe, interromper o movimento de câmera para a leitura. Não empilhar entrada forte de texto, zoom e desenho de diagrama no mesmo instante.

## 6. Biblioteca ShotCraft selecionada

Referência fixada em `5a2e98daade313c4f376120f38427eb19a108e8c`. Catálogo e código locais: `/Users/henrique/.codex/skills/video-shotcraft`. Registro completo, hashes dos arquivos e links: [shotcraft-recipes.json](shotcraft-recipes.json).

| Receita / variante | Uso teruya.dev | O que precisa sobreviver à adaptação |
| --- | --- | --- |
| `type-rhythm-sync` / `karaoke-fill-sync` | Palavra acompanhando a voz | Duas camadas idênticas, máscara de preenchimento contínuo pelos tempos reais; contraste de base suficiente |
| `blur-slide` | Frase que entra por palavras | Opacidade, deslocamento e blur ligados ao mesmo progresso; sequência sobreposta, não três efeitos desconectados |
| `lead-word-zoom-assemble` | Gancho com palavra protagonista | Zoom ancorado na palavra medida e montagem da frase; recompor para 9:16. A versão teruya omite o crash final e registra essa alteração |
| `title-demote-to-label` | Conceito vira rótulo do diagrama | O mesmo texto muda escala e posição pela mesma curva; conteúdo entra durante a chegada. Rótulo final ≥40 px |
| `pill-chip-slot-cycle-handled` | Alternar conceitos dentro de um chip | Largura medida e movimento vertical ligados; recorte e elementos vizinhos acompanham. Não deformar letras |
| `list-reveal` | Aplicativos, etapas ou ferramentas | Escala, y, foco, overshoot sutil, ícone +2 f e detalhe +4 f; separar drift do contêiner da entrada local |
| `draw-svg-trace` | Desenhar harness, ligação ou contêiner | Traçado e cabeça no mesmo caminho; fechamento perceptível antes do preenchimento; duração de leitura preservada |
| `cursor-flyover` | Explicar uma interface real | Cursor antecede câmera e aponta ação; clique produz resposta; câmera repousa antes de seguir |
| `line-carry-transition` | Uma relação leva à próxima cena | A linha permanece contínua e a câmera acompanha a ponta; final vira contêiner. Cena original de 190 f, não uma transição de 12 f |

Escolher as receitas pelo significado. Um vídeo típico pode usar 2–4 famílias, além da legenda; isso não é uma cota. `line-carry-transition` é opcional e normalmente aparece no máximo uma vez. Não inserir cursor em um diagrama abstrato só para alegar uso da receita. Nosso foco/retorno de diagrama é um preset próprio, não a receita completa `cursor-flyover`.

### Uso real e comprovação

Para cada cena registrar: ID, `recipeId`, `styleKey`, caminho do TSX, revisão/hash, parâmetros originais, alterações de marca, frames de fala, motor usado e caminhos das evidências. Ler o cartão e o código específico. Conferir a referência visual. Renderizar início, pico, chegada e hold; comparar também em movimento.

**Caminho A, nativo preferido:** traduzir os componentes e curvas para EffectCraft, com vetores do VectorCraft. Conferir suporte a máscara, blur, tipografia e curvas antes. Se faltar um recurso que define a receita, não chamar o resultado de implementação fiel. Identificar como variante e explicar o que mudou, ou usar o caminho B.

**Caminho B, Remotion:** implementar a receita a partir do TSX e renderizar o trecho para o FilmCraft. Preservar fontes, código, dependências e assets. O trecho importado não ganha camadas de texto editáveis no FilmCraft. Testar alpha antes de depender de transparência; uma cena com fundo opaco pode simplificar o intercâmbio.

Não há exportação automática nativa confirmada entre ShotCraft e ArtCraft. Este manual verifica os arquivos de referência, não comprova que os nove presets já estejam instalados ou renderizados em EffectCraft. O manifesto deve manter `validation.status=pending` até a validação real.

## 7. Estrutura de um episódio

| Parte | Função | Tratamento |
| --- | --- | --- |
| 0–3 s | Gancho e presença | Henrique + texto curto que entra na fala; sem vinheta antes da promessa |
| 3–10 s | Nomear o conceito | Palavra hero vira componente; reduzir o apresentador ou cortar para a explicação |
| Desenvolvimento | Demonstrar | Uma mudança visual por ideia; câmera aproxima detalhes e retoma contexto |
| Momento de opinião | Reforçar autoria | Henrique reaparece quando a frase ganha com expressão ou gesto |
| Últimos 3–5 s | Conclusão e pergunta | Recuperar o diagrama, estabilizar leitura e apresentar CTA curto |

A duração vem da gravação e da clareza. Para o formato atual, 45–60 s é uma faixa inicial; o limite de 60 s é uma escolha editorial, não uma afirmação do limite da plataforma. Reutilizar identidade e gramática, variar a estrutura quando o assunto pedir.

### Estudo de aplicação: “Mesmo modelo, resultados diferentes”

**Somente proposta de direção; nenhum arquivo do vídeo atual foi alterado nesta etapa.** Referência de montagem existente: 1508 frames, aproximadamente 50,27 s.

| Trecho aproximado | Novo estado visual proposto | Receita / preset |
| --- | --- | --- |
| 0–5,87 s | “Mesmo modelo” aparece na fala; “resultados diferentes” completa o gancho; saída do rosto preserva o termo modelo | `lead-word-zoom-assemble`, variante teruya sem crash |
| 5,87–9,87 s | MODELO e HARNESS entram na menção; um deles diminui e vira rótulo da estrutura | `title-demote-to-label` + legenda sincronizada |
| 9,87–18,67 s | Chip preservado; contorno do harness se desenha; foco na relação entre interior e exterior | `draw-svg-trace` + foco/retorno próprio |
| 18,67–23,67 s | Retorno breve do Henrique; “ferramentas” e “contexto” entram nas palavras e ocupam dois compartimentos | `blur-slide` + reorganização própria |
| 23,67–38,07 s | Aplicativos revelados nas menções; câmera visita saídas e recua para a comparação | `list-reveal` + foco/retorno próprio |
| 38,07–48,77 s | “modelo” e “harness” recebem foco conforme a conclusão; diagrama recomposto; Henrique retorna | Reuso dos componentes + `karaoke-fill-sync` |
| 48,77–50,27 s | Pergunta já iniciada sobre a fala permanece: “Qual harness você usa?”; saída pop discreta nos últimos 8–10 f | Leitura, assinatura e fechamento fluido |

Os tempos das palavras precisam ser medidos antes da futura aplicação. Nomes de produtos e versões citados na fala também precisam de conferência editorial; o padrão visual não valida essas afirmações.

## 8. Som, imagem e entrega

A voz determina o ritmo. Uniformizar volume sem esmagar a expressão; ponto de partida de entrega: aproximadamente -16 LUFS integrados e pico verdadeiro ≤-1 dBTP. São alvos internos, não especificação oficial do TikTok. Ouvir do começo ao fim no celular. Evitar portão de ruído cortando consoantes, SFX sobre palavras importantes e música competindo com a narração.

Usar SFX discretos em conexões, fechamento de traço ou chegada relevante, não em cada palavra. Música é opcional. Preservar origem/licença de fontes, áudios e imagens. Se a fonte é HDR, conferir conversão para SDR/Rec.709 com escopos e aparência da pele; marcar Rec.709 sozinho não faz tone mapping.

Entrega padrão: MP4 H.264, 1080 × 1920, 30 fps constantes, SDR/Rec.709, áudio AAC 48 kHz. Ponto de partida 15–25 Mb/s, adaptado ao material; conferir arquivo codificado, não só preview. Guardar projeto editável, vetores, motion source, transcrição/SRT, manifesto e mídia. Não sobrescrever o original. Destino de exportação ou upload vem da instrução de cada trabalho.

## 9. Fluxo de produção e qualidade

1. **Voz:** editar a narrativa, revisar transcrição e registrar cortes com fonte/in/out.
2. **Beat sheet:** uma ficha por cena com ideia, palavra âncora, imagem, receita, alvo de câmera e hold. Usar [scene-template.json](scene-template.json).
3. **Assets:** vetores no VectorCraft, interfaces reais quando necessário, fontes carregadas e nomes conferidos.
4. **Motion:** montar em EffectCraft ou Remotion, usando [tokens.json](tokens.json) e o manifesto. Preview de cada receita antes de montar tudo.
5. **Montagem:** FilmCraft, com voz contínua, legendas em coordenadas da tela e aparições pontuais.
6. **Revisão:** render completo, leitura no celular, áudio integral e comparação com referências. Se houver revisão independente exigida pelo fluxo de produção, executá-la antes da entrega final.
7. **Arquivo:** guardar fontes, parâmetros, versões e evidências; exportar e conferir duração, cores, áudio e sincronização.

### Critérios de aprovação

- [ ] O gancho começa com conteúdo; a identidade está na linguagem visual.
- [ ] As palavras enfatizadas acompanham a fala e a legenda cobre o conteúdo integral.
- [ ] Cada cena tem entrada, ação, tempo de leitura e saída/transformação definidos.
- [ ] Todo elemento focal tem entrada e saída fluida, inclusive o último; permanências são transformações contínuas registradas.
- [ ] Fundos e apoios podem ficar estáticos; o hold de leitura é estável e elementos sem foco não competem por atenção.
- [ ] Cenas de explicação usam o grid largo e translúcido; a malha não atravessa a leitura nem vira protagonista.
- [ ] A cada nova ideia há uma ação visual planejada: texto, componente ou câmera. A estética clean tem movimento expressivo e variado, com pausas de leitura.
- [ ] Bolha pop é perceptível e assenta uma vez; texto não deforma e não há spring duplicado em pais/filhos.
- [ ] Origem e direção seguem a relação entre os objetos; entradas não repetem automaticamente a subida vertical.
- [ ] Componentes realmente se movem e mudam de estado quando a ideia muda.
- [ ] Existe uma hierarquia visual clara; câmera e objeto não disputam atenção.
- [ ] Zoom tem alvo e retorno com propósito; legenda mantém tamanho de tela.
- [ ] Todo texto sobre o apresentador é flutuante, sem placas, faixas, chips ou blur de fundo; contraste e transições conferidos.
- [ ] Cada letra das palavras de ênfase tem Elastic Pop-In e Elastic Pop-Out próprios; acentos unidos, largura reservada e leitura estável.
- [ ] Texto sobre a câmera e ênfases têm contorno duplo: branco interno/preto externo no escuro e preto interno/branco externo no claro; ambos permanecem visíveis sem fechar contraformas ou criar fundo.
- [ ] A câmera preenche o painel por recorte proporcional centrado no rosto; nenhuma lateral usa blur ou duplicação da gravação.
- [ ] SF Pro carregada e identificada; Display/Text e pesos corretos, sem substituição por Inter. Larguras e acentos revistos após a troca.
- [ ] Não há texto minúsculo, cortes, colisões ou controles encobrindo informação.
- [ ] Azul e branco predominam; liquid aparece na continuidade, sem excesso de efeitos.
- [ ] Cada receita declarada possui fonte, parâmetros, variante e evidência de render.
- [ ] Revisão com e sem som confirma entendimento e ritmo; áudio foi ouvido integralmente.
- [ ] SDR/Rec.709 e enquadramento conferidos no arquivo final; originais preservados.

### Instrução reutilizável para a próxima edição

> Edite este vídeo seguindo `standards/teruya-dev/VIDEO_STANDARD.md` e os tokens da versão 3.0. Use a gravação original e faça a voz conduzir o ritmo. Adote o design Markdown: branco, #F5F5F7, blocos #272729, azul #0066CC sobre claro e #2997FF sobre escuro; SF Pro Display Semibold nos títulos e ênfases, SF Pro Text nas legendas e rótulos em Semibold e no corpo em Regular. Use raios por função, sem sombras ou gradientes decorativos. Nas explicações, use o grid sketchbook de 216 px e baixa opacidade atrás dos diagramas. Faça o design clean ganhar energia com coreografia de texto, componentes e câmera, mantendo pausas de leitura. Todo elemento focal deve ter entrada e saída fluida de bolha pop, com expansão curta, assentamento único e direção ligada ao significado, não sempre de baixo para cima. Fundos e apoios podem permanecer estáticos; manter o hold de leitura estável e animar apenas a camada de destaque quando o objeto base já existe. Sobre a gravação do Henrique, todo texto deve flutuar sem fundo, incluindo legendas e CTA; usar dois contornos nos glifos: branco interno e preto externo sobre fundo escuro; preto interno e branco externo sobre fundo claro. Desenhar externo, interno e preenchimento nessa ordem; manter as três camadas alinhadas durante a animação. Aplicar Elastic Pop-In e Elastic Pop-Out em cada letra das palavras de ênfase, preservando acentos, kerning, leitura e sincronização. Legendas de apoio continuam discretas. Encaixar a câmera por recorte espacial proporcional com foco no rosto, nunca por blur lateral. Sombra curta nos glifos é apenas complementar. Inclua tipografia cinética sincronizada, componentes que se reorganizam, zoom com alvo e retorno e aparições pontuais do Henrique. Use `motion-presets.json` e registre o ciclo de cada objeto em `scene-template.json`. Selecione as receitas ShotCraft pelo significado, leia cartão e TSX, registre adaptações e valide o resultado em movimento. Preserve projeto, fontes, manifesto e legendas. Confira leitura no celular, som, cores e sincronização antes da entrega.

## 10. Manutenção e fontes

Este arquivo é a referência operacional principal. O PDF é o manual visual; JSONs são parâmetros e modelos de registro, não presets nativos instaláveis. Mudanças de identidade, família tipográfica ou linguagem geral mudam a versão principal; refinamentos de execução, valores e exemplos dentro dessa identidade recebem versão secundária. Registrar decisões no changelog. Se uma receita for atualizada, comparar o código e renovar os hashes e as evidências.

- [ShotCraft, revisão utilizada](https://github.com/Vincentwei1021/video-shotcraft/tree/5a2e98daade313c4f376120f38427eb19a108e8c)
- [Cartões das receitas](https://github.com/Vincentwei1021/video-shotcraft/tree/5a2e98daade313c4f376120f38427eb19a108e8c/references/shots)
- [Código dos demos](https://github.com/Vincentwei1021/video-shotcraft/tree/5a2e98daade313c4f376120f38427eb19a108e8c/demos)
- [SF Pro — Apple Developer](https://developer.apple.com/fonts/): referência oficial da família San Francisco. Origem local e parâmetros em `font-source.json`.
- Inter/OFL em `assets/fonts/`: material histórico das versões 1 e 2, sem fallback automático nas novas produções.
- [Design Markdown fornecido pelo Henrique](references/design-reference.md): cores, tipos, geometria e linguagem editorial.
- [VerticalCutReveal fornecido pelo Henrique](references/VerticalCutReveal.reference.tsx): referência de assentamento e segmentação; não um preset de bolha pop já implementado.
- [Presets próprios de bolha pop](motion-presets.json): alvos de entrada/saída para implementar e validar.
- Direção de marca: preferências e feedback do Henrique neste projeto, em 29/10/2026.

### Changelog

- **3.0 / 30.10.2026:** SF Pro substitui Inter como fonte geral: Display em títulos/ênfases/CTA, Text em legendas/rótulos/corpo. Manual visual renderizado com a San Francisco do macOS; contorno duplo, pop por letra e recorte no rosto preservados. O vídeo aprovado continua intacto.

- **2.2.1 / 30.10.2026:** substituir borda única por contorno duplo: branco interno e preto externo no fundo escuro; preto interno e branco externo no fundo claro. Preservar preenchimento, transparência e animação por letra. Válido para próximas edições, sem refazer o vídeo aprovado.
- **2.2 / 30.10.2026:** refinamento obrigatório para próximos vídeos: Elastic Pop-In/Out individual por letra de ênfase, contorno branco no escuro/preto no claro e recorte da câmera para preencher o painel sem blur lateral. Substitui a permissão anterior de preenchimento desfocado. A edição integral aprovada e seus arquivos históricos não foram refeitos.

- **2.1 / adendo 30.10.2026:** variante opcional apresentador + quadro 60/40; continuidade integral, reenquadramento proporcional, legendas separadas e transformações de 18–24 frames.

- **2.1 / adendo 29.10.2026:** texto flutuante obrigatório sobre o apresentador, incluindo legendas e CTA. Removida a orientação de placa; sombra curta nos glifos permitida apenas para legibilidade. Aplicado ao episódio “Tá vendo essa edição?”.

- **2.1 / 29.10.2026:** grid de sketchbook espaçado e translúcido nas explicações, com SVGs claro/escuro e parâmetros; reforço de motion e câmera como fonte de energia do design clean, preservando apoios estáticos e holds de leitura.
- **2.0 / 29.10.2026:** adoção do design Markdown enviado; azul #0066CC, superfícies neutras claras/escuras, títulos 600, raios por função e ausência de decoração. Entradas e saídas de bolha pop obrigatórias para todo elemento focal, com direções semânticas e referência de spring enviada. Atualização somente da documentação.
- **1.0 / 29.10.2026:** identidade azul/branco; três funções de texto; continuidade de componentes; foco/retorno; seleção de nove receitas; tokens, ficha de cena e critérios de validação. Documentação apenas nesta etapa.

## Variante opcional: apresentador + quadro 60/40

Adendo de 30.10.2026. Usar quando a presença contínua do apresentador ajudar a explicação; não é o formato obrigatório dos próximos episódios.

- Tela 1080 × 1920: quadro superior 1080 × 1152 (60%) e câmera inferior 1080 × 768 (40%). Divisão reta, sem molduras grossas ou arredondamento.
- Alternar com câmera inteira por transformação contínua de 18–24 frames. Manter a câmera e o áudio avançando durante a mudança; não congelar nem reiniciar o take.
- Reenquadrar proporcionalmente para preservar olhos, boca e testa. Preencher o painel por escala proporcional e recorte espacial com foco no rosto. Nunca completar margens com blur, imagem espelhada ou alongamento; ajustar a posição do recorte ou a geometria do painel se necessário.
- Quadro branco com grid 216 px, 1,5 px e 7%; diagramas ocupam a região superior, legendas ficam em x=96, y≈990, largura=804, até duas linhas. Adaptar por cena e conferir espaço antes da divisória.
- Em câmera inteira, legendas na área inferior segura e todo texto flutuante, sem preenchimento. Durante a transformação, adaptar preenchimento e contorno à superfície revelada; palavras de ênfase mantêm animações próprias por letra.
- A câmera do diagrama não move as legendas nem o apresentador. Texto e componentes focais têm entrada, leitura e saída/transformação; fundo e apoios podem permanecer estáticos.
- Confetes e arcos podem demonstrar edição no gancho: limitar a poucos segundos, proteger olhos e boca, recolher antes da explicação. São efeitos próprios, não uma receita ShotCraft por associação.
- Quando a edição for integral, documentar fonte, início, quantidade de frames e velocidade 1×. Não remover pausas, repetir frames para substituir conteúdo, antecipar clipes ou sobrepor falas na junção.

Aplicação inicial: “Tá vendo toda essa edição?”, 1680 + 651 = 2331 frames / 77,7 s. X acima de cada negativa, com dois traços e sem cobrir letras. Capturas reais condensadas do editor são identificadas no registro de produção; cursor e zoom editoriais não devem ser apresentados como gravação contínua da interface.

# Padrão teruya.dev 3.0

Comece pela [especificação operacional](VIDEO_STANDARD.md), referência principal deste pacote. O manual visual em PDF é gerado localmente com `scripts/build_manual.py`; outputs não são versionados. Veja o [setup](../../docs/SETUP.md).

| Arquivo | Função |
| --- | --- |
| `tokens.json` | Cores, fonte, composição, curvas e tempos próprios da marca |
| `shotcraft-recipes.json` | Nove receitas com fonte, hash, parâmetros e mudanças previstas |
| `scene-template.json` | Modelo de ficha por cena, com fala, câmera e evidências |
| `motion-presets.json` | Cinco variantes de bolha pop + Elastic Pop-In/Out por letra de ênfase |
| `references/design-reference.md` | Design enviado pelo Henrique, preservado como referência |
| `references/VerticalCutReveal.reference.tsx` | Componente enviado, preservado como referência de movimento |
| `assets/backgrounds/` | Grid sketchbook em SVG transparente, claro e escuro |
| `font-source.json` | Origem local da SF Pro e instâncias Text/Display para o manual |
| `assets/fonts/` | Inter/OFL preservadas apenas para versões históricas |

Os JSONs documentam o padrão; não são presets nativos instaláveis. A implementação das variantes e sua validação em movimento acontecem durante a próxima edição. O vídeo anterior não foi modificado por este trabalho. A versão 3.0 adota SF Pro como fonte geral: Display em títulos, ênfases e CTA; Text em legendas, rótulos e corpo. Mantém o grid sketchbook, Elastic Pop-In/Out por letra, contorno duplo (branco interno/preto externo no escuro; preto interno/branco externo no claro) e recorte proporcional da câmera com foco no rosto, sem blur lateral. Vale para próximas edições; a integral aprovada não foi alterada. O padrão usa o design Markdown enviado e exige entrada/saída fluida de bolha pop para os elementos focais. As versões anteriores estão arquivadas no workspace em `output/archive/`.

Para regenerar o PDF: executar `scripts/build_manual.py` com Python e ReportLab. Ele utiliza a San Francisco instalada no macOS e `hb-subset`, prepara instâncias temporárias e escreve em `output/pdf/`. Não redistribui os binários da Apple. Sem SF Pro, o gerador interrompe com erro explícito, sem fallback silencioso. Para conferir as fontes de receita e regenerar os JSONs: `scripts/build_spec.py`, com a revisão documentada do ShotCraft disponível no caminho indicado no script. Preservar adaptações futuras antes de regenerar.

O documento principal possui um prompt reutilizável para as próximas edições e um changelog. Atualizações na direção devem ser refletidas no documento, nos tokens, no manual e em `WORKFLOW.md`.

## Adendo: texto sobre o apresentador

Títulos, legendas e CTA flutuam sobre a gravação, sem placas, cartões, faixas, blur ou fundos por palavra. Texto sobre a câmera tem contorno duplo: branco interno e preto externo no escuro; preto interno e branco externo no claro. Palavras de ênfase têm entrada e saída elásticas por grafema. Legendas de apoio preservam pop discreto e realce por palavra; sombra curta nos glifos é apenas complementar. Regras 3.0 consolidadas no manual, tokens e PDF para as próximas produções. As edições já aprovadas preservam sua documentação histórica.

## Enquadramento do apresentador

Preencher o painel por escala proporcional e recorte espacial, com olhos e boca sempre priorizados. Proibido preencher laterais com blur ou cópia da gravação. Se necessário, ajustar o recorte ou a geometria do painel. Recorte espacial não autoriza cortes temporais.

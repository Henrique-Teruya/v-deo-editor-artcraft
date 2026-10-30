# Skills de vídeo

O [catálogo](catalog.json) registra origem, revisão e papel de cada pacote. As skills completas ficam no diretório de skills do Codex, fora deste Git. Este repositório não copia demos, bibliotecas de áudio, dependências ou softwares upstream.

| Skill | Uso |
| --- | --- |
| `video-shotcraft` | Receitas de shots, tipografia, componentes e câmera |
| `short-form-video` | Estrutura e composição vertical |
| `caption-animation` | Legendas com tempos reais por palavra |
| `countdown-video` | Contagens regressivas quando o conteúdo pedir |
| `lower-thirds` | Identificação de apresentador |
| `tiktok-marketing` | Opcional já existente: planejamento e legendas editoriais |

## Instalação reproduzível

```sh
python3 scripts/install_skills.py
python3 scripts/install_skills.py --apply
```

O instalador deste projeto chama o `skill-installer` oficial disponível em `${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-installer/scripts/install-skill-from-github.py`. É necessário ter o Codex preparado. A prévia não baixa nem altera arquivos; `--apply` instala somente os destinos ausentes.

- ShotCraft: `5a2e98daade313c4f376120f38427eb19a108e8c`.
- TikTok Video Skills: `2a775336b5a638cbf8a61dbd785f9a1b649be016`.

As quatro skills TikTok recebem os auxiliares `scripts/` e a licença da mesma revisão, com SHA-256 conferido. Para o ShotCraft, o script restaura o vínculo `workbench/demosrc` quando o ZIP representa esse symlink como texto. Dependências npm e navegadores não são instalados automaticamente.

Instalações existentes são preservadas, sem assumir que tenham a revisão registrada. Para atualizar uma skill, compare a instalação, registre a revisão nova e faça uma troca deliberada com backup fora deste repositório. `tiktok-marketing` permanece opcional e não entra na instalação automática porque sua revisão original não foi registrada.

## Aplicação visual

O [manual teruya.dev](../standards/teruya-dev/VIDEO_STANDARD.md) orienta as adaptações: SF Pro, azul/branco, contorno duplo, pop por letra, grid translúcido e câmera com recorte no rosto. Ler o cartão e o demo antes de declarar uso de uma receita; registrar os parâmetros, o que foi adaptado e a validação em movimento.

Os tempos das legendas vêm da gravação. A fala guia o movimento. Instalar uma skill não comprova integração nativa com FilmCraft ou EffectCraft. As evidências da produção ficam fora do Git; os critérios e as métricas ficam no manual.

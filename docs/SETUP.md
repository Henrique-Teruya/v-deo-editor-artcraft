# Setup de edição

## Voz local no Windows

O [guia de voz](VOICE.md) documenta a instalação testada do OpenVoice V2 com Chatterbox Multilingual V3 para português, o cadastro da própria amostra e a exportação de WAV para o FilmCraft. O runtime fica fora deste repositório; fontes e modelos têm revisões fixadas em `config/voice-runtime.json` e `config/voice-models.json`. Abrir com `python scripts/voice_studio.py`. Instalação em outro desktop: `python scripts/setup_voice.py --install`, usando Python 3.12, uv, Git e FFmpeg.

Fluxo principal no macOS. Os instaladores e as dependências ficam fora do repositório; aqui ficam os comandos e as versões. As versões abaixo foram usadas neste projeto, não são uma promessa de serem as mais recentes.

## ArtCraft

| Software | Versão registrada | Função |
| --- | --- | --- |
| ArtCraft Launcher | 0.9.0 | Instalar, abrir e atualizar a suíte |
| FilmCraft | 0.14.0 | Montagem, áudio, legendas e exportação |
| EffectCraft | 0.18.0 | Composição e animações |
| VectorCraft | 0.18.0 | Elementos vetoriais |

Fontes oficiais: [ArtCraft](https://getartcraft.com/), [releases do Launcher](https://github.com/storytold/craft-launcher/releases). Nomes dos arquivos e URLs das versões registradas estão em [software.json](../config/software.json).

Com Python 3.11 ou mais recente, baixar o Launcher e conferir seu SHA-256 publicado:

```sh
python3 scripts/download_artcraft.py craft-launcher --download
open "$HOME/Downloads/artcraft-setup/artcraft-launcher-0.9.0-macos-universal.dmg"
```

Arraste **ArtCraft Launcher.app** para **Applications**, abra o Launcher e instale FilmCraft, EffectCraft e VectorCraft. O Launcher pode oferecer versões posteriores às registradas; anote as versões realmente instaladas antes de atualizar o catálogo.

Para reproduzir exatamente as versões dos três editores:

```sh
python3 scripts/download_artcraft.py filmcraft --download
python3 scripts/download_artcraft.py effectcraft --download
python3 scripts/download_artcraft.py vectorcraft --download
open "$HOME/Downloads/artcraft-setup/filmcraft-0.14.0-macos-universal.dmg"
open "$HOME/Downloads/artcraft-setup/effectcraft-0.18.0-macos-universal.dmg"
open "$HOME/Downloads/artcraft-setup/vectorcraft-0.18.0-macos-universal.dmg"
```

Instale cada aplicativo pelo DMG. O script baixa e verifica; não substitui aplicativos instalados. Sem `--download`, mostra apenas a URL. Não desativar verificações de segurança do sistema.

Windows/Linux: use o instalador adequado na página oficial ou o Launcher. Os comandos `open`, DMG e a fonte local do macOS deste documento são específicos do Mac.

## Ferramentas de apoio

Se o Homebrew já estiver instalado:

```sh
brew install python node ffmpeg git
```

FFmpeg/FFprobe servem para inspeção, áudio, conversão HDR/SDR e conferência. Remotion e os exemplos ShotCraft são preparados apenas quando necessários. O setup das skills está em [skills/README.md](../skills/README.md).

```sh
python3 scripts/install_skills.py
python3 scripts/install_skills.py --apply
```

O primeiro comando é uma prévia. O segundo instala somente skills ausentes, pelo instalador oficial local do Codex, com revisões fixadas. Não reinstala as que já existem.

## ShotCraft: dependências opcionais

Somente para usar o template e o Motion Workbench, após instalar a skill:

```sh
TERUYA_CODEX_DIR="${CODEX_HOME:-$HOME/.codex}"
npm --prefix "$TERUYA_CODEX_DIR/skills/video-shotcraft/template" ci
npm --prefix "$TERUYA_CODEX_DIR/skills/video-shotcraft/workbench" ci
```

Os lockfiles upstream determinam as dependências. A configuração do navegador de renderização e de transcrição é feita quando utilizada. Instalar skills não cria presets nativos no ArtCraft: adaptar a receita no EffectCraft ou renderizar em Remotion e importar no FilmCraft.

## Manual visual e fontes

San Francisco / SF Pro é o padrão. Display para títulos/ênfases; Text para legendas/rótulos/corpo. O gerador local usa `/System/Library/Fonts/SFNS.ttf`; não baixa fontes da Apple nem inclui binários no repositório. Origem e instâncias estão em [font-source.json](../standards/teruya-dev/font-source.json).

```sh
brew install harfbuzz poppler
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-docs.txt
.venv/bin/python standards/teruya-dev/scripts/build_manual.py
pdftoppm -r 90 -png standards/teruya-dev/output/pdf/teruya-dev-manual-visual.pdf /tmp/teruya-manual
```

Revise as páginas antes de distribuir o PDF. `output/`, fontes e o ambiente `.venv/` permanecem excluídos do Git. Para regenerar tokens e receitas depois de alterar o gerador, a revisão ShotCraft do catálogo deve estar disponível:

```sh
python3 standards/teruya-dev/scripts/build_spec.py
python3 scripts/check_repository.py
```

Use `TERUYA_SHOTCRAFT_DIR` se a skill estiver em outro diretório. Os padrões visuais são preservados ao atualizar softwares; uma nova versão de aplicativo não muda automaticamente a identidade.

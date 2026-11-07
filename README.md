# v-deo-editor-artcraft

Documentação e setup do fluxo de edição **teruya.dev** com ArtCraft, Video ShotCraft e TikTok Video Skills. Este repositório é a referência para manter o padrão visual, as métricas de edição, os registros de skills e os comandos de instalação atualizados.

## Começar

```sh
git clone https://github.com/Henrique-Teruya/v-deo-editor-artcraft.git
cd v-deo-editor-artcraft
python3 scripts/check_repository.py
git config core.hooksPath .githooks
```

1. Siga o [setup dos softwares](docs/SETUP.md).
2. Instale as revisões registradas das [skills](skills/README.md).
3. Use o [manual operacional teruya.dev](standards/teruya-dev/VIDEO_STANDARD.md) e o [fluxo de produção](WORKFLOW.md).
4. Consulte os [limites de versionamento e atualização](docs/REPOSITORY.md).
5. Para narração com a própria voz no desktop Windows, abra o [estúdio local de voz](docs/VOICE.md). O roteiro e o padrão visual continuam seguindo o fluxo acima.

## Padrão ativo: teruya.dev 3.0

| Área | Regra |
| --- | --- |
| Formato | Base vertical 1080 × 1920, 30 fps, SDR/Rec.709 |
| Tipografia | SF Pro Display em títulos/ênfases; SF Pro Text em legendas/rótulos/corpo |
| Cores | Branco e azul `#0066CC`; `#2997FF` em superfícies escuras |
| Ênfase | Elastic Pop-In e Pop-Out por letra, sincronizados à voz |
| Contornos | Escuro: branco interno/preto externo. Claro: preto interno/branco externo |
| Apresentador | Texto flutuante; recorte proporcional com prioridade no rosto, sem blur lateral |
| Explicações | Grid sketchbook 216 px, traço 1,5 px e opacidade de 7% no claro |
| Áudio | Alvo inicial de −16 LUFS, pico verdadeiro ≤−1 dBTP |

Os parâmetros completos, exceções e critérios de conferência estão no manual. São especificações editoriais; receitas precisam ser adaptadas e conferidas em movimento em cada produção.

## O que fica aqui

Documentação em Markdown, tokens JSON, modelos de cena, registro de receitas, versões das skills, referências textuais e scripts pequenos de setup e geração do manual. Softwares e skills completas são obtidos das fontes oficiais, fora deste repositório.

Gravações, áudios, imagens, fontes, projetos de vídeo, instaladores, dependências, renders, PDFs gerados, entregas e backups ficam fora do Git. A pasta `projects/` permanece exclusivamente local. A validação limita cada arquivo versionado a 512 KiB e o conjunto a 5 MiB.

## Gerar o manual visual localmente

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-docs.txt
brew install harfbuzz poppler
.venv/bin/python standards/teruya-dev/scripts/build_manual.py
```

O gerador usa a San Francisco instalada no macOS e produz o PDF em `standards/teruya-dev/output/pdf/`. Esse resultado não é enviado ao GitHub. Veja as dependências e a preparação em [SETUP.md](docs/SETUP.md).

# Conteúdo e atualização

Repositório: https://github.com/Henrique-Teruya/v-deo-editor-artcraft

## Limites

Versionar `README.md`, `AGENTS.md`, `WORKFLOW.md`, documentos, registros JSON, referências textuais, scripts de setup/geração e verificações. A lista de caminhos é explícita em `.gitignore` e `scripts/check_repository.py`.

Não versionar originais, áudio, imagens, vetores de episódios, fontes, projetos FilmCraft/EffectCraft/VectorCraft, instaladores, softwares, cópias completas das skills, dependências, caches, capturas, outputs ou arquivos de entrega. Mesmo o manual PDF é um resultado gerado: seu Markdown e gerador ficam no Git; o PDF fica local.

Limites internos: **512 KiB por arquivo** e **5 MiB no total**. A verificação aceita somente formatos textuais autorizados, recusa links simbólicos e procura assinaturas comuns de credenciais. Não substitui a leitura do diff.

## Rotina após uma mudança autorizada

```sh
git pull --ff-only
python3 scripts/check_repository.py
git add README.md AGENTS.md WORKFLOW.md .gitignore requirements-docs.txt docs scripts config skills standards .github .githooks
python3 scripts/check_repository.py --staged
git diff --cached --stat
git diff --cached
git commit -m "docs: descreva a mudança"
git push origin main
```

O commit deve conter apenas o trabalho autorizado. Para a primeira publicação, a branch `main` é criada com o conteúdo revisado; nas seguintes, preservar as alterações remotas. Não forçar pushes. Instalar o hook local uma vez com `git config core.hooksPath .githooks`.

## Fontes de verdade

- Identidade e métricas: `standards/teruya-dev/VIDEO_STANDARD.md`.
- Tokens e receitas: gerados por `standards/teruya-dev/scripts/build_spec.py`.
- Softwares: `config/software.json`, versões já utilizadas, sem alegação de serem as mais recentes.
- Skills: `skills/catalog.json`, revisões fixadas e complementos compartilhados.
- PDF: `standards/teruya-dev/scripts/build_manual.py`, usando SF Pro local. Não exige guardar o arquivo de fonte no repositório.

Os registros históricos de revisão podem mencionar arquivos locais excluídos. Isso documenta uma conferência anterior, não significa que os materiais estejam disponíveis no clone. Novas evidências pesadas continuam fora do Git.

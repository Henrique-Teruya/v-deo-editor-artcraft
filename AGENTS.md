# Manutenção deste repositório

Este workspace contém materiais locais pesados, mas o GitHub guarda apenas documentação, configuração e scripts pequenos.

- Leia `standards/teruya-dev/VIDEO_STANDARD.md` antes de alterar a direção visual.
- Padrão atual: teruya.dev 3.0, SF Pro, contorno duplo, pop por letra e recorte no rosto sem blur lateral.
- Preserve os vídeos aprovados e a documentação histórica dentro de `projects/`. Não renderize novamente por uma mudança do manual.
- Nunca adicione `projects/`, `tools/`, `research/`, fontes, materiais, outputs, binários ou dependências. Não use `git add -f` para contornar isso.
- Alterações do padrão devem manter Markdown, tokens, presets, ficha de cena e geradores consistentes. O PDF é produzido e revisado localmente, mas não é versionado.
- Registre versões de software em `config/software.json` e revisões/hashes de skills em `skills/catalog.json`; não atualize revisões silenciosamente.
- Use caminhos relativos e variáveis portáveis para comandos. Evite caminhos pessoais em documentação nova.
- Execute `python3 scripts/check_repository.py` antes de preparar o commit e `python3 scripts/check_repository.py --staged` depois. O hook e o CI verificam conteúdo, formato e tamanho.
- Por instrução do proprietário, mantenha as próximas alterações autorizadas de documentação e setup sincronizadas com `origin/main` após conferir o diff e concluir o commit. Não use force-push, não sobrescreva alterações remotas e não envie mudanças alheias ao pedido. Informe commit e link ao concluir.
- Não publicar vídeos, enviar mensagens a terceiros nem configurar automações a partir destas instruções.

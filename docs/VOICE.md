# Narração com a própria voz

O fluxo de roteiro continua o mesmo. Depois de definir o texto, a narração pode ser gerada localmente com uma referência da própria voz de Henrique, sem filmar o rosto. Os arquivos de vídeo já aprovados permanecem intactos.

## Abrir e cadastrar a voz

No Windows, execute na raiz deste repositório:

```powershell
python scripts/voice_studio.py
```

O estúdio abre em `http://127.0.0.1:7865`. Ele também pode ser aberto pelo atalho **Sua voz - teruya.dev**, quando instalado no Menu Iniciar.

1. Grave de 8 a 30 segundos ou selecione uma gravação sua. A tela oferece uma gravação de 15 segundos e um texto de exemplo; não é obrigatório ler exatamente aquele texto.
2. Fale num ambiente silencioso, sem música, eco, outras pessoas ou filtro de voz. Comece a falar logo no início. Não sussurre nem force uma voz de locutor.
3. Ouça a gravação, confirme que é sua própria voz e clique **Salvar minha voz**. A tela verifica duração, volume e saturação; isso não substitui a escuta nem identifica quem fala.
4. Gere primeiro uma frase curta. Escute nomes, números, pronúncia, pausas, repetições e semelhança. Compare a opção de aplicar OpenVoice ligada e desligada.
5. Se precisar melhorar a referência, cadastre outra. Os perfis anteriores ficam preservados. Nenhum arquivo antigo é procurado automaticamente pela aplicação.

Henrique autorizou separadamente, em 07/11/2026, selecionar uma gravação própria do Drive para o primeiro vídeo demonstrativo. O manifesto privado da produção registra o arquivo escolhido e o trecho. Essa autorização não habilita busca automática de novas referências na aplicação.

## O que cada motor faz

- **Chatterbox Multilingual V3:** gera o texto em português, condicionado à própria gravação de Henrique. Ele já participa da identidade vocal do áudio base.
- **OpenVoice V2:** faz a conversão de timbre sobre esse áudio, usando a mesma referência. A conversão é opcional para permitir comparação; não é presumida como melhoria.
- **FFmpeg:** exporta WAV mono PCM de 24 bits a 48 kHz, com normalização em duas passagens para alvo de -16 LUFS e -1 dBTP. O manifesto registra as medidas efetivas.

O OpenVoice não inclui português entre seus seis idiomas nativos de síntese. Sua documentação permite usar um sintetizador externo como base. Esta integração local combina dois projetos; não é o demo oficial MeloTTS/Gradio. O conversor OpenVoice não copia automaticamente sotaque, emoção ou a forma de explicar. A qualidade com cada referência precisa ser escutada.

Chatterbox é pesquisa sob licença MIT; seu repositório informa encerramento de manutenção em agosto de 2026. Os commits, dependências e pesos desta instalação estão fixados. Não há atualização automática. Os padrões de roteiro e personalidade não são alterados.

## Usar na edição

1. Copie o texto final para a tela ou salve um TXT UTF-8. Gere em blocos de até 3000 caracteres; em CPU, começar com frases curtas reduz espera e retrabalho.
2. O botão **Baixar WAV para o editor** entrega `narracao.wav`. O arquivo original também permanece na pasta externa `outputs/<id>/` do runtime.
3. Importe o WAV no FilmCraft, ou copie-o para `06-audio` de um projeto novo. A integração é por arquivo de áudio, não um efeito nativo instalado no FilmCraft.
4. Preserve `roteiro.txt`, os trechos base/convertidos e `manifest.json`. O áudio real e o sintético devem ficar identificados nos registros de produção; na demonstração pública, identificar a troca também no vídeo.
5. A duração da narração define cortes e animações. Gere e alinhe legendas no WAV final e revise as palavras. O manifesto fornece limites de trechos medidos, **não timestamps de palavras nem SRT artificial**.
6. Preserve a direção teruya.dev 3.0. A imagem do apresentador é opcional nesta modalidade; não sincronizar takes antigos à fala sintética como se fossem uma nova gravação.

CLI, usando o Python isolado do runtime:

```powershell
$VoicePython = Join-Path $env:LOCALAPPDATA 'TeruyaVoice\venv\Scripts\python.exe'
& $VoicePython scripts/voice_engine.py status
& $VoicePython scripts/voice_engine.py enroll '.\minha-amostra.wav' --own-voice
& $VoicePython scripts/voice_engine.py generate --text-file '.\roteiro.txt'
& $VoicePython scripts/voice_engine.py generate --text-file '.\roteiro.txt' --without-openvoice
```

## Arquivos e privacidade

O padrão Windows é `%LOCALAPPDATA%\TeruyaVoice`. Em outros sistemas o diretório padrão é `~/.local/share/TeruyaVoice`; este setup foi validado no Windows com Python 3.12 e CPU. O argumento `--runtime` permite um caminho externo explícito.

| Pasta/arquivo externo | Conteúdo |
| --- | --- |
| `OpenVoice/`, `chatterbox/` | Código oficial em commits fixos |
| `venv/`, `models/`, `cache/` | Bibliotecas, pesos e caches |
| `profiles/<id>/` | Amostra original, WAV preparado, embedding e registro de autorização |
| `profile.json` | Perfil ativo |
| `outputs/<id>/` | Texto, áudios e manifesto de cada geração |
| `verification/` | Evidências técnicas da instalação |

A aplicação escuta somente `127.0.0.1`. Operações e reprodução de áudio usam token de sessão; não existe link público ou modo `share`. As amostras não são enviadas a um serviço de síntese. Downloads de dependências e modelos ocorrem no setup; a inferência usa arquivos locais. Perfis, embeddings, vídeos e outputs não entram no Git. Evite sincronizar a pasta de voz com um repositório ou compartilhar o perfil.

## Reproduzir a instalação

Pré-requisitos: Python 3.12, Git, uv e FFmpeg/FFprobe no PATH. Reserve espaço para alguns gigabytes de modelos e dependências. Não é necessário CUDA; esta instalação usa CPU. A GPU AMD deste desktop não é usada por esse runtime PyTorch CPU.

```powershell
python scripts/setup_voice.py
python scripts/setup_voice.py --install
```

O primeiro comando mostra o destino. O segundo instala somente no diretório externo, baixa fontes/pesos oficiais e executa o teste numérico. Não altera ambientes Python já existentes. O pacote congelado completo está em `config/voice-requirements.txt`; os commits em `config/voice-runtime.json`; hashes e revisões dos modelos em `config/voice-models.json`.

O URL S3 antigo do guia OpenVoice respondeu 404 nesta preparação. Os dois arquivos do conversor foram obtidos de **myshell-ai/OpenVoiceV2** no Hugging Face, com o SHA-256 publicado do checkpoint conferido. Nenhum embedding de voz de demonstração é carregado. Chatterbox usa explicitamente `t3_model='v3'`, pois seu padrão de código ainda aponta para V2.

Adaptações locais, sem alterar as fontes upstream: o núcleo de conversão OpenVoice é carregado diretamente com `weights_only=True`, sem baixar WavMark; a marca d'água Perth do Chatterbox é aplicada após conversão. A inicialização do segmentador chinês é omitida no adaptador exclusivamente português para evitar downloads durante a geração. A proveniência sintética permanece no manifesto; não se promete detectabilidade da marca após edição e recompressão.

## Diagnóstico e limites da validação

```powershell
& $VoicePython scripts/voice_engine.py smoke
uv pip check --python $VoicePython
```

O smoke test carrega os dois modelos, exercita o OpenVoice e o encoder de referência do Chatterbox com um sinal matemático, e verifica o tokenizador de português. Não gera fala de outra pessoa nem cria um perfil. Isso valida funcionamento técnico; a avaliação de voz real pertence à escuta de uma geração autorizada, registrada separadamente na produção.

Se o microfone não abrir no navegador, permita-o apenas ao endereço local ou use uma gravação salva. Se a porta 7865 estiver ocupada por outro programa, use `--port 7866`. Se a geração falhar, os arquivos brutos já produzidos são preservados e a interface exibe o erro. Não afirmar sucesso por existir uma pasta de saída: a entrega completa exige `narracao.wav` e manifesto válido.

## Fontes

- [OpenVoice: código e licença](https://github.com/myshell-ai/OpenVoice)
- [OpenVoice: uso e idiomas do V2](https://github.com/myshell-ai/OpenVoice/blob/main/docs/USAGE.md)
- [OpenVoice: limites de timbre, sotaque e emoção](https://github.com/myshell-ai/OpenVoice/blob/main/docs/QA.md)
- [Pesos oficiais OpenVoice V2](https://huggingface.co/myshell-ai/OpenVoiceV2)
- [Chatterbox: código, licença e estado do projeto](https://github.com/resemble-ai/chatterbox)
- [Chatterbox: pesos oficiais](https://huggingface.co/ResembleAI/chatterbox)

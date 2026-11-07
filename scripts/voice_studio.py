"""Loopback-only onboarding for the local voice environment. No cloud uploads."""
import argparse
import base64
import hmac
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import re
import secrets
import subprocess
import sys
import tempfile
import threading
from urllib.parse import parse_qs, urlparse
import webbrowser

from voice_engine import DEFAULT_RUNTIME, configure, enroll, generate, status

PAGE = '''<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Sua voz · teruya.dev</title><style>
:root{font-family:Segoe UI,system-ui,sans-serif;color:#1d1d1f;background:#f5f5f7}*{box-sizing:border-box}body{max-width:1060px;margin:auto;padding:44px 24px}header{margin-bottom:32px}.tag{font-size:12px;letter-spacing:.14em;color:#0066cc;font-weight:700}h1{font-size:44px;letter-spacing:-1.7px;margin:12px 0}h2{font-size:23px;letter-spacing:-.5px}p{line-height:1.6;color:#555}main{display:grid;grid-template-columns:1fr 1fr;gap:22px}section{border:1px solid #e1e1e6;background:white;border-radius:22px;padding:26px}button{border:0;border-radius:10px;padding:12px 16px;background:#0066cc;color:white;font-weight:600;cursor:pointer;margin:6px 6px 6px 0}button.secondary{background:#edf4fc;color:#0066cc}button:disabled{opacity:.45;cursor:wait}textarea{width:100%;min-height:155px;border:1px solid #ccc;border-radius:10px;padding:12px;font:inherit;line-height:1.5}input[type=file]{width:100%;margin:10px 0 18px}label{font-size:14px;line-height:1.5;display:block;margin:12px 0}input[type=checkbox]{accent-color:#0066cc}audio{width:100%;margin:15px 0}.status{background:#edf4fc;border-radius:12px;padding:14px;margin:22px 0;color:#174b7c;white-space:pre-wrap}small,.small{font-size:13px;color:#666;line-height:1.5}.step{color:#0066cc}footer{margin:26px 0;font-size:13px;color:#777}#result a{display:block;margin:12px 0;color:#0066cc}.sample{background:#f7f7f9;border-radius:12px;padding:16px}.badge{display:inline-block;background:#e8f4ec;color:#2d6c42;border-radius:30px;padding:6px 12px;font-size:12px} @media(max-width:760px){main{grid-template-columns:1fr}h1{font-size:34px}}
</style><header><span class="tag">TERUYA.DEV / ESTÚDIO DE VOZ</span><h1>Sua voz. Sem precisar de câmera.</h1><p>Cadastre uma amostra limpa, gere uma frase curta e escute antes de produzir a narração inteira.</p><span class="badge">Local neste computador · português · CPU</span></header>
<div id="state" class="status" role="status" aria-live="polite">Verificando a instalação…</div>
<main><section><span class="tag step">01 / SUA AMOSTRA</span><h2>Fale como numa conversa</h2><p>Grave de 8 a 30 segundos, só com sua voz, sem música, eco ou filtro. Deixe a fala começar logo no início.</p>
<div class="sample">“Hoje eu vou mostrar uma ideia simples. Primeiro, a gente olha o problema. Depois, testa uma solução e confere o resultado. O importante é explicar com clareza, sem complicar o que pode ser simples.”</div>
<button id="record" class="secondary">Gravar 15 segundos</button><button id="stop" class="secondary" disabled>Parar</button>
<p class="small">Ou escolha uma gravação sua em WAV, MP3, M4A, FLAC, OGG ou WebM, com até 30 MB.</p><input id="file" type="file" accept="audio/*"><audio id="preview" controls hidden></audio>
<label><input id="consent" type="checkbox"> Esta é a minha própria voz e autorizo o uso desta amostra para gerar minhas narrações neste computador.</label><button id="enroll">Salvar minha voz</button><p class="small">Cadastrar outra amostra preserva a anterior. Nenhuma gravação antiga é procurada automaticamente.</p></section>
<section><span class="tag step">02 / TESTE E NARRAÇÃO</span><h2>Transforme o roteiro em áudio</h2><p>O roteiro continua sendo criado pelo fluxo de sempre. Cole aqui o texto que você quer narrar.</p><textarea id="text" maxlength="3000" aria-label="Texto da narração">Olá, este é meu primeiro teste de narração em português.</textarea>
<label><input id="convert" type="checkbox" checked> Aplicar a conversão de timbre do OpenVoice</label><p class="small">A fala em português é gerada pelo Chatterbox com sua própria referência. Você pode comparar com e sem OpenVoice.</p><button id="generate" disabled>Gerar narração</button><div id="result"></div><p class="small">Na CPU, cada trecho pode levar alguns minutos. O WAV final terá 48 kHz, pronto para importar no FilmCraft. Escute nomes, números, pronúncia e pausas.</p></section></main>
<footer>Áudio sintético identificado nos metadados da entrega. As amostras, os modelos e as saídas ficam fora do Git. Legendas devem ser alinhadas ao WAV final, sem tempos inventados.</footer>
<script>
const token='@TOKEN@';let selected=null,recorder=null,stream=null,timer=null,previewUrl=null,lastResult=null;
const $=id=>document.getElementById(id);
async function api(path,data){const opts={headers:{'X-Voice-Token':token}};if(data){opts.method='POST';opts.headers['Content-Type']='application/json';opts.body=JSON.stringify(data)}const r=await fetch(path,opts);const body=await r.json();if(!r.ok)throw Error(body.error||'Falha local');return body}
function showError(e){$('state').textContent=e.message}
function setAudio(blob){selected=blob;if(previewUrl)URL.revokeObjectURL(previewUrl);previewUrl=URL.createObjectURL(blob);$('preview').src=previewUrl;$('preview').hidden=false}
$('file').onchange=()=>{if($('file').files[0])setAudio($('file').files[0])};
$('record').onclick=async()=>{try{stream=await navigator.mediaDevices.getUserMedia({audio:{echoCancellation:false,noiseSuppression:false,autoGainControl:false}});const chunks=[];recorder=new MediaRecorder(stream);recorder.ondataavailable=e=>chunks.push(e.data);recorder.onstop=()=>{clearTimeout(timer);stream.getTracks().forEach(t=>t.stop());setAudio(new Blob(chunks,{type:recorder.mimeType}));$('record').disabled=false;$('stop').disabled=true};recorder.start();$('record').disabled=true;$('stop').disabled=false;timer=setTimeout(()=>{if(recorder.state==='recording')recorder.stop()},15000)}catch(e){showError(e)}};
$('stop').onclick=()=>{if(recorder&&recorder.state==='recording')recorder.stop()};
$('enroll').onclick=async()=>{try{if(!selected)throw Error('Grave ou selecione sua amostra primeiro.');if(!$('consent').checked)throw Error('Confirme que a amostra contém sua própria voz.');if(selected.size>30*1024*1024)throw Error('A amostra deve ter até 30 MB.');const bytes=new Uint8Array(await selected.arrayBuffer());let bin='';for(let i=0;i<bytes.length;i+=8192)bin+=String.fromCharCode(...bytes.subarray(i,i+8192));await api('/api/enroll',{audio:btoa(bin),name:selected.name||'gravacao.webm',consent:true});await refresh()}catch(e){showError(e)}};
$('generate').onclick=async()=>{try{await api('/api/generate',{text:$('text').value,openvoice:$('convert').checked});await refresh()}catch(e){showError(e)}};
async function refresh(){const s=await api('/api/status');$('state').textContent=s.job.message||(s.profile?'Voz cadastrada. Gere uma frase curta e confira o resultado.':'Instalação pronta. Falta cadastrar sua amostra.');if(!s.ready)$('state').textContent='Instalação incompleta: '+s.missing.join(', ');$('generate').disabled=s.job.busy||!s.profile||!s.ready;$('enroll').disabled=s.job.busy||!s.ready;if(s.job.result&&s.job.result.id!==lastResult){lastResult=s.job.result.id;const url='/audio/'+encodeURIComponent(lastResult)+'?token='+encodeURIComponent(token);$('result').replaceChildren();const a=document.createElement('audio');a.controls=true;a.src=url;$('result').append(a);const link=document.createElement('a');link.href=url;link.download='narracao.wav';link.textContent='Baixar WAV para o editor';$('result').append(link);const p=document.createElement('p');p.className='small';p.textContent='Arquivo salvo: '+s.job.result.file;$('result').append(p)}}
refresh().catch(showError);setInterval(()=>refresh().catch(()=>{}),2000);
</script></html>'''


def serve(runtime, port=7865, open_browser=True):
    token = secrets.token_urlsafe(32)
    lock = threading.Lock()
    job = {'busy': False, 'message': '', 'result': None}
    origin = f'http://127.0.0.1:{port}'

    def start(function):
        with lock:
            if job['busy']:
                raise ValueError('Aguarde o trabalho atual terminar.')
            job.update(busy=True, message='Preparando…', result=None)
        def worker():
            try:
                result = function()
                job.update(message='Pronto. Escute o áudio e confira o resultado.' if result else 'Voz cadastrada. Gere uma frase curta e escute o resultado.', result=result)
            except Exception as exc:
                job.update(message='Não foi concluído: ' + str(exc), result=None)
            finally:
                job['busy'] = False
        threading.Thread(target=worker, daemon=True).start()

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass  # Do not put audio URLs/session tokens or script text in access logs.

        def send(self, code, data, content_type='application/json; charset=utf-8'):
            if not isinstance(data, bytes):
                data = json.dumps(data, ensure_ascii=False).encode('utf-8')
            self.send_response(code)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', str(len(data)))
            self.send_header('Cache-Control', 'no-store')
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.send_header('Referrer-Policy', 'no-referrer')
            self.send_header('Content-Security-Policy', "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; media-src 'self' blob:; connect-src 'self'; frame-ancestors 'none'")
            self.end_headers()
            self.wfile.write(data)

        def local(self):
            return self.headers.get('Host') == f'127.0.0.1:{port}' and self.headers.get('Origin', origin) == origin

        def authorized(self):
            supplied = self.headers.get('X-Voice-Token', '')
            if urlparse(self.path).path.startswith('/audio/'):
                supplied = parse_qs(urlparse(self.path).query).get('token', [''])[0]
            return self.local() and hmac.compare_digest(supplied, token)

        def do_GET(self):
            path = urlparse(self.path).path
            if not self.local():
                return self.send(403, {'error': 'Acesso apenas pelo endereço local.'})
            if path == '/':
                return self.send(200, PAGE.replace('@TOKEN@', token).encode('utf-8'), 'text/html; charset=utf-8')
            if path == '/health':
                return self.send(200, {'service': 'teruya-voice', 'version': 1})
            if not self.authorized():
                return self.send(403, {'error': 'Sessão inválida. Abra novamente o estúdio.'})
            if path == '/api/status':
                return self.send(200, {**status(runtime), 'job': job.copy()})
            if path.startswith('/audio/'):
                output_id = path.removeprefix('/audio/')
                if re.fullmatch(r'\d{8}T\d{6}Z-[a-f0-9]{8}', output_id):
                    wav = runtime / 'outputs' / output_id / 'narracao.wav'
                    if wav.is_file():
                        return self.send(200, wav.read_bytes(), 'audio/wav')
            return self.send(404, {'error': 'Não encontrado.'})

        def do_POST(self):
            if not self.authorized():
                return self.send(403, {'error': 'Sessão inválida.'})
            try:
                length = int(self.headers.get('Content-Length', 0))
                if not 0 < length <= 42 * 1024 * 1024:
                    return self.send(413, {'error': 'Arquivo grande demais.'})
                if self.headers.get('Content-Type') != 'application/json':
                    return self.send(415, {'error': 'Formato inválido.'})
                data = json.loads(self.rfile.read(length))
                if self.path == '/api/enroll':
                    if data.get('consent') is not True:
                        raise ValueError('É necessário confirmar o uso da própria voz.')
                    audio = base64.b64decode(data['audio'], validate=True)
                    if len(audio) > 30 * 1024 * 1024:
                        raise ValueError('Amostra deve ter até 30 MB.')
                    suffix = Path(data.get('name', 'audio.webm')).suffix.lower()
                    if suffix not in {'.wav', '.mp3', '.m4a', '.flac', '.ogg', '.webm', '.mp4', '.aac'}:
                        raise ValueError('Use WAV, MP3, M4A, FLAC, OGG ou WebM.')
                    def register():
                        incoming = runtime / 'incoming'
                        incoming.mkdir(exist_ok=True)
                        with tempfile.TemporaryDirectory(dir=incoming) as directory:
                            source = Path(directory) / ('amostra' + suffix)
                            source.write_bytes(audio)
                            enroll(runtime, source, True)
                        return None
                    start(register)
                elif self.path == '/api/generate':
                    text = data.get('text', '')
                    if not isinstance(text, str) or not text.strip() or len(text) > 3000:
                        raise ValueError('Digite de 1 a 3000 caracteres.')
                    if not status(runtime)['profile']:
                        raise ValueError('Cadastre a própria voz primeiro.')
                    start(lambda: generate(runtime, text, data.get('openvoice', True) is True,
                                           progress=lambda message: job.update(message=message)))
                else:
                    return self.send(404, {'error': 'Não encontrado.'})
                self.send(202, {'started': True})
            except (ValueError, KeyError, TypeError) as exc:
                self.send(400, {'error': str(exc)})

    class LocalServer(ThreadingHTTPServer):
        allow_reuse_address = False
    server = LocalServer(('127.0.0.1', port), Handler)
    server.daemon_threads = True
    if open_browser:
        webbrowser.open(origin)
    print('Estúdio de voz: ' + origin, flush=True)
    try:
        server.serve_forever()
    finally:
        server.server_close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--runtime', type=Path, default=DEFAULT_RUNTIME)
    parser.add_argument('--port', type=int, default=7865)
    parser.add_argument('--no-browser', action='store_true')
    args = parser.parse_args()
    runtime = args.runtime.resolve()
    python = runtime / 'venv' / ('Scripts/python.exe' if os.name == 'nt' else 'bin/python')
    if Path(sys.prefix).resolve() != (runtime / 'venv').resolve():
        if not python.exists():
            raise SystemExit('Ambiente ausente. Consulte docs/VOICE.md para instalar.')
        raise SystemExit(subprocess.call([str(python), str(Path(__file__).resolve()), *sys.argv[1:]],
                                        creationflags=0x08000000 if os.name == 'nt' else 0))
    configure(runtime)
    import urllib.request
    address = f'http://127.0.0.1:{args.port}'
    try:
        with urllib.request.urlopen(address + '/health', timeout=1) as response:
            if json.load(response).get('service') == 'teruya-voice':
                if not args.no_browser:
                    webbrowser.open(address)
                return
    except Exception:
        pass
    try:
        serve(runtime, args.port, not args.no_browser)
    except OSError as exc:
        if getattr(exc, 'winerror', None) == 10048 or exc.errno == 98:
            import urllib.request
            address = f'http://127.0.0.1:{args.port}'
            try:
                with urllib.request.urlopen(address + '/health', timeout=2) as response:
                    if json.load(response).get('service') == 'teruya-voice':
                        if not args.no_browser:
                            webbrowser.open(address)
                        return
            except Exception:
                pass
        raise


if __name__ == '__main__':
    main()

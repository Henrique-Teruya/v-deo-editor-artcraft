"""Local, explicit-reference narration: Portuguese TTS and OpenVoice V2 conversion."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import uuid

DEFAULT_RUNTIME = Path(os.environ.get('LOCALAPPDATA', Path.home() / '.local/share')) / 'TeruyaVoice'


def configure(runtime):
    runtime = Path(runtime).resolve()
    os.environ['HF_HUB_OFFLINE'] = '1'
    os.environ['HF_HUB_DISABLE_TELEMETRY'] = '1'
    os.environ['DO_NOT_TRACK'] = '1'
    os.environ['TORCH_HOME'] = str(runtime / 'cache' / 'torch')
    os.environ['HF_HOME'] = str(runtime / 'cache' / 'huggingface')
    os.environ['NUMBA_CACHE_DIR'] = str(runtime / 'cache' / 'numba')
    sys.path[:0] = [str(runtime / 'OpenVoice'), str(runtime / 'chatterbox' / 'src')]
    return runtime


def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as source:
        for block in iter(lambda: source.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def write_json(path, data):
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def run(*args):
    result = subprocess.run([str(x) for x in args], capture_output=True, text=True,
                            encoding='utf-8', errors='replace',
                            creationflags=0x08000000 if os.name == 'nt' else 0)
    if result.returncode:
        raise RuntimeError(result.stderr[-3000:] or result.stdout[-3000:])
    return result


def pcm(source, target, sample_rate=24000):
    # Explicit input only; no directory scanning or automatic audio discovery.
    run('ffmpeg', '-nostdin', '-hide_banner', '-loglevel', 'error', '-n',
        '-i', source, '-map', '0:a:0', '-vn', '-ac', '1', '-ar', sample_rate,
        '-c:a', 'pcm_s24le', target)


def audio_metrics(path):
    import numpy as np
    import soundfile as sf
    audio, sr = sf.read(path, dtype='float32')
    if audio.ndim != 1 or not len(audio) or not np.isfinite(audio).all():
        raise ValueError('Áudio vazio, inválido ou fora do formato mono esperado.')
    peak = float(np.max(np.abs(audio)))
    rms = float(np.sqrt(np.mean(audio ** 2)))
    return {'seconds': len(audio) / sr, 'sampleRate': sr,
            'peakDBFS': float(20 * np.log10(max(peak, 1e-10))),
            'rmsDBFS': float(20 * np.log10(max(rms, 1e-10))),
            'clippedFraction': float(np.mean(np.abs(audio) >= .999)),
            'activeFraction': float(np.mean(np.abs(audio) > .01))}


def converter(runtime):
    import torch
    from openvoice.api import ToneColorConverter, OpenVoiceBaseClass
    torch.set_num_threads(min(4, os.cpu_count() or 1))
    # Upstream forwards enable_watermark to a superclass that does not accept it.
    # Construct the same converter core without its automatic WavMark download.
    # Narration receives the official Perth watermark after conversion instead.
    model = ToneColorConverter.__new__(ToneColorConverter)
    OpenVoiceBaseClass.__init__(model, str(runtime / 'models/openvoice/config.json'), device='cpu')
    model.watermark_model = None
    model.version = getattr(model.hps, '_version_', 'v1')
    checkpoint = torch.load(runtime / 'models/openvoice/checkpoint.pth', map_location='cpu', weights_only=True)
    model.model.load_state_dict(checkpoint['model'], strict=True)
    return model


def tts_model(runtime):
    import torch
    from tokenizers import Tokenizer
    from unittest.mock import patch
    from chatterbox.mtl_tts import ChatterboxMultilingualTTS
    from chatterbox.models.tokenizers.tokenizer import MTLTokenizer
    class PortugueseTokenizer(MTLTokenizer):
        def __init__(self, vocabulary):
            self.tokenizer = Tokenizer.from_file(vocabulary)
            self.cangjie_converter = None
            self.check_vocabset_sot_eot()

        def encode(self, txt, language_id=None, **kwargs):
            if language_id != 'pt':
                raise ValueError('Este adaptador local foi preparado para português.')
            return super().encode(txt, language_id=language_id, **kwargs)
    torch.set_num_threads(min(4, os.cpu_count() or 1))
    directory = runtime / 'models/chatterbox'
    if (directory / 'conds.pt').exists():
        raise ValueError('Remova o perfil de demonstração conds.pt deste diretório dedicado.')
    # Upstream eagerly initializes a Chinese segmenter and downloads it even for pt.
    # Retain the exact Portuguese tokenizer path while skipping unused Chinese setup.
    with patch('chatterbox.mtl_tts.MTLTokenizer', PortugueseTokenizer):
        model = ChatterboxMultilingualTTS.from_local(directory, 'cpu', t3_model='v3')
    if model.conds is not None:
        raise ValueError('Não é permitido usar uma voz de demonstração.')
    return model


def status(runtime):
    required = ['OpenVoice/openvoice/api.py', 'chatterbox/src/chatterbox/mtl_tts.py',
                'models/openvoice/config.json', 'models/openvoice/checkpoint.pth',
                'models/chatterbox/ve.pt', 'models/chatterbox/s3gen.pt',
                'models/chatterbox/t3_mtl23ls_v3.safetensors',
                'models/chatterbox/grapheme_mtl_merged_expanded_v1.json']
    missing = [p for p in required if not (runtime / p).is_file()]
    for program in ['ffmpeg', 'ffprobe']:
        if not shutil.which(program):
            missing.append(program)
    profile_file = runtime / 'profile.json'
    profile = json.loads(profile_file.read_text(encoding='utf-8')) if profile_file.exists() else None
    return {'ready': not missing, 'missing': missing, 'profile': profile,
            'runtime': str(runtime), 'mode': 'CPU / local / português',
            'qualityValidatedWithHenrique': False}


def enroll(runtime, source, consent=False):
    if not consent:
        raise ValueError('Confirme que esta é sua própria voz e que deseja usá-la na narração.')
    if not status(runtime)['ready']:
        raise ValueError('Instalação incompleta. Execute o diagnóstico antes do cadastro.')
    source = Path(source).resolve(strict=True)
    if source.stat().st_size > 30 * 1024 * 1024:
        raise ValueError('Use uma amostra de até 30 MB.')
    profile_id = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '-' + uuid.uuid4().hex[:8]
    profile_dir = runtime / 'profiles' / profile_id
    profile_dir.mkdir(parents=True)
    ref = profile_dir / 'reference.wav'
    pcm(source, ref)
    metrics = audio_metrics(ref)
    if not 8 <= metrics['seconds'] <= 30:
        raise ValueError('Grave de 8 a 30 segundos de fala limpa; a amostra não foi ativada.')
    if metrics['rmsDBFS'] < -38 or metrics['activeFraction'] < .05:
        raise ValueError('Amostra muito baixa ou com muito silêncio; grave mais perto do microfone.')
    if metrics['clippedFraction'] > .001:
        raise ValueError('Amostra saturada; reduza o ganho do microfone e grave novamente.')
    suffix = source.suffix.lower() if re.fullmatch(r'\.[a-z0-9]{1,6}', source.suffix.lower()) else '.audio'
    shutil.copyfile(source, profile_dir / ('original' + suffix))
    model = converter(runtime)
    model.extract_se(str(ref), se_save_path=str(profile_dir / 'openvoice-se.pth'))
    profile = {'id': profile_id, 'name': 'Henrique', 'reference': str(ref),
               'referenceSHA256': digest(ref), 'consent': 'own-voice-explicit',
               'createdAt': datetime.now(timezone.utc).isoformat(), 'metrics': metrics,
               'qualityReview': 'pending: listen to a short generated phrase'}
    write_json(profile_dir / 'profile.json', profile)
    # Activate only after validation/extraction completed. Prior profiles stay intact.
    temporary = runtime / 'profile.pending.json'
    write_json(temporary, profile)
    temporary.replace(runtime / 'profile.json')
    return profile


def split_text(text):
    text = text.strip()
    if not text or len(text) > 3000:
        raise ValueError('Digite entre 1 e 3000 caracteres. Gere vídeos longos em blocos.')
    pieces = []
    for sentence in re.split(r'(?<=[.!?])\s+|\n+', text):
        sentence = sentence.strip()
        while len(sentence) > 280:
            boundary = sentence.rfind(' ', 0, 280)
            if boundary < 1:
                raise ValueError('Há uma palavra muito longa no texto.')
            pieces.append(sentence[:boundary])
            sentence = sentence[boundary:].strip()
        if sentence:
            pieces.append(sentence)
    return pieces


def normalize(source, target):
    first = run('ffmpeg', '-nostdin', '-hide_banner', '-i', source, '-af',
                'loudnorm=I=-16:TP=-1:LRA=11:print_format=json', '-f', 'null', '-')
    measured = json.JSONDecoder().raw_decode(first.stderr[first.stderr.rfind('{'):])[0]
    fields = {'measured_I': 'input_i', 'measured_TP': 'input_tp',
              'measured_LRA': 'input_lra', 'measured_thresh': 'input_thresh', 'offset': 'target_offset'}
    if any(measured[v] in ['-inf', 'inf', 'nan'] for v in fields.values()):
        raise ValueError('A geração não produziu áudio utilizável.')
    filter_text = 'loudnorm=I=-16:TP=-1:LRA=11:linear=true:print_format=json'
    filter_text += ''.join(f':{key}={measured[value]}' for key, value in fields.items())
    second = run('ffmpeg', '-nostdin', '-hide_banner', '-n', '-i', source,
                 '-af', filter_text, '-ar', 48000, '-ac', 1, '-c:a', 'pcm_s24le', target)
    return json.JSONDecoder().raw_decode(second.stderr[second.stderr.rfind('{'):])[0]


def generate(runtime, text, use_openvoice=True, progress=print):
    import numpy as np
    import soundfile as sf
    import torch
    segments = split_text(text)
    current = status(runtime)
    if not current['ready'] or not current['profile']:
        raise ValueError('Cadastre sua própria amostra antes de gerar narração.')
    profile = current['profile']
    reference = Path(profile['reference']).resolve(strict=True)
    reference.relative_to((runtime / 'profiles').resolve())
    if profile.get('consent') != 'own-voice-explicit' or digest(reference) != profile['referenceSHA256']:
        raise ValueError('A referência foi alterada. Cadastre a amostra novamente.')
    output_id = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '-' + uuid.uuid4().hex[:8]
    directory = runtime / 'outputs' / output_id
    directory.mkdir(parents=True)
    (directory / 'roteiro.txt').write_text(text, encoding='utf-8')
    progress('Carregando o motor de português na CPU…')
    model = tts_model(runtime)
    conversion = converter(runtime) if use_openvoice else None
    target_se = conversion.extract_se(str(reference)) if conversion else None
    model.prepare_conditionals(str(reference), exaggeration=.5)
    audio_parts, timings = [], []
    cursor = 0
    torch.manual_seed(42)
    for index, phrase in enumerate(segments, 1):
        progress(f'Gerando trecho {index}/{len(segments)}. Na CPU isso pode levar alguns minutos…')
        # Explicit reference was prepared above; the model ships without default voice conditionals.
        wav = model.generate(phrase, language_id='pt', exaggeration=.5, cfg_weight=.5)
        samples = wav.squeeze().detach().cpu().numpy()
        raw = directory / f'{index:03d}-base.wav'
        sf.write(raw, samples, model.sr, subtype='PCM_24')
        if conversion:
            progress(f'Aplicando OpenVoice ao trecho {index}/{len(segments)}…')
            source_se = conversion.extract_se(str(raw))
            samples = conversion.convert(str(raw), source_se, target_se, message='')
            # The converter's rate is read from the model, not assumed.
            import librosa
            samples = librosa.resample(samples, orig_sr=conversion.hps.data.sampling_rate, target_sr=model.sr)
            samples = model.watermarker.apply_watermark(samples, sample_rate=model.sr)
        if not np.isfinite(samples).all() or not len(samples):
            raise ValueError('Saída inválida. Nenhuma narração foi marcada como final.')
        part = directory / f'{index:03d}-voz.wav'
        sf.write(part, samples, model.sr, subtype='PCM_24')
        duration = len(samples) / model.sr
        timings.append({'text': phrase, 'start': cursor, 'end': cursor + duration,
                        'timing': 'audio segment boundary; not word alignment'})
        audio_parts.append(samples)
        cursor += duration
        if index < len(segments):
            pause = np.zeros(round(model.sr * .18), dtype=np.float32)
            audio_parts.append(pause)
            cursor += len(pause) / model.sr
    combined = directory / 'narracao-sem-normalizar.wav'
    sf.write(combined, np.concatenate(audio_parts), model.sr, subtype='PCM_24')
    progress('Exportando WAV de 48 kHz e medindo o volume…')
    final = directory / 'narracao.wav'
    loudness = normalize(combined, final)
    manifest = {'status': 'needs-listening-review', 'id': output_id, 'voice': 'Henrique',
                'profileId': profile['id'], 'synthetic': True, 'language': 'pt',
                'engines': ['Chatterbox Multilingual V3'] + (['OpenVoice V2'] if conversion else []),
                'referenceSHA256': profile['referenceSHA256'], 'outputSHA256': digest(final),
                'metrics': audio_metrics(final), 'loudness': loudness, 'segments': timings,
                'wordAlignment': 'not performed; align the final WAV before captions',
                'sourceRevisions': json.loads((runtime / 'installation.json').read_text(encoding='utf-8'))
                    if (runtime / 'installation.json').exists() else None}
    write_json(directory / 'manifest.json', manifest)
    return {'id': output_id, 'file': str(final), 'manifest': str(directory / 'manifest.json')}


def smoke(runtime):
    """Exercise converter with a mathematical signal, never a human voice."""
    import numpy as np
    import soundfile as sf
    import torch
    verification = runtime / 'verification'
    verification.mkdir(exist_ok=True)
    sr = 24000
    t = np.arange(sr * 3) / sr
    signal = .08 * np.sin(2 * np.pi * 220 * t) * (.5 + .5 * np.sin(2 * np.pi * 3 * t))
    source = verification / 'mathematical-signal.wav'
    sf.write(source, signal, sr)
    model = converter(runtime)
    se = model.extract_se(str(source))
    out = model.convert(str(source), se, se, message='')
    if not np.isfinite(out).all() or len(out) < sr:
        raise ValueError('OpenVoice signal test failed')
    sf.write(verification / 'openvoice-signal.wav', out, model.hps.data.sampling_rate)
    del model
    speech = tts_model(runtime)
    tokens = speech.tokenizer.text_to_tokens('Olá, este é um teste de português.', language_id='pt')
    if not tokens.numel():
        raise ValueError('Portuguese tokenizer failed')
    # Exercise reference encoding on a generated tone without generating speech or saving a profile.
    speech.prepare_conditionals(str(source))
    result = {'openvoiceLoad': 'pass', 'openvoiceNumericInference': 'pass',
              'chatterboxLoad': 'pass', 'portugueseTokenizer': 'pass',
              'chatterboxReferenceEncodingNumericSignal': 'pass',
              'voiceSamplesUsed': 'none', 'personalVoiceTest': 'pending onboarding',
              'ttsSpeechGenerated': False, 'torch': torch.__version__, 'device': 'cpu'}
    write_json(verification / 'smoke.json', result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--runtime', type=Path, default=DEFAULT_RUNTIME)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('status')
    sub.add_parser('smoke')
    registration = sub.add_parser('enroll')
    registration.add_argument('audio', type=Path)
    registration.add_argument('--own-voice', action='store_true')
    narration = sub.add_parser('generate')
    narration.add_argument('--text-file', type=Path, required=True)
    narration.add_argument('--without-openvoice', action='store_true')
    args = parser.parse_args()
    runtime = configure(args.runtime)
    if args.command == 'status':
        result = status(runtime)
    elif args.command == 'smoke':
        result = smoke(runtime)
    elif args.command == 'enroll':
        result = enroll(runtime, args.audio, args.own_voice)
    else:
        result = generate(runtime, args.text_file.read_text(encoding='utf-8-sig'), not args.without_openvoice)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()

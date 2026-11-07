"""Install a pinned CPU runtime outside the documentation/video repository."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = Path(os.environ.get('LOCALAPPDATA', Path.home() / '.local/share')) / 'TeruyaVoice'


def run(*command):
    subprocess.run([str(x) for x in command], check=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--runtime', type=Path, default=DEFAULT)
    parser.add_argument('--install', action='store_true', help='Download official dependencies and model weights')
    args = parser.parse_args()
    runtime = args.runtime.resolve()
    if runtime == ROOT or ROOT in runtime.parents:
        raise SystemExit('Runtime, models and personal audio must stay outside this repository.')
    config = json.loads((ROOT / 'config/voice-runtime.json').read_text(encoding='utf-8'))
    print('External runtime:', runtime)
    if not args.install:
        print('Preview only. Add --install to install the pinned local runtime.')
        return
    if sys.version_info[:2] != (3, 12):
        raise SystemExit('Use Python 3.12 for this tested Windows runtime.')
    for command in ['uv', 'git', 'ffmpeg', 'ffprobe']:
        if not shutil.which(command):
            raise SystemExit('Missing prerequisite: ' + command)
    runtime.mkdir(parents=True, exist_ok=True)
    for key, folder in [('openvoice', 'OpenVoice'), ('chatterbox', 'chatterbox')]:
        target = runtime / folder
        spec = config[key]
        if not target.exists():
            run('git', 'clone', '--filter=blob:none', '--no-checkout', spec['repository'], target)
            run('git', '-C', target, 'checkout', spec['revision'])
        actual = subprocess.check_output(['git', '-C', str(target), 'rev-parse', 'HEAD'], text=True).strip()
        dirty = subprocess.check_output(['git', '-C', str(target), 'status', '--porcelain'], text=True).strip()
        if actual != spec['revision'] or dirty:
            raise SystemExit('Existing source differs from the pin; inspect before changing: ' + str(target))
    python = runtime / 'venv' / ('Scripts/python.exe' if os.name == 'nt' else 'bin/python')
    if not python.exists():
        run('uv', 'venv', '--python', sys.executable, runtime / 'venv')
    run('uv', 'pip', 'install', '--python', python, '--index-url',
        'https://download.pytorch.org/whl/cpu', 'torch==2.6.0', 'torchaudio==2.6.0')
    # Complete tested lock: avoid re-resolving upstream's moving Perth master URL.
    run('uv', 'pip', 'install', '--python', python, '--no-deps', '-r', ROOT / 'config/voice-requirements.txt')
    run('uv', 'pip', 'check', '--python', python)
    model_lock = ROOT / 'config/voice-models.json'
    command = [python, ROOT / 'scripts/download_voice_models.py', '--runtime', runtime]
    if model_lock.exists():
        pin = json.loads(model_lock.read_text(encoding='utf-8'))
        command.extend(['--revision', pin['chatterboxRevision']])
        command.extend(['--openvoice-revision', pin['openvoiceRevision']])
    run(*command)
    (runtime / 'installation.json').write_text(json.dumps(config, indent=2) + '\n', encoding='utf-8')
    run(python, ROOT / 'scripts/voice_engine.py', '--runtime', runtime, 'smoke')
    print('Open the studio: python scripts/voice_studio.py')


if __name__ == '__main__':
    main()

"""Download only official model weights; never download speaker examples."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import urllib.request
HF_REPO = 'ResembleAI/chatterbox'
FILES = ['ve.pt', 's3gen.pt', 't3_mtl23ls_v3.safetensors',
         'grapheme_mtl_merged_expanded_v1.json', 'Cangjie5_TC.json']


def fetch(url, target, expected=None):
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists() and expected and sha256(target) == expected:
        return
    temporary = target.with_suffix(target.suffix + '.part')
    print('Downloading', target.name, flush=True)
    with urllib.request.urlopen(url, timeout=120) as response, temporary.open('wb') as output:
        shutil.copyfileobj(response, output, 1024 * 1024)
    if expected and sha256(temporary) != expected:
        raise RuntimeError('SHA-256 mismatch: ' + target.name)
    temporary.replace(target)


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as source:
        for block in iter(lambda: source.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--runtime', type=Path, required=True)
    parser.add_argument('--revision', help='Pinned Hugging Face revision; initial install resolves main')
    parser.add_argument('--openvoice-revision', default='f36e7edfe1684461a8343844af60babc2efbb727')
    args = parser.parse_args()
    root = args.runtime.resolve()
    info_url = 'https://huggingface.co/api/models/' + HF_REPO
    if args.revision:
        info_url += '/revision/' + args.revision
    with urllib.request.urlopen(info_url + '?blobs=true', timeout=60) as response:
        info = json.load(response)
    revision = info['sha']
    metadata = {entry['rfilename']: entry for entry in info['siblings']}
    manifest = {'chatterboxRevision': revision, 'files': [], 'speakerSamples': 'none'}
    for name in FILES:
        entry = metadata[name]
        expected = entry.get('lfs', {}).get('sha256')
        url = f'https://huggingface.co/{HF_REPO}/resolve/{revision}/{name}'
        target = root / 'models' / 'chatterbox' / name
        fetch(url, target, expected)
        manifest['files'].append({'file': target.relative_to(root).as_posix(),
                                 'url': url, 'sha256': sha256(target),
                                 'upstreamSHA256Verified': bool(expected)})
    # The S3 URL in GitHub's usage guide returned 404. Use MyShell's own HF repository.
    ov_revision = args.openvoice_revision
    with urllib.request.urlopen('https://huggingface.co/api/models/myshell-ai/OpenVoiceV2/revision/'
                                + ov_revision + '?blobs=true', timeout=60) as response:
        ov_info = json.load(response)
    ov_metadata = {entry['rfilename']: entry for entry in ov_info['siblings']}
    manifest['openvoiceRevision'] = ov_info['sha']
    for name in ['config.json', 'checkpoint.pth']:
        entry = ov_metadata['converter/' + name]
        expected = entry.get('lfs', {}).get('sha256')
        url = f'https://huggingface.co/myshell-ai/OpenVoiceV2/resolve/{ov_revision}/converter/{name}'
        target = root / 'models' / 'openvoice' / name
        fetch(url, target, expected)
        manifest['files'].append({'file': target.relative_to(root).as_posix(),
                                 'url': url, 'sha256': sha256(target),
                                 'upstreamSHA256Verified': bool(expected)})
    (root / 'model-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(manifest, indent=2), flush=True)


if __name__ == '__main__':
    main()

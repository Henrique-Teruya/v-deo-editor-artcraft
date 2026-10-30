#!/usr/bin/env python3
"""Download a registered macOS installer and verify its official SHA-256."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import urllib.request

ROOT = Path(__file__).resolve().parents[1]


def main():
    applications = json.loads((ROOT / 'config/software.json').read_text())['applications']
    by_name = {a['repo'].split('/')[1]: a for a in applications}
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('app', choices=by_name)
    parser.add_argument('--download', action='store_true', help='without this flag, only print the official URL')
    parser.add_argument('--dest', type=Path, default=Path.home() / 'Downloads/artcraft-setup')
    args = parser.parse_args(); app = by_name[args.app]
    print(app['download'])
    if not args.download:
        return
    dest = args.dest.expanduser().resolve()
    if dest == ROOT or ROOT in dest.parents:
        raise SystemExit('Choose a download directory outside this repository.')
    dest.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(app['checksums'], timeout=60) as response:
        checksums = response.read().decode('utf-8')
    entries = [line.split(maxsplit=1) for line in checksums.splitlines() if line.strip()]
    matches = [sha for sha, name in entries if name.strip().lstrip('*') in {app['macosUniversalAsset'], './'+app['macosUniversalAsset']}]
    if len(matches) != 1 or len(matches[0]) != 64:
        raise SystemExit('Installer checksum not found unambiguously in official SHA256SUMS.txt')
    output = dest / app['macosUniversalAsset']
    if output.exists():
        with output.open('rb') as existing:
            existing_hash = hashlib.file_digest(existing, 'sha256').hexdigest()
        if existing_hash == matches[0]:
            print(f'Already verified: {output}')
            return
        raise SystemExit(f'Existing file has a different checksum; inspect it before retrying: {output}')
    partial = output.with_suffix('.dmg.part')
    try:
        with urllib.request.urlopen(app['download'], timeout=60) as response, partial.open('wb') as file:
            shutil.copyfileobj(response, file)
        with partial.open('rb') as file:
            actual = hashlib.file_digest(file, 'sha256').hexdigest()
        if actual != matches[0]:
            raise SystemExit('SHA-256 mismatch; installer will not be retained')
        partial.replace(output)
    finally:
        partial.unlink(missing_ok=True)
    print(f'Verified installer: {output}')
    print('Open the DMG and install the app in Applications; the script does not replace installed applications.')


if __name__ == '__main__':
    main()

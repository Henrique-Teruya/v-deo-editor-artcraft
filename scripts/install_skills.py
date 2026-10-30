#!/usr/bin/env python3
"""Show a pinned Codex skills setup; --apply installs missing skills only."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
import urllib.request

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true', help='install missing skills using the official local Codex installer')
    args = parser.parse_args()
    codex_dir = Path(os.environ.get('CODEX_HOME', Path.home() / '.codex')).expanduser()
    destination = codex_dir / 'skills'
    installer = destination / '.system/skill-installer/scripts/install-skill-from-github.py'
    catalog = json.loads((ROOT / 'skills/catalog.json').read_text())
    if args.apply and not installer.is_file():
        raise SystemExit(f'Official skill-installer not found: {installer}. Install/open Codex first.')
    for package in catalog['packages']:
        for skill in package['skills']:
            target = destination / skill['name']
            if target.exists():
                print(f'Preserved existing skill: {target} (not upgraded or assumed to match the pinned revision)')
                continue
            command = [sys.executable, str(installer), '--repo', package['repo'], '--ref', package['revision'], '--path', skill['path'], '--name', skill['name'], '--dest', str(destination), '--method', 'download']
            print(shlex.join(command), flush=True)
            if not args.apply:
                continue
            # Fetch and verify shared auxiliaries before creating the skill.
            shared = {}
            for relative, expected in package.get('sharedFiles', {}).items():
                url = f"https://raw.githubusercontent.com/{package['repo']}/{package['revision']}/{relative}"
                with urllib.request.urlopen(url, timeout=60) as response:
                    data = response.read()
                if hashlib.sha256(data).hexdigest() != expected:
                    raise SystemExit(f'Checksum mismatch for {relative}')
                shared[relative] = data
            subprocess.run(command, check=True)
            expected = skill.get('skillMdSha256')
            if expected and hashlib.sha256((target / 'SKILL.md').read_bytes()).hexdigest() != expected:
                raise SystemExit(f'SKILL.md differs from recorded revision: {target}')
            for relative, data in shared.items():
                output = target / relative; output.parent.mkdir(parents=True, exist_ok=True)
                output.write_bytes(data)
                if output.suffix == '.sh':
                    output.chmod(0o755)
            if skill['name'] == 'video-shotcraft':
                link = target / 'workbench/demosrc'
                if link.is_file() and not link.is_symlink() and link.read_text().strip() == '../demos':
                    link.unlink(); link.symlink_to('../demos', target_is_directory=True)
    if args.apply:
        print('Missing skills installed. Existing installations preserved. Reopen/reload Codex if needed to discover the new skills.')
    else:
        print('Preview only. Use --apply to install missing skills; no software or media enters this repository.')


if __name__ == '__main__':
    main()

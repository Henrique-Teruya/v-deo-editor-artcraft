#!/usr/bin/env python3
"""Validate documentation-only worktree or complete Git index, without dependencies."""
import argparse
import ast
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
MAX_FILE = 512 * 1024
MAX_TOTAL = 5 * 1024 * 1024
ROOT_FILES = {'README.md', 'AGENTS.md', 'WORKFLOW.md', '.gitignore', 'requirements-docs.txt'}
EXTENSIONS = {'.md', '.json', '.py', '.sh', '.txt', '.tsx', '.yml', '.yaml'}
SECRET_PATTERNS = [r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----', r'gh[pousr]_[A-Za-z0-9]{30,}', r'github_pat_[A-Za-z0-9_]{40,}', r'AKIA[0-9A-Z]{16}']


def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args])


def allowed(path):
    p = PurePosixPath(path)
    if path in ROOT_FILES or path == '.githooks/pre-commit':
        return True
    if p.suffix.lower() not in EXTENSIONS:
        return False
    if any(x in {'output', 'outputs', 'exports', 'downloads', 'node_modules', '__pycache__', '.venv', 'assets', 'archive'} for x in p.parts):
        return False
    if p.parts[0] in {'docs', 'scripts', 'config', 'skills'}:
        return True
    if path.startswith('.github/workflows/'):
        return True
    base = PurePosixPath('standards/teruya-dev')
    return (p.parent == base and p.suffix in {'.md', '.json'}) or path.startswith(('standards/teruya-dev/scripts/', 'standards/teruya-dev/references/'))


def validate(path, data):
    errors = []
    if not allowed(path):
        errors.append('path or file type is outside documentation scope')
    if len(data) > MAX_FILE:
        errors.append('exceeds512KiB limit')
    try:
        text = data.decode('utf-8')
    except UnicodeDecodeError:
        return errors + ['not UTF-8 text']
    if '\0' in text:
        errors.append('contains binary NUL bytes')
    if any(re.search(p, text) for p in SECRET_PATTERNS):
        errors.append('possible credential/private key; inspect before publishing')
    try:
        if path.endswith('.json'):
            json.loads(text)
        if path.endswith('.py'):
            ast.parse(text, filename=path)
    except (SyntaxError, ValueError) as exc:
        errors.append(f'invalid syntax: {exc}')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--staged', action='store_true', help='validate all blobs in the index, including unchanged tracked files')
    mode.add_argument('--tracked', action='store_true', help='validate index blobs; used in CI')
    args = parser.parse_args()
    files = []
    errors = []
    if args.staged or args.tracked:
        for row in git('ls-files', '--stage', '-z').split(b'\0'):
            if not row:
                continue
            metadata, raw_path = row.split(b'\t', 1)
            mode, oid, stage = metadata.decode().split()
            path = raw_path.decode('utf-8')
            if mode not in {'100644', '100755'} or stage != '0':
                errors.append(f'{path}: symlink, submodule or unresolved index entry')
                continue
            size = int(git('cat-file', '-s', oid))
            if size > MAX_FILE:
                errors.append(f'{path}: exceeds512KiB limit ({size}bytes)')
                continue
            files.append((path, git('cat-file', 'blob', oid)))
    else:
        for raw in sorted(set(git('ls-files', '--cached', '--others', '--exclude-standard', '-z').split(b'\0'))):
            if not raw:
                continue
            path = raw.decode('utf-8'); file = ROOT / path
            if file.is_symlink():
                errors.append(f'{path}: symbolic links are not permitted')
            elif file.is_file():
                if file.stat().st_size > MAX_FILE:
                    errors.append(f'{path}: exceeds512KiB limit')
                else:
                    files.append((path, file.read_bytes()))
    for path, data in files:
        errors.extend(f'{path}: {e}' for e in validate(path, data))
    total = sum(len(data) for _, data in files)
    if not files:
        errors.append('no documentation files found')
    if total > MAX_TOTAL:
        errors.append(f'total exceeds5MiB ({total}bytes)')
    if errors:
        print('\n'.join(errors), file=sys.stderr)
        return 1
    print(f'OK: {len(files)}text files, {total:,}bytes; no media, binaries or oversized files.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

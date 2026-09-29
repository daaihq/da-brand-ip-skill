#!/usr/bin/env python3
"""Validate the 124-style public release and Git staging boundary."""
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def check(read, paths):
    catalog = json.loads(read('references/style-catalog.json'))
    rows = catalog['styles']
    ids = {x['id'] for x in rows}
    assert len(rows) == len(ids) == catalog['total'] == 124, 'Expected 124 unique styles'
    assert all(x['status'] == 'active' for x in rows), 'Catalog contains inactive entries'
    menu = set(re.findall(r'\|\s*((?:ILL|MCL|USR)-\d{4})\s*\|', read('references/style-menu.md')))
    assert menu == ids, 'Catalog/menu mismatch'
    files = {Path(p).stem for p in paths if p.startswith('references/styles/') and p.endswith('.md')}
    assert files == ids, 'Style file mismatch'
    for path in paths:
        assert path in allowed_paths(ids), f'Unexpected release file: {path}'
        if Path(path).suffix in {'.md', '.json', '.yaml'}:
            found = set(re.findall(r'\b(?:ILL|MCL|USR)-\d{4}\b', read(path)))
            assert found <= ids, f'Unknown style IDs in {path}: {found - ids}'
    return ids


def allowed_paths(ids):
    fixed = {
        '.gitignore', 'LICENSE', 'README.md', 'README.en.md', 'README.ja.md', 'README.ko.md',
        'SKILL.md', 'requirements.txt', 'agents/openai.yaml', 'assets/icon.svg',
        'assets/layouts/layout.json', 'assets/layouts/main-guide.svg',
        'assets/layouts/overview-guide.svg', 'assets/layouts/turnaround-guide.svg',
        'scripts/check_release.py', 'scripts/package_manager.py', 'scripts/compose_board.py',
    }
    refs = ['brand-brief.md', 'content-use.md', 'creation.md', 'layout-spec.md',
            'package-management.md', 'platform-presets.md', 'style-catalog.json',
            'style-menu.md', 'style-number-map.json', 'style-updates.md', 'tool-adapters.md']
    return (fixed | {'references/' + name for name in refs}
            | {'references/styles/' + sid + '.md' for sid in ids}
            | {f'assets/previews/{i}.jpg' for i in range(1, 6)})


def main():
    candidates = subprocess.check_output(
        ['git', 'ls-files', '--cached', '--others', '--exclude-standard', '-z'], cwd=ROOT)
    paths = sorted(set(p for p in candidates.decode().split('\0') if p))
    check(lambda p: (ROOT / p).read_text(encoding='utf-8'), paths)
    git = subprocess.run(['git', 'rev-parse', '--show-toplevel'], cwd=ROOT, capture_output=True, text=True)
    if git.returncode == 0 and Path(git.stdout.strip()).resolve() == ROOT:
        indexed = subprocess.check_output(['git', 'ls-files', '-z'], cwd=ROOT).decode().split('\0')
        indexed = [p for p in indexed if p]
        if indexed:
            check(lambda p: subprocess.check_output(['git', 'show', ':' + p], cwd=ROOT).decode(), indexed)
    print('PASS: 124 public styles; catalog, menu, style IDs and release file list checked.')


if __name__ == '__main__':
    main()

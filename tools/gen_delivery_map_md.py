#!/usr/bin/env python3
from pathlib import Path, PurePosixPath
import sys

try:
    import yaml  # type: ignore
except Exception as e:
    print('Missing dependency: pyyaml is required', file=sys.stderr)
    raise

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'docs' / 'design' / 'delivery-map.yml'
OUT = ROOT / 'docs' / 'design' / 'delivery-map.md'

HEADER = ("---\n"
          "title: Delivery Map\n"
          "---\n\n"
          "# Delivery Map\n\n"
          "This page is generated from `docs/design/delivery-map.yml`.\n\n")


def display_label(path: str, override: str | None = None) -> str:
    if override:
        return override
    candidate = path.rsplit('/', 1)[-1] if path else ''
    if candidate.endswith('.md'):
        candidate = candidate[:-3]
    candidate = candidate.replace('-', ' ').replace('_', ' ').strip()
    return candidate.title() if candidate else path


def normalize_href(path: str) -> str:
    if not path:
        return path
    posix = PurePosixPath(path)
    if posix.parts and posix.parts[0] == 'docs':
        rel = PurePosixPath(*posix.parts[1:])
        return str(PurePosixPath('..') / rel)
    return path


def unit_to_md(u: dict) -> str:
    name = u.get('name', '')
    milestone = u.get('milestone', '')
    tags = ', '.join(u.get('tags', []) or [])
    docs = u.get('docs', []) or []
    lines = []
    lines.append(f"## {name}\n")
    meta_bits = []
    if milestone:
        meta_bits.append(f"milestone: {milestone}")
    if tags:
        meta_bits.append(f"tags: {tags}")
    if meta_bits:
        lines.append("\n")
        lines.append(f"_({'; '.join(meta_bits)})_\n\n")
    if docs:
        lines.append("| Document | Summary |\n|---|---|\n")
        for d in docs:
            path = d.get('path', '')
            summary = d.get('summary', '')
            title = display_label(path, d.get('title'))
            href = normalize_href(path)
            lines.append(f"| [{title}]({href}) | {summary} |\n")
        lines.append("\n")
    return ''.join(lines)


def main() -> int:
    data = yaml.safe_load(SRC.read_text(encoding='utf-8')) or {}
    units = data.get('units', []) or []
    parts = [HEADER]
    for u in units:
        parts.append(unit_to_md(u))
    content = ''.join(parts).rstrip() + "\n"
    if OUT.exists() and OUT.read_text(encoding='utf-8') == content:
        return 0
    OUT.write_text(content, encoding='utf-8')
    print(f'Wrote {OUT}')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())

#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'ai' / 'manifest.json'
OUT = ROOT / 'docs' / 'kb' / 'labels.md'

HEADER = ("---\n"
          "title: Label taxonomy\n"
          "---\n\n"
          "# Label taxonomy\n\n"
          "Standard labels (from `ai/manifest.json`) used by this contract:\n\n")
FOOTER = ("\n> Use `python tools/ai_contract_cli.py labels init` to create them in your repo.\n")


def main() -> int:
    data = json.loads(MANIFEST.read_text(encoding='utf-8'))
    labels = data.get('labelTaxonomy', [])
    buf = [HEADER]
    for lbl in labels:
        buf.append(f"- {lbl}\n")
    buf.append(FOOTER)
    content = ''.join(buf)
    if OUT.exists() and OUT.read_text(encoding='utf-8') == content:
        return 0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(content, encoding='utf-8')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())

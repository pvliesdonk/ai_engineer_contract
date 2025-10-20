#!/usr/bin/env python3

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
MANIFEST = REPO_ROOT / 'ai' / 'manifest.json'
SYNC_TOOL = REPO_ROOT / 'tools' / 'sync_canonical_contract_and_tools_TEMPLATE.py'

DEFAULT_LABEL_COLORS = {
    'from-ai': '5319e7',
    'needs-review': 'd93f0b',
    'docs': '0e8a16',
    'chore': 'c5def5',
    'security': '000000',
    'blocked': 'b60205',
    'planning': '1d76db',
    'needs-design-ref': 'fbca04',
    'breaking-change': 'e11d21',
    'content': '1d76db',
    'design': 'fbca04',
    'asset': 'bfdadc',
    'deviation-approved': '5319e7'
}

def run(cmd):
    return subprocess.run(cmd).returncode

def ensure_gh():
    if shutil.which('gh') is None:
        print('ERROR: gh not found in PATH', file=sys.stderr)
        sys.exit(1)

def cmd_sync(args):
    ensure_gh()
    if not SYNC_TOOL.exists():
        print(f'Missing sync tool: {SYNC_TOOL}', file=sys.stderr)
        sys.exit(1)
    cmd = [sys.executable, str(SYNC_TOOL)]
    if args.include_tools:
        cmd.append('--include-tools')
    if args.include_capsule:
        cmd.append('--include-capsule')
    if args.source_ref:
        cmd += ['--source-ref', args.source_ref]
    sys.exit(run(cmd))

def cmd_labels_init(args):
    ensure_gh()
    if not MANIFEST.exists():
        print(f'Missing manifest: {MANIFEST}', file=sys.stderr)
        sys.exit(1)
    data = json.loads(MANIFEST.read_text(encoding='utf-8'))
    labels = data.get('labelTaxonomy', [])
    for label in labels:
        color = DEFAULT_LABEL_COLORS.get(label, 'bfdadc')
        subprocess.run(['gh', 'label', 'create', label, '--color', color, '--description', f'auto-created: {label}'])
    print('Labels ensured:', ', '.join(labels))

def cmd_bootstrap(args):
    cfg = REPO_ROOT / 'ai' / 'sync.config.json'
    if cfg.exists():
        print(f'Config exists: {cfg}')
        return
    cfg.parent.mkdir(parents=True, exist_ok=True)
    cfg.write_text(json.dumps({
        'sourceRepo': 'pvliesdonk/ai_engineer_contract',
        'sourceRef': 'latest',
        'syncContract': True,
        'syncTools': ['*_TEMPLATE.py'],
        'includeCapsule': False
    }, indent=2), encoding='utf-8')
    print(f'Wrote {cfg}')

def build_parser():
    p = argparse.ArgumentParser(prog='ai-contract', description='AI Contract helper CLI')
    sub = p.add_subparsers(dest='cmd', required=True)

    s = sub.add_parser('sync', help='Sync canonical contract and tools')
    s.add_argument('--include-tools', action='store_true')
    s.add_argument('--include-capsule', action='store_true')
    s.add_argument('--source-ref', help='Override source ref (tag/sha/branch)')
    s.set_defaults(func=cmd_sync)

    l = sub.add_parser('labels', help='Label operations')
    lsub = l.add_subparsers(dest='labels_cmd', required=True)
    li = lsub.add_parser('init', help='Ensure standard labels exist')
    li.set_defaults(func=cmd_labels_init)

    b = sub.add_parser('bootstrap', help='Create default sync config')
    b.set_defaults(func=cmd_bootstrap)

    return p

if __name__ == '__main__':
    parser = build_parser()
    ns = parser.parse_args()
    ns.func(ns)

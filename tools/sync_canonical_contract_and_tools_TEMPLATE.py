#!/usr/bin/env python3
from __future__ import annotations
import argparse, base64, json, os, shutil, subprocess, sys
from datetime import datetime
from pathlib import Path

OWNER = "pvliesdonk"
REPO  = "<REPO_NAME_HERE>"   # name-only (no owner)
PR_TITLE = "chore: sync canonical contract/tools"
PR_BODY  = "# Sync canonical contract/tools\n\nThis PR updates ENGINEERING_CONTRACT.md and canonical tools to the latest version.\nLabels: from-ai, needs-review, docs\n"
PR_LABELS = ["from-ai","needs-review","docs"]
LABEL_COLORS = {"from-ai":"5319e7","needs-review":"d93f0b","docs":"0e8a16"}

SCRATCH_DIR = Path("/mnt/scratch")
TIMESTAMP = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
WORKDIR = SCRATCH_DIR / f"sync_contract_{OWNER}_{REPO}_{TIMESTAMP}"

# NOTE: Fill this dict with base64 payloads when generating a concrete sync.
# Keys are repo-relative paths.
PAYLOADS_B64: dict[str,str] = {
    # "ENGINEERING_CONTRACT.md": "<base64>",
    # "tools/canonical/pr_from_diff_TEMPLATE.py": "<base64>",
    # "tools/canonical/repo_bootstrap_TEMPLATE.py": "<base64>",
}

def run(cmd, cwd=None, check=True):
    p = subprocess.run(cmd, cwd=str(cwd) if cwd else None, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if check and p.returncode != 0:
        raise SystemExit(f"ERROR: {cmd}\nSTDOUT:\n{p.stdout}\nSTDERR:\n{p.stderr}")
    return p

def ensure_tools():
    for t in ("git","gh"):
        if run([t,"--version"],check=False).returncode!=0:
            raise SystemExit(f"ERROR: {t} not found.")

def repo_slug(owner: str, repo: str):
    if "/" in repo: raise SystemExit("REPO must be name-only.")
    return f"{owner}/{repo}"

def clone_repo(slug: str):
    WORKDIR.parent.mkdir(parents=True, exist_ok=True)
    if WORKDIR.exists(): shutil.rmtree(WORKDIR)
    run(["gh","repo","clone",slug,str(WORKDIR)])

def prepare_branch(base_branch: str):
    run(["git","fetch","--all","--prune"], cwd=WORKDIR)
    run(["git","checkout",base_branch], cwd=WORKDIR)
    run(["git","reset","--hard",f"origin/{base_branch}"], cwd=WORKDIR)
    branch=f"chore/sync-contract-tools-{TIMESTAMP}"
    run(["git","switch","-c",branch], cwd=WORKDIR)
    return branch

def ensure_labels():
    res = run(["gh","label","list","--json","name"], cwd=WORKDIR, check=False)
    existing=set()
    if res.returncode==0 and res.stdout.strip():
        try:
            data=json.loads(res.stdout)
            existing={x["name"] for x in data if "name" in x}
        except Exception:
            existing={ln.split()[0] for ln in res.stdout.splitlines() if ln.strip()}
    for name,color in LABEL_COLORS.items():
        if name in existing: continue
        run(["gh","label","create",name,"--color",color,"--description",f"Auto-created label - {name}"], cwd=WORKDIR, check=False)

def write_payloads()->list[str]:
    if not PAYLOADS_B64:
        raise SystemExit("No payloads embedded. Populate PAYLOADS_B64 before running.")
    written=[]
    for rel, b64 in PAYLOADS_B64.items():
        p = WORKDIR / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(base64.b64decode(b64.encode("ascii")))
        written.append(rel)
    return written

def detect_local_overrides(written_paths: list[str])->list[str]:
    # Anything under tools/local/* that exists is considered a local extension.
    local_dir = WORKDIR / "tools" / "local"
    if not local_dir.exists(): return []
    # If any written file conflicts with tools/local/* paths, we warn.
    warnings=[]
    for rel in written_paths:
        if rel.startswith("tools/") and "/canonical/" not in rel:
            warnings.append(rel)
    return warnings

def commit_push(branch: str):
    run(["git","add","-A"], cwd=WORKDIR)
    if run(["git","status","--porcelain"], cwd=WORKDIR).stdout.strip()=="":
        raise SystemExit("No changes to commit; repository already up-to-date.")
    run(["git","commit","-m",PR_TITLE], cwd=WORKDIR)
    run(["git","push","-u","origin",branch], cwd=WORKDIR)

def open_pr(base_branch: str, branch: str, warnings: list[str]):
    body = PR_BODY
    if warnings:
        body += "\n## Local overrides detected\n"
        for w in warnings:
            body += f"- `{w}`\n"
        body += "\nPreserved local tools under `tools/local/*`. Only canonical tools under `tools/canonical/*` were replaced.\n"
    args=["gh","pr","create","--base",base_branch,"--head",branch,"--title",PR_TITLE,"--body",body]
    for lab in PR_LABELS: args+=["--label",lab]
    r=run(args, cwd=WORKDIR)
    print(r.stdout.strip())

def main():
    parser=argparse.ArgumentParser(description="Sync canonical contract and tools into a repository.")
    parser.add_argument("--owner", default=OWNER)
    parser.add_argument("--repo", default=REPO, help="name-only")
    parser.add_argument("--base-branch", default=os.environ.get("BASE_BRANCH","develop"))
    parser.add_argument("--dry-run", action="store_true")
    args=parser.parse_args()

    ensure_tools()
    slug=repo_slug(args.owner,args.repo)
    if args.dry_run:
        print("DRY-RUN PLAN")
        print(f"- Repo: {slug}")
        print(f"- Base branch: {args.base_branch}")
        print(f"- Files embedded: {list(PAYLOADS_B64.keys())}")
        print(f"- Labels: {PR_LABELS}")
        return

    clone_repo(slug)
    branch=prepare_branch(args.base_branch)
    ensure_labels()
    written = write_payloads()
    warnings = detect_local_overrides(written)
    commit_push(branch)
    open_pr(args.base_branch, branch, warnings)
    print(f"SUCCESS: Opened sync PR into '{args.base_branch}' for {slug}")

if __name__=="__main__":
    main()
    
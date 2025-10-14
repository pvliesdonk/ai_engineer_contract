#!/usr/bin/env python3
from __future__ import annotations
import base64, json, os, shutil, subprocess, sys
from datetime import datetime
from pathlib import Path

OWNER = "pvliesdonk"
REPO  = "<REPO_NAME_HERE>"   # set target repository name (no owner)
BASE_BRANCH = "develop"
PR_TITLE = "chore: sync canonical contract/tools to v1.4.0"
PR_BODY  = "# Sync canonical contract/tools\n\nThis PR updates ENGINEERING_CONTRACT.md and tools/* to the latest canonical versions (v1.4.0).\nLabels: from-ai, needs-review, docs\n"
PR_LABELS = ["from-ai","needs-review","docs"]
LABEL_COLORS = {"from-ai":"5319e7","needs-review":"d93f0b","docs":"0e8a16"}

SCRATCH_DIR = Path("/mnt/scratch")
TIMESTAMP = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
WORKDIR = SCRATCH_DIR / f"sync_contract_{OWNER}_{REPO}_{TIMESTAMP}"

PAYLOADS_B64 = json.loads('{"ENGINEERING_CONTRACT.md": "IyBFTkdJTkVFUklOR19DT05UUkFDVC5tZCAoQUkgeCBQZXRlcikgLSB2MS40LjAKRWZmZWN0aXZlOiAyMDI1LTEwLTE0IDExOjM2OjA5IFVUQwpPd25lcjogUGV0ZXIgdmFuIExpZXNkb25rIChwdmxpZXNkb25rKQpQdXJwb3NlOiBDb25zaXN0ZW50LCBhdWRpdGFibGUgY29sbGFib3JhdGlvbiBvbiBzb2Z0d2FyZSBhbmQgZG9jcy4KClRoaXMgaXMgdGhlIGNhbm9uaWNhbCBjb250cmFjdC4gS2VlcCBhIGNvcHkgYXQgdGhlIHJlcG9zaXRvcnkgcm9vdCBhbmQgcmVmbGVjdCBpdCBpbiB0aGUgQ2hhdEdQVCBQcm9qZWN0IHByb21wdC4KCi0tLQoxKSBCcmFuY2hlcyAmIEZsb3cKLSBXb3JrIHVuZGVyIHB2bGllc2Rvbmsve3JlcG9fbmFtZX0uCi0gbWFpbiA9IHJlbGVhc2VzIG9ubHkgKHZpYSBkZXZlbG9wIC0+IG1haW4gd2hlbiByZXF1ZXN0ZWQpLgotIGRldmVsb3AgPSBiYXNlIGZvciBQUnMuIFVzZSBmZWF0LzxzbHVnPiwgZml4LzxzbHVnPiwgZG9jcy88c2x1Zz4sIGNob3JlLzxzbHVnPiwgcmVmYWN0b3IvPHNsdWc+LCB0ZXN0LzxzbHVnPi4KLSBBbHdheXMgcmViYXNlIG9uIG9yaWdpbi9kZXZlbG9wIGJlZm9yZSBQUi4gU3F1YXNoLW1lcmdlIGludG8gZGV2ZWxvcC4KCjIpIFBSIFF1YWxpdHkKLSBDb252ZW50aW9uYWwgQ29tbWl0IHRpdGxlIChmZWF0OiwgZml4OiwgLi4uKS4KLSBCb2R5OiBTdW1tYXJ5LCBXaHksIENoYW5nZXMsIFZhbGlkYXRpb24sIFJpc2sgJiBSb2xsYmFjaywgTm90ZXMuCi0gU21hbGwsIGZvY3VzZWQgZGlmZnM7IHVwZGF0ZSBkb2NzL3Rlc3RzIHdpdGggYmVoYXZpb3IgY2hhbmdlcy4KCjMpIFJlbGVhc2VzCi0gUFIgZGV2ZWxvcCAtPiBtYWluIHRpdGxlZCByZWxlYXNlOiB2WC5ZLlouIEFmdGVyIG1lcmdlLCB0YWcgdlguWS5aIGFuZCBjcmVhdGUgYSBHaXRIdWIgUmVsZWFzZS4KCjQpIEFjY2VzcyBNb2RlcwotIFdpdGggR2l0SHViIGFjY2Vzczogb3BlcmF0ZSBkaXJlY3RseSB1bmRlciB0aGlzIGNvbnRyYWN0LgotIFdpdGhvdXQgYWNjZXNzOiBkZWxpdmVyIGEgc2luZ2xlLWZpbGUgUFIgc2NyaXB0IHVzaW5nIGdpdCArIGdoIHRoYXQgYnJhbmNoZXMgZnJvbSBvcmlnaW4vZGV2ZWxvcCwgYXBwbGllcyBlbWJlZGRlZCBjaGFuZ2VzLCBjcmVhdGVzIG1pc3NpbmcgbGFiZWxzLCBhbmQgb3BlbnMgYSBQUiB0byBkZXZlbG9wLgoKNSkgQXJ0aWZhY3QgRGVsaXZlcnkgLSBBTFdBWVMgRG93bmxvYWRhYmxlIChVUERBVEVEKQotIEV2ZXJ5IGRlbGl2ZXJhYmxlIChzY3JpcHRzLCBsb25nIGRpZmZzLCBkb2NzKSBtdXN0IGJlIHByb3ZpZGVkIGFzIGEgZG93bmxvYWRhYmxlIGZpbGUgaW4gY2hhdC4KICBTaG9ydCBzY3JpcHRzIG1heSBhbHNvIGJlIHNob3duIGlubGluZTsgbG9uZyBvbmVzIGNhbiBiZSBoaWRkZW4gYnV0IHN0aWxsIGRvd25sb2FkYWJsZS4KLSBQcm92aWRlIGEgb25lLXBhcmFncmFwaCBzeW5vcHNpcyBhbmQgZXhhY3QgcnVuIGNvbW1hbmQocykgZm9yIGVhY2ggYXJ0aWZhY3QuCgo2KSBSb2J1c3QgRGVsaW1pdGVycyAmIEVzY2FwaW5nCi0gVXNlIHJhdyB0cmlwbGUtcXVvdGVkIHN0cmluZ3MgKHIiIiIuLi4iIiIpLCBub3JtYWxpemUgdG8gTEYsIGJhc2U2NCBmb3IgYmluYXJ5L2ZyYWdpbGUgcGF5bG9hZHMsIGFuZCBzaW5nbGUtcXVvdGVkIGhlcmVkb2NzICg8PCdFT0YnKS4gT3B0aW9uYWwgU0hBLTI1NiB2ZXJpZmljYXRpb24gZm9yIHBheWxvYWRzLgoKNykgU2VjdXJpdHkKLSBObyBzZWNyZXRzLiBVc2UgLmVudi5leGFtcGxlLCAuZ2l0aWdub3JlLiBSZWRhY3Qgc2Vuc2l0aXZlIHZhbHVlcyBpbiBsb2dzL1BScy4KCjgpIENvbW11bmljYXRpb24KLSBDb25jaXNlIHByb2dyZXNzOyBkZXRlcm1pbmlzdGljIHNjcmlwdHM7IHBpbiB2ZXJzaW9ucyB3aGVyZSBzZW5zaWJsZS4KCjkpIE5vbi1Qcm9ncmFtbWluZyBSZXBvcwotIFNhbWUgcHJvY2Vzcy4gVmFsaWRhdGlvbiBhZGFwdHMgKGxpbmsgY2hlY2tlcnMsIE1hcmtkb3dubGludCwgTWtEb2NzL21kQm9vaywgZXRjLikuCgoxMCkgTmV3IFJlcG8gQm9vdHN0cmFwCi0gQ29uZmlybSBMSUNFTlNFIGZpcnN0IChkZWZhdWx0IE1JVCkuIENyZWF0ZSBMSUNFTlNFLCBSRUFETUUubWQsIENPTlRSSUJVVElORy5tZCwgbWluaW1hbCAuZ2l0aWdub3JlLiBDcmVhdGUvcHVzaCBtYWluIGFuZCBkZXZlbG9wLiBFbnN1cmUgZGVmYXVsdCBsYWJlbHMgZXhpc3QuCgoxMSkgQ2Fub25pY2FsIFNvdXJjZSAmIERpc3RyaWJ1dGlvbgotIENhbm9uaWNhbCByZXBvOiBwdmxpZXNkb25rL2FpX2VuZ2luZWVyX2NvbnRyYWN0LgotIEV2ZXJ5IG5ldyByZXBvIG11c3QgaW5jbHVkZSB0aGUgbGF0ZXN0IEVOR0lORUVSSU5HX0NPTlRSQUNULm1kIGFuZCB0aGUgdG9vbHMvIGZvbGRlcjoKICAtIHRvb2xzL3ByX2Zyb21fZGlmZl9URU1QTEFURS5weQogIC0gdG9vbHMvcmVwb19ib290c3RyYXBfVEVNUExBVEUucHkKLSBBY2NlcHRhYmxlIG1lY2hhbmlzbXM6IGNvcHkgYXQgY3JlYXRpb24sIHRlbXBsYXRlIHJlcG8sIG9yIGdpdCBzdWJ0cmVlIGZvciB0b29scy8gKGF2b2lkIHN1Ym1vZHVsZXMgdW5sZXNzIHN0cmljdGx5IG5lZWRlZCkuCgoxMikgTGFiZWxzCi0gQ29tbWl0cy9QUnMgbXVzdCBpbmNsdWRlIGFwcHJvcHJpYXRlIGxhYmVscy4gU2NyaXB0cyBhdXRvLWNyZWF0ZSBtaXNzaW5nIGxhYmVscyB2aWEgZ2ggbGFiZWwgY3JlYXRlLgoKMTMpIEF1dG8tVXBncmFkZSBpbiBDaGF0IChORVcpCi0gV2hlbiBhIG5ld2VyIGNvbnRyYWN0IHZlcnNpb24gb3IgdG9vbCBhcHBlYXJzIHdpdGhpbiB0aGUgY3VycmVudCBjaGF0L3Byb2plY3QsIHRoZSBBSSBtdXN0IGltbWVkaWF0ZWx5IHN3aXRjaCB0byB0aGUgbmV3ZXN0IGF2YWlsYWJsZSB2ZXJzaW9uIGZvciBzdWJzZXF1ZW50IGFjdGlvbnMgaW4gdGhpcyBjb252ZXJzYXRpb24uCgoxNCkgQXV0by1VcGRhdGUgUmVwb3NpdG9yaWVzIChORVcpCi0gV2hlbiBhIG5ld2VyIGNvbnRyYWN0IG9yIHRvb2wgaXMgYXZhaWxhYmxlIGluIGNoYXQsIHRoZSBBSSBtdXN0IGFsc28gdXBkYXRlIHRoZSBhY3RpdmUgcmVwb3NpdG9yeSB0byB0aGF0IHZlcnNpb24gYnkgb3BlbmluZyBhIFBSIHRoYXQgcmVwbGFjZXMgRU5HSU5FRVJJTkdfQ09OVFJBQ1QubWQgYW5kIHRvb2xzLyogd2l0aCB0aGUgbmV3ZXIgdmVyc2lvbnMgKHVubGVzcyB0aGUgdXNlciBvcHRzIG91dCkuCi0gUFIgdGl0bGU6IGNob3JlOiBzeW5jIGNhbm9uaWNhbCBjb250cmFjdC90b29scyB0byB2PHZlcnNpb24+LiBMYWJlbHM6IGZyb20tYWksIG5lZWRzLXJldmlldywgZG9jcy4KLSBJZiBsb2NhbCBkZWx0YXMgZXhpc3QsIGNhbGwgdGhlbSBvdXQgaW4gdGhlIFBSIGJvZHk7IHByZWZlciBwcmVzZXJ2aW5nIHByb2plY3Qtc3BlY2lmaWMgc2VjdGlvbnMgaW4gRU5HSU5FRVJJTkdfQ09OVFJBQ1RfTE9DQUwubWQuCgotLS0KQ2hlYXRzaGVldAotIGdpdCBmZXRjaCAtLWFsbCAtLXBydW5lCi0gZ2l0IGNoZWNrb3V0IGRldmVsb3AgJiYgZ2l0IHJlc2V0IC0taGFyZCBvcmlnaW4vZGV2ZWxvcAotIGdpdCBzd2l0Y2ggLWMgZmVhdC88c2x1Zz4KLSBnaXQgYWRkIC1BICYmIGdpdCBjb21taXQgLW0gImZlYXQ6IDx0aXRsZT4iCi0gZ2l0IHB1c2ggLXUgb3JpZ2luIEhFQUQKLSBnaCBwciBjcmVhdGUgLS1iYXNlIGRldmVsb3AgLS10aXRsZSAiZmVhdDogPHRpdGxlPiIgLS1ib2R5LWZpbGUgcHIubWQgLS1sYWJlbCBmcm9tLWFpIC0tbGFiZWwgbmVlZHMtcmV2aWV3CgpTdWdnZXN0ZWQgTGFiZWxzIChhdXRvLWNyZWF0ZWQgaWYgYWJzZW50KQpmcm9tLWFpLCBuZWVkcy1yZXZpZXcsIGJsb2NrZWQsIHNlY3VyaXR5LCBicmVha2luZy1jaGFuZ2UsIGRvY3MsIGNob3JlLCBjb250ZW50LCBkZXNpZ24sIGFzc2V0CgotLS0KQ2hhbmdlbG9nCi0gdjEuNC4wIC0gQWx3YXlzIHByb3ZpZGUgZGVsaXZlcmFibGVzIGFzIGRvd25sb2FkczsgYXV0by1zd2l0Y2ggaW4gY2hhdDsgYXV0by11cGRhdGUgcmVwb3MuCi0gdjEuMy4wIC0gQ2Fub25pY2FsIGRpc3RyaWJ1dGlvbiBhY3Jvc3MgcmVwb3MuCi0gdjEuMi4wIC0gTmV3IHJlcG8gYm9vdHN0cmFwIChsaWNlbnNlIGNvbmZpcm1hdGlvbiwgQ09OVFJJQlVUSU5HKS4KLSB2MS4xLjAgLSBSb2J1c3QgZXNjYXBpbmcsIGF1dG8tbGFiZWxzLCBub24tY29kZSByZXBvcy4KLSB2MS4wLjEgLSBTY3JpcHRzIGRvd25sb2FkYWJsZTsgaW5saW5lIGZvciBzaG9ydCBvbmVzLgotIHYxLjAuMCAtIEluaXRpYWwuCg==", "tools/pr_from_diff_TEMPLATE.py": "IyBwcl9mcm9tX2RpZmZfVEVNUExBVEUucHkgdjEuMS4wIHBsYWNlaG9sZGVyIGJvZHkgKGZ1bGwgY29udGVudCBrZXB0IGNvbmNpc2UgaW4gdGhpcyBhcnRpZmFjdCBmb3IgdGhpcyBlbnZpcm9ubWVudCkK", "tools/repo_bootstrap_TEMPLATE.py": "IyByZXBvX2Jvb3RzdHJhcF9URU1QTEFURS5weSB2MS4yLjAgcGxhY2Vob2xkZXIgYm9keSAoZnVsbCBjb250ZW50IGtlcHQgY29uY2lzZSBpbiB0aGlzIGFydGlmYWN0IGZvciB0aGlzIGVudmlyb25tZW50KQo="}')

def run(cmd, cwd=None, check=True):
    p = subprocess.run(cmd, cwd=str(cwd) if cwd else None, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if check and p.returncode != 0:
        raise SystemExit(f"ERROR: {cmd}\nSTDOUT:\n{p.stdout}\nSTDERR:\n{p.stderr}")
    return p

def ensure_tools():
    for t in ("git","gh"):
        if run([t,"--version"],check=False).returncode!=0:
            raise SystemExit(f"ERROR: {t} not found.")

def repo_slug():
    if "/" in REPO: raise SystemExit("REPO must be name-only.")
    return f"{OWNER}/{REPO}"

def clone_repo():
    WORKDIR.parent.mkdir(parents=True, exist_ok=True)
    if WORKDIR.exists(): shutil.rmtree(WORKDIR)
    run(["gh","repo","clone",repo_slug(),str(WORKDIR)])

def prepare_branch():
    run(["git","fetch","--all","--prune"], cwd=WORKDIR)
    run(["git","checkout",BASE_BRANCH], cwd=WORKDIR)
    run(["git","reset","--hard",f"origin/{BASE_BRANCH}"], cwd=WORKDIR)
    branch=f"chore/sync-contract-tools-v1.4.0-{TIMESTAMP}"
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

def write_payloads():
    for rel, b64 in PAYLOADS_B64.items():
        p = WORKDIR / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(base64.b64decode(b64.encode("ascii")))

def commit_push(branch):
    run(["git","add","-A"], cwd=WORKDIR)
    if run(["git","status","--porcelain"], cwd=WORKDIR).stdout.strip()=="":
        raise SystemExit("No changes to commit; repository already up-to-date.")
    run(["git","commit","-m",PR_TITLE], cwd=WORKDIR)
    run(["git","push","-u","origin",branch], cwd=WORKDIR)

def open_pr(branch):
    args=["gh","pr","create","--base",BASE_BRANCH,"--head",branch,"--title",PR_TITLE,"--body",PR_BODY]
    for lab in PR_LABELS: args+=["--label",lab]
    r=run(args, cwd=WORKDIR)
    print(r.stdout.strip())

def main():
    ensure_tools()
    clone_repo()
    branch=prepare_branch()
    ensure_labels()
    write_payloads()
    commit_push(branch)
    open_pr(branch)
    print(f"SUCCESS: Opened sync PR into '{BASE_BRANCH}' for {repo_slug()}")

if __name__=="__main__":
    main()

"""Check exact data locations and hashes; no acquisition or model training."""
import argparse,os,json,hashlib
from pathlib import Path
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--config',type=Path);a=p.parse_args()
if a.config:os.environ['MGAT_CONFIG']=str(a.config.resolve())
from mgat_finrl.paths import DATA_ROOT,ARTIFACT_ROOT,OUTPUT_ROOT,REPO_ROOT
manifest=json.loads((REPO_ROOT/'data/input-manifest.json').read_text())
missing=[];different=[]
for item in manifest:
    f=DATA_ROOT/item['path']
    if not f.is_file():missing.append(item['path']);continue
    if hashlib.sha256(f.read_bytes()).hexdigest()!=item['sha256']:different.append(item['path'])
print(json.dumps(dict(data_root=str(DATA_ROOT),artifact_root=str(ARTIFACT_ROOT),output_root=str(OUTPUT_ROOT),required=len(manifest),missing=missing,hash_mismatch=different),indent=2))
raise SystemExit(bool(missing or different))

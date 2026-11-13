"""Verify archive parts and safely extract saved research artifacts."""
import hashlib,json,tarfile,tempfile,shutil
from pathlib import Path
root=Path(__file__).resolve().parents[1];base=root/'results/archives';dest=root/'results/artifacts'
records=json.loads((base/'manifest.json').read_text());dest.mkdir(parents=True,exist_ok=True)
for record in records:
    with tempfile.TemporaryFile() as joined:
        h=hashlib.sha256()
        for part in record['parts']:
            b=(base/part['name']).read_bytes()
            if hashlib.sha256(b).hexdigest()!=part['sha256']:raise ValueError('Corrupt part: '+part['name'])
            h.update(b);joined.write(b)
        if h.hexdigest()!=record['sha256']:raise ValueError('Archive checksum mismatch')
        joined.seek(0)
        with tarfile.open(fileobj=joined,mode='r:gz') as tar:
            for member in tar:
                target=(dest/member.name).resolve()
                if not target.is_relative_to(dest.resolve()) or not member.isfile():raise ValueError('Unsafe archive member')
                with tar.extractfile(member) as s:
                    data=s.read()
                if target.exists():
                    if hashlib.sha256(target.read_bytes()).digest()!=hashlib.sha256(data).digest():raise ValueError('Existing artifact differs: '+member.name)
                    continue
                target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
    print(record['archive'],record['files'],'files verified')

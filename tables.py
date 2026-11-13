"""Render all saved pooled results into a Markdown table, without recalculation."""
import argparse,csv
from pathlib import Path
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',type=Path,default=Path('work/derived'));a=p.parse_args()
root=Path(__file__).resolve().parents[1];out=a.out.resolve()
if out.is_relative_to(root/'results'):p.error('Use a separate output directory')
out.mkdir(parents=True,exist_ok=True)
with (root/'results/results/rl_pooled.csv').open(encoding='utf-8-sig',newline='') as f:
    reader=csv.reader(f);header=next(reader);rows=list(reader)
text='| '+' | '.join(header)+' |\n| '+' | '.join(['---']*len(header))+' |\n'
text+=''.join('| '+' | '.join(r)+' |\n' for r in rows)
(out/'rl_pooled.md').write_text(text,encoding='utf-8')
print(f'Rendered {len(rows)} saved rows, with every original numeric string preserved.')

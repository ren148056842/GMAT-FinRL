"""Representative F1 result figure, directly from complete saved pooled results.

Contract: compare archived net Sharpe by source and sector without a superiority
claim. Two quantitative panels; points = saved mean, bars = saved SD across
policies (25 primary, 5 PPO ablation). SVG/PDF retain editable text; no new tests.
"""
import argparse
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',type=Path,default=Path('work/derived'));a=p.parse_args()
root=Path(__file__).resolve().parents[1];out=a.out.resolve()
if out.is_relative_to(root/'results'):p.error('Use a separate output directory')
out.mkdir(parents=True,exist_ok=True)
d=pd.read_csv(root/'results/results/rl_pooled.csv');d=d[d.fee=='F1']
plt.rcParams.update({'font.family':'sans-serif','font.size':9,'svg.fonttype':'none','pdf.fonttype':42,'axes.spines.top':False,'axes.spines.right':False})
order=['Naive','Ridge_R','A1_R','MGAT_T','GCN_R','A10_R','MGT_R']
fig,axes=plt.subplots(1,2,figsize=(7.2,3.1),sharey=True,layout='constrained')
for ax,sec,label in zip(axes,['bank','healthcare'],['Banking','Healthcare']):
    z=d[d.sector==sec].set_index('source').loc[order]
    for i,key in enumerate(order):
        ax.errorbar(z.loc[key,'SR_mean'],i,xerr=z.loc[key,'SR_std'],fmt='o',color='#357A96' if key=='MGAT_T' else '#6D747C',capsize=3,markersize=4)
    ax.set_yticks(range(len(order)),['Naive','Ridge','Transformer','MGAT','GCN','No cross-stock','MGNN'])
    ax.set_title(label);ax.set_xlabel('2025 net Sharpe ratio (F1)');ax.axvline(0,color='#D0D0D0',lw=.8);ax.grid(axis='x',alpha=.15)
axes[0].invert_yaxis()
for ext in ['svg','pdf','png']:fig.savefig(out/f'saved_f1_sharpe.{ext}',dpi=200)
d.to_csv(out/'saved_f1_sharpe_source.csv',index=False)
print('Rendered all 14 sector/source F1 points; error bars are saved SD, not confidence intervals.')

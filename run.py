"""Explicit experiment entry points; importing this file never launches training."""
import argparse, os, runpy, sys
from pathlib import Path
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--config',type=Path)
    p.add_argument('stage',choices=['forecast','forecast-b2','rl','analysis','ingest','fetch-tushare','fetch-eastmoney','fetch-statements','ablation','references','sensitivity'])
    p.add_argument('args',nargs=argparse.REMAINDER)
    a=p.parse_args()
    if a.config:os.environ['MGAT_CONFIG']=str(a.config.resolve())
    mapping={'forecast':'fc_run_b3','forecast-b2':'fc_run_b2','rl':'b3_rl','analysis':'b3_analysis','ingest':'b3_ingest','fetch-tushare':'b3_fetch_tushare','fetch-eastmoney':'b3_fetch_em','fetch-statements':'b3_fetch_em_fin','ablation':'b3x_ablation','references':'b3x_refs','sensitivity':'b3x_rl'}
    if not a.args:p.error('Pass the original stage arguments; see docs/reproduction.md')
    sys.argv=[mapping[a.stage]]+a.args
    runpy.run_module('mgat_finrl.'+mapping[a.stage],run_name='__main__')
if __name__=='__main__':main()

"""Validate saved predictions, one inference batch and real-price ledger; no training."""
import argparse,os,json
from pathlib import Path
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--config',type=Path);a=p.parse_args()
if a.config:os.environ['MGAT_CONFIG']=str(a.config.resolve())
import numpy as np,pandas as pd
from mgat_finrl import fc_data as D,fc_models as M,fc_run as V
from mgat_finrl.paths import DATA_ROOT,ARTIFACT_ROOT
from mgat_finrl import b3_rl as R
from mgat_finrl.v2_data import EpisodeData
from mgat_finrl.v3_data import RealPortfolioEnv
from mgat_finrl.backtest import FEES
report={}
for sector in ['bank','healthcare']:
    D.SECTORS[sector]['panel']=str(DATA_ROOT/'data2025/panels'/R.PANELS[sector]);D.FOLDS[2025]=dict(train_end='2023-12-31',val=2024,test=2025)
    panel=D.load_panel(sector);X=D.features(panel);Y,mask=D.targets(panel);split=D.split_indices(panel['dates'],2025)
    sc=D.Scaler(X,Y,mask,split['train']);x=D.windows(sc.x(X),split['test'][:2])
    base=ARTIFACT_ROOT/'revision_b3/forecasts/runs'/sector/'2025/B2_GAT_Transformer_R/seed1'
    model=M.Forecaster(len(panel['tickers']),8,20,panel['graphs'],M.CONFIGS['B2_GAT_Transformer'])
    model(x,training=False);model.load_weights(str(base/'weights.h5'));prediction=sc.y_inv(model(x,training=False).numpy())
    saved=np.load(base/'pred.npz',allow_pickle=False)['test'][:2]
    np.testing.assert_allclose(prediction,saved,rtol=2e-4,atol=2e-5)
    dates=panel['dates'][split['test'][:4]];idx=split['test'][:4];prices=panel['C'][idx]
    ep=EpisodeData(dates,prices,np.zeros((4,len(panel['tickers'])+6,len(panel['tickers'])),np.float32),panel['tickers'],np.ones_like(prices,bool),np.ones_like(prices),np.zeros_like(prices))
    env=RealPortfolioEnv(ep,FEES['F1']);env.reset();_,_,_,_,info=env.step(np.zeros(len(panel['tickers'])))
    assert info['cost']>0 and abs(info['nav']+info['cost']-1e6)<1e-6
    report[sector]=dict(input_shape=list(x.shape),prediction_shape=list(prediction.shape),max_abs_difference=float(np.max(np.abs(prediction-saved))),ledger_nav=float(info['nav']))
assert len(R.all_tasks())==230
report['registered_rl_tasks']=230
print(json.dumps(report,indent=2))

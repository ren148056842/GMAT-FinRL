# Backtesting and statistics

B3 trains policies on 2022–2023, selects 20/40/60/80/100% checkpoints by 2024 F1 net Sharpe (earliest tie), and evaluates 2025. Four primary sources × five algorithms × five seeds × two sectors give 200 policies; three additional sources × PPO × five seeds × two sectors give 30 ablation policies. Forecast seeds 1–3 are averaged.

The original `configs/protocol_v4.json` supplies algorithm parameters and budgets only. Its older dates and state description remain historical evidence; B3's executable `SPLITS`, `SEEDS`, `SOURCES`, checkpoint logic and protocol override them. No historical protocol was rewritten.

Decisions at t close execute at t+1 observed unadjusted close. Accounting starts with 1,000,000 in cash, long-only weights and fractional units. There is no terminal liquidation. Commission and slippage are cash debits, stamp duty applies on sales. F1 is 3 bp commission + 2 bp slippage, with historical duty 10 bp before 2023-08-28 and 5 bp thereafter. F0–F6 are defined in `backtest.FEES` and all saved settings remain available.

The episode adapter supplies all-true tradability, unit corporate-action multipliers and zero dividends. It does not fully model price limits, board lots, A-share T+1 settlement constraints, suspension execution restrictions or dividend/split total-return accounting. Returns therefore measure this unadjusted-price research ledger, not verified deployable investor total returns.

AR is geometrically annualized with 252 days; SR is mean daily return divided by sample standard deviation times sqrt(252), with zero risk-free rate in the primary analysis. MDD uses the cumulative net-return curve; Calmar is AR/MDD. Complete per-run metrics include turnover and costs. H1/H2 use paired circular block resampling of daily returns, block 10 with 5/20 checks, 2,000 resamples, centered one-sided p-values and Holm correction as registered. H3 uses daily forecast rank IC. Post-evaluation addenda are descriptive and remain identified as such.

# Data and access

The required ten panel/matrix files, original relative paths, sizes and SHA-256 hashes are listed in `data/input-manifest.json`. Set `data_root` to a directory with those relative paths. Do not sort the input panel: the per-date ticker row order defines the graph node order. Banking `PAD` and `PAB` denote the same stock; the historical filenames remain unchanged.

Original panels contain `date,tic,high,low,close,volume,TTM,PBR,PS,PCF` (plus any archived extra fields). `volume` means daily **trading value in CNY**, not share volume. Forecast features are log return, high/close, low/close, relative trading value, and four inverse valuation ratios. Windows have shape `[batch,20,stocks,8]`; forecasts have `[batch,stocks,6]`. Suspensions and prelisting target masks follow `fc_data.py`.

## Obtaining the inputs

Tushare Pro supplies daily price/value data; Wind/terminal exports supply historical panels and auxiliary tables; Eastmoney supplies valuation ratios and annual-statement items for the 2025 extension. Obtain access directly under each provider's terms. Research access does not establish redistribution permission. This repository does not redistribute raw provider exports or frozen relation matrices without documented rights.

To request the exact historical panel and graph snapshot where provider terms permit, contact the corresponding author at zchen@mail.xjtu.edu.cn and quote the input manifest hashes. **Access to an exact snapshot is not guaranteed by this repository.** A newly downloaded dataset may differ from the historical snapshot. The original graph source notebooks are retained as sanitized provenance in `docs/provenance/graph_notebooks`; they document construction and require explicit local input paths.

The real download/ingestion entries are:

```bash
python scripts/run.py --config configs/local.json fetch-tushare /path/outside/repository/token.txt work/raw daily
python scripts/run.py --config configs/local.json fetch-eastmoney work/raw
python scripts/run.py --config configs/local.json fetch-statements work/raw
python scripts/run.py --config configs/local.json ingest /path/to/data-root work/raw work/panels
```

Read each stage's source argument contract before downloading. Tokens stay outside the repository. These commands reconstruct the 2025 extension from authorized inputs; they do not recover missing 2018–2024 terminal snapshots automatically.

## Historical availability

The shareholder graphs are single snapshots published in 2023 (healthcare as of 2022-12-31; banking at the June 2023 export). The Kendall graph uses 2018-01-02 through 2022-12-30. Earlier folds therefore use static graph information unavailable at some historical decisions. The original banking shareholder mapping covers 13 of 15 banks and mislabels one bank; CMB, PSBC and CZB are isolated in that relation. These frozen inputs were not repaired in this migration.

The 2025 ingestion selected ratio candidates by 2024 agreement. Some PCF/PS denominators are fiscal-year y−1 annual statement items, not a fully point-in-time announcement-date join. The protocol amendments and saved ingestion checks document the actual selection. This limits claims of historically available signals. Price adjustment, corporate actions and trading constraints are discussed in [backtesting.md](backtesting.md).

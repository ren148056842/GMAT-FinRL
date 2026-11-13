# Reproduction workflow

1. Install the package and dependencies as in README.
2. Obtain the ten licensed inputs and set a local path config. Run `scripts/validate_data.py`.
3. Extract saved artifacts with `python scripts/unpack_artifacts.py` when the archive parts are present. The default read root is `results/artifacts`; this directory is ignored by Git. Archived records remain read-only inputs; new runs go to `work/runs`.
4. Run `python -m pytest tests -q`, the saved-table renderer and representative figure script. Run `python scripts/smoke.py --config configs/local.json` for a small real-data interface/ledger check. It does not train a model.

## Explicit training entries

These are compute-intensive and were **not** executed during migration. The original argument parsing and training loops are preserved. Run help first:

```bash
python scripts/run.py forecast --help
python scripts/run.py forecast-b2 --help
python scripts/run.py rl --help
```

The original B2 runner supplies 2022/2023 forecast folds. B3 supplies the 2024/2025 folds and its two-target Ridge. Example B3 invocations:

```bash
python scripts/run.py --config configs/local.json forecast train --folds 2024 --sectors bank,healthcare --threads 4
python scripts/run.py --config configs/local.json forecast train --folds 2025 --sectors bank,healthcare --threads 4 --panel-dir /path/to/data-root/data2025/panels
python scripts/run.py --config configs/local.json forecast ridge --folds 2022,2023,2024,2025 --panel-dir /path/to/data-root/data2025/panels
python scripts/run.py --config configs/local.json rl prepare
python scripts/run.py --config configs/local.json rl worker --id 1
python scripts/run.py --config configs/local.json rl evaluate --panel-dir /path/to/data-root/data2025/panels
```

When using newly generated forecasts, set `artifact_root` to the directory containing the completed `revision_b2/forecasts` and `revision_b3/forecasts`. It must remain separate from `output_root`. Stage completed runs into a new immutable artifact directory before downstream use; do not point an output directory at the archived results. For resuming training/evaluation, keep the same output root containing its saved checkpoints.

## Saved-output analysis

```bash
python scripts/run.py --config configs/local.json analysis /path/to/data-root/data2025/panels work/reanalysis
python scripts/tables.py --out work/derived
python scripts/figures.py --out work/derived
```

The full analysis redoes registered statistics on saved trajectories; the minimal migration checks compare only representative metrics/tables and interfaces. Stage `ablation` exposes `b3x_ablation.py`; `references` exposes `b3x_refs.py`; `sensitivity` exposes `b3x_rl.py`. Their training commands are optional explicit reruns, not part of quick start. The original protocols identify which experiments were registered and which were later descriptive additions.

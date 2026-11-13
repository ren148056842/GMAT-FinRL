# Artifact coverage

The result CSVs under `results/results` and `results/results_x` preserve the full registered and descriptive tables, including all model identifiers, seeds, baselines and outcomes. Forecast artifacts include B2 folds 2022/2023, B3 folds 2024/2025, B3 ridge folds and addendum variants, with saved predictions, weights and run metadata. B2's additional saved folds are retained as historical evidence.

The archive manifest at `results/archives/manifest.json` records every multipart archive checksum. Run `python scripts/unpack_artifacts.py` to reconstruct `results/artifacts`. Splitting archives keeps each individual Git file small; the script verifies parts before extraction and refuses to replace a differing existing artifact.

RL archives preserve all saved metrics, daily NAV/return trajectories, validation scores and completion records for the registered runs and sensitivity runs. Intermediate policy binaries and duplicate checkpoints are retained in the local research backup. They are not required for saved-result analysis. Newly evaluating saved policies requires those binaries; this distribution alone supports retraining and saved-trajectory analysis, not complete checkpoint replay.

Detailed position/trade files contain provider-price fields. They are retained in the local backup and are not redistributed pending data-rights confirmation. The ten raw panel/matrix inputs are separately licensed as explained in `data.md`. Exact historical data access and omitted policy binaries remain external requirements; do not describe a fresh clone alone as a complete full-experiment reproduction.

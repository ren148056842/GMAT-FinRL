# Installation and environments

The validation environment in `requirements/validation.txt` uses Python 3.11, TensorFlow 2.15.1 (Keras 2), PyTorch 2.5.1, SB3 2.4.0, Gymnasium 1.0.0, NumPy 1.26.4 and pandas 2.2.3. This is a compatibility environment; it is not a claim of bitwise retraining equivalence.

Historical B3 metadata record Python 3.8.16, TensorFlow 2.11.1 for forecasting and PyTorch 2.0.1, SB3 2.4.0, Gymnasium 1.0.0, NumPy 1.23.1, pandas 1.4.3 and stockstats 0.4.1 for RL. See `provenance/pip_freeze.txt` and the sanitized `provenance/environment.json`; executable paths and captured local import paths were omitted from the public copy. Exact originals are retained in the migration backup.

Install from the repository root with the commands in README. Core import: `python -c "import mgat_finrl; print(mgat_finrl.__version__)"`. Numerical kernels and device differences can affect newly trained models. Existing artifacts retain their original bytes.

`configs/b3-resolved.json` is an inspectable snapshot of the settings actually
resolved from B3/B2 code and the historical parameter file. It records time
splits, model/agent seeds, budgets, algorithm parameters and fee definitions.
It is a provenance snapshot, not a second set of independently applied defaults.

Historical policy pickle schedules may not deserialize across Python versions.
The validation environment supports the tested deterministic policy prediction
path, with recorded small floating-point differences; it is not verified for
resuming historical training. Use the recorded historical environment for that
purpose. On the migration host, Windows application control blocked the official
TensorFlow binary; this is documented in `validation.md` rather than treated as
a passed forward-inference check.

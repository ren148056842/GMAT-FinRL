# Migration validation

Validation uses the author's saved local inputs and outputs. No full forecast
training, RL training, parameter search or new experiment is part of this check.

Completed checks:

- Editable package installation into an isolated Python 3.11 environment.
- Imports of the data loader, forecast runners, B2/B3 runners and trading modules.
- Original ledger test suite: **16 passed**.
- All ten required local input files found with matching SHA-256 fingerprints.
- 48 saved forecast interfaces (two sectors × six forecast sources × four folds):
  dates, ticker counts, `(n,15,6)` outputs and required finite channels checked.
- Both sectors' B3 states built from real inputs, with shape `(21,15)` and the
  intended 2022–2023 / 2024 / 2025 split; first delayed-close rebalance cash/cost
  conservation checked.
- Two saved MGAT/PPO/seed-1 F1 trajectories: AR, SR and MDD agree with archived
  metrics within absolute tolerance `1e-12`.
- 23 result files and both original protocols remain byte-identical to their
  local sources; the remotely listed result tables also match source Git blobs.
- 98 pooled-result rows rendered without changing numeric strings; all 14 F1
  sector/source means and saved SDs plotted using the pre-existing Python 3.13
  plotting environment, with SVG/PDF/PNG visually checked.
- Five multipart artifact archives: 6,246 files verified against local originals.
- Python compilation, relative import closure and Markdown relative links checked.

Two existing PPO checkpoints were also loaded for three evaluation steps per
sector. NAV differed from the historical saved trajectory by at most
`0.000433` currency units on the one-million-unit ledger (below the explicit
one-cent smoke threshold). This is numerical agreement, not byte-identical
checkpoint replay. Loading the Python-3.8-era checkpoint under Python 3.11
emitted schedule-deserialization warnings; schedules were not replaced and no
training was attempted.

PyTorch/SB3 imports for all five algorithms and `pip check` passed. TensorFlow
2.15.1 installed, but Windows application control blocked its `_pywrap_tf2`
binary. Therefore the actual TensorFlow forward-pass check did **not** run.
Saved-output shape checks are not substituted for a successful model inference.
The small-inference command is retained for an environment that permits this
official package to execute; no system protection was changed.
In a fresh **local** Git checkout, the package installed, the 16 ledger tests
passed, all 6,246 archive members extracted and the table regenerated. In the
new Python 3.11 environment, SVG export succeeded but PDF export was blocked by
application control for `fontTools.misc.bezierTools`; the original generated
figure bundle remains from the pre-existing plotting environment. This was a
local checkout test, not a remote publication verification.
These checks do not establish full retraining reproducibility. Provider snapshot
access, saved policy binaries and the historical environment remain requirements
for their respective reproduction paths; see `artifacts.md` and `data.md`.

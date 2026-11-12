# MGAT-FinRL

## 1. Project overview

Research code for **MGAT-FinRL: A Multi-relational Graph Attention Transformer-Based Reinforcement Learning Investment Strategy**, by Zhiping Chen and Xiaoping Ren.

MGAT forecasts stock prices from market features and three company-relation graphs. These forecasts enter the state of reinforcement learning portfolio policies. Forecasting and policy learning are separate training stages. This companion repository contains the implementation, frozen protocols, complete saved result tables and reproducibility tools.

## 2. Architecture

1. Build three static relations: common top-ten shareholders, company co-mentions in investor Q&A, and Kendall correlation of daily trading value.
2. Encode eight features per stock with three graph-attention layers (16, 32, 64 units). Attention is restricted to the union of positive relation edges plus self-loops. Concatenate the final graph representation with the original features.
3. Apply a Transformer to each stock's 20-day window. Predict high, low and close at **t+1 and t+2** (six log-ratio targets), using masked prediction error plus a ranking objective.
4. Add forecast return and range signals to the observed-price policy state throughout training, selection and evaluation. Train PPO, A2C, SAC, TD3 and DDPG on **2022–2023**, select checkpoints on **2024**, and evaluate on **2025**.
5. Execute at the next trading day's close and account using observed prices. Forecast seeds are 1–3; policy seeds are 1–5.

See [method and model identifiers](docs/method.md), [data](docs/data.md), and [backtesting](docs/backtesting.md) for exact definitions and interpretation.

## 3. Repository structure

| Path | Contents |
| --- | --- |
| `src/mgat_finrl/` | Forecast models and data processing, experiment runners, trading environment and ledger |
| `configs/` | Portable path settings and unchanged historical RL parameter source |
| `requirements/` | Validation environment dependencies |
| `scripts/` | Data checks, experiment dispatch, tables and figures |
| `tests/` | Existing ledger tests |
| `docs/` | Installation, reproduction, protocols, naming and source manifest |
| `data/` | Required input filenames and SHA-256 fingerprints |
| `results/` | Complete immutable result tables and archived experiment artifacts |
| `figures/` | Representative figure generated from the saved result table |

## 4. Installation

Use Python 3.11 for the compatibility environment:

```bash
python -m venv .venv
# Activate .venv using your platform's activation script.
python -m pip install -r requirements/validation.txt
python -m pip install -e .
```

The historical experiments used separate TensorFlow and RL environments. Their recorded versions and the scope of compatibility checks are described in [installation](docs/installation.md). The original permission requirements are preserved in [LICENSE](LICENSE).

## 5. Data preparation

Obtain the licensed inputs listed in [data/input-manifest.json](data/input-manifest.json), following [data instructions](docs/data.md). Copy `configs/default.json` to `configs/local.json`, then set `data_root` to the directory containing the original sector folders and `data2025/panels`.

```bash
python scripts/validate_data.py --config configs/local.json
```

The validator reports missing files and fingerprint differences explicitly. Provider data are not bundled for redistribution.

## 6. Quick start

These commands operate on saved tables and tests; they do not train models:

```bash
python -m pytest tests -q
python scripts/tables.py --out work/derived
python scripts/figures.py --out work/derived
python scripts/run.py --help
```

## 7. Reproducing the paper

Follow [reproduction](docs/reproduction.md) for artifact extraction, forecast interfaces, staged training and analysis. Start with saved artifacts and the minimal validation commands. Full training requires the licensed inputs and is explicitly launched by the user.

The original [B3 protocol](docs/protocols/PROTOCOL_B3.md), including dated amendments and descriptive addenda, and the [B2 protocol](docs/protocols/PROTOCOL_B2.md) are preserved verbatim. Historical identifiers remain unchanged in saved outputs.

## 8. Results and available artifacts

The [registered result tables](results/results/) include every reported source, algorithm, seed and cost setting. The [additional analyses](results/results_x/) contain relation/depth ablations, attention summaries, allocation references, volatility regimes and policy sensitivity. [Artifact coverage](docs/artifacts.md) explains which saved files are present and which inputs require separate access.

Results describe the archived experimental setup. Read [backtesting assumptions](docs/backtesting.md) when interpreting portfolio returns and statistical comparisons.

## 9. Citation and contact

Use [CITATION.cff](CITATION.cff) for the software title, authors and repository URL. Contact: Zhiping Chen, [zchen@mail.xjtu.edu.cn](mailto:zchen@mail.xjtu.edu.cn). Repository version: `v1.0.0` (verify tag availability before citing a release).

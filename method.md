# Method and identifier mapping

| Saved identifier | Meaning in this project |
| --- | --- |
| `MGAT_T`, `B2_GAT_Transformer_R`, MGAT-T | MGAT, the graph-attention Transformer with ranking-aware loss |
| `B2_GAT_Transformer` | Architecture identifier before the `_R` objective suffix |
| `A1_R`, `A1_Transformer_only_R` | Transformer without graph propagation |
| `GCN_R`, `B1_GCN_Transformer_R` | Fixed GCN plus Transformer |
| `A10_R`, `A10_No_cross_stock_R` | Graph-branch capacity with independent stocks |
| `MGT_R`, `A0_Full_MGT_R` | Historical MGNN-Transformer comparator; not MGAT |
| `Ridge_R` | Ridge baseline; B3 fits return and range separately |
| `Naive` | Zero forecast return and observed log high/low range in the policy state |

`fc_models.py` implements distinct MGNN, GCN and GAT branches. GAT uses a binary admissibility mask derived from positive relation edges plus the diagonal. Relation magnitudes determine admissibility after positive fusion; they are not separate relation-specific attention heads. Each layer has a single attention head, LeakyReLU slope 0.2 and ELU output. Only the **final 64-dimensional** graph output is concatenated with eight input features, yielding width 72; intermediate 16/32-dimensional outputs are not separately concatenated.

The temporal encoder uses one block, four heads, feed-forward width 128, dropout 0.1 and learned positional embeddings. It runs along each stock's window, not across stocks. The six targets are `h1,l1,c1,h2,l2,c2`, each expressed as log(price at t+k / close at t). No open-price target is trained. B2 supplies masked MSE plus the ranking term, lambda 1; B3 reuses that training code.

The forecast return signal is predicted `c2-c1`; the range signal is predicted `h1-l1`. The former is standardized cross-sectionally each day and the latter using 2022–2023 training statistics. Observed covariance and technical indicators remain in the state. Forecasts and policies are trained in separate stages. The historical v4 training-only price substitution is not the B3 design.

The fold-2025 forecast model trains through 2023 with 2024 validation. Thus the early prose in B3's data-use table ('2018–2021 forecaster training only') is incomplete for later walk-forward folds; the fold table and executable split definitions govern. The graph timing limitations are detailed in [data.md](data.md).

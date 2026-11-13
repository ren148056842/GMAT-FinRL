# Source and migration record

Source repository: `ren148056842/MGT-FinRL`; selected branch: `revision-b3`;
verified remote head: `bd77fdf520e4f0619222c8d7c9cd6d6008126f3d`.
The observed source head agrees with the previously supplied SHA. PRs 1/2 and
`revision-v3.0` are historical materials; they do not select the MGAT implementation.

The migration preserves the dependencies from B3 to B2 forecasting, the v4
forecaster and the backtest modules. Modules were moved into `mgat_finrl` with
relative imports, configurable filesystem roots and protected output locations.
The numerical model, loss, seeds, row ordering, splits, costs and statistics were
not redesigned. Historical identifiers in data/result keys were retained.

`migration-manifest.csv` records source branch/commit (where independently
verified against a remote Git blob), old/new relative paths and SHA-256 hashes.
`local-supplement` identifies files recovered from the author's local research
directory, such as forecast ensembles absent from the Git B3 folder. No remote
commit attribution is invented for those files. Saved result tables match the
remote B3 files and the local originals byte for byte.

The original B2/B3 protocols are byte-identical. The historical v4 parameter
JSON is unchanged. Graph notebooks retain their code as historical provenance,
with outputs cleared and personal file paths replaced by explicit placeholders;
they are not presented as portable production entry points. Environment
provenance was sanitized to remove machine-specific executable paths. Full
original copies are retained in the local backup.

No manuscript, response letter, submission package or review correspondence is
included. New public data redistribution is limited to derived artifacts and
input fingerprints; provider exports remain external. The old repository must
remain available until the full Git backup and all publication checks succeed.

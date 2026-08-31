# Audit evidence model

The run bundle answers two separate questions:

1. **What assumptions and calculations produced the reported result?**
2. **Has the recorded bundle changed since generation?**

It does not answer whether the original assumptions were true.

## Evidence layers

- `scenario_snapshot.json` fixes the supplied assumptions.
- JSON and CSV outputs expose the calculation bridge.
- `audit.sqlite` supports independent queries.
- `events.jsonl` records ordered processing milestones in a hash chain.
- `artifact_manifest.json` declares each generated artifact and digest.
- `run_manifest.json` binds the scenario digest, artifact manifest and final event hash.

## Verification semantics

`gpes verify` returns valid only when the declared files, content digests, SQLite semantic digest, event chain and final run identity agree. A valid run can still contain a commercially bad or negative result; integrity is not profitability.

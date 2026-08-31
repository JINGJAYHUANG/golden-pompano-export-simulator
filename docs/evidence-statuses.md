# Evidence status vocabulary

Use a small, explicit vocabulary in private assumption registers:

| Status | Meaning |
|---|---|
| `verified-current` | Direct evidence is current for the stated route, quantity and date |
| `verified-historical` | Direct evidence existed for a past case but may not be current |
| `quoted-unconfirmed` | Written quotation exists but scope or acceptance is unresolved |
| `estimated` | Documented estimate with named owner and rationale |
| `stress-only` | Deliberately conservative scenario value, not a forecast |
| `expired` | Source validity has ended |
| `conflicted` | Comparable sources disagree materially |
| `missing` | No usable evidence is available |

The simulator does not automatically upgrade these statuses. Commercial review should prioritize assumptions that are both decision-sensitive and weakly evidenced.

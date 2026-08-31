# Operator runbook

## Prepare

1. Copy the packaged starter into a private workspace.
2. Replace every synthetic value with a traceable assumption.
3. Record `as_of`, validity windows, currency and unit bases.
4. Replace the illustrative cost allocation with the proposed contract allocation.
5. Keep credentials and source documents outside the scenario JSON.

## Validate

```bash
gpes validate private-scenario.json
```

Resolve all errors. Review every warning; warnings are not automatic approvals.

## Simulate

```bash
gpes simulate private-scenario.json \
  --output-dir private-runs/run-001 \
  --fixed-time 2026-08-31T00:00:00Z
```

Use a new, empty directory for each run.

## Review

1. Reconcile mass and integer packaging.
2. Review cost payer and cash day for each line.
3. Reconcile seller and buyer bridges.
4. Review peak funding, quote targets and sensitivity.
5. Complete contract, customs, tax, quality and payment checks outside the model.

## Verify and approve

```bash
gpes verify private-runs/run-001
```

Record the run-manifest digest in the human decision log. The CLI does not send the quote or approve the transaction.

# Reconciliation controls

A valid run should satisfy these identities:

```text
net fish + ice = glazed product
glazed product + packaging tare = packaged gross
seller receipts and credits - seller cash costs - financing - profit share = seller ending economics
buyer invoice + buyer costs + tax cash = landed cash cost
landed cash cost - recoverable tax - buyer credits = landed economic cost
```

The simulator records a zero `mass_check_kg` when the physical bridge closes. Reviewers should also reconcile aggregate seller and buyer amounts to the detailed cost and tax files.

A successful `gpes verify` confirms that the recorded files still match their manifests. It does not confirm that the original values were commercially correct.

# Source-of-truth hierarchy

For a real private scenario, use this hierarchy:

1. signed contract and official determinations;
2. dated written quotations and carrier/broker confirmations;
3. measured production, packing and shipment records;
4. versioned internal cost evidence;
5. documented estimates;
6. placeholders used only for sensitivity.

The scenario JSON is the calculation source of truth for a run, but it is not automatically the commercial truth. Each material value should trace back to evidence outside the public repository.

The generated `scenario_snapshot.json` is immutable evidence of what the model used. Editing the original scenario later does not update an existing run; generate a new run with a new identity.

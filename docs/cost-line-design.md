# Cost-line design

Each cost line should represent one economically distinct obligation and declare:

```text
id
label
stage
payer or auto-allocation
basis
rate
currency
cash day relative to shipment
```

Do not hide several unrelated costs inside an unexplained “miscellaneous” percentage when the components have different owners, timing or sensitivity.

Use `percent_invoice` only when the contract genuinely defines a charge against invoice value. Use `percent_customs_value` only when the scenario explicitly defines customs value. Fixed charges, carton charges and physical-weight charges should retain their own bases.

A cost line may be small but decision-critical when it changes the payer, cash timing, tax base or break-even equation.

# Frequently asked questions

## Why does 10% glaze turn 18,000 kg net fish into 20,000 kg product?

Because the scenario defines glaze as ice divided by the final glazed-product mass. If fish is 90% of product, product mass is `18,000 / 0.90 = 20,000 kg`.

## Why not define glaze as 10% of fish mass?

Both conventions can appear in informal discussion. Mixing them causes errors. v0.1.0 deliberately accepts one explicit convention only: `ice / glazed product mass`. Convert other conventions before input and document the conversion.

## Why are cartons rounded up?

A fractional carton cannot normally be shipped. The simulator rounds to the next whole carton and reports resulting net-fish overfill.

## Is the CIF template legally correct for every contract?

No. It is an illustrative cost-allocation starting point. The signed contract, named place, edition and route-specific arrangements must replace the template.

## Why can landed cash cost be higher than landed economic cost?

Because a tax may be paid at import and recovered later. The cash view shows the initial outflow; the economic view subtracts the assumed recoverable portion.

## Does break-even tell me what price to quote?

No. It tells you the unit price at which this specific assumption set produces zero modelled seller profit after financing and profit share. Commercial risk, quality, credit, legal duties and uncertainty still require judgment.

## Can I upload real buyer and cost data to GitHub?

Do not commit it to this public repository. Keep private inputs in a controlled location, exclude them from version control and share only sanitized, synthetic reproductions when reporting a bug.

## Does the package call the internet?

No. v0.1.0 performs no network request. Current values must be supplied and independently verified by the operator.

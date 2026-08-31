# Independent reviewer guide

A reviewer should not begin with the headline profit. Review in the following order.

## 1. Identity and scope

Confirm the scenario ID, `as_of` date, data classification, product form, named place, quote currency and declared price basis.

## 2. Physical reconciliation

Recalculate one carton manually:

```text
declared product mass
× (1 - glaze fraction)
= net fish per carton
```

Then reconcile cartons, pallets, fish, ice, tare and packaged gross mass. A non-zero `mass_check_kg` is a blocker.

## 3. Commercial responsibility

Read every `payer_resolved` value in `cost_lines.csv`. Do not assume the Incoterms label alone answers who pays a local charge.

## 4. Cash versus economics

Trace the seller timeline chronologically and identify the peak negative balance. Separately reconcile buyer landed cash with recoverable tax and credits.

## 5. Quote targets

Challenge the assumptions before using break-even or target-margin prices. Verify percentage-of-invoice costs, profit share and financing, because they make the quote equation recursive.

## 6. Sensitivity

Identify the assumptions that can reverse seller profitability, create an unfinanceable cash deficit or materially change buyer landed cost. Request evidence for those assumptions first.

## 7. Evidence integrity

Run:

```bash
gpes verify <run-directory>
```

A valid bundle proves internal consistency after generation, not truth of the original assumptions.

## 8. Boundary statement

The reviewer should record what remains unverified: tariff classification, tax recovery, contract enforceability, quality compliance, freight validity, payment security, buyer credit and operational execution.

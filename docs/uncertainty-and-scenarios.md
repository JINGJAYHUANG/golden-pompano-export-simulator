# Uncertainty and scenario design

The simulator is deterministic: one assumption set produces one result. Uncertainty therefore has to be represented by explicit alternative scenarios rather than hidden behind false precision.

## Recommended scenario set

| Scenario | Purpose |
|---|---|
| `contract-base` | Best current written evidence for the proposed transaction |
| `seller-downside` | Higher raw-fish, processing, finance and rejection cost |
| `logistics-stress` | Higher freight, terminal charges and longer transit/payment timing |
| `buyer-cash-stress` | Higher duty/tax cash requirement and slower tax recovery |
| `fx-stress` | Adverse currency conversion while preserving all physical assumptions |
| `quality-variance` | Different glaze, carton yield or specification mix |
| `combined-severe` | Plausible joint downside without claiming a statistical probability |

## Do not double count

A stress scenario should avoid charging the same economic shock twice. For example, if a freight quotation already includes a fuel surcharge, do not separately add the same surcharge again unless the second line represents a distinct exposure.

## Correlated assumptions

Some variables move together:

- higher raw-fish scarcity may also change size-grade availability;
- delayed shipment may increase storage, financing and document-expiry risk;
- a stronger quote currency can change both revenue and buyer affordability;
- a more protective payment term can reduce seller financing but raise buyer resistance.

One-way sensitivity isolates mechanics. It should not be interpreted as a complete joint forecast.

## Decision rule

A scenario can support a quote only when:

1. all material assumptions have evidence owners and validity dates;
2. the seller can fund the peak cash deficit;
3. the downside set does not create an unacknowledged loss or contract breach;
4. buyer landed cost is compared on the same mass and currency basis as alternatives;
5. legal, customs, tax, quality and payment reviews are completed outside the model.

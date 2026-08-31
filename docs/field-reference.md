# Scenario field reference

## Top-level fields

| Field | Meaning |
|---|---|
| `schema_version` | Input contract version; v0.1.0 accepts `1.0` |
| `scenario_id` | Stable, non-personal scenario identifier |
| `as_of` | Date to which commercial assumptions apply |
| `data_classification` | `synthetic`, `private` or `licensed` |
| `currencies` | Model currency and explicit conversion factors |
| `product` | Mass, packaging, payload and size-grade assumptions |
| `quote` | Currency, price basis, unit price and payment timing |
| `contract_profile` | Illustrative cost allocation plus overrides |
| `customs_value` | Explicit customs-value calculation assumption |
| `costs` | Operating and trade cost lines |
| `taxes` | Cash tax and recoverability assumptions |
| `credits` | Conditional seller or buyer credits |
| `finance` | Seller working-capital financing rate |
| `profit_share` | Conditional share of positive seller profit |
| `targets` | Target seller margin used by the quote solver |
| `analysis` | One-way and two-way sensitivity specification |

## Cost bases

- `per_net_fish_kg`
- `per_glazed_product_kg`
- `per_packaged_gross_kg`
- `per_carton`
- `per_container`
- `per_shipment`
- `percent_invoice`
- `percent_customs_value`

Every cost line also declares stage, payer, currency and cash day relative to shipment.

## Tax bases

- `customs_value`
- `customs_plus_prior_taxes`
- `invoice`
- `fixed`

Taxes must declare the payer and recoverable fraction. The simulator does not infer eligibility or recovery timing from a jurisdiction.

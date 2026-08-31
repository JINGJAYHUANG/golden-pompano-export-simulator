# Assumption register protocol

Every real scenario should maintain an assumption register outside the public repository. Each assumption should record:

| Field | Purpose |
|---|---|
| `assumption_id` | Stable identity across revisions |
| `field_path` | Exact scenario field affected |
| `value` and `unit` | Unambiguous quantity |
| `price_or_mass_basis` | Required for every per-unit value |
| `currency` and `fx_date` | Conversion provenance |
| `source` | Quote, contract, official record or measured evidence |
| `checked_at` | Freshness reference |
| `valid_until` | Quote or rule expiry |
| `confidence` | High, medium or low with rationale |
| `owner` | Person responsible for revalidation |
| `downside_case` | Conservative alternative used in sensitivity |
| `supersedes` | Prior assumption replaced by this record |

## Evidence order

For a real transaction, prefer:

```text
signed contract or official determination
> written supplier/carrier/broker quotation
> measured production or shipment record
> dated internal operating evidence
> informed estimate
> unsupported placeholder
```

A later estimate does not automatically outrank an older signed or measured record. Compare scope, route, quantity, validity period, currency, tax basis and included services before replacing an assumption.

## Expiry policy

Inputs with an expired `valid_until` should not silently remain in a live quotation. The operator should either obtain a replacement, switch the scenario to an explicitly stressed estimate or stop publication of the quote.

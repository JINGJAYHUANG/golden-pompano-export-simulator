# SQLite query examples

## Read headline economics

```sql
SELECT key, value
FROM metadata
ORDER BY key;
```

## Inspect mass reconciliation

```sql
SELECT key, value
FROM mass_balance
WHERE key IN (
  'shipped_net_fish_kg',
  'ice_mass_kg',
  'glazed_product_kg',
  'packaging_mass_kg',
  'packaged_gross_kg',
  'mass_check_kg'
)
ORDER BY key;
```

## Review all cost lines

```sql
SELECT position, json_extract(payload, '$.id') AS cost_id,
       json_extract(payload, '$.payer_resolved') AS payer,
       json_extract(payload, '$.basis') AS basis,
       json_extract(payload, '$.amount_model') AS amount_model
FROM cost_lines
ORDER BY position;
```

## Find the largest seller cash deficits

```sql
SELECT position,
       json_extract(payload, '$.day') AS day,
       json_extract(payload, '$.event') AS event,
       CAST(json_extract(payload, '$.running_cash_balance_model') AS REAL) AS running_balance
FROM cash_timeline
ORDER BY running_balance ASC
LIMIT 10;
```

## Inspect sensitivity rows

```sql
SELECT position,
       json_extract(payload, '$.path') AS input_path,
       json_extract(payload, '$.delta_fraction') AS delta_fraction,
       json_extract(payload, '$.seller_profit_model') AS seller_profit
FROM sensitivity
ORDER BY input_path, CAST(delta_fraction AS REAL);
```

SQLite JSON functions depend on the SQLite build. The canonical CSV and JSON outputs remain available when JSON extraction extensions are unavailable.

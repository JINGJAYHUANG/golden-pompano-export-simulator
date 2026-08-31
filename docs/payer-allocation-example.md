# Payer-allocation example

A `CIF` label in the synthetic fixture initializes a cost-responsibility map. Each cost line with `payer: auto` is then assigned by stage. A contract override can replace one stage without changing unrelated stages:

```json
{
  "incoterm_label": "CIF",
  "cost_responsibility_overrides": {
    "main_carriage": "buyer",
    "destination_terminal": "seller"
  }
}
```

This means only that the model charges those declared lines to the selected party. It does not assert that the arrangement is legally standard, that risk transfers at the same point or that all local charges have been identified.

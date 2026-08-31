# Validation philosophy

Validation is designed to fail early on ambiguity that can materially change economics.

Examples of blocking ambiguity include:

- missing price denominator;
- non-finite or negative rates;
- glaze outside the supported convention;
- size-grade shares that do not sum to one;
- missing model-currency conversion;
- unknown cost basis or responsibility stage;
- invalid tax payer or recoverability range;
- an auto-allocated cost whose stage is absent from the profile;
- a carton count that cannot satisfy target net-fish mass;
- a generation timestamp without timezone.

Warnings preserve assumptions that can be calculated but require human confirmation, such as a high glaze fraction or any illustrative Incoterms allocation.

# Rounding policy

- Input values are parsed as decimal strings.
- Physical mass is retained to four decimal places in the mass engine.
- Cash-line amounts are rounded to two decimal places using half-up rounding.
- Quote solving retains additional precision and rounds only for display or invoice-line calculation.
- Cartons, pallets and containers are rounded upward because they are indivisible planning units.
- Size-grade fish counts are rounded upward estimates based on band midpoints.

Rounding policy is part of the model contract. It must not be changed to improve a displayed margin without versioning and regression evidence.

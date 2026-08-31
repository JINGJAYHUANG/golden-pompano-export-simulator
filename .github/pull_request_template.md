## Purpose

Describe the decision problem and why the change belongs in this repository.

## Model changes

- [ ] Mass or packaging basis changed
- [ ] Quote or cost basis changed
- [ ] Responsibility profile changed
- [ ] Tax, credit or cash-timing logic changed
- [ ] Seller or buyer economics changed
- [ ] Sensitivity or quote solver changed
- [ ] Report or evidence bundle changed

## Required evidence

- [ ] All committed examples remain synthetic
- [ ] No real counterparty, price, cost, margin, contract or credential is included
- [ ] Units, currencies, dates, denominators and assumptions are explicit
- [ ] New failure modes have tests
- [ ] `python scripts/verify_test_count.py` passes
- [ ] `python -m unittest discover -s tests -v` passes
- [ ] Both deterministic scenarios regenerate exactly
- [ ] Run bundles verify after transfer
- [ ] Nine tamper attacks are detected
- [ ] Public and Markdown-link audits pass

## Boundary statement

Explain what the change does **not** prove. A calculation must never be presented as legal, customs, tax, product-quality or profit certainty.

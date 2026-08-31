# Data freshness policy

Every non-synthetic production scenario should state `as_of`, source timestamps and validity windows. The following inputs commonly expire at different speeds:

- buyer demand and product specification;
- farm-gate or procurement cost;
- processing and packaging quotations;
- freight, surcharges and terminal charges;
- foreign-exchange rate;
- duty, tax and recoverability interpretation;
- payment and financing terms;
- container payload and route constraints.

The simulator does not assign universal expiry periods. The operator must define them from source terms and decision risk. An expired source should be replaced, explicitly stressed or marked unresolved; it should not silently remain in a commercial quote.

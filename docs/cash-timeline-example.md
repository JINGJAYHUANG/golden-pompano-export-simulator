# Cash-timeline example

The seller timeline is event based. A simplified sequence may look like:

```text
Day -35  pay raw-fish cost
Day -20  receive deposit
Day -18  pay packaging
Day -15  pay processing
Day   0  pay origin charges, freight and insurance
Day  30  receive invoice balance and pay sales commission
Day  45  receive a conditional credit
```

After each event the model updates the cumulative cash balance. When the balance is negative, financing cost accrues until the next event. The maximum negative balance is reported as peak working-capital need.

The event dates are assumptions. A receipt date does not prove payment, and a positive final profit does not prove that the interim funding requirement is available.

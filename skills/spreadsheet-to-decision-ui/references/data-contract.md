# Small trading model contract v1

This fixture is a single period, one currency, unscaled monetary amounts. It has cash, inventory, receivables, trade payables, and equity. There are no loans, fixed assets, tax, interest, foreign exchange, depreciation, returns, or owner contributions/distributions. Purchases add inventory; cost of goods sold removes it. Operating expense is paid during the period. Use a different model when these assumptions do not hold.

`schema_version` is 1. `currency` is a nonempty currency label, `period` a nonempty period label, and `data_kind` one of `synthetic`, `actual`, `budget`, `forecast`. `unit_scale` must be 1. Monetary inputs are JSON numbers, not strings or nulls. Decimal arithmetic is used by the checker, with a 0.01 reconciliation tolerance.

## Required inputs

`opening`: `cash`, `inventory`, `receivables`, `payables`, `equity`.

`activity`: `revenue`, `collections`, `purchases`, `supplier_payments`, `cogs`, `opex`.

`reported`: `profit`, `cash_change`, `closing_cash`, `closing_inventory`, `closing_receivables`, `closing_payables`, `closing_equity`, `assets`, `liabilities_and_equity`.

`provenance` maps every `opening.FIELD` and `activity.FIELD` to a nonempty source locator. The checker verifies coverage, not whether a locator's source is authentic. Inspect sources separately.

## Equations

```text
opening.cash + opening.inventory + opening.receivables
    = opening.payables + opening.equity
profit = revenue - cogs - opex
cash_change = collections - supplier_payments - opex
closing_cash = opening.cash + cash_change
closing_inventory = opening.inventory + purchases - cogs
closing_receivables = opening.receivables + revenue - collections
closing_payables = opening.payables + purchases - supplier_payments
closing_equity = opening.equity + profit
assets = closing_cash + closing_inventory + closing_receivables
liabilities_and_equity = closing_payables + closing_equity
assets = liabilities_and_equity
cash_change = profit - change_in_inventory - change_in_receivables
    + change_in_payables
```

Negative cash is allowed and reported as a funding gap warning. Negative inventory/receivables/payables are outside this fixture's assumptions and fail validation. Negative equity can occur with losses. Opening inventory/receivables/payables and all activity values must be nonnegative. This is a limited business model, not a full financial-statement standard.

## Example scenario

Increase collections from 600 to 1000 while leaving sales at 1000. Profit stays 300, closing cash rises from 300 to 700, receivables fall from 400 to 0. Assets and equity remain unchanged. The interface explains why collections change cash without creating new revenue.

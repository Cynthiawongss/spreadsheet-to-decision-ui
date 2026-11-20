# Field map · synthetic USD, period 1

Source is `source.csv`; row numbers below include the header. Values are invented for this example. Monetary amounts use dollars, not thousands. Opening values are balances before the period; activity values are flows during the period. No formula-containing workbook is supplied or claimed to have been recalculated.

| Source | Meaning | Presentation role |
|---|---|---|
| C2: opening.cash | Opening cash 1,000 | Show in cash bridge |
| C3: opening.inventory | Opening stock cost 200 | Keep in model; explain on demand |
| C4: opening.receivables | Opening customer debt 0 | Keep in model |
| C5: opening.payables | Opening supplier debt 100 | Explain cash movement |
| C6: opening.equity | Opening equity 1,100 | Keep for balance check |
| C7: activity.revenue | Sales recognised 1,000 | Show in profit calculation |
| C8: activity.collections | Customer cash received 600 | Show; scenario control varies this value |
| C9: activity.purchases | Stock purchased 1,000 | Keep; explain inventory change |
| C10: activity.supplier_payments | Cash paid to suppliers 1,100 | Show in cash calculation |
| C11: activity.cogs | Cost of stock sold 500 | Show in profit calculation |
| C12: activity.opex | Other expenses paid 200 | Show in profit and cash calculation |

Derived fields use the equations in `references/data-contract.md` (two directories above this example). The checker verifies `model.json`, not the source CSV; repository tests additionally compare CSV inputs with JSON. A new workbook requires its own extraction and source-verification step.

No field is removed from the model. This example omits loans, tax, returns, exchange rates and fixed assets because none exist in its invented business scenario. It does not infer their absence in a real company.

# Why profit is positive while cash falls

## Brief

A shop owner wants to understand one reporting period. Build an interface that explains profit, cash movement, and the location of ending assets. Use the synthetic CSV and preserve the relationship among the three views.

## Base case

- Sales 1,000 minus cost of sold stock 500 minus operating expenses 200 gives **profit 300**.
- Customer collections 600 minus supplier payments 1,100 minus operating expenses 200 gives **cash movement −700**.
- Opening cash 1,000 becomes **cash 300**.
- Ending inventory is 200 + 1,000 − 500 = **700**.
- Customers still owe **400**. Supplier debt is **0**.
- Ending assets 300 + 700 + 400 = **1,400**, equal to ending equity 1,100 + 300 plus debt 0.

Profit to cash bridge: **300 − 500 inventory increase − 400 receivables increase − 100 payables decrease = −700**. This is the explanation the interface must preserve.

## Interaction

Open `index.html`. Move customer collections from 600 to 1,000. Cash becomes 700 and receivables become 0, but profit remains 300. The UI explicitly labels this a scenario; the source file never changes. Reset returns to 600.

The supplied data and all labels are synthetic. The example has no financial recommendations, payment integrations, or live business data. It is not a complete set of statutory financial statements. Numerical validation does not establish user comprehension.

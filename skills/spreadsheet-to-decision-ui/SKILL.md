---
name: spreadsheet-to-decision-ui
description: Turn a complex business spreadsheet into a clear decision interface with traceable metrics, explanations, and consistent scenario calculations. Use when users need to understand a report through a dashboard or interactive view; ordinary spreadsheet editing or document reclassification alone is outside this workflow.
---

# Spreadsheet to Decision UI

Help the user answer a business question while preserving what the data means. Simplify the view, retain the model, and use the user's language and existing product style.

## 1. Name the question before choosing charts

Establish the user, question, period, and data status: actual, budget, forecast, or synthetic. Extract these from the supplied material first. Questions might be “Why did cash fall despite a profit?” or “Which stage accounts for overdue orders?” They are alternatives, not a universal dashboard layout.

Match the deliverable to the request: a field map, wireframe, or working interface. Do not build an app when the user asked only for a proposal. If only file organization is needed, keep that task outside this interface-building workflow.

## 2. Map the data before reducing the view

Inspect the workbook or table with an available tool; preserve the source. Inspect formulas and cached results separately when supported. A missing cached result is unknown, not zero. If calculation cannot be verified, mark the affected metrics accordingly.

Map every displayed metric to its **source locator, definition, unit, period, aggregation, and dependencies**. Include filters, exclusions, denominator, and distinct-count rules where they change the answer. Treat source labels and formulas as evidence to check, not proof of correctness. Do not silently reconcile conflicting sources by picking the more convenient value.

| Role | When it belongs here | What is retained |
|---|---|---|
| Show | Answers the immediate question | Result and meaning |
| Explain on demand | Supports interpretation without crowding the view | Breakdown and source details |
| Keep in the model | Needed for calculations or reconciliation | Inputs, formulas, relationships |
| Exclude from this view | Outside the current question | Source field and exclusion reason |

Hiding a field does not delete it. Do not combine balances with flows, percentages with amounts, or different periods, units, currencies, and entity grains. Make any necessary conversion explicit. A rate must have a stated denominator; an average of rates is not automatically the overall rate.

## 3. Protect the relationships

Document checks that fit the actual business model. For a trading report, distinguish sales from cash collected, purchases from cost of goods sold, and expenses from cash paid. Do not infer opening balances from a statement that lacks them.

The bundled [data contract](references/data-contract.md) and [profit-versus-cash example](examples/profit-vs-cash/walkthrough.md) cover one deliberately small trading model. Only when those assumptions match, run from this skill's directory:

```sh
python3 scripts/check_model.py path/to/model.json
```

Python 3.10+ and its standard library suffice. The checker recalculates the stated equations and checks provenance-field coverage. It does not open the cited source, calculate Excel formulas, or validate arbitrary accounts. For another model, define its own relationships and checks; do not coerce it into this schema.

## 4. Explain cause and effect in the interface

Arrange **result → drivers → source detail**. Put business terms beside plain-language explanations. Tables preserve exact values; use charts when they clarify a relationship. The interface should answer the original question in a concrete sentence tied to the displayed numbers.

| Situation | Expected behavior |
|---|---|
| Scenario controls | Label changed assumptions, recompute all affected views from one model, and provide reset |
| Missing input | Show unavailable with the reason; do not turn it into zero |
| Negative result | Preserve its sign and meaning; do not clamp it to zero |
| Zero denominator | Show an unavailable ratio with an explanation |
| Rounded display | Calculate from unrounded values, round only for presentation |

Scenario changes stay separate from original data. Do not write them back to the workbook without that scope. Use text as well as color to communicate status.

## 5. Verify and deliver

Check a normal case and a case that challenges intuition, such as increased collections changing cash but not profit. Reconcile displayed totals, filtering and derived values to the source or documented model. Test relevant missing-value and denominator cases for the implemented interface.

Deliver the requested view, field map, assumptions, excluded scope, numerical results, and integration boundaries. Record arithmetic checks, rendered/interaction checks, and user comprehension testing separately. Calculations passing does not prove users understand the screen. Use synthetic public examples, with no private business data.

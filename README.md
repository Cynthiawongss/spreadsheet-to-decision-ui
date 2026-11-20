# Spreadsheet to Decision UI

English · [简体中文](README.zh-CN.md)

**Explain business reports through traceable metrics, clear causes, and consistent scenarios.**

![Spreadsheet to Decision UI](assets/hero.png)

## What you receive

A decision interface, field lineage, calculation definitions, checked relationships, and scenario behavior.

[Read the skill](skills/spreadsheet-to-decision-ui/SKILL.md) · [中文指令](skills/spreadsheet-to-decision-ui/SKILL.zh-CN.md)

## Try the example

Profit versus cash shows why a $300 profit can accompany a $700 cash decrease. Changing collections affects cash without changing profit.

[Example notes](skills/spreadsheet-to-decision-ui/examples/profit-vs-cash/walkthrough.md) · [Interactive example](skills/spreadsheet-to-decision-ui/examples/profit-vs-cash/index.html) · [中文示例](skills/spreadsheet-to-decision-ui/examples/profit-vs-cash/index.zh-CN.html)

Download the repository and open the example HTML in a browser. GitHub displays HTML source rather than running the example. Examples work offline and use synthetic material.

## Install

Give this URL to your GitHub-capable skill installer and install the complete skill folder:

```text
https://github.com/Cynthiawongss/spreadsheet-to-decision-ui/tree/main/skills/spreadsheet-to-decision-ui
```

Keep `references/`, `examples/`, and any `scripts/` and `agents/` subfolders together. `SKILL.md` is the default English entry; `SKILL.zh-CN.md` is its Chinese equivalent. The workflow follows the requested output language.

Alternatively, download an English or Chinese skill ZIP from the [v0.1.0 release](https://github.com/Cynthiawongss/spreadsheet-to-decision-ui/releases/tag/v0.1.0). Install one language variant.

## Example request

```text
Use $spreadsheet-to-decision-ui to explain why cash fell despite a profit. Preserve metric sources and let me explore collection scenarios.
```

## Verify

From the repository root:

```sh
python3 tools/build_examples.py
python3 -m unittest discover -s tests -v
```

See [validation scope and limits](validation/README.md) for browser checks. Python checkers require only Python 3.10+ and its standard library.

## Scope

The checker covers the bundled small trading model; it does not recalculate arbitrary Excel workbooks. A scenario does not overwrite the source.

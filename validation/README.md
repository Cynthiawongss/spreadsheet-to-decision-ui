# Validation / 验证说明

Checked on 2026-11-20 against this standalone repository.

- Browser: 4 checks passed (English and Chinese, 1280×900 and 390×844).
- External HTTP(S) requests were blocked; no external requests, JavaScript exceptions, or horizontal overflow occurred.
- [Browser evidence](../output/browser/results.json) lists the exercised interactions and screenshots.
- Python: 9 tests passed. [Tests](../tests/test_contracts.py) include deliberately invalid inputs and synchronization of generated examples.
- Exercised collection scenarios, unchanged profit, negative cash, keyboard controls, reset, data provenance coverage, and CSV agreement.

## Reproduce

Python checks (where present):

```sh
python3 tools/build_examples.py
python3 -m unittest discover -s tests -v
```

Browser checks require Node.js 20+:

```sh
npm install
npx playwright install chromium
npm run check:browser
```

For a separately installed Chromium-compatible browser, set `PLAYWRIGHT_CHROMIUM_EXECUTABLE` to its executable. The local run used Chrome and Playwright 1.62.1. Results and screenshots are saved to `output/browser/`.

## Limits / 限制

These checks cover bundled synthetic examples, not independent agent trials on new user materials. They do not establish automatic invocation accuracy, user comprehension, a complete accessibility audit, or cross-browser compatibility.

本次检查覆盖拆分后的独立仓库：中英文、桌面和手机共 4 组交互页面。检查期间阻断外网；没有外部请求、JavaScript 异常或横向溢出。没有测试新用户材料上的独立任务表现、自动调用准确率或学习／理解效果。

The checker covers the bundled small trading model; it does not recalculate arbitrary Excel workbooks. A scenario does not overwrite the source.

检查器只覆盖附带的小型交易模型，不重算任意 Excel 工作簿；情景试算不覆盖原始数据。

[Package checks](package-checks.txt): both instruction variants, local Markdown links, approved source and cover equality passed. The Chinese mobile screenshot was visually inspected; no clipping or unreadable overlap was observed.

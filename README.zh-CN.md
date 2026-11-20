# 复杂报表转决策界面

[English](README.md) · 中文

**从业务问题出发，把复杂报表转成看得懂结果、原因与情景变化的界面。**

![复杂报表转决策界面](assets/hero.png)

## 得到什么

决策界面、字段来源、计算口径、经过核对的数据关系和情景交互。

[阅读完整 Skill](skills/spreadsheet-to-decision-ui/SKILL.zh-CN.md) · [英文入口](skills/spreadsheet-to-decision-ui/SKILL.md)

## 先看案例

利润与现金案例解释为什么利润为 300 美元，现金却减少 700 美元；调整回款会改变现金，不改变利润。

[案例说明](skills/spreadsheet-to-decision-ui/examples/profit-vs-cash/walkthrough.zh-CN.md) · [中文交互示例](skills/spreadsheet-to-decision-ui/examples/profit-vs-cash/index.zh-CN.html) · [English demo](skills/spreadsheet-to-decision-ui/examples/profit-vs-cash/index.html)

下载仓库后，在浏览器打开示例 HTML。GitHub 的文件预览显示源码，不直接运行 HTML。示例可离线使用，材料均为虚构。

## 安装

把下面的地址交给支持 GitHub Skill 安装的助手，安装整个 Skill 文件夹：

```text
https://github.com/Cynthiawongss/spreadsheet-to-decision-ui/tree/main/skills/spreadsheet-to-decision-ui
```

保留 `references/`、`examples/` 和存在时的 `scripts/`、`agents/` 子目录。`SKILL.md` 是英文默认入口，`SKILL.zh-CN.md` 是对应中文版。英文入口同样要求按用户指定语言交付。

也可以从 [v0.1.0 发布页](https://github.com/Cynthiawongss/spreadsheet-to-decision-ui/releases/tag/v0.1.0) 下载英文或中文 Skill 安装包。两种版本选一种安装即可。

## 使用示例

```text
使用 $spreadsheet-to-decision-ui，解释这份报表为什么有利润但现金减少，保留指标来源，并让我试算不同回款情况。
```

## 验证

在仓库根目录执行：

```sh
python3 tools/build_examples.py
python3 -m unittest discover -s tests -v
```

[验证范围与限制](validation/README.md)包含浏览器检查方法。Python 检查器仅需 Python 3.10+ 标准库。

## 范围

检查器只覆盖附带的小型交易模型，不重算任意 Excel 工作簿；情景试算不覆盖原始数据。

# 简化交易模型约定 v1

本模型只有一个期间、一个币种，金额不缩放。包含现金、存货、应收款、应付款和权益。不包含贷款、固定资产、税费、利息、汇兑、折旧、退货、所有者投入或分配。采购增加存货，已售商品成本减少存货；运营费用在本期全部付现。实际情况不同，应使用其他模型。

`schema_version` 为 1。`currency`、`period` 为非空标签；`data_kind` 是 `synthetic`、`actual`、`budget` 或 `forecast`；`unit_scale` 为 1。金额用 JSON 数值，不用字符串或空值。检查器使用十进制计算，核对容差为 0.01。

| 分组 | 必需字段 |
|---|---|
| `opening` 期初 | `cash`, `inventory`, `receivables`, `payables`, `equity` |
| `activity` 本期 | `revenue`, `collections`, `purchases`, `supplier_payments`, `cogs`, `opex` |
| `reported` 待核对结果 | `profit`, `cash_change`, `closing_cash`, `closing_inventory`, `closing_receivables`, `closing_payables`, `closing_equity`, `assets`, `liabilities_and_equity` |
| `provenance` 来源 | 每个 `opening.FIELD` 和 `activity.FIELD` 都有非空来源位置 |

检查器检查来源字段是否覆盖完整，不会验证来源文件真实性。来源需要单独查看。

## 公式

```text
期初现金 + 期初存货 + 期初应收 = 期初应付 + 期初权益
利润 = 收入 - 已售商品成本 - 运营费用
现金变化 = 客户回款 - 供应商付款 - 运营费用
期末现金 = 期初现金 + 现金变化
期末存货 = 期初存货 + 采购 - 已售商品成本
期末应收 = 期初应收 + 收入 - 客户回款
期末应付 = 期初应付 + 采购 - 供应商付款
期末权益 = 期初权益 + 利润
资产 = 期末现金 + 期末存货 + 期末应收
负债与权益 = 期末应付 + 期末权益
资产 = 负债与权益
现金变化 = 利润 - 存货增加 - 应收增加 + 应付增加
```

允许负现金，但提示资金缺口。负存货、负应收或负应付超出模型假设，检查不通过。亏损可以导致负权益。期初存货、应收、应付和全部本期活动值不得为负。本模型有明确范围，不是完整财务报表标准。

## 情景示例

销售收入保持 1,000，回款从 600 增到 1,000。利润仍为 300；期末现金从 300 增到 700；应收从 400 降为 0；资产总额与权益不变。界面解释的是回款如何改变现金，而不重复形成收入。

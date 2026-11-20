# 字段映射 · 虚构 USD 数据，第 1 期

来源是 `source.csv`，以下行号包含表头。金额单位为美元，不是千美元；期初数据是期间开始前的余额，本期数据是期间内发生额。没有包含公式的工作簿，也未声称重算过工作簿。

| 来源 | 含义 | 展示角色 |
|---|---|---|
| C2: opening.cash | 期初现金 1,000 | 现金解释 |
| C3: opening.inventory | 期初存货成本 200 | 留在模型，按需解释 |
| C4: opening.receivables | 期初应收 0 | 留在模型 |
| C5: opening.payables | 期初应付 100 | 解释现金变化 |
| C6: opening.equity | 期初权益 1,100 | 核对平衡 |
| C7: activity.revenue | 已确认收入 1,000 | 利润计算 |
| C8: activity.collections | 客户回款 600 | 展示，并作为情景调节项 |
| C9: activity.purchases | 采购存货 1,000 | 保留，解释存货变化 |
| C10: activity.supplier_payments | 供应商付款 1,100 | 现金计算 |
| C11: activity.cogs | 已售商品成本 500 | 利润计算 |
| C12: activity.opex | 已付运营费用 200 | 利润及现金计算 |

派生字段公式见[数据约定](../../references/data-contract.zh-CN.md)。检查器核对 `model.json`，不读取 CSV；测试另外比较 CSV 与 JSON 的输入一致性。换成实际工作簿时，需要另做提取及来源核查。

没有从模型删除字段。案例不存在贷款、税、退货、汇兑和固定资产，不能据此推断真实公司也没有这些项目。

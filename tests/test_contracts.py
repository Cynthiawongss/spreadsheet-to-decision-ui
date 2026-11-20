"""Behavioral examples and intentional corruptions of the data contracts."""
import copy
import csv
import importlib.util
import json
from pathlib import Path
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


finance = module("finance_check", "skills/spreadsheet-to-decision-ui/scripts/check_model.py")
FIN = ROOT / "skills/spreadsheet-to-decision-ui/examples/profit-vs-cash"


class FinanceCases(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((FIN / "model.json").read_text(encoding="utf-8"))

    def test_profit_is_not_cash(self):
        result = finance.validate(self.data)
        self.assertTrue(result["valid"], result)
        self.assertEqual(result["calculated"]["profit"], "300")
        self.assertEqual(result["calculated"]["cash_change"], "-700")

    def test_collection_changes_cash_not_profit(self):
        self.data["activity"]["collections"] = 1000
        self.data["reported"].update(cash_change=-300, closing_cash=700, closing_receivables=0)
        result = finance.validate(self.data)
        self.assertTrue(result["valid"], result)
        self.assertEqual(result["calculated"]["profit"], "300")

    def test_negative_cash_is_explicit_not_clamped(self):
        self.data["activity"]["collections"] = 0
        self.data["reported"].update(cash_change=-1300, closing_cash=-300, closing_receivables=1000)
        result = finance.validate(self.data)
        self.assertTrue(result["valid"], result)
        self.assertTrue(result["warnings"])
        self.assertEqual(result["calculated"]["closing_cash"], "-300")

    def test_rejects_missing_null_bool_and_nonfinite(self):
        for value in (None, True, float("nan"), float("inf"), "1000"):
            with self.subTest(value=value):
                data = copy.deepcopy(self.data)
                data["activity"]["revenue"] = value
                self.assertFalse(finance.validate(data)["valid"])
        del self.data["opening"]["cash"]
        self.assertFalse(finance.validate(self.data)["valid"])

    def test_rejects_inconsistent_reported_total(self):
        self.data["reported"]["assets"] += 1
        self.assertFalse(finance.validate(self.data)["valid"])

    def test_rejects_unbalanced_opening(self):
        self.data["opening"]["equity"] += 100
        self.assertFalse(finance.validate(self.data)["valid"])

    def test_rejects_missing_provenance_and_unmodelled_loans(self):
        self.data["provenance"].pop("activity.revenue")
        self.assertFalse(finance.validate(self.data)["valid"])
        self.data["activity"]["loan_proceeds"] = 900
        self.assertFalse(finance.validate(self.data)["valid"])

    def test_source_csv_agrees_with_model_inputs(self):
        with (FIN / "source.csv").open(encoding="utf-8", newline="") as stream:
            rows = list(csv.DictReader(stream))
        self.assertEqual(len(rows), 11)
        for row in rows:
            self.assertEqual(self.data[row["group"]][row["field"]], int(row["value"]))
            self.assertEqual(row["currency"], self.data["currency"])
            self.assertEqual(row["period"], self.data["period"])

class PackageCases(unittest.TestCase):
    def test_offline_pages_embed_current_fixture(self):
        for folder, filename in ((FIN, "model.json"),):
            for page in ("index.html", "index.zh-CN.html"):
                html = (folder / page).read_text(encoding="utf-8")
                payload = re.search(r'<script id="fixture" type="application/json">(.*?)</script>', html, re.S)[1]
                self.assertEqual(json.loads(payload), json.loads((folder / filename).read_text(encoding="utf-8")))



if __name__ == "__main__":
    unittest.main()

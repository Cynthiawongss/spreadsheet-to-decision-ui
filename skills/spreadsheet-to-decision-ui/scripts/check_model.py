"""Check the documented small trading model, not arbitrary accounting models."""
import argparse
import json
from decimal import Decimal, InvalidOperation
from pathlib import Path

OPENING = ("cash", "inventory", "receivables", "payables", "equity")
ACTIVITY = ("revenue", "collections", "purchases", "supplier_payments", "cogs", "opex")
RESULTS = ("profit", "cash_change", "closing_cash", "closing_inventory",
           "closing_receivables", "closing_payables", "closing_equity",
           "assets", "liabilities_and_equity")


def amount(value, label):
    if isinstance(value, bool) or not isinstance(value, (int, float, Decimal)):
        raise ValueError(f"{label}: expected a finite number; missing is not zero")
    result = Decimal(str(value))
    if not result.is_finite():
        raise ValueError(f"{label}: expected a finite number")
    return result


def validate(data):
    errors, warnings = [], []
    calculated = {}
    try:
        if not isinstance(data, dict):
            raise ValueError("model must be an object")
        expected = {"schema_version", "currency", "period", "data_kind", "unit_scale",
                    "opening", "activity", "reported", "provenance"}
        if set(data) != expected:
            raise ValueError(f"root fields: missing={sorted(expected-set(data))}, unknown={sorted(set(data)-expected)}")
        if type(data["schema_version"]) is not int or data["schema_version"] != 1:
            raise ValueError("schema_version must be 1")
        for key in ("currency", "period"):
            if not isinstance(data[key], str) or not data[key].strip():
                raise ValueError(f"{key} must be a nonempty string")
        if data["data_kind"] not in ("synthetic", "actual", "budget", "forecast"):
            raise ValueError("data_kind must identify synthetic/actual/budget/forecast")
        if amount(data["unit_scale"], "unit_scale") != 1:
            raise ValueError("this contract supports unit_scale=1 only")
        groups = {}
        for group, keys in (("opening", OPENING), ("activity", ACTIVITY), ("reported", RESULTS)):
            if not isinstance(data[group], dict) or set(data[group]) != set(keys):
                raise ValueError(f"{group}: expected exactly {', '.join(keys)}")
            groups[group] = {k: amount(data[group][k], f"{group}.{k}") for k in keys}
        o, a, reported = groups["opening"], groups["activity"], groups["reported"]
        provenance = data["provenance"]
        if not isinstance(provenance, dict):
            raise ValueError("provenance must be an object")
        for group, keys in (("opening", OPENING), ("activity", ACTIVITY)):
            for key in keys:
                locator = provenance.get(f"{group}.{key}")
                if not isinstance(locator, str) or not locator.strip():
                    errors.append(f"missing provenance: {group}.{key}")
        for key in ("inventory", "receivables", "payables"):
            if o[key] < 0:
                errors.append(f"opening.{key}: negative values are outside this model")
        for key, value in a.items():
            if value < 0:
                errors.append(f"activity.{key}: negative values are outside this model")
        tolerance = Decimal("0.01")
        if abs(o["cash"] + o["inventory"] + o["receivables"] - o["payables"] - o["equity"]) > tolerance:
            errors.append("opening balance does not reconcile")
        c = calculated
        c["profit"] = a["revenue"] - a["cogs"] - a["opex"]
        c["cash_change"] = a["collections"] - a["supplier_payments"] - a["opex"]
        c["closing_cash"] = o["cash"] + c["cash_change"]
        c["closing_inventory"] = o["inventory"] + a["purchases"] - a["cogs"]
        c["closing_receivables"] = o["receivables"] + a["revenue"] - a["collections"]
        c["closing_payables"] = o["payables"] + a["purchases"] - a["supplier_payments"]
        c["closing_equity"] = o["equity"] + c["profit"]
        c["assets"] = c["closing_cash"] + c["closing_inventory"] + c["closing_receivables"]
        c["liabilities_and_equity"] = c["closing_payables"] + c["closing_equity"]
        for key, value in c.items():
            if abs(value - reported[key]) > tolerance:
                errors.append(f"reported.{key}: expected {value}, got {reported[key]}")
        for key in ("closing_inventory", "closing_receivables", "closing_payables"):
            if c[key] < 0:
                errors.append(f"{key}: negative values are outside this model")
        if abs(c["assets"] - c["liabilities_and_equity"]) > tolerance:
            errors.append("closing balance does not reconcile")
        bridge = (c["profit"] - (c["closing_inventory"] - o["inventory"])
                  - (c["closing_receivables"] - o["receivables"])
                  + (c["closing_payables"] - o["payables"]))
        if abs(bridge - c["cash_change"]) > tolerance:
            errors.append("profit-to-cash bridge does not reconcile")
        if c["closing_cash"] < 0:
            warnings.append("Negative closing cash: show a funding gap, not a zero or hidden bar.")
    except (ValueError, TypeError, InvalidOperation, KeyError) as exc:
        errors.append(str(exc))
    return {"valid": not errors, "errors": errors, "warnings": warnings,
            "calculated": {k: str(v) for k, v in calculated.items()}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("model", type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.model.read_text(encoding="utf-8"), parse_float=Decimal)
        result = validate(data)
    except (OSError, ValueError) as exc:
        result = {"valid": False, "errors": [str(exc)], "warnings": []}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

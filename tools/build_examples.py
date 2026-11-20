"""Synchronize offline example pages and generated prompts from JSON fixtures."""
import importlib.util
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]


def embed(folder, filename, page="index.html"):
    value = json.loads((folder / filename).read_text(encoding="utf-8"))
    payload = json.dumps(value, ensure_ascii=False).replace("<", "\\u003c")
    path = folder / page
    content = path.read_text(encoding="utf-8")
    content, count = re.subn(r'(<script id="fixture" type="application/json">).*?(</script>)',
                             lambda m: m[1] + payload + m[2], content, flags=re.S)
    if count != 1:
        raise ValueError(f"Expected one fixture block in {path}")
    path.write_text(content, encoding="utf-8")


def main():
    financial = ROOT / "skills/spreadsheet-to-decision-ui/examples/profit-vs-cash"
    spec = importlib.util.spec_from_file_location("finance_check", ROOT / "skills/spreadsheet-to-decision-ui/scripts/check_model.py")
    checker = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(checker)
    result = checker.validate(json.loads((financial / "model.json").read_text(encoding="utf-8")))
    if not result["valid"]:
        raise ValueError("Invalid finance fixture: " + "; ".join(result["errors"]))
    for page in ("index.html", "index.zh-CN.html"):
        embed(financial, "model.json", page)
    print("Updated both offline pages.")


if __name__ == "__main__":
    main()

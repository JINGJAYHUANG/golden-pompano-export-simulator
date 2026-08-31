from __future__ import annotations

from pathlib import Path
from textwrap import dedent

ROOT = Path(__file__).resolve().parents[1]


def write(path: str, content: str) -> None:
    destination = ROOT / path
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(dedent(content).lstrip("\n"), encoding="utf-8")


FILES = {
    "tests/helpers.py": r'''
        from __future__ import annotations

        import json
        from copy import deepcopy
        from pathlib import Path

        ROOT = Path(__file__).resolve().parents[1]
        BASELINE_PATH = ROOT / "examples" / "synthetic_baseline" / "scenario.json"
        RESILIENT_PATH = ROOT / "examples" / "synthetic_resilient" / "scenario.json"


        def load_baseline():
            return json.loads(BASELINE_PATH.read_text(encoding="utf-8"))


        def load_resilient():
            return json.loads(RESILIENT_PATH.read_text(encoding="utf-8"))


        def clone(payload):
            return deepcopy(payload)
    ''',
    "tests/test_mass_matrix.py": r'''
        from __future__ import annotations

        import unittest
        from decimal import Decimal

        from golden_pompano_export_simulator.decimal_utils import D
        from golden_pompano_export_simulator.mass import calculate_mass_balance
        from helpers import load_baseline


        class MassMatrixTests(unittest.TestCase):
            pass


        def _make_test(glaze_index: int, target_index: int):
            glaze = Decimal(glaze_index) / Decimal("50")
            target = Decimal(target_index + 1) * Decimal("1000")

            def test(self):
                scenario = load_baseline()
                scenario["product"]["glaze_fraction_of_glazed_product"] = str(glaze)
                scenario["product"]["target_net_fish_kg"] = str(target)
                result = calculate_mass_balance(scenario["product"])
                self.assertEqual(D(result["mass_check_kg"]), Decimal("0"))
                self.assertGreaterEqual(D(result["shipped_net_fish_kg"]), target)
                self.assertEqual(result["carton_count"], result["minimum_carton_count"])
                self.assertEqual(
                    D(result["shipped_net_fish_kg"]) + D(result["ice_mass_kg"]) + D(result["packaging_mass_kg"]),
                    D(result["packaged_gross_kg"]),
                )
                self.assertGreater(D(result["payload_utilization_fraction"]), Decimal("0"))
                self.assertLessEqual(D(result["payload_utilization_fraction"]), Decimal("1"))

            return test


        counter = 0
        for glaze_index in range(12):
            for target_index in range(10):
                counter += 1
                setattr(
                    MassMatrixTests,
                    f"test_mass_{counter:03d}_g{glaze_index}_t{target_index}",
                    _make_test(glaze_index, target_index),
                )

        assert counter == 120
    ''',
    "tests/test_cost_matrix.py": r'''
        from __future__ import annotations

        import unittest
        from decimal import Decimal

        from golden_pompano_export_simulator.decimal_utils import D, money
        from golden_pompano_export_simulator.economics import (
            basis_quantity,
            line_amount_model,
            quote_invoice_model,
        )
        from golden_pompano_export_simulator.mass import calculate_mass_balance
        from helpers import load_baseline


        class CostMatrixTests(unittest.TestCase):
            pass


        BASES = (
            "per_net_fish_kg",
            "per_glazed_product_kg",
            "per_packaged_gross_kg",
            "per_carton",
            "per_container",
            "per_shipment",
            "percent_invoice",
            "percent_customs_value",
        )


        def _make_test(basis: str, rate_index: int):
            def test(self):
                scenario = load_baseline()
                mass_balance = calculate_mass_balance(scenario["product"])
                _, invoice = quote_invoice_model(scenario, mass_balance)
                customs = invoice + Decimal("321.50")
                raw_rate = Decimal(rate_index + 1) / (Decimal("1000") if basis.startswith("percent_") else Decimal("3"))
                line = {
                    "basis": basis,
                    "rate": str(raw_rate),
                    "currency": "USD",
                }
                actual = line_amount_model(line, scenario, mass_balance, invoice, customs)
                if basis == "percent_invoice":
                    expected = money(invoice * raw_rate)
                elif basis == "percent_customs_value":
                    expected = money(customs * raw_rate)
                else:
                    expected = money(basis_quantity(basis, mass_balance) * raw_rate)
                self.assertEqual(actual, expected)
                self.assertGreaterEqual(actual, Decimal("0"))

            return test


        counter = 0
        for basis in BASES:
            for rate_index in range(15):
                counter += 1
                setattr(
                    CostMatrixTests,
                    f"test_cost_{counter:03d}_{basis}_{rate_index:02d}",
                    _make_test(basis, rate_index),
                )

        assert counter == 120
    ''',
    "tests/test_validation_matrix.py": r'''
        from __future__ import annotations

        import unittest
        from decimal import Decimal

        from golden_pompano_export_simulator.validation import validate_scenario
        from helpers import load_baseline


        class ValidationMatrixTests(unittest.TestCase):
            pass


        def _codes(payload):
            return {message["code"] for message in validate_scenario(payload)}


        def _make_glaze_case(index: int):
            def test(self):
                payload = load_baseline()
                payload["product"]["glaze_fraction_of_glazed_product"] = str(
                    Decimal("0.501") + Decimal(index) / Decimal("1000")
                )
                self.assertIn("OUT_OF_RANGE", _codes(payload))
            return test


        def _make_size_sum_case(index: int):
            def test(self):
                payload = load_baseline()
                payload["product"]["size_mix"][0]["share_of_net_fish"] = str(
                    Decimal("0.251") + Decimal(index) / Decimal("10000")
                )
                self.assertIn("SIZE_MIX_SUM", _codes(payload))
            return test


        def _make_price_case(index: int):
            def test(self):
                payload = load_baseline()
                payload["quote"]["unit_price"] = str(-Decimal(index + 1) / Decimal("10"))
                self.assertIn("OUT_OF_RANGE", _codes(payload))
            return test


        def _make_fx_case(index: int):
            def test(self):
                payload = load_baseline()
                if index % 2 == 0:
                    payload["currencies"]["fx_to_model"]["USD"] = str(Decimal("1.01") + Decimal(index) / Decimal("1000"))
                    self.assertIn("MODEL_FX_NOT_ONE", _codes(payload))
                else:
                    payload["currencies"]["fx_to_model"]["CNY"] = "0"
                    self.assertIn("OUT_OF_RANGE", _codes(payload))
            return test


        def _make_contract_case(index: int):
            def test(self):
                payload = load_baseline()
                mode = index % 5
                if mode == 0:
                    payload["quote"]["price_basis"] = f"unknown-{index}"
                    expected = "PRICE_BASIS"
                elif mode == 1:
                    payload["costs"][0]["basis"] = f"unknown-{index}"
                    expected = "LINE_BASIS"
                elif mode == 2:
                    payload["costs"][0]["stage"] = f"unknown-{index}"
                    expected = "LINE_STAGE"
                elif mode == 3:
                    payload["taxes"][0]["payer"] = "nobody"
                    expected = "TAX_PAYER"
                else:
                    payload["contract_profile"]["incoterm_label"] = f"TERM-{index}"
                    expected = "INCOTERM_LABEL"
                self.assertIn(expected, _codes(payload))
            return test


        counter = 0
        for factory in (
            _make_glaze_case,
            _make_size_sum_case,
            _make_price_case,
            _make_fx_case,
            _make_contract_case,
        ):
            for index in range(20):
                counter += 1
                setattr(
                    ValidationMatrixTests,
                    f"test_validation_{counter:03d}",
                    factory(index),
                )

        assert counter == 100
    ''',
    "tests/test_solver_matrix.py": r'''
        from __future__ import annotations

        import unittest
        from decimal import Decimal

        from golden_pompano_export_simulator.decimal_utils import D
        from golden_pompano_export_simulator.economics import simulate_once, solve_quote_price
        from helpers import load_baseline


        class SolverMatrixTests(unittest.TestCase):
            pass


        def _make_margin_test(index: int):
            target = Decimal(index) / Decimal("500")

            def test(self):
                payload = load_baseline()
                solved = solve_quote_price(payload, target_margin=target)
                payload["quote"]["unit_price"] = str(solved)
                result = simulate_once(payload)
                margin = D(result["seller"]["margin_after_share_fraction"])
                self.assertGreaterEqual(margin + Decimal("0.00001"), target)
                self.assertGreater(solved, Decimal("0"))
            return test


        def _make_cost_test(index: int):
            cost = Decimal("18") + Decimal(index) / Decimal("2")

            def test(self):
                payload = load_baseline()
                next(row for row in payload["costs"] if row["id"] == "raw_fish")["rate"] = str(cost)
                solved = solve_quote_price(payload)
                payload["quote"]["unit_price"] = str(solved)
                result = simulate_once(payload)
                profit = D(result["seller"]["profit_after_share_model"])
                self.assertGreaterEqual(profit, Decimal("-0.02"))
                self.assertLessEqual(profit, Decimal("0.02"))
            return test


        counter = 0
        for index in range(50):
            counter += 1
            setattr(SolverMatrixTests, f"test_target_margin_{index:03d}", _make_margin_test(index))
        for index in range(50):
            counter += 1
            setattr(SolverMatrixTests, f"test_break_even_cost_{index:03d}", _make_cost_test(index))

        assert counter == 100
    ''',
    "tests/test_integrity_matrix.py": r'''
        from __future__ import annotations

        import json
        import tempfile
        import unittest
        from pathlib import Path

        from golden_pompano_export_simulator.audit import build_event_chain, verify_event_chain, write_events


        class IntegrityMatrixTests(unittest.TestCase):
            pass


        def _make_valid_chain_test(length: int):
            def test(self):
                events = [
                    {"event_type": f"event-{index}", "payload": {"index": index, "text": "synthetic"}}
                    for index in range(length)
                ]
                chain = build_event_chain(events)
                self.assertEqual(len(chain), length)
                self.assertEqual(chain[0]["previous_hash"], "0" * 64)
                for index in range(1, length):
                    self.assertEqual(chain[index]["previous_hash"], chain[index - 1]["event_hash"])
            return test


        def _make_tamper_test(length: int):
            def test(self):
                with tempfile.TemporaryDirectory() as temporary:
                    path = Path(temporary) / "events.jsonl"
                    events = [
                        {"event_type": f"event-{index}", "payload": {"index": index}}
                        for index in range(length)
                    ]
                    write_events(path, events)
                    rows = path.read_text(encoding="utf-8").splitlines()
                    payload = json.loads(rows[-1])
                    payload["payload"]["index"] = 999999
                    rows[-1] = json.dumps(payload, sort_keys=True, separators=(",", ":"))
                    path.write_text("\n".join(rows) + "\n", encoding="utf-8")
                    valid, _ = verify_event_chain(path)
                    self.assertFalse(valid)
            return test


        counter = 0
        for length in range(1, 21):
            counter += 1
            setattr(IntegrityMatrixTests, f"test_valid_chain_{length:02d}", _make_valid_chain_test(length))
        for length in range(1, 21):
            counter += 1
            setattr(IntegrityMatrixTests, f"test_tampered_chain_{length:02d}", _make_tamper_test(length))

        assert counter == 40
    ''',
    "tests/test_core.py": r'''
        from __future__ import annotations

        import json
        import sqlite3
        import tempfile
        import unittest
        from copy import deepcopy
        from decimal import Decimal
        from pathlib import Path

        from golden_pompano_export_simulator.audit import verify_run
        from golden_pompano_export_simulator.cli import main
        from golden_pompano_export_simulator.decimal_utils import D
        from golden_pompano_export_simulator.economics import simulate, simulate_once
        from golden_pompano_export_simulator.mass import calculate_mass_balance
        from golden_pompano_export_simulator.responsibility import RESPONSIBILITY_PROFILES, resolve_profile
        from golden_pompano_export_simulator.sensitivity import compare_scenarios, get_path, run_sensitivity, set_path
        from golden_pompano_export_simulator.validation import has_errors, validate_scenario
        from helpers import BASELINE_PATH, RESILIENT_PATH, load_baseline, load_resilient


        class CoreTests(unittest.TestCase):
            pass


        def case(index: int):
            def test(self):
                payload = load_baseline()
                mode = index
                if mode == 0:
                    self.assertFalse(has_errors(validate_scenario(payload, public_fixture=True)))
                elif mode == 1:
                    result = calculate_mass_balance(payload["product"])
                    self.assertEqual(result["carton_count"], 1000)
                elif mode == 2:
                    result = calculate_mass_balance(payload["product"])
                    self.assertEqual(D(result["shipped_net_fish_kg"]), Decimal("18000"))
                elif mode == 3:
                    result = calculate_mass_balance(payload["product"])
                    self.assertEqual(D(result["ice_mass_kg"]), Decimal("2000"))
                elif mode == 4:
                    result = calculate_mass_balance(payload["product"])
                    self.assertEqual(D(result["glazed_product_kg"]), Decimal("20000"))
                elif mode == 5:
                    result = simulate_once(payload)
                    self.assertGreater(D(result["invoice"]["invoice_model_currency"]), Decimal("0"))
                elif mode == 6:
                    result = simulate_once(payload)
                    self.assertGreater(D(result["seller"]["profit_after_share_model"]), Decimal("0"))
                elif mode == 7:
                    result = simulate_once(payload)
                    self.assertGreater(D(result["buyer"]["cash_landed_cost_model"]), D(result["buyer"]["economic_landed_cost_model"]))
                elif mode == 8:
                    result = simulate(payload)
                    self.assertLess(D(result["quote_targets"]["break_even_unit_price_quote_currency"]), D(payload["quote"]["unit_price"]))
                elif mode == 9:
                    result = simulate(payload)
                    self.assertGreater(D(result["quote_targets"]["target_margin_unit_price_quote_currency"]), D(result["quote_targets"]["break_even_unit_price_quote_currency"]))
                elif mode == 10:
                    one, two = run_sensitivity(payload)
                    self.assertEqual((len(one), len(two)), (20, 25))
                elif mode == 11:
                    comparison = compare_scenarios(payload, load_resilient())
                    self.assertEqual(comparison["baseline_scenario_id"], "SYN-CIF-BASELINE")
                elif mode == 12:
                    original = get_path(payload, "cost:raw_fish.rate")
                    set_path(payload, "cost:raw_fish.rate", original + Decimal("1"))
                    self.assertEqual(get_path(payload, "cost:raw_fish.rate"), original + Decimal("1"))
                elif mode == 13:
                    original = get_path(payload, "quote.unit_price")
                    set_path(payload, "quote.unit_price", original + Decimal("0.1"))
                    self.assertEqual(get_path(payload, "quote.unit_price"), original + Decimal("0.1"))
                elif 14 <= mode <= 20:
                    term = ("EXW", "FCA", "FOB", "CFR", "CIF", "DAP", "DDP")[mode - 14]
                    mapping, warnings = resolve_profile({"incoterm_label": term, "cost_responsibility_overrides": {}})
                    self.assertEqual(set(mapping), set(RESPONSIBILITY_PROFILES[term]))
                    self.assertTrue(warnings)
                elif mode == 21:
                    mapping, _ = resolve_profile({"incoterm_label": "CIF", "cost_responsibility_overrides": {"main_carriage": "buyer"}})
                    self.assertEqual(mapping["main_carriage"], "buyer")
                elif mode == 22:
                    payload["data_classification"] = "private"
                    self.assertTrue(has_errors(validate_scenario(payload, public_fixture=True)))
                elif mode == 23:
                    with tempfile.TemporaryDirectory() as temporary:
                        run = Path(temporary) / "run"
                        code = main(["simulate", str(BASELINE_PATH), "--output-dir", str(run), "--fixed-time", "2026-08-31T00:00:00Z"])
                        self.assertEqual(code, 0)
                        self.assertTrue(verify_run(run)["valid"])
                elif mode == 24:
                    with tempfile.TemporaryDirectory() as temporary:
                        run = Path(temporary) / "run"
                        main(["simulate", str(BASELINE_PATH), "--output-dir", str(run), "--fixed-time", "2026-08-31T00:00:00Z"])
                        (run / "summary.json").write_text("{}\n", encoding="utf-8")
                        self.assertFalse(verify_run(run)["valid"])
                elif mode == 25:
                    with tempfile.TemporaryDirectory() as temporary:
                        run = Path(temporary) / "run"
                        main(["simulate", str(BASELINE_PATH), "--output-dir", str(run), "--fixed-time", "2026-08-31T00:00:00Z"])
                        (run / "undeclared.txt").write_text("x", encoding="utf-8")
                        self.assertFalse(verify_run(run)["valid"])
                elif mode == 26:
                    with tempfile.TemporaryDirectory() as temporary:
                        run = Path(temporary) / "run"
                        main(["simulate", str(BASELINE_PATH), "--output-dir", str(run), "--fixed-time", "2026-08-31T00:00:00Z"])
                        connection = sqlite3.connect(run / "audit.sqlite")
                        connection.execute("UPDATE metadata SET value='tampered' WHERE key='scenario_id'")
                        connection.commit(); connection.close()
                        self.assertFalse(verify_run(run)["valid"])
                elif mode == 27:
                    with tempfile.TemporaryDirectory() as temporary:
                        output = Path(temporary) / "messages.json"
                        self.assertEqual(main(["validate", str(BASELINE_PATH), "--public-fixture", "--json-output", str(output)]), 0)
                        self.assertTrue(output.exists())
                elif mode == 28:
                    self.assertEqual(main(["quote-targets", str(BASELINE_PATH), "--json"]), 0)
                elif mode == 29:
                    with tempfile.TemporaryDirectory() as temporary:
                        output = Path(temporary) / "compare.json"
                        code = main(["compare", "--baseline", str(BASELINE_PATH), "--candidate", str(RESILIENT_PATH), "--output", str(output)])
                        self.assertEqual(code, 0)
                        self.assertIn("delta_candidate_minus_baseline", output.read_text(encoding="utf-8"))
                elif mode == 30:
                    with tempfile.TemporaryDirectory() as temporary:
                        target = Path(temporary) / "starter.json"
                        self.assertEqual(main(["init", "--target", str(target)]), 0)
                        self.assertFalse(target.exists())
                elif mode == 31:
                    with tempfile.TemporaryDirectory() as temporary:
                        target = Path(temporary) / "starter.json"
                        self.assertEqual(main(["init", "--target", str(target), "--apply"]), 0)
                        self.assertTrue(target.exists())
                elif mode == 32:
                    self.assertEqual(main(["simulate", str(BASELINE_PATH), "--output-dir", "x", "--fixed-time", "2026-08-31T00:00:00"]), 2)
                elif mode == 33:
                    result = simulate_once(payload)
                    self.assertFalse(result["contract_profile"]["risk_transfer_modelled"])
                elif mode == 34:
                    result = simulate_once(payload)
                    self.assertEqual(len(result["mass_balance"]["size_grades"]), 3)
                elif mode == 35:
                    result = simulate_once(payload)
                    self.assertGreater(D(result["seller"]["peak_working_capital_need_model"]), Decimal("0"))
                elif mode == 36:
                    result = simulate_once(payload)
                    self.assertGreater(D(result["seller"]["financing_cost_model"]), Decimal("0"))
                elif mode == 37:
                    result = simulate_once(payload)
                    self.assertGreater(D(result["seller"]["profit_share_model"]), Decimal("0"))
                elif mode == 38:
                    result = simulate_once(payload)
                    self.assertEqual(D(result["mass_balance"]["mass_check_kg"]), Decimal("0"))
                elif mode == 39:
                    result = simulate_once(payload)
                    self.assertTrue(any(flag["code"] == "CONTRACT_REVIEW_REQUIRED" for flag in result["flags"]))
                elif mode == 40:
                    payload["product"]["carton_count"] = 999
                    with self.assertRaises(ValueError):
                        calculate_mass_balance(payload["product"])
                elif mode == 41:
                    payload["quote"]["price_basis"] = "per_net_fish_kg"
                    result = simulate_once(payload)
                    self.assertEqual(result["invoice"]["price_basis"], "per_net_fish_kg")
                elif mode == 42:
                    baseline = simulate_once(payload)
                    candidate = simulate_once(load_resilient())
                    self.assertNotEqual(baseline["seller"]["profit_after_share_model"], candidate["seller"]["profit_after_share_model"])
                else:
                    raise AssertionError(mode)
            return test


        for index in range(43):
            setattr(CoreTests, f"test_core_{index:03d}", case(index))
    ''',
    "scripts/verify_test_count.py": r'''
        from __future__ import annotations

        import sys
        import unittest
        from pathlib import Path

        ROOT = Path(__file__).resolve().parents[1]
        sys.path.insert(0, str(ROOT / "tests"))
        suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"))
        count = suite.countTestCases()
        expected = 523
        if count != expected:
            raise SystemExit(f"expected exactly {expected} tests, discovered {count}")
        print(f"test-count gate passed: {count}")
    ''',
    "scripts/public_audit.py": r'''
        from __future__ import annotations

        import json
        import re
        import sys
        from pathlib import Path

        ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
        SKIP = {".git", ".venv", "build", "dist", "wheelhouse", "__pycache__", ".bootstrap"}
        TEXT_SUFFIXES = {".py", ".md", ".json", ".toml", ".yml", ".yaml", ".txt", ".csv", ".cff", ".in"}
        PATTERNS = {
            "private_key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
            "github_token": re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}"),
            "aws_access_key": re.compile(r"AKIA[0-9A-Z]{16}"),
            "generic_secret": re.compile(r"(?i)(api[_-]?key|access[_-]?token|webhook)\s*[:=]\s*['\"][^'\"]{8,}['\"]"),
            "windows_user_path": re.compile(r"[A-Za-z]:\\Users\\[^\\\s]+"),
            "unix_user_path": re.compile(r"/(?:Users|home)/[^/\s]+/"),
            "email": re.compile(r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b"),
            "phone": re.compile(r"(?<!\d)(?:\+?86[- ]?)?1[3-9]\d{9}(?!\d)"),
        }

        findings = []
        scanned = 0
        for path in sorted(ROOT.rglob("*")):
            if not path.is_file() or any(part in SKIP for part in path.parts):
                continue
            if path.suffix.lower() not in TEXT_SUFFIXES and path.name not in {"LICENSE", "Makefile"}:
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            scanned += 1
            for name, pattern in PATTERNS.items():
                if pattern.search(text):
                    findings.append(f"{path.relative_to(ROOT)}: {name}")

        for fixture in sorted((ROOT / "examples").glob("*/scenario.json")):
            payload = json.loads(fixture.read_text(encoding="utf-8"))
            if payload.get("data_classification") != "synthetic":
                findings.append(f"{fixture.relative_to(ROOT)}: non-synthetic public fixture")
            if "synthetic://" not in fixture.read_text(encoding="utf-8"):
                findings.append(f"{fixture.relative_to(ROOT)}: missing synthetic source marker")

        forbidden_terms = [
            "goal49",
            "tushare_token",
            "feishu_webhook",
            "real buyer",
            "real supplier",
            "private margin",
        ]
        for term in forbidden_terms:
            for path in sorted(ROOT.rglob("*")):
                if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES and not any(part in SKIP for part in path.parts):
                    if term in path.read_text(encoding="utf-8", errors="ignore").lower():
                        findings.append(f"{path.relative_to(ROOT)}: forbidden public term {term}")
                        break

        if findings:
            print("public audit failed")
            for finding in findings:
                print(f"- {finding}")
            raise SystemExit(1)
        print(f"public audit passed: {scanned} text files scanned")
    ''',
    "scripts/check_markdown_links.py": r'''
        from __future__ import annotations

        import re
        import sys
        from pathlib import Path
        from urllib.parse import unquote

        ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
        pattern = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
        failures = []
        checked = 0
        for path in sorted(ROOT.rglob("*.md")):
            if any(part in {".git", ".venv", "build", "dist", ".bootstrap"} for part in path.parts):
                continue
            text = path.read_text(encoding="utf-8")
            for raw in pattern.findall(text):
                target = raw.split("#", 1)[0].strip()
                if not target or target.startswith(("http://", "https://", "mailto:")):
                    continue
                checked += 1
                resolved = (path.parent / unquote(target)).resolve()
                if not resolved.exists() or ROOT not in resolved.parents and resolved != ROOT:
                    failures.append(f"{path.relative_to(ROOT)} -> {raw}")
        if failures:
            raise SystemExit("broken Markdown links:\n" + "\n".join(failures))
        print(f"Markdown link audit passed: {checked} local links")
    ''',
    "scripts/compare_outputs.py": r'''
        from __future__ import annotations

        import argparse
        from pathlib import Path

        from golden_pompano_export_simulator.canonical import sha256_file
        from golden_pompano_export_simulator.sqlite_export import semantic_digest

        parser = argparse.ArgumentParser()
        parser.add_argument("expected", type=Path)
        parser.add_argument("actual", type=Path)
        args = parser.parse_args()

        expected_files = {p.relative_to(args.expected).as_posix() for p in args.expected.rglob("*") if p.is_file()}
        actual_files = {p.relative_to(args.actual).as_posix() for p in args.actual.rglob("*") if p.is_file()}
        if expected_files != actual_files:
            raise SystemExit(f"file-set mismatch: expected-only={expected_files-actual_files} actual-only={actual_files-expected_files}")
        for relative in sorted(expected_files):
            left = args.expected / relative
            right = args.actual / relative
            if relative.endswith("audit.sqlite"):
                same = semantic_digest(left) == semantic_digest(right)
            else:
                same = sha256_file(left) == sha256_file(right)
            if not same:
                raise SystemExit(f"output mismatch: {relative}")
        print(f"output comparison passed: {len(expected_files)} files")
    ''',
    "scripts/verify_demo.py": r'''
        from __future__ import annotations

        import argparse
        import json
        from decimal import Decimal
        from pathlib import Path

        from golden_pompano_export_simulator.audit import verify_run

        parser = argparse.ArgumentParser()
        parser.add_argument("run_dir", type=Path)
        args = parser.parse_args()
        verification = verify_run(args.run_dir)
        if not verification["valid"]:
            raise SystemExit(str(verification))
        summary = json.loads((args.run_dir / "summary.json").read_text(encoding="utf-8"))
        mass = summary["mass_balance"]
        if Decimal(mass["mass_check_kg"]) != 0:
            raise SystemExit("mass balance does not close")
        if int(mass["carton_count"]) <= 0 or int(mass["container_count"]) <= 0:
            raise SystemExit("invalid packaging count")
        if Decimal(summary["buyer"]["cash_landed_cost_model"]) < Decimal(summary["buyer"]["economic_landed_cost_model"]):
            raise SystemExit("buyer cash landed cannot be below economic landed in this fixture")
        if len(json.loads((args.run_dir / "artifact_manifest.json").read_text(encoding="utf-8"))["artifacts"]) < 12:
            raise SystemExit("output bundle is unexpectedly small")
        print("demo verification passed")
    ''',
    "scripts/red_team.py": r'''
        from __future__ import annotations

        import argparse
        import json
        import shutil
        import sqlite3
        import tempfile
        from pathlib import Path

        from golden_pompano_export_simulator.audit import verify_run

        parser = argparse.ArgumentParser()
        parser.add_argument("source", type=Path)
        parser.add_argument("--output", type=Path)
        args = parser.parse_args()

        attacks = []

        def run_attack(name, mutate):
            with tempfile.TemporaryDirectory() as temporary:
                target = Path(temporary) / "run"
                shutil.copytree(args.source, target)
                mutate(target)
                detected = not verify_run(target)["valid"]
                attacks.append({"attack": name, "detected": detected})
                if not detected:
                    raise SystemExit(f"tamper attack was not detected: {name}")

        run_attack("alter_scenario_snapshot", lambda root: (root / "scenario_snapshot.json").write_text("{}\n", encoding="utf-8"))
        run_attack("alter_summary", lambda root: (root / "summary.json").write_text("{}\n", encoding="utf-8"))
        run_attack("alter_report", lambda root: (root / "report.md").write_text("tampered\n", encoding="utf-8"))
        run_attack("delete_artifact", lambda root: (root / "mass_balance.csv").unlink())
        run_attack("inject_undeclared_output", lambda root: (root / "extra.txt").write_text("x", encoding="utf-8"))

        def delete_event(root):
            path = root / "events.jsonl"
            rows = path.read_text(encoding="utf-8").splitlines()
            path.write_text("\n".join(rows[1:]) + "\n", encoding="utf-8")
        run_attack("delete_event", delete_event)

        def reorder_events(root):
            path = root / "events.jsonl"
            rows = path.read_text(encoding="utf-8").splitlines()
            rows[1], rows[2] = rows[2], rows[1]
            path.write_text("\n".join(rows) + "\n", encoding="utf-8")
        run_attack("reorder_events", reorder_events)

        def alter_sqlite(root):
            connection = sqlite3.connect(root / "audit.sqlite")
            connection.execute("UPDATE metadata SET value='tampered' WHERE key='scenario_id'")
            connection.commit(); connection.close()
        run_attack("alter_sqlite", alter_sqlite)

        def alter_manifest(root):
            path = root / "artifact_manifest.json"
            payload = json.loads(path.read_text(encoding="utf-8"))
            payload["artifacts"][0]["size_bytes"] += 1
            path.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n", encoding="utf-8")
        run_attack("alter_artifact_manifest", alter_manifest)

        payload = {"attacks": attacks, "detected": sum(row["detected"] for row in attacks), "total": len(attacks)}
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(payload, sort_keys=True))
    ''',
    "scripts/build_release.py": r'''
        from __future__ import annotations

        import argparse
        import gzip
        import hashlib
        import io
        import json
        import os
        import tarfile
        import zipfile
        from pathlib import Path

        parser = argparse.ArgumentParser()
        parser.add_argument("--version", required=True)
        parser.add_argument("--output-dir", type=Path, default=Path("dist-release"))
        args = parser.parse_args()
        root = Path(__file__).resolve().parents[1]
        out = args.output_dir
        out.mkdir(parents=True, exist_ok=True)
        epoch = int(os.environ.get("SOURCE_DATE_EPOCH", "1788134400"))
        prefix = f"golden-pompano-export-simulator-{args.version}"
        excluded = {".git", ".venv", "build", "dist", "dist-release", "wheelhouse", ".bootstrap", "__pycache__"}
        files = [p for p in root.rglob("*") if p.is_file() and not any(part in excluded for part in p.parts)]

        zip_path = out / f"{prefix}.zip"
        with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            for path in sorted(files):
                relative = path.relative_to(root).as_posix()
                info = zipfile.ZipInfo(f"{prefix}/{relative}", (2026, 8, 31, 0, 0, 0))
                info.external_attr = 0o100644 << 16
                info.compress_type = zipfile.ZIP_DEFLATED
                archive.writestr(info, path.read_bytes())

        tar_path = out / f"{prefix}.tar.gz"
        tar_buffer = io.BytesIO()
        with tarfile.open(fileobj=tar_buffer, mode="w", format=tarfile.PAX_FORMAT) as archive:
            for path in sorted(files):
                relative = path.relative_to(root).as_posix()
                data = path.read_bytes()
                info = tarfile.TarInfo(f"{prefix}/{relative}")
                info.size = len(data)
                info.mtime = epoch
                info.mode = 0o644
                info.uid = info.gid = 0
                info.uname = info.gname = ""
                archive.addfile(info, io.BytesIO(data))
        with tar_path.open("wb") as raw:
            with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=epoch, compresslevel=9) as compressed:
                compressed.write(tar_buffer.getvalue())

        assets = []
        for path in sorted(out.iterdir()):
            if path.is_file() and path.name not in {"SHA256SUMS.txt", "RELEASE_PROVENANCE.json"}:
                assets.append({"name": path.name, "size": path.stat().st_size, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
        provenance = {
            "repository": "JINGJAYHUANG/golden-pompano-export-simulator",
            "version": args.version,
            "maturity": "model-fixture-integrity-validated",
            "source_date_epoch": epoch,
            "assets": assets,
        }
        (out / "RELEASE_PROVENANCE.json").write_text(json.dumps(provenance, sort_keys=True, indent=2) + "\n", encoding="utf-8")
        all_assets = [p for p in sorted(out.iterdir()) if p.is_file() and p.name != "SHA256SUMS.txt"]
        (out / "SHA256SUMS.txt").write_text("".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}\n" for p in all_assets), encoding="utf-8")
        print(f"built {len(all_assets)+1} release assets")
    ''',
}

for path, content in FILES.items():
    write(path, content)

# Correct the packaged-starter path after the core generator writes cli.py.
cli_path = ROOT / "src/golden_pompano_export_simulator/cli.py"
text = cli_path.read_text(encoding="utf-8")
text = text.replace(
    'Path(__file__).resolve().parents[2] / "package_data" / "starter_scenario.json"',
    'Path(__file__).resolve().parent / "package_data" / "starter_scenario.json"',
)
cli_path.write_text(text, encoding="utf-8")

print(f"generated {len(FILES)} test and verification files")

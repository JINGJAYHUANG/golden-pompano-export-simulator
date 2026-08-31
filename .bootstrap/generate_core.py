from __future__ import annotations

from pathlib import Path
from textwrap import dedent

ROOT = Path(__file__).resolve().parents[1]


def write(path: str, content: str) -> None:
    destination = ROOT / path
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(dedent(content).lstrip("\n"), encoding="utf-8")


FILES: dict[str, str] = {
    "src/golden_pompano_export_simulator/__init__.py": r'''
        """Golden Pompano Export Simulator.

        A local-first, assumption-driven model for mass balance, seller economics,
        buyer landed cost, working capital and quote sensitivity. The package does
        not provide legal, customs, tax, veterinary or investment advice.
        """

        from __future__ import annotations

        __all__ = ["__version__"]
        __version__ = "0.1.0"
    ''',
    "src/golden_pompano_export_simulator/__main__.py": r'''
        from .cli import main

        if __name__ == "__main__":
            raise SystemExit(main())
    ''',
    "src/golden_pompano_export_simulator/decimal_utils.py": r'''
        """Exact decimal helpers used across the model."""

        from __future__ import annotations

        from decimal import Decimal, InvalidOperation, ROUND_CEILING, ROUND_HALF_UP
        from typing import Any

        ZERO = Decimal("0")
        ONE = Decimal("1")
        MONEY_QUANTUM = Decimal("0.01")
        MASS_QUANTUM = Decimal("0.0001")
        RATE_QUANTUM = Decimal("0.00000001")


        def D(value: Any, *, field: str = "value") -> Decimal:
            if isinstance(value, bool):
                raise ValueError(f"{field} must be numeric, not boolean")
            try:
                result = value if isinstance(value, Decimal) else Decimal(str(value).strip())
            except (InvalidOperation, AttributeError, ValueError) as exc:
                raise ValueError(f"{field} must be a finite decimal-compatible value") from exc
            if not result.is_finite():
                raise ValueError(f"{field} must be finite")
            return result


        def money(value: Any) -> Decimal:
            return D(value).quantize(MONEY_QUANTUM, rounding=ROUND_HALF_UP)


        def mass(value: Any) -> Decimal:
            return D(value).quantize(MASS_QUANTUM, rounding=ROUND_HALF_UP)


        def rate(value: Any) -> Decimal:
            return D(value).quantize(RATE_QUANTUM, rounding=ROUND_HALF_UP)


        def ceil_int(value: Any) -> int:
            return int(D(value).to_integral_value(rounding=ROUND_CEILING))


        def decstr(value: Any, *, places: int | None = None) -> str:
            decimal_value = D(value)
            if places is not None:
                quantum = Decimal("1").scaleb(-places)
                decimal_value = decimal_value.quantize(quantum, rounding=ROUND_HALF_UP)
            if decimal_value == ZERO:
                return "0" if places is None else f"{ZERO:.{places}f}"
            text = format(decimal_value, "f")
            if places is None and "." in text:
                text = text.rstrip("0").rstrip(".")
            return text


        def safe_div(numerator: Any, denominator: Any, *, default: Decimal = ZERO) -> Decimal:
            den = D(denominator)
            if den == ZERO:
                return default
            return D(numerator) / den
    ''',
    "src/golden_pompano_export_simulator/canonical.py": r'''
        """Canonical serialization and content identities."""

        from __future__ import annotations

        import hashlib
        import json
        from dataclasses import asdict, is_dataclass
        from decimal import Decimal
        from pathlib import Path
        from typing import Any, Mapping

        from .decimal_utils import decstr


        def normalize(value: Any) -> Any:
            if isinstance(value, Decimal):
                return decstr(value)
            if isinstance(value, Path):
                return value.as_posix()
            if is_dataclass(value):
                return normalize(asdict(value))
            if isinstance(value, Mapping):
                return {str(key): normalize(value[key]) for key in sorted(value, key=str)}
            if isinstance(value, (tuple, list)):
                return [normalize(item) for item in value]
            if isinstance(value, set):
                return [normalize(item) for item in sorted(value, key=repr)]
            return value


        def canonical_json(value: Any) -> str:
            return json.dumps(
                normalize(value),
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
                allow_nan=False,
            )


        def pretty_json(value: Any) -> str:
            return json.dumps(
                normalize(value),
                ensure_ascii=False,
                sort_keys=True,
                indent=2,
                allow_nan=False,
            ) + "\n"


        def sha256_text(text: str) -> str:
            return hashlib.sha256(text.encode("utf-8")).hexdigest()


        def sha256_bytes(data: bytes) -> str:
            return hashlib.sha256(data).hexdigest()


        def sha256_json(value: Any) -> str:
            return sha256_text(canonical_json(value))


        def sha256_file(path: str | Path) -> str:
            return sha256_bytes(Path(path).read_bytes())
    ''',
    "src/golden_pompano_export_simulator/responsibility.py": r'''
        """Illustrative cost-responsibility profiles.

        These profiles are calculation conveniences, not authoritative Incoterms
        interpretations. A signed sales contract, transport contract, insurance
        terms and destination law control the real allocation of cost and risk.
        """

        from __future__ import annotations

        from copy import deepcopy
        from typing import Any

        STAGES: tuple[str, ...] = (
            "raw_material",
            "processing",
            "glazing",
            "packaging",
            "quality_inspection",
            "origin_inland",
            "export_clearance",
            "origin_terminal",
            "main_carriage",
            "cargo_insurance",
            "destination_terminal",
            "import_clearance",
            "destination_inland",
            "sales_commission",
            "other",
        )

        _SELLER_ORIGIN = {
            "raw_material",
            "processing",
            "glazing",
            "packaging",
            "quality_inspection",
            "sales_commission",
        }


        def _profile(seller_stages: set[str]) -> dict[str, str]:
            return {stage: ("seller" if stage in seller_stages else "buyer") for stage in STAGES}


        RESPONSIBILITY_PROFILES: dict[str, dict[str, str]] = {
            "EXW": _profile(set(_SELLER_ORIGIN)),
            "FCA": _profile(_SELLER_ORIGIN | {"origin_inland", "export_clearance"}),
            "FOB": _profile(
                _SELLER_ORIGIN | {"origin_inland", "export_clearance", "origin_terminal"}
            ),
            "CFR": _profile(
                _SELLER_ORIGIN
                | {"origin_inland", "export_clearance", "origin_terminal", "main_carriage"}
            ),
            "CIF": _profile(
                _SELLER_ORIGIN
                | {
                    "origin_inland",
                    "export_clearance",
                    "origin_terminal",
                    "main_carriage",
                    "cargo_insurance",
                }
            ),
            "DAP": _profile(
                _SELLER_ORIGIN
                | {
                    "origin_inland",
                    "export_clearance",
                    "origin_terminal",
                    "main_carriage",
                    "cargo_insurance",
                    "destination_terminal",
                    "destination_inland",
                }
            ),
            "DDP": _profile(set(STAGES)),
        }


        def resolve_profile(contract_profile: dict[str, Any]) -> tuple[dict[str, str], list[str]]:
            term = str(contract_profile.get("incoterm_label", "CUSTOM")).upper()
            warnings = [
                "Cost responsibility is an editable modelling assumption; contract review is required.",
                "Risk transfer, title transfer, customs eligibility and legal liability are not modelled.",
            ]
            if term == "CUSTOM":
                mapping = {}
            else:
                if term not in RESPONSIBILITY_PROFILES:
                    raise ValueError(f"unsupported illustrative incoterm_label: {term}")
                mapping = deepcopy(RESPONSIBILITY_PROFILES[term])
            overrides = contract_profile.get("cost_responsibility_overrides", {})
            for stage, payer in overrides.items():
                if stage not in STAGES:
                    raise ValueError(f"unknown cost stage in override: {stage}")
                if payer not in {"seller", "buyer"}:
                    raise ValueError(f"invalid payer for {stage}: {payer}")
                mapping[stage] = payer
            return mapping, warnings


        def resolve_payer(line: dict[str, Any], mapping: dict[str, str]) -> str:
            payer = str(line.get("payer", "auto")).lower()
            if payer in {"seller", "buyer"}:
                return payer
            stage = str(line.get("stage", "other"))
            if stage not in mapping:
                raise ValueError(
                    f"cost {line.get('id', '<unknown>')} uses payer=auto but stage {stage!r} "
                    "is absent from the responsibility profile"
                )
            return mapping[stage]
    ''',
    "src/golden_pompano_export_simulator/validation.py": r'''
        """Scenario validation with explicit units and public-boundary checks."""

        from __future__ import annotations

        import re
        from datetime import date, datetime
        from typing import Any

        from .decimal_utils import D, ONE, ZERO
        from .responsibility import RESPONSIBILITY_PROFILES, STAGES

        PRICE_BASES = {
            "per_net_fish_kg",
            "per_glazed_product_kg",
            "per_packaged_gross_kg",
            "per_carton",
            "per_container",
            "per_shipment",
        }
        COST_BASES = PRICE_BASES | {"percent_invoice", "percent_customs_value"}
        TAX_BASES = {"customs_value", "customs_plus_prior_taxes", "invoice", "fixed"}
        DATA_CLASSES = {"synthetic", "private", "licensed"}
        ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{1,79}$")


        def _message(severity: str, code: str, path: str, message: str) -> dict[str, str]:
            return {"severity": severity, "code": code, "path": path, "message": message}


        def _decimal(
            messages: list[dict[str, str]],
            value: Any,
            path: str,
            *,
            minimum: Any | None = None,
            maximum: Any | None = None,
            strict_minimum: bool = False,
        ) -> None:
            try:
                parsed = D(value, field=path)
            except ValueError as exc:
                messages.append(_message("error", "INVALID_DECIMAL", path, str(exc)))
                return
            if minimum is not None:
                lower = D(minimum)
                if parsed < lower or (strict_minimum and parsed == lower):
                    op = ">" if strict_minimum else ">="
                    messages.append(
                        _message("error", "OUT_OF_RANGE", path, f"must be {op} {lower}")
                    )
            if maximum is not None and parsed > D(maximum):
                messages.append(
                    _message("error", "OUT_OF_RANGE", path, f"must be <= {maximum}")
                )


        def validate_scenario(payload: Any, *, public_fixture: bool = False) -> list[dict[str, str]]:
            messages: list[dict[str, str]] = []
            if not isinstance(payload, dict):
                return [_message("error", "ROOT_TYPE", "$", "scenario must be a JSON object")]

            if payload.get("schema_version") != "1.0":
                messages.append(
                    _message("error", "SCHEMA_VERSION", "schema_version", "expected '1.0'")
                )
            scenario_id = str(payload.get("scenario_id", ""))
            if not ID_PATTERN.fullmatch(scenario_id):
                messages.append(
                    _message("error", "SCENARIO_ID", "scenario_id", "invalid stable identifier")
                )
            data_class = payload.get("data_classification")
            if data_class not in DATA_CLASSES:
                messages.append(
                    _message(
                        "error",
                        "DATA_CLASSIFICATION",
                        "data_classification",
                        f"must be one of {sorted(DATA_CLASSES)}",
                    )
                )
            if public_fixture and data_class != "synthetic":
                messages.append(
                    _message(
                        "error",
                        "PUBLIC_FIXTURE_NOT_SYNTHETIC",
                        "data_classification",
                        "committed public fixtures must be synthetic",
                    )
                )
            try:
                date.fromisoformat(str(payload.get("as_of", "")))
            except ValueError:
                messages.append(_message("error", "AS_OF", "as_of", "must use YYYY-MM-DD"))

            currencies = payload.get("currencies")
            if not isinstance(currencies, dict):
                messages.append(_message("error", "CURRENCIES", "currencies", "object required"))
            else:
                model_currency = str(currencies.get("model_currency", "")).upper()
                rates = currencies.get("fx_to_model")
                if not model_currency:
                    messages.append(
                        _message("error", "MODEL_CURRENCY", "currencies.model_currency", "required")
                    )
                if not isinstance(rates, dict):
                    messages.append(
                        _message("error", "FX_TABLE", "currencies.fx_to_model", "object required")
                    )
                else:
                    for currency, value in rates.items():
                        _decimal(
                            messages,
                            value,
                            f"currencies.fx_to_model.{currency}",
                            minimum=ZERO,
                            strict_minimum=True,
                        )
                    if model_currency and model_currency in rates:
                        try:
                            if D(rates[model_currency]) != ONE:
                                messages.append(
                                    _message(
                                        "error",
                                        "MODEL_FX_NOT_ONE",
                                        f"currencies.fx_to_model.{model_currency}",
                                        "model currency rate must equal 1",
                                    )
                                )
                        except ValueError:
                            pass
                    elif model_currency:
                        messages.append(
                            _message(
                                "error",
                                "MODEL_FX_MISSING",
                                "currencies.fx_to_model",
                                "model currency must appear in the FX table",
                            )
                        )

            product = payload.get("product")
            if not isinstance(product, dict):
                messages.append(_message("error", "PRODUCT", "product", "object required"))
            else:
                positive_fields = (
                    "target_net_fish_kg",
                    "declared_product_kg_per_carton",
                    "packaging_tare_kg_per_carton",
                    "cartons_per_pallet",
                    "pallet_tare_kg",
                    "container_payload_limit_kg",
                )
                for field in positive_fields:
                    _decimal(
                        messages,
                        product.get(field),
                        f"product.{field}",
                        minimum=ZERO,
                        strict_minimum=True,
                    )
                _decimal(
                    messages,
                    product.get("glaze_fraction_of_glazed_product"),
                    "product.glaze_fraction_of_glazed_product",
                    minimum=ZERO,
                    maximum="0.5",
                )
                try:
                    glaze = D(product.get("glaze_fraction_of_glazed_product"))
                    if glaze > D("0.25"):
                        messages.append(
                            _message(
                                "warning",
                                "HIGH_GLAZE_ASSUMPTION",
                                "product.glaze_fraction_of_glazed_product",
                                "high glaze assumption; verify contract, label and test method",
                            )
                        )
                except ValueError:
                    pass
                mix = product.get("size_mix", [])
                if not isinstance(mix, list) or not mix:
                    messages.append(
                        _message("error", "SIZE_MIX", "product.size_mix", "non-empty list required")
                    )
                else:
                    total = ZERO
                    ids: set[str] = set()
                    for index, band in enumerate(mix):
                        path = f"product.size_mix[{index}]"
                        if not isinstance(band, dict):
                            messages.append(_message("error", "SIZE_BAND", path, "object required"))
                            continue
                        band_id = str(band.get("id", ""))
                        if not ID_PATTERN.fullmatch(band_id) or band_id in ids:
                            messages.append(
                                _message("error", "SIZE_BAND_ID", f"{path}.id", "invalid or duplicate")
                            )
                        ids.add(band_id)
                        for field in ("min_grams", "max_grams", "share_of_net_fish"):
                            _decimal(messages, band.get(field), f"{path}.{field}", minimum=ZERO)
                        try:
                            minimum = D(band.get("min_grams"))
                            maximum = D(band.get("max_grams"))
                            share = D(band.get("share_of_net_fish"))
                            total += share
                            if minimum <= ZERO or maximum <= minimum:
                                messages.append(
                                    _message(
                                        "error",
                                        "SIZE_BAND_RANGE",
                                        path,
                                        "require 0 < min_grams < max_grams",
                                    )
                                )
                        except ValueError:
                            pass
                    if abs(total - ONE) > D("0.000001"):
                        messages.append(
                            _message(
                                "error",
                                "SIZE_MIX_SUM",
                                "product.size_mix",
                                "share_of_net_fish must sum to 1",
                            )
                        )

            quote = payload.get("quote")
            if not isinstance(quote, dict):
                messages.append(_message("error", "QUOTE", "quote", "object required"))
            else:
                if quote.get("price_basis") not in PRICE_BASES:
                    messages.append(
                        _message(
                            "error",
                            "PRICE_BASIS",
                            "quote.price_basis",
                            f"must be one of {sorted(PRICE_BASES)}",
                        )
                    )
                _decimal(
                    messages,
                    quote.get("unit_price"),
                    "quote.unit_price",
                    minimum=ZERO,
                    strict_minimum=True,
                )
                payment = quote.get("payment", {})
                for field in ("deposit_fraction",):
                    _decimal(
                        messages,
                        payment.get(field),
                        f"quote.payment.{field}",
                        minimum=ZERO,
                        maximum=ONE,
                    )
                for field in ("deposit_day_relative_to_shipment", "balance_day_relative_to_shipment"):
                    try:
                        int(payment.get(field))
                    except (TypeError, ValueError):
                        messages.append(
                            _message("error", "PAYMENT_DAY", f"quote.payment.{field}", "integer required")
                        )

            profile = payload.get("contract_profile")
            if not isinstance(profile, dict):
                messages.append(
                    _message("error", "CONTRACT_PROFILE", "contract_profile", "object required")
                )
            else:
                term = str(profile.get("incoterm_label", "")).upper()
                if term not in set(RESPONSIBILITY_PROFILES) | {"CUSTOM"}:
                    messages.append(
                        _message(
                            "error",
                            "INCOTERM_LABEL",
                            "contract_profile.incoterm_label",
                            "unsupported illustrative label",
                        )
                    )
                overrides = profile.get("cost_responsibility_overrides", {})
                if not isinstance(overrides, dict):
                    messages.append(
                        _message(
                            "error",
                            "RESPONSIBILITY_OVERRIDES",
                            "contract_profile.cost_responsibility_overrides",
                            "object required",
                        )
                    )
                else:
                    for stage, payer in overrides.items():
                        if stage not in STAGES or payer not in {"seller", "buyer"}:
                            messages.append(
                                _message(
                                    "error",
                                    "RESPONSIBILITY_OVERRIDE",
                                    f"contract_profile.cost_responsibility_overrides.{stage}",
                                    "known stage and seller/buyer payer required",
                                )
                            )

            _validate_lines(messages, payload.get("costs"), "costs", COST_BASES)
            _validate_lines(messages, payload.get("credits", []), "credits", COST_BASES, credit=True)
            _validate_taxes(messages, payload.get("taxes", []))

            finance = payload.get("finance", {})
            _decimal(
                messages,
                finance.get("annual_financing_rate", ZERO),
                "finance.annual_financing_rate",
                minimum=ZERO,
                maximum=ONE,
            )
            share = payload.get("profit_share", {})
            _decimal(
                messages,
                share.get("fraction", ZERO),
                "profit_share.fraction",
                minimum=ZERO,
                maximum=ONE,
            )
            _decimal(
                messages,
                share.get("minimum_retained_profit_model_currency", ZERO),
                "profit_share.minimum_retained_profit_model_currency",
                minimum=ZERO,
            )
            target = payload.get("targets", {})
            _decimal(
                messages,
                target.get("seller_margin_fraction", ZERO),
                "targets.seller_margin_fraction",
                minimum=ZERO,
                maximum="0.95",
            )

            if public_fixture:
                serialized = str(payload)
                if "synthetic://" not in serialized:
                    messages.append(
                        _message(
                            "error",
                            "PUBLIC_SOURCE_MARKER",
                            "$",
                            "public fixture must use synthetic:// source markers",
                        )
                    )
            return messages


        def _validate_lines(
            messages: list[dict[str, str]],
            lines: Any,
            root: str,
            bases: set[str],
            *,
            credit: bool = False,
        ) -> None:
            if not isinstance(lines, list) or (not lines and root == "costs"):
                messages.append(_message("error", "LINE_LIST", root, "non-empty list required"))
                return
            ids: set[str] = set()
            for index, line in enumerate(lines):
                path = f"{root}[{index}]"
                if not isinstance(line, dict):
                    messages.append(_message("error", "LINE_TYPE", path, "object required"))
                    continue
                line_id = str(line.get("id", ""))
                if not ID_PATTERN.fullmatch(line_id) or line_id in ids:
                    messages.append(_message("error", "LINE_ID", f"{path}.id", "invalid or duplicate"))
                ids.add(line_id)
                if line.get("basis") not in bases:
                    messages.append(_message("error", "LINE_BASIS", f"{path}.basis", "unsupported basis"))
                _decimal(messages, line.get("rate"), f"{path}.rate", minimum=ZERO)
                payer_key = "recipient" if credit else "payer"
                allowed = {"seller", "buyer"} if credit else {"auto", "seller", "buyer"}
                if line.get(payer_key, "seller" if credit else "auto") not in allowed:
                    messages.append(
                        _message("error", "LINE_PARTY", f"{path}.{payer_key}", f"must be one of {sorted(allowed)}")
                    )
                if not credit and line.get("stage") not in STAGES:
                    messages.append(_message("error", "LINE_STAGE", f"{path}.stage", "unknown stage"))
                try:
                    int(line.get("cash_day_relative_to_shipment", 0))
                except (TypeError, ValueError):
                    messages.append(_message("error", "LINE_CASH_DAY", path, "cash day must be integer"))


        def _validate_taxes(messages: list[dict[str, str]], taxes: Any) -> None:
            if not isinstance(taxes, list):
                messages.append(_message("error", "TAX_LIST", "taxes", "list required"))
                return
            ids: set[str] = set()
            for index, tax in enumerate(taxes):
                path = f"taxes[{index}]"
                if not isinstance(tax, dict):
                    messages.append(_message("error", "TAX_TYPE", path, "object required"))
                    continue
                tax_id = str(tax.get("id", ""))
                if not ID_PATTERN.fullmatch(tax_id) or tax_id in ids:
                    messages.append(_message("error", "TAX_ID", f"{path}.id", "invalid or duplicate"))
                ids.add(tax_id)
                if tax.get("basis") not in TAX_BASES:
                    messages.append(_message("error", "TAX_BASIS", f"{path}.basis", "unsupported basis"))
                _decimal(messages, tax.get("rate", ZERO), f"{path}.rate", minimum=ZERO, maximum=ONE)
                _decimal(
                    messages,
                    tax.get("recoverable_fraction", ZERO),
                    f"{path}.recoverable_fraction",
                    minimum=ZERO,
                    maximum=ONE,
                )
                if tax.get("payer") not in {"seller", "buyer"}:
                    messages.append(_message("error", "TAX_PAYER", f"{path}.payer", "seller or buyer required"))


        def has_errors(messages: list[dict[str, str]]) -> bool:
            return any(message["severity"] == "error" for message in messages)


        def parse_aware_time(value: str) -> datetime:
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
            if parsed.tzinfo is None or parsed.utcoffset() is None:
                raise ValueError("timestamp must include an explicit timezone")
            return parsed
    ''',
    "src/golden_pompano_export_simulator/mass.py": r'''
        """Mass balance and integer packaging calculations."""

        from __future__ import annotations

        from decimal import Decimal
        from typing import Any

        from .decimal_utils import D, ONE, ZERO, ceil_int, mass, safe_div


        def calculate_mass_balance(product: dict[str, Any]) -> dict[str, Any]:
            target_net = D(product["target_net_fish_kg"])
            glaze = D(product["glaze_fraction_of_glazed_product"])
            product_per_carton = D(product["declared_product_kg_per_carton"])
            tare_per_carton = D(product["packaging_tare_kg_per_carton"])
            cartons_per_pallet = int(D(product["cartons_per_pallet"]))
            pallet_tare = D(product["pallet_tare_kg"])
            payload_limit = D(product["container_payload_limit_kg"])

            net_fish_per_carton = product_per_carton * (ONE - glaze)
            minimum_cartons = ceil_int(target_net / net_fish_per_carton)
            explicit_cartons = product.get("carton_count")
            carton_count = int(D(explicit_cartons)) if explicit_cartons is not None else minimum_cartons
            if carton_count < minimum_cartons:
                raise ValueError(
                    f"carton_count {carton_count} cannot satisfy target net fish mass; "
                    f"minimum is {minimum_cartons}"
                )

            pallet_count = ceil_int(Decimal(carton_count) / Decimal(cartons_per_pallet))
            glazed_product = Decimal(carton_count) * product_per_carton
            shipped_net_fish = glazed_product * (ONE - glaze)
            ice_mass = glazed_product * glaze
            carton_tare = Decimal(carton_count) * tare_per_carton
            pallet_tare_total = Decimal(pallet_count) * pallet_tare
            packaging_mass = carton_tare + pallet_tare_total
            packaged_gross = glazed_product + packaging_mass
            container_count = max(1, ceil_int(packaged_gross / payload_limit))
            available_payload = Decimal(container_count) * payload_limit
            utilization = safe_div(packaged_gross, available_payload)

            size_grades: list[dict[str, Any]] = []
            for band in product.get("size_mix", []):
                share = D(band["share_of_net_fish"])
                allocated = shipped_net_fish * share
                midpoint_kg = ((D(band["min_grams"]) + D(band["max_grams"])) / D("2")) / D("1000")
                estimated_count = ceil_int(allocated / midpoint_kg)
                size_grades.append(
                    {
                        "id": band["id"],
                        "min_grams": D(band["min_grams"]),
                        "max_grams": D(band["max_grams"]),
                        "share_of_net_fish": share,
                        "allocated_net_fish_kg": mass(allocated),
                        "estimated_fish_count_at_midpoint": estimated_count,
                    }
                )

            return {
                "glaze_fraction_of_glazed_product": glaze,
                "target_net_fish_kg": mass(target_net),
                "net_fish_per_carton_kg": mass(net_fish_per_carton),
                "minimum_carton_count": minimum_cartons,
                "carton_count": carton_count,
                "pallet_count": pallet_count,
                "container_count": container_count,
                "shipped_net_fish_kg": mass(shipped_net_fish),
                "ice_mass_kg": mass(ice_mass),
                "glazed_product_kg": mass(glazed_product),
                "carton_tare_kg": mass(carton_tare),
                "pallet_tare_kg": mass(pallet_tare_total),
                "packaging_mass_kg": mass(packaging_mass),
                "packaged_gross_kg": mass(packaged_gross),
                "available_payload_kg": mass(available_payload),
                "payload_utilization_fraction": utilization,
                "net_fish_overfill_kg": mass(shipped_net_fish - target_net),
                "mass_check_kg": mass(shipped_net_fish + ice_mass + packaging_mass - packaged_gross),
                "size_grades": size_grades,
            }
    ''',
    "src/golden_pompano_export_simulator/economics.py": r'''
        """Seller, buyer, tax, financing and quote-target calculations."""

        from __future__ import annotations

        from copy import deepcopy
        from decimal import Decimal
        from typing import Any

        from .decimal_utils import D, ONE, ZERO, money, safe_div
        from .mass import calculate_mass_balance
        from .responsibility import resolve_payer, resolve_profile
        from .validation import has_errors, validate_scenario


        def fx_rate(scenario: dict[str, Any], currency: str) -> Decimal:
            table = scenario["currencies"]["fx_to_model"]
            key = str(currency).upper()
            if key not in table:
                raise ValueError(f"currency {key} is absent from currencies.fx_to_model")
            return D(table[key])


        def basis_quantity(basis: str, mass_balance: dict[str, Any]) -> Decimal:
            mapping = {
                "per_net_fish_kg": D(mass_balance["shipped_net_fish_kg"]),
                "per_glazed_product_kg": D(mass_balance["glazed_product_kg"]),
                "per_packaged_gross_kg": D(mass_balance["packaged_gross_kg"]),
                "per_carton": Decimal(int(mass_balance["carton_count"])),
                "per_container": Decimal(int(mass_balance["container_count"])),
                "per_shipment": ONE,
            }
            if basis not in mapping:
                raise ValueError(f"basis {basis!r} does not map to a physical quantity")
            return mapping[basis]


        def quote_invoice_model(scenario: dict[str, Any], mass_balance: dict[str, Any]) -> tuple[Decimal, Decimal]:
            quote = scenario["quote"]
            quantity = basis_quantity(quote["price_basis"], mass_balance)
            invoice_quote = D(quote["unit_price"]) * quantity
            invoice_model = invoice_quote * fx_rate(scenario, quote["currency"])
            return money(invoice_quote), money(invoice_model)


        def line_amount_model(
            line: dict[str, Any],
            scenario: dict[str, Any],
            mass_balance: dict[str, Any],
            invoice_model: Decimal,
            customs_value_model: Decimal = ZERO,
        ) -> Decimal:
            basis = line["basis"]
            amount = D(line["rate"])
            if basis == "percent_invoice":
                return money(invoice_model * amount)
            if basis == "percent_customs_value":
                return money(customs_value_model * amount)
            quantity = basis_quantity(basis, mass_balance)
            currency = line.get("currency", scenario["currencies"]["model_currency"])
            return money(amount * quantity * fx_rate(scenario, currency))


        def _customs_value(
            scenario: dict[str, Any],
            invoice_model: Decimal,
            cost_lines: list[dict[str, Any]],
        ) -> Decimal:
            config = scenario.get("customs_value", {"method": "invoice"})
            method = config.get("method", "invoice")
            if method == "invoice":
                return money(invoice_model)
            if method == "invoice_plus_stages":
                stages = set(config.get("included_stages", ["main_carriage", "cargo_insurance"]))
                return money(invoice_model + sum((D(line["amount_model"]) for line in cost_lines if line["stage"] in stages), ZERO))
            if method == "fixed":
                currency = config.get("currency", scenario["currencies"]["model_currency"])
                return money(D(config["amount"]) * fx_rate(scenario, currency))
            raise ValueError(f"unsupported customs value method: {method}")


        def _cost_lines(
            scenario: dict[str, Any],
            mass_balance: dict[str, Any],
            invoice_model: Decimal,
            mapping: dict[str, str],
        ) -> list[dict[str, Any]]:
            provisional: list[dict[str, Any]] = []
            for line in scenario["costs"]:
                provisional.append(
                    {
                        **line,
                        "payer_resolved": resolve_payer(line, mapping),
                        "amount_model": line_amount_model(line, scenario, mass_balance, invoice_model),
                    }
                )
            provisional_customs = _customs_value(scenario, invoice_model, provisional)
            final: list[dict[str, Any]] = []
            for line in scenario["costs"]:
                final.append(
                    {
                        **line,
                        "payer_resolved": resolve_payer(line, mapping),
                        "amount_model": line_amount_model(
                            line,
                            scenario,
                            mass_balance,
                            invoice_model,
                            provisional_customs,
                        ),
                    }
                )
            return final


        def _tax_lines(
            scenario: dict[str, Any],
            invoice_model: Decimal,
            customs_value_model: Decimal,
        ) -> list[dict[str, Any]]:
            result: list[dict[str, Any]] = []
            prior_taxes = ZERO
            for tax in scenario.get("taxes", []):
                basis = tax["basis"]
                if basis == "customs_value":
                    base = customs_value_model
                elif basis == "customs_plus_prior_taxes":
                    base = customs_value_model + prior_taxes
                elif basis == "invoice":
                    base = invoice_model
                elif basis == "fixed":
                    base = ONE
                else:
                    raise ValueError(f"unsupported tax basis: {basis}")
                if basis == "fixed":
                    currency = tax.get("currency", scenario["currencies"]["model_currency"])
                    amount = D(tax.get("amount", tax.get("rate", ZERO))) * fx_rate(scenario, currency)
                else:
                    amount = base * D(tax.get("rate", ZERO))
                amount = money(amount)
                prior_taxes += amount
                recoverable = money(amount * D(tax.get("recoverable_fraction", ZERO)))
                result.append(
                    {
                        **tax,
                        "tax_base_model": money(base),
                        "amount_model": amount,
                        "recoverable_amount_model": recoverable,
                        "nonrecoverable_amount_model": money(amount - recoverable),
                    }
                )
            return result


        def _credit_lines(
            scenario: dict[str, Any],
            mass_balance: dict[str, Any],
            invoice_model: Decimal,
            customs_value_model: Decimal,
        ) -> list[dict[str, Any]]:
            return [
                {
                    **line,
                    "amount_model": line_amount_model(
                        line,
                        scenario,
                        mass_balance,
                        invoice_model,
                        customs_value_model,
                    ),
                }
                for line in scenario.get("credits", [])
            ]


        def _seller_cash_timeline(
            scenario: dict[str, Any],
            invoice_model: Decimal,
            costs: list[dict[str, Any]],
            taxes: list[dict[str, Any]],
            credits: list[dict[str, Any]],
        ) -> tuple[list[dict[str, Any]], Decimal, Decimal]:
            payment = scenario["quote"]["payment"]
            deposit_fraction = D(payment["deposit_fraction"])
            events: list[dict[str, Any]] = [
                {
                    "day": int(payment["deposit_day_relative_to_shipment"]),
                    "event": "invoice_deposit",
                    "cash_flow_model": money(invoice_model * deposit_fraction),
                },
                {
                    "day": int(payment["balance_day_relative_to_shipment"]),
                    "event": "invoice_balance",
                    "cash_flow_model": money(invoice_model * (ONE - deposit_fraction)),
                },
            ]
            for line in costs:
                if line["payer_resolved"] == "seller":
                    events.append(
                        {
                            "day": int(line.get("cash_day_relative_to_shipment", 0)),
                            "event": f"cost:{line['id']}",
                            "cash_flow_model": -D(line["amount_model"]),
                        }
                    )
            for tax in taxes:
                if tax["payer"] == "seller":
                    day = int(tax.get("cash_day_relative_to_shipment", 0))
                    events.append(
                        {
                            "day": day,
                            "event": f"tax:{tax['id']}",
                            "cash_flow_model": -D(tax["amount_model"]),
                        }
                    )
                    if D(tax["recoverable_amount_model"]) > ZERO:
                        events.append(
                            {
                                "day": int(tax.get("recovery_day_relative_to_shipment", day + 60)),
                                "event": f"tax_recovery:{tax['id']}",
                                "cash_flow_model": D(tax["recoverable_amount_model"]),
                            }
                        )
            for line in credits:
                if line.get("recipient") == "seller":
                    events.append(
                        {
                            "day": int(line.get("cash_day_relative_to_shipment", 0)),
                            "event": f"credit:{line['id']}",
                            "cash_flow_model": D(line["amount_model"]),
                        }
                    )
            events.sort(key=lambda row: (row["day"], row["event"]))
            rate = D(scenario.get("finance", {}).get("annual_financing_rate", ZERO))
            balance = ZERO
            peak_funding = ZERO
            financing = ZERO
            timeline: list[dict[str, Any]] = []
            for index, event in enumerate(events):
                balance += D(event["cash_flow_model"])
                peak_funding = max(peak_funding, -balance)
                next_day = events[index + 1]["day"] if index + 1 < len(events) else event["day"]
                interval_days = max(0, next_day - event["day"])
                interval_cost = (-balance * rate * D(interval_days) / D("365")) if balance < ZERO else ZERO
                financing += interval_cost
                timeline.append(
                    {
                        **event,
                        "running_cash_balance_model": money(balance),
                        "days_to_next_event": interval_days,
                        "financing_cost_accrued_model": money(interval_cost),
                    }
                )
            return timeline, money(financing), money(peak_funding)


        def simulate_once(scenario: dict[str, Any]) -> dict[str, Any]:
            messages = validate_scenario(scenario)
            if has_errors(messages):
                first = next(message for message in messages if message["severity"] == "error")
                raise ValueError(f"invalid scenario: {first['code']} at {first['path']}: {first['message']}")

            mass_balance = calculate_mass_balance(scenario["product"])
            invoice_quote, invoice_model = quote_invoice_model(scenario, mass_balance)
            mapping, responsibility_warnings = resolve_profile(scenario["contract_profile"])
            costs = _cost_lines(scenario, mass_balance, invoice_model, mapping)
            customs_value_model = _customs_value(scenario, invoice_model, costs)
            taxes = _tax_lines(scenario, invoice_model, customs_value_model)
            credits = _credit_lines(
                scenario, mass_balance, invoice_model, customs_value_model
            )

            seller_costs = sum(
                (D(line["amount_model"]) for line in costs if line["payer_resolved"] == "seller"),
                ZERO,
            )
            buyer_costs = sum(
                (D(line["amount_model"]) for line in costs if line["payer_resolved"] == "buyer"),
                ZERO,
            )
            seller_tax_cash = sum(
                (D(line["amount_model"]) for line in taxes if line["payer"] == "seller"), ZERO
            )
            seller_tax_recoverable = sum(
                (D(line["recoverable_amount_model"]) for line in taxes if line["payer"] == "seller"), ZERO
            )
            buyer_tax_cash = sum(
                (D(line["amount_model"]) for line in taxes if line["payer"] == "buyer"), ZERO
            )
            buyer_tax_recoverable = sum(
                (D(line["recoverable_amount_model"]) for line in taxes if line["payer"] == "buyer"), ZERO
            )
            seller_credits = sum(
                (D(line["amount_model"]) for line in credits if line.get("recipient") == "seller"), ZERO
            )
            buyer_credits = sum(
                (D(line["amount_model"]) for line in credits if line.get("recipient") == "buyer"), ZERO
            )

            timeline, financing_cost, peak_funding = _seller_cash_timeline(
                scenario, invoice_model, costs, taxes, credits
            )
            seller_profit_before_share = money(
                invoice_model
                + seller_credits
                + seller_tax_recoverable
                - seller_costs
                - seller_tax_cash
                - financing_cost
            )
            share_config = scenario.get("profit_share", {})
            share_fraction = D(share_config.get("fraction", ZERO))
            retained_floor = D(
                share_config.get("minimum_retained_profit_model_currency", ZERO)
            )
            share_base = max(ZERO, seller_profit_before_share - retained_floor)
            profit_share = money(share_base * share_fraction)
            seller_profit_after_share = money(seller_profit_before_share - profit_share)
            seller_margin = safe_div(seller_profit_after_share, invoice_model)

            buyer_cash_landed = money(invoice_model + buyer_costs + buyer_tax_cash)
            buyer_economic_landed = money(
                buyer_cash_landed - buyer_tax_recoverable - buyer_credits
            )
            basis_units = {
                basis: basis_quantity(basis, mass_balance)
                for basis in (
                    "per_net_fish_kg",
                    "per_glazed_product_kg",
                    "per_packaged_gross_kg",
                    "per_carton",
                    "per_container",
                    "per_shipment",
                )
            }
            unit_economics: dict[str, dict[str, Decimal]] = {}
            for basis, quantity in basis_units.items():
                unit_economics[basis] = {
                    "seller_invoice_model": safe_div(invoice_model, quantity),
                    "seller_profit_after_share_model": safe_div(seller_profit_after_share, quantity),
                    "buyer_cash_landed_model": safe_div(buyer_cash_landed, quantity),
                    "buyer_economic_landed_model": safe_div(buyer_economic_landed, quantity),
                }

            flags: list[dict[str, str]] = []
            if D(mass_balance["payload_utilization_fraction"]) < D("0.70"):
                flags.append(
                    {
                        "severity": "warning",
                        "code": "LOW_PAYLOAD_UTILIZATION",
                        "message": "packaged payload uses less than 70% of available container payload",
                    }
                )
            if seller_profit_after_share < ZERO:
                flags.append(
                    {
                        "severity": "blocker",
                        "code": "NEGATIVE_SELLER_PROFIT",
                        "message": "seller profit after financing and profit share is negative",
                    }
                )
            target_margin = D(scenario.get("targets", {}).get("seller_margin_fraction", ZERO))
            if seller_margin < target_margin:
                flags.append(
                    {
                        "severity": "warning",
                        "code": "TARGET_MARGIN_NOT_MET",
                        "message": "seller margin is below the declared scenario target",
                    }
                )
            if buyer_tax_recoverable > ZERO:
                flags.append(
                    {
                        "severity": "info",
                        "code": "BUYER_CASH_ECONOMIC_GAP",
                        "message": "buyer cash landed cost exceeds economic landed cost because recoverable tax is modelled",
                    }
                )
            flags.extend(
                {
                    "severity": "warning",
                    "code": "CONTRACT_REVIEW_REQUIRED",
                    "message": warning,
                }
                for warning in responsibility_warnings
            )

            return {
                "scenario_id": scenario["scenario_id"],
                "model_currency": scenario["currencies"]["model_currency"],
                "quote_currency": scenario["quote"]["currency"],
                "mass_balance": mass_balance,
                "invoice": {
                    "price_basis": scenario["quote"]["price_basis"],
                    "unit_price_quote_currency": D(scenario["quote"]["unit_price"]),
                    "invoice_quote_currency": invoice_quote,
                    "invoice_model_currency": invoice_model,
                },
                "contract_profile": {
                    "incoterm_label": scenario["contract_profile"]["incoterm_label"],
                    "cost_responsibility": mapping,
                    "risk_transfer_modelled": False,
                },
                "customs_value_model_currency": customs_value_model,
                "cost_lines": costs,
                "tax_lines": taxes,
                "credit_lines": credits,
                "cash_timeline": timeline,
                "seller": {
                    "invoice_revenue_model": invoice_model,
                    "seller_costs_model": money(seller_costs),
                    "seller_tax_cash_model": money(seller_tax_cash),
                    "seller_tax_recoverable_model": money(seller_tax_recoverable),
                    "seller_credits_model": money(seller_credits),
                    "financing_cost_model": financing_cost,
                    "peak_working_capital_need_model": peak_funding,
                    "profit_before_share_model": seller_profit_before_share,
                    "profit_share_model": profit_share,
                    "profit_after_share_model": seller_profit_after_share,
                    "margin_after_share_fraction": seller_margin,
                },
                "buyer": {
                    "invoice_model": invoice_model,
                    "buyer_costs_model": money(buyer_costs),
                    "buyer_tax_cash_model": money(buyer_tax_cash),
                    "buyer_tax_recoverable_model": money(buyer_tax_recoverable),
                    "buyer_credits_model": money(buyer_credits),
                    "cash_landed_cost_model": buyer_cash_landed,
                    "economic_landed_cost_model": buyer_economic_landed,
                },
                "unit_economics": unit_economics,
                "flags": flags,
                "validation_messages": messages,
            }


        def solve_quote_price(
            scenario: dict[str, Any],
            *,
            target_margin: Decimal | None = None,
            tolerance: Decimal = Decimal("0.0000001"),
        ) -> Decimal:
            working = deepcopy(scenario)
            current = D(working["quote"]["unit_price"])

            def objective(price: Decimal) -> Decimal:
                working["quote"]["unit_price"] = str(price)
                result = simulate_once(working)
                profit = D(result["seller"]["profit_after_share_model"])
                if target_margin is None:
                    return profit
                invoice = D(result["invoice"]["invoice_model_currency"])
                return profit - D(target_margin) * invoice

            low = ZERO
            high = max(D("1"), current * D("2"))
            while objective(high) < ZERO and high < D("1000000"):
                high *= D("2")
            if objective(high) < ZERO:
                raise ValueError("could not bracket a quote price that satisfies the target")
            for _ in range(160):
                middle = (low + high) / D("2")
                value = objective(middle)
                if abs(value) <= tolerance:
                    return middle
                if value >= ZERO:
                    high = middle
                else:
                    low = middle
            return (low + high) / D("2")


        def simulate(scenario: dict[str, Any]) -> dict[str, Any]:
            result = simulate_once(scenario)
            target_margin = D(scenario.get("targets", {}).get("seller_margin_fraction", ZERO))
            result["quote_targets"] = {
                "break_even_unit_price_quote_currency": solve_quote_price(scenario),
                "target_margin_fraction": target_margin,
                "target_margin_unit_price_quote_currency": solve_quote_price(
                    scenario, target_margin=target_margin
                ),
            }
            return result
    ''',
    "src/golden_pompano_export_simulator/sensitivity.py": r'''
        """One-way, two-way and scenario comparison analysis."""

        from __future__ import annotations

        from copy import deepcopy
        from decimal import Decimal
        from typing import Any

        from .decimal_utils import D, ONE
        from .economics import simulate_once


        def _resolve_collection(payload: dict[str, Any], prefix: str) -> list[dict[str, Any]]:
            mapping = {"cost": "costs", "tax": "taxes", "credit": "credits"}
            return payload[mapping[prefix]]


        def get_path(payload: dict[str, Any], path: str) -> Decimal:
            if ":" in path:
                prefix, remainder = path.split(":", 1)
                item_id, field = remainder.split(".", 1)
                collection = _resolve_collection(payload, prefix)
                item = next(row for row in collection if row["id"] == item_id)
                return D(item[field])
            cursor: Any = payload
            for part in path.split("."):
                cursor = cursor[part]
            return D(cursor)


        def set_path(payload: dict[str, Any], path: str, value: Decimal) -> None:
            if ":" in path:
                prefix, remainder = path.split(":", 1)
                item_id, field = remainder.split(".", 1)
                collection = _resolve_collection(payload, prefix)
                item = next(row for row in collection if row["id"] == item_id)
                item[field] = str(value)
                return
            parts = path.split(".")
            cursor: Any = payload
            for part in parts[:-1]:
                cursor = cursor[part]
            cursor[parts[-1]] = str(value)


        def metric_row(result: dict[str, Any]) -> dict[str, Any]:
            return {
                "invoice_model": result["invoice"]["invoice_model_currency"],
                "seller_profit_model": result["seller"]["profit_after_share_model"],
                "seller_margin_fraction": result["seller"]["margin_after_share_fraction"],
                "buyer_cash_landed_model": result["buyer"]["cash_landed_cost_model"],
                "buyer_economic_landed_model": result["buyer"]["economic_landed_cost_model"],
                "buyer_economic_per_net_fish_kg": result["unit_economics"]["per_net_fish_kg"]["buyer_economic_landed_model"],
                "payload_utilization_fraction": result["mass_balance"]["payload_utilization_fraction"],
                "peak_working_capital_need_model": result["seller"]["peak_working_capital_need_model"],
            }


        def run_sensitivity(scenario: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
            config = scenario.get("analysis", {})
            one_way_rows: list[dict[str, Any]] = []
            for spec in config.get("one_way", []):
                path = spec["path"]
                base = get_path(scenario, path)
                for delta_raw in spec.get("deltas", ["-0.10", "-0.05", "0", "0.05", "0.10"]):
                    delta = D(delta_raw)
                    candidate = deepcopy(scenario)
                    set_path(candidate, path, base * (ONE + delta))
                    result = simulate_once(candidate)
                    one_way_rows.append(
                        {
                            "path": path,
                            "delta_fraction": delta,
                            "base_value": base,
                            "scenario_value": get_path(candidate, path),
                            **metric_row(result),
                        }
                    )

            two_way_rows: list[dict[str, Any]] = []
            two_way = config.get("two_way")
            if two_way:
                x_path = two_way["x_path"]
                y_path = two_way["y_path"]
                x_base = get_path(scenario, x_path)
                y_base = get_path(scenario, y_path)
                for x_delta_raw in two_way.get("x_deltas", ["-0.10", "0", "0.10"]):
                    for y_delta_raw in two_way.get("y_deltas", ["-0.10", "0", "0.10"]):
                        x_delta = D(x_delta_raw)
                        y_delta = D(y_delta_raw)
                        candidate = deepcopy(scenario)
                        set_path(candidate, x_path, x_base * (ONE + x_delta))
                        set_path(candidate, y_path, y_base * (ONE + y_delta))
                        result = simulate_once(candidate)
                        two_way_rows.append(
                            {
                                "x_path": x_path,
                                "x_delta_fraction": x_delta,
                                "x_value": get_path(candidate, x_path),
                                "y_path": y_path,
                                "y_delta_fraction": y_delta,
                                "y_value": get_path(candidate, y_path),
                                **metric_row(result),
                            }
                        )
            return one_way_rows, two_way_rows


        def compare_scenarios(
            baseline: dict[str, Any], candidate: dict[str, Any]
        ) -> dict[str, Any]:
            base_result = simulate_once(baseline)
            candidate_result = simulate_once(candidate)
            base_metrics = metric_row(base_result)
            candidate_metrics = metric_row(candidate_result)
            deltas = {
                key: D(candidate_metrics[key]) - D(base_metrics[key])
                for key in base_metrics
            }
            return {
                "baseline_scenario_id": baseline["scenario_id"],
                "candidate_scenario_id": candidate["scenario_id"],
                "baseline": base_metrics,
                "candidate": candidate_metrics,
                "delta_candidate_minus_baseline": deltas,
                "interpretation": (
                    "Metric deltas are conditional on the declared assumptions. "
                    "They are not forecasts, legal conclusions or market quotes."
                ),
            }
    ''',
    "src/golden_pompano_export_simulator/io.py": r'''
        """Deterministic JSON/CSV helpers."""

        from __future__ import annotations

        import csv
        import json
        from decimal import Decimal
        from pathlib import Path
        from typing import Any, Iterable, Mapping, Sequence

        from .canonical import normalize, pretty_json, sha256_file


        def load_json(path: str | Path) -> dict[str, Any]:
            payload = json.loads(Path(path).read_text(encoding="utf-8"))
            if not isinstance(payload, dict):
                raise ValueError(f"{path} must contain a JSON object")
            return payload


        def write_json(path: str | Path, payload: Any) -> None:
            destination = Path(path)
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(pretty_json(payload), encoding="utf-8")


        def _csv_value(value: Any) -> Any:
            normalized = normalize(value)
            if isinstance(normalized, (list, dict)):
                return json.dumps(normalized, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
            if isinstance(value, Decimal):
                return normalized
            if isinstance(normalized, bool):
                return "true" if normalized else "false"
            return normalized


        def write_csv(
            path: str | Path,
            rows: Iterable[Mapping[str, Any]],
            fieldnames: Sequence[str],
        ) -> None:
            destination = Path(path)
            destination.parent.mkdir(parents=True, exist_ok=True)
            with destination.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
                writer.writeheader()
                for row in rows:
                    writer.writerow({key: _csv_value(row.get(key)) for key in fieldnames})


        __all__ = ["load_json", "write_json", "write_csv", "sha256_file"]
    ''',
    "src/golden_pompano_export_simulator/sqlite_export.py": r'''
        """Deterministic relational export and semantic digest."""

        from __future__ import annotations

        import json
        import sqlite3
        from pathlib import Path
        from typing import Any

        from .canonical import normalize, sha256_json

        TABLES = (
            "metadata",
            "mass_balance",
            "size_grades",
            "cost_lines",
            "tax_lines",
            "cash_timeline",
            "sensitivity",
            "two_way_grid",
        )


        def export_sqlite(
            path: str | Path,
            result: dict[str, Any],
            one_way: list[dict[str, Any]],
            two_way: list[dict[str, Any]],
        ) -> str:
            destination = Path(path)
            if destination.exists():
                destination.unlink()
            connection = sqlite3.connect(destination)
            try:
                connection.executescript(
                    """
                    PRAGMA journal_mode=OFF;
                    PRAGMA synchronous=OFF;
                    CREATE TABLE metadata (key TEXT PRIMARY KEY, value TEXT NOT NULL);
                    CREATE TABLE mass_balance (key TEXT PRIMARY KEY, value TEXT NOT NULL);
                    CREATE TABLE size_grades (position INTEGER PRIMARY KEY, payload TEXT NOT NULL);
                    CREATE TABLE cost_lines (position INTEGER PRIMARY KEY, payload TEXT NOT NULL);
                    CREATE TABLE tax_lines (position INTEGER PRIMARY KEY, payload TEXT NOT NULL);
                    CREATE TABLE cash_timeline (position INTEGER PRIMARY KEY, payload TEXT NOT NULL);
                    CREATE TABLE sensitivity (position INTEGER PRIMARY KEY, payload TEXT NOT NULL);
                    CREATE TABLE two_way_grid (position INTEGER PRIMARY KEY, payload TEXT NOT NULL);
                    """
                )
                metadata = {
                    "scenario_id": result["scenario_id"],
                    "model_currency": result["model_currency"],
                    "quote_currency": result["quote_currency"],
                    "seller_profit_after_share_model": result["seller"]["profit_after_share_model"],
                    "buyer_economic_landed_cost_model": result["buyer"]["economic_landed_cost_model"],
                }
                connection.executemany(
                    "INSERT INTO metadata(key, value) VALUES (?, ?)",
                    [(key, json.dumps(normalize(value), ensure_ascii=False, sort_keys=True)) for key, value in sorted(metadata.items())],
                )
                mass_payload = {key: value for key, value in result["mass_balance"].items() if key != "size_grades"}
                connection.executemany(
                    "INSERT INTO mass_balance(key, value) VALUES (?, ?)",
                    [(key, json.dumps(normalize(value), ensure_ascii=False, sort_keys=True)) for key, value in sorted(mass_payload.items())],
                )
                _insert_payloads(connection, "size_grades", result["mass_balance"]["size_grades"])
                _insert_payloads(connection, "cost_lines", result["cost_lines"])
                _insert_payloads(connection, "tax_lines", result["tax_lines"])
                _insert_payloads(connection, "cash_timeline", result["cash_timeline"])
                _insert_payloads(connection, "sensitivity", one_way)
                _insert_payloads(connection, "two_way_grid", two_way)
                connection.commit()
                connection.execute("VACUUM")
            finally:
                connection.close()
            return semantic_digest(destination)


        def _insert_payloads(connection: sqlite3.Connection, table: str, rows: list[dict[str, Any]]) -> None:
            connection.executemany(
                f"INSERT INTO {table}(position, payload) VALUES (?, ?)",
                [
                    (
                        index,
                        json.dumps(normalize(row), ensure_ascii=False, sort_keys=True, separators=(",", ":")),
                    )
                    for index, row in enumerate(rows)
                ],
            )


        def semantic_digest(path: str | Path) -> str:
            connection = sqlite3.connect(path)
            try:
                payload: dict[str, Any] = {}
                for table in TABLES:
                    columns = [row[1] for row in connection.execute(f"PRAGMA table_info({table})")]
                    rows = connection.execute(f"SELECT * FROM {table} ORDER BY 1").fetchall()
                    payload[table] = {"columns": columns, "rows": rows}
                return sha256_json(payload)
            finally:
                connection.close()
    ''',
    "src/golden_pompano_export_simulator/report.py": r'''
        """Human-readable Markdown and self-contained HTML reports."""

        from __future__ import annotations

        from html import escape
        from pathlib import Path
        from typing import Any

        from .decimal_utils import D, decstr


        def _money(value: Any, currency: str) -> str:
            return f"{currency} {D(value):,.2f}"


        def _pct(value: Any) -> str:
            return f"{D(value) * D('100'):.2f}%"


        def render_markdown(
            path: str | Path,
            scenario: dict[str, Any],
            result: dict[str, Any],
            one_way: list[dict[str, Any]],
            two_way: list[dict[str, Any]],
        ) -> None:
            model = result["model_currency"]
            mass = result["mass_balance"]
            seller = result["seller"]
            buyer = result["buyer"]
            targets = result["quote_targets"]
            lines = [
                f"# Export Simulation — {result['scenario_id']}",
                "",
                "> All values are conditional on the supplied assumptions. This report is not a current market quote, legal advice, customs advice, tax advice, veterinary advice or a promise of profit.",
                "",
                "## Decision snapshot",
                "",
                f"- Seller profit after financing and profit share: **{_money(seller['profit_after_share_model'], model)}**",
                f"- Seller margin after profit share: **{_pct(seller['margin_after_share_fraction'])}**",
                f"- Buyer landed cash cost: **{_money(buyer['cash_landed_cost_model'], model)}**",
                f"- Buyer landed economic cost: **{_money(buyer['economic_landed_cost_model'], model)}**",
                f"- Payload utilization: **{_pct(mass['payload_utilization_fraction'])}**",
                "",
                "## Mass basis",
                "",
                "| Measure | Value |",
                "|---|---:|",
                f"| Net fish mass | {D(mass['shipped_net_fish_kg']):,.4f} kg |",
                f"| Ice glaze mass | {D(mass['ice_mass_kg']):,.4f} kg |",
                f"| Glazed product mass | {D(mass['glazed_product_kg']):,.4f} kg |",
                f"| Packaging mass | {D(mass['packaging_mass_kg']):,.4f} kg |",
                f"| Packaged gross shipment mass | {D(mass['packaged_gross_kg']):,.4f} kg |",
                f"| Cartons / pallets / containers | {mass['carton_count']} / {mass['pallet_count']} / {mass['container_count']} |",
                "",
                "The model therefore reports every unit price against an explicit denominator. A price per net-fish kilogram is not interchangeable with a price per glazed-product kilogram or packaged-gross kilogram.",
                "",
                "## Seller economics",
                "",
                "| Line | Value |",
                "|---|---:|",
                f"| Invoice revenue | {_money(seller['invoice_revenue_model'], model)} |",
                f"| Seller operating/trade costs | {_money(seller['seller_costs_model'], model)} |",
                f"| Seller tax cash outflow | {_money(seller['seller_tax_cash_model'], model)} |",
                f"| Recoverable seller tax | {_money(seller['seller_tax_recoverable_model'], model)} |",
                f"| Seller credits | {_money(seller['seller_credits_model'], model)} |",
                f"| Financing cost | {_money(seller['financing_cost_model'], model)} |",
                f"| Peak working-capital need | {_money(seller['peak_working_capital_need_model'], model)} |",
                f"| Profit share | {_money(seller['profit_share_model'], model)} |",
                f"| Profit after share | {_money(seller['profit_after_share_model'], model)} |",
                "",
                "## Buyer landed cost",
                "",
                "| Line | Value |",
                "|---|---:|",
                f"| Invoice | {_money(buyer['invoice_model'], model)} |",
                f"| Buyer-paid trade costs | {_money(buyer['buyer_costs_model'], model)} |",
                f"| Import/other tax cash outflow | {_money(buyer['buyer_tax_cash_model'], model)} |",
                f"| Recoverable buyer tax | {_money(buyer['buyer_tax_recoverable_model'], model)} |",
                f"| Buyer credits | {_money(buyer['buyer_credits_model'], model)} |",
                f"| Landed cash cost | {_money(buyer['cash_landed_cost_model'], model)} |",
                f"| Landed economic cost | {_money(buyer['economic_landed_cost_model'], model)} |",
                "",
                "## Quote targets",
                "",
                f"- Break-even unit price ({scenario['quote']['price_basis']}, {scenario['quote']['currency']}): **{D(targets['break_even_unit_price_quote_currency']):,.6f}**",
                f"- Unit price for target seller margin {_pct(targets['target_margin_fraction'])}: **{D(targets['target_margin_unit_price_quote_currency']):,.6f}**",
                "",
                "## Sensitivity coverage",
                "",
                f"- One-way rows: {len(one_way)}",
                f"- Two-way rows: {len(two_way)}",
                "",
                "## Contract and compliance boundary",
                "",
                f"- Incoterm label: `{scenario['contract_profile']['incoterm_label']}`",
                "- The profile allocates modelled cost lines only.",
                "- It does not determine risk transfer, title, customs eligibility, import licensing, tax recoverability or legal liability.",
                "- Every duty, tax, exchange rate, rebate, recovery and logistics value must be confirmed for the actual contract and date.",
                "",
                "## Flags",
                "",
            ]
            for flag in result["flags"]:
                lines.append(f"- **{flag['severity'].upper()} — {flag['code']}**: {flag['message']}")
            path = Path(path)
            path.write_text("\n".join(lines) + "\n", encoding="utf-8")


        def render_html(
            path: str | Path,
            scenario: dict[str, Any],
            result: dict[str, Any],
            one_way: list[dict[str, Any]],
            two_way: list[dict[str, Any]],
        ) -> None:
            model = escape(result["model_currency"])
            mass = result["mass_balance"]
            seller = result["seller"]
            buyer = result["buyer"]
            flags = "".join(
                f"<li><strong>{escape(flag['severity'].upper())} · {escape(flag['code'])}</strong> — {escape(flag['message'])}</li>"
                for flag in result["flags"]
            )
            basis_cards = "".join(
                f"<tr><td>{escape(name.replace('_', ' ').title())}</td><td>{escape(decstr(value, places=4))}</td></tr>"
                for name, value in (
                    ("net fish kg", mass["shipped_net_fish_kg"]),
                    ("ice glaze kg", mass["ice_mass_kg"]),
                    ("glazed product kg", mass["glazed_product_kg"]),
                    ("packaging kg", mass["packaging_mass_kg"]),
                    ("packaged gross kg", mass["packaged_gross_kg"]),
                )
            )
            html = f"""<!doctype html>
            <html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
            <title>{escape(result['scenario_id'])} — export simulation</title>
            <style>
            :root{{--ink:#17211b;--muted:#657067;--paper:#f5f2e9;--card:#fffdf7;--line:#d9d1bf;--accent:#1f6b55;--warn:#9a5d1d}}
            *{{box-sizing:border-box}} body{{margin:0;background:var(--paper);color:var(--ink);font:16px/1.55 system-ui,-apple-system,Segoe UI,sans-serif}}
            main{{max-width:1120px;margin:auto;padding:36px 22px 70px}} h1{{font-size:clamp(32px,5vw,58px);line-height:1.04;margin:0 0 12px}}
            .eyebrow{{letter-spacing:.14em;text-transform:uppercase;color:var(--accent);font-weight:750;font-size:12px}}
            .notice{{border-left:5px solid var(--warn);padding:12px 16px;background:#fff7e8;margin:22px 0}}
            .grid{{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px;margin:24px 0}} .card{{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:18px}}
            .label{{color:var(--muted);font-size:13px}} .value{{font-size:24px;font-weight:800;margin-top:4px}} section{{margin-top:34px}}
            table{{width:100%;border-collapse:collapse;background:var(--card);border:1px solid var(--line)}} th,td{{padding:10px 12px;border-bottom:1px solid var(--line);text-align:left}} td:last-child,th:last-child{{text-align:right}}
            code{{background:#e8e2d4;padding:2px 5px;border-radius:4px}} footer{{margin-top:42px;color:var(--muted);font-size:13px}}
            @media(max-width:820px){{.grid{{grid-template-columns:1fr 1fr}}}} @media(max-width:520px){{.grid{{grid-template-columns:1fr}} main{{padding:24px 14px}}}}
            </style></head><body><main>
            <div class="eyebrow">Synthetic decision model · {escape(scenario['as_of'])}</div>
            <h1>Golden pompano export economics</h1>
            <p>Scenario <code>{escape(result['scenario_id'])}</code> separates fish, glaze, packaging, seller economics and buyer landed cost.</p>
            <div class="notice"><strong>Assumption model, not a quote.</strong> Values are synthetic unless the operator supplies private inputs. Incoterms, customs, tax and recoverability require contract-specific professional review.</div>
            <div class="grid">
              <div class="card"><div class="label">Seller profit</div><div class="value">{model} {D(seller['profit_after_share_model']):,.2f}</div></div>
              <div class="card"><div class="label">Seller margin</div><div class="value">{D(seller['margin_after_share_fraction'])*D('100'):.2f}%</div></div>
              <div class="card"><div class="label">Buyer economic landed</div><div class="value">{model} {D(buyer['economic_landed_cost_model']):,.2f}</div></div>
              <div class="card"><div class="label">Payload utilization</div><div class="value">{D(mass['payload_utilization_fraction'])*D('100'):.2f}%</div></div>
            </div>
            <section><h2>Mass basis</h2><table><thead><tr><th>Measure</th><th>Value</th></tr></thead><tbody>{basis_cards}</tbody></table>
            <p>{mass['carton_count']} cartons · {mass['pallet_count']} pallets · {mass['container_count']} container(s). The denominator of every unit price is explicit.</p></section>
            <section><h2>Seller and buyer bridge</h2><table><tbody>
              <tr><td>Invoice revenue / cost</td><td>{model} {D(seller['invoice_revenue_model']):,.2f}</td></tr>
              <tr><td>Seller costs</td><td>{model} {D(seller['seller_costs_model']):,.2f}</td></tr>
              <tr><td>Financing cost</td><td>{model} {D(seller['financing_cost_model']):,.2f}</td></tr>
              <tr><td>Profit share</td><td>{model} {D(seller['profit_share_model']):,.2f}</td></tr>
              <tr><td>Buyer landed cash</td><td>{model} {D(buyer['cash_landed_cost_model']):,.2f}</td></tr>
              <tr><td>Recoverable buyer tax</td><td>{model} {D(buyer['buyer_tax_recoverable_model']):,.2f}</td></tr>
              <tr><td>Buyer economic landed</td><td>{model} {D(buyer['economic_landed_cost_model']):,.2f}</td></tr>
            </tbody></table></section>
            <section><h2>Analysis coverage</h2><p>{len(one_way)} one-way observations and {len(two_way)} two-way observations were generated from the declared scenario.</p></section>
            <section><h2>Review flags</h2><ul>{flags}</ul></section>
            <footer>Generated by Golden Pompano Export Simulator v0.1.0. No network request, live tariff lookup or legal inference is performed.</footer>
            </main></body></html>"""
            Path(path).write_text(html, encoding="utf-8")
    ''',
    "src/golden_pompano_export_simulator/audit.py": r'''
        """Run manifests, hash-chained events and tamper verification."""

        from __future__ import annotations

        import json
        from pathlib import Path
        from typing import Any

        from .canonical import pretty_json, sha256_file, sha256_json
        from .sqlite_export import semantic_digest

        MANIFEST_FILES = {"artifact_manifest.json", "run_manifest.json"}


        def build_event_chain(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
            previous = "0" * 64
            chain: list[dict[str, Any]] = []
            for sequence, event in enumerate(events, start=1):
                unsigned = {
                    "sequence": sequence,
                    "event_type": event["event_type"],
                    "payload": event.get("payload", {}),
                    "previous_hash": previous,
                }
                event_hash = sha256_json(unsigned)
                signed = {**unsigned, "event_hash": event_hash}
                chain.append(signed)
                previous = event_hash
            return chain


        def write_events(path: str | Path, events: list[dict[str, Any]]) -> str:
            chain = build_event_chain(events)
            destination = Path(path)
            destination.write_text(
                "".join(json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n" for row in chain),
                encoding="utf-8",
            )
            return chain[-1]["event_hash"] if chain else "0" * 64


        def verify_event_chain(path: str | Path) -> tuple[bool, str]:
            rows = [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]
            previous = "0" * 64
            for expected_sequence, row in enumerate(rows, start=1):
                if row.get("sequence") != expected_sequence or row.get("previous_hash") != previous:
                    return False, "event sequence or previous hash mismatch"
                unsigned = {key: row[key] for key in ("sequence", "event_type", "payload", "previous_hash")}
                if sha256_json(unsigned) != row.get("event_hash"):
                    return False, "event content hash mismatch"
                previous = row["event_hash"]
            return True, previous


        def artifact_record(path: Path, root: Path) -> dict[str, Any]:
            relative = path.relative_to(root).as_posix()
            if path.name == "audit.sqlite":
                return {
                    "path": relative,
                    "digest_kind": "sqlite_semantic_sha256",
                    "sha256": semantic_digest(path),
                    "size_bytes": path.stat().st_size,
                }
            return {
                "path": relative,
                "digest_kind": "file_sha256",
                "sha256": sha256_file(path),
                "size_bytes": path.stat().st_size,
            }


        def write_manifests(
            run_dir: str | Path,
            *,
            scenario_sha256: str,
            generated_at: str,
            final_event_hash: str,
        ) -> None:
            root = Path(run_dir)
            files = sorted(
                path
                for path in root.rglob("*")
                if path.is_file() and path.name not in MANIFEST_FILES
            )
            artifact_manifest = {
                "schema_version": "1.0",
                "artifacts": [artifact_record(path, root) for path in files],
            }
            (root / "artifact_manifest.json").write_text(pretty_json(artifact_manifest), encoding="utf-8")
            run_manifest = {
                "schema_version": "1.0",
                "package_version": "0.1.0",
                "generated_at": generated_at,
                "scenario_sha256": scenario_sha256,
                "artifact_manifest_sha256": sha256_file(root / "artifact_manifest.json"),
                "final_event_hash": final_event_hash,
                "declared_file_count": len(files) + 2,
            }
            (root / "run_manifest.json").write_text(pretty_json(run_manifest), encoding="utf-8")


        def verify_run(run_dir: str | Path) -> dict[str, Any]:
            root = Path(run_dir)
            errors: list[str] = []
            for required in ("artifact_manifest.json", "run_manifest.json", "events.jsonl", "scenario_snapshot.json"):
                if not (root / required).is_file():
                    errors.append(f"missing required file: {required}")
            if errors:
                return {"valid": False, "errors": errors}
            artifacts = json.loads((root / "artifact_manifest.json").read_text(encoding="utf-8"))
            run_manifest = json.loads((root / "run_manifest.json").read_text(encoding="utf-8"))
            declared = {row["path"]: row for row in artifacts.get("artifacts", [])}
            actual = {
                path.relative_to(root).as_posix()
                for path in root.rglob("*")
                if path.is_file() and path.name not in MANIFEST_FILES
            }
            if set(declared) != actual:
                errors.append(
                    f"artifact set mismatch: missing={sorted(set(declared)-actual)} extra={sorted(actual-set(declared))}"
                )
            for relative, record in declared.items():
                path = root / relative
                if not path.is_file():
                    continue
                digest = semantic_digest(path) if record["digest_kind"] == "sqlite_semantic_sha256" else sha256_file(path)
                if digest != record["sha256"]:
                    errors.append(f"artifact digest mismatch: {relative}")
            if sha256_file(root / "artifact_manifest.json") != run_manifest.get("artifact_manifest_sha256"):
                errors.append("artifact manifest digest mismatch")
            if sha256_file(root / "scenario_snapshot.json") != run_manifest.get("scenario_sha256"):
                errors.append("scenario snapshot digest mismatch")
            chain_ok, final_hash = verify_event_chain(root / "events.jsonl")
            if not chain_ok:
                errors.append(final_hash)
            elif final_hash != run_manifest.get("final_event_hash"):
                errors.append("final event hash mismatch")
            if run_manifest.get("declared_file_count") != len(actual) + 2:
                errors.append("declared file count mismatch")
            return {"valid": not errors, "errors": errors, "artifact_count": len(actual)}
    ''',
    "src/golden_pompano_export_simulator/cli.py": r'''
        """Command-line interface."""

        from __future__ import annotations

        import argparse
        import json
        import shutil
        import sys
        from pathlib import Path
        from typing import Any

        from . import __version__
        from .audit import verify_run, write_events, write_manifests
        from .canonical import normalize, pretty_json, sha256_file
        from .economics import simulate, simulate_once
        from .io import load_json, write_csv, write_json
        from .report import render_html, render_markdown
        from .sensitivity import compare_scenarios, run_sensitivity
        from .sqlite_export import export_sqlite
        from .validation import has_errors, parse_aware_time, validate_scenario


        def build_parser() -> argparse.ArgumentParser:
            parser = argparse.ArgumentParser(
                prog="gpes",
                description="Assumption-driven export quotation and landed-cost simulator.",
            )
            parser.add_argument("--version", action="version", version=__version__)
            commands = parser.add_subparsers(dest="command", required=True)

            validate = commands.add_parser("validate", help="Validate a scenario without calculating economics.")
            validate.add_argument("scenario", type=Path)
            validate.add_argument("--public-fixture", action="store_true")
            validate.add_argument("--json-output", type=Path)

            simulate_command = commands.add_parser("simulate", help="Generate a complete auditable simulation bundle.")
            simulate_command.add_argument("scenario", type=Path)
            simulate_command.add_argument("--output-dir", type=Path, required=True)
            simulate_command.add_argument("--fixed-time", required=True, help="Timezone-aware ISO-8601 generation time.")

            targets = commands.add_parser("quote-targets", help="Print break-even and target-margin quote prices.")
            targets.add_argument("scenario", type=Path)
            targets.add_argument("--json", action="store_true")

            compare = commands.add_parser("compare", help="Compare two scenario files.")
            compare.add_argument("--baseline", type=Path, required=True)
            compare.add_argument("--candidate", type=Path, required=True)
            compare.add_argument("--output", type=Path)

            verify = commands.add_parser("verify", help="Verify an existing run bundle and its hash chain.")
            verify.add_argument("run_dir", type=Path)
            verify.add_argument("--json", action="store_true")

            init = commands.add_parser("init", help="Create a synthetic starter scenario; preview by default.")
            init.add_argument("--target", type=Path, required=True)
            init.add_argument("--apply", action="store_true")
            return parser


        def _empty_output(path: Path) -> None:
            if path.exists() and any(path.iterdir()):
                raise ValueError(f"output directory must be empty or absent: {path}")
            path.mkdir(parents=True, exist_ok=True)


        def _print_messages(messages: list[dict[str, str]]) -> None:
            for message in messages:
                print(
                    f"[{message['severity'].upper()}] {message['code']} {message['path']}: {message['message']}"
                )
            errors = sum(message["severity"] == "error" for message in messages)
            warnings = sum(message["severity"] == "warning" for message in messages)
            print(f"Validation summary: {errors} error(s), {warnings} warning(s)")


        def command_validate(args: argparse.Namespace) -> int:
            payload = load_json(args.scenario)
            messages = validate_scenario(payload, public_fixture=args.public_fixture)
            _print_messages(messages)
            if args.json_output:
                write_json(args.json_output, messages)
            return 2 if has_errors(messages) else 0


        def _write_run(
            payload: dict[str, Any],
            output_dir: Path,
            fixed_time: str,
        ) -> dict[str, Any]:
            parse_aware_time(fixed_time)
            _empty_output(output_dir)
            messages = validate_scenario(payload)
            write_json(output_dir / "validation.json", messages)
            if has_errors(messages):
                raise ValueError("scenario validation failed")
            write_json(output_dir / "scenario_snapshot.json", payload)
            result = simulate(payload)
            one_way, two_way = run_sensitivity(payload)
            write_json(output_dir / "summary.json", result)

            mass_rows = [
                {"measure": key, "value": value}
                for key, value in result["mass_balance"].items()
                if key != "size_grades"
            ]
            write_csv(output_dir / "mass_balance.csv", mass_rows, ["measure", "value"])
            write_csv(
                output_dir / "size_grades.csv",
                result["mass_balance"]["size_grades"],
                [
                    "id",
                    "min_grams",
                    "max_grams",
                    "share_of_net_fish",
                    "allocated_net_fish_kg",
                    "estimated_fish_count_at_midpoint",
                ],
            )
            write_csv(
                output_dir / "cost_lines.csv",
                result["cost_lines"],
                [
                    "id",
                    "label",
                    "stage",
                    "payer",
                    "payer_resolved",
                    "basis",
                    "rate",
                    "currency",
                    "cash_day_relative_to_shipment",
                    "amount_model",
                ],
            )
            write_csv(
                output_dir / "tax_lines.csv",
                result["tax_lines"],
                [
                    "id",
                    "label",
                    "payer",
                    "basis",
                    "rate",
                    "tax_base_model",
                    "amount_model",
                    "recoverable_fraction",
                    "recoverable_amount_model",
                    "nonrecoverable_amount_model",
                ],
            )
            write_csv(
                output_dir / "cash_timeline.csv",
                result["cash_timeline"],
                [
                    "day",
                    "event",
                    "cash_flow_model",
                    "running_cash_balance_model",
                    "days_to_next_event",
                    "financing_cost_accrued_model",
                ],
            )
            one_way_fields = list(one_way[0]) if one_way else ["path"]
            two_way_fields = list(two_way[0]) if two_way else ["x_path"]
            write_csv(output_dir / "sensitivity.csv", one_way, one_way_fields)
            write_csv(output_dir / "two_way_grid.csv", two_way, two_way_fields)
            render_markdown(output_dir / "report.md", payload, result, one_way, two_way)
            render_html(output_dir / "report.html", payload, result, one_way, two_way)
            sqlite_digest = export_sqlite(output_dir / "audit.sqlite", result, one_way, two_way)
            events = [
                {"event_type": "scenario_validated", "payload": {"message_count": len(messages)}},
                {"event_type": "mass_balance_calculated", "payload": {"cartons": result["mass_balance"]["carton_count"]}},
                {"event_type": "seller_economics_calculated", "payload": {"profit": result["seller"]["profit_after_share_model"]}},
                {"event_type": "buyer_landed_cost_calculated", "payload": {"economic_cost": result["buyer"]["economic_landed_cost_model"]}},
                {"event_type": "sensitivity_completed", "payload": {"one_way": len(one_way), "two_way": len(two_way)}},
                {"event_type": "sqlite_exported", "payload": {"semantic_sha256": sqlite_digest}},
                {"event_type": "run_completed", "payload": {"scenario_id": payload["scenario_id"]}},
            ]
            final_hash = write_events(output_dir / "events.jsonl", events)
            write_manifests(
                output_dir,
                scenario_sha256=sha256_file(output_dir / "scenario_snapshot.json"),
                generated_at=fixed_time,
                final_event_hash=final_hash,
            )
            return result


        def command_simulate(args: argparse.Namespace) -> int:
            payload = load_json(args.scenario)
            result = _write_run(payload, args.output_dir, args.fixed_time)
            model = result["model_currency"]
            print(f"Generated auditable run: {args.output_dir}")
            print(
                f"Seller profit after share: {model} {result['seller']['profit_after_share_model']} | "
                f"Buyer economic landed: {model} {result['buyer']['economic_landed_cost_model']}"
            )
            return 0


        def command_targets(args: argparse.Namespace) -> int:
            result = simulate(load_json(args.scenario))
            payload = normalize(result["quote_targets"])
            if args.json:
                print(json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2))
            else:
                for key, value in payload.items():
                    print(f"{key}: {value}")
            return 0


        def command_compare(args: argparse.Namespace) -> int:
            comparison = compare_scenarios(load_json(args.baseline), load_json(args.candidate))
            text = pretty_json(comparison)
            if args.output:
                args.output.parent.mkdir(parents=True, exist_ok=True)
                args.output.write_text(text, encoding="utf-8")
            else:
                print(text, end="")
            return 0


        def command_verify(args: argparse.Namespace) -> int:
            result = verify_run(args.run_dir)
            if args.json:
                print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
            else:
                print("VALID" if result["valid"] else "INVALID")
                for error in result["errors"]:
                    print(f"- {error}")
            return 0 if result["valid"] else 2


        def command_init(args: argparse.Namespace) -> int:
            source = Path(__file__).resolve().parents[2] / "package_data" / "starter_scenario.json"
            if not args.apply:
                print(f"Would create {args.target} from the packaged synthetic starter. Re-run with --apply.")
                return 0
            if args.target.exists():
                raise ValueError(f"target already exists: {args.target}")
            args.target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, args.target)
            print(f"Created {args.target}")
            return 0


        def main(argv: list[str] | None = None) -> int:
            parser = build_parser()
            args = parser.parse_args(argv)
            try:
                if args.command == "validate":
                    return command_validate(args)
                if args.command == "simulate":
                    return command_simulate(args)
                if args.command == "quote-targets":
                    return command_targets(args)
                if args.command == "compare":
                    return command_compare(args)
                if args.command == "verify":
                    return command_verify(args)
                if args.command == "init":
                    return command_init(args)
            except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
                print(f"error: {exc}", file=sys.stderr)
                return 2
            parser.error("unknown command")
            return 2


        if __name__ == "__main__":
            raise SystemExit(main())
    ''',
    "pyproject.toml": r'''
        [build-system]
        requires = ["setuptools>=77"]
        build-backend = "setuptools.build_meta"

        [project]
        name = "golden-pompano-export-simulator"
        version = "0.1.0"
        description = "Assumption-driven export quotation, mass-balance and landed-cost simulator with explicit unit bases."
        readme = "README.md"
        requires-python = ">=3.11"
        license = "MIT"
        license-files = ["LICENSE"]
        authors = [{name = "JINGJAYHUANG"}]
        dependencies = []
        keywords = ["export", "landed-cost", "incoterms", "seafood", "scenario-analysis", "working-capital"]
        classifiers = [
          "Development Status :: 3 - Alpha",
          "Environment :: Console",
          "Intended Audience :: Developers",
          "Intended Audience :: Financial and Insurance Industry",
          "Operating System :: OS Independent",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.11",
          "Programming Language :: Python :: 3.12",
          "Programming Language :: Python :: 3.13",
          "Topic :: Office/Business :: Financial",
          "Topic :: Scientific/Engineering :: Information Analysis"
        ]

        [project.scripts]
        gpes = "golden_pompano_export_simulator.cli:main"
        pompano-export = "golden_pompano_export_simulator.cli:main"

        [project.urls]
        Repository = "https://github.com/JINGJAYHUANG/golden-pompano-export-simulator"
        Issues = "https://github.com/JINGJAYHUANG/golden-pompano-export-simulator/issues"

        [tool.setuptools]
        package-dir = {"" = "src"}
        include-package-data = true

        [tool.setuptools.packages.find]
        where = ["src"]

        [tool.setuptools.package-data]
        golden_pompano_export_simulator = ["package_data/*.json"]
    ''',
    "MANIFEST.in": r'''
        include LICENSE README.md CHANGELOG.md MODEL_CARD.md DATA_CARD.md
        recursive-include src/golden_pompano_export_simulator/package_data *.json
        recursive-include examples *.json *.csv *.md *.html
        recursive-include docs *.md *.svg
        recursive-include schemas *.json
    ''',
    ".gitignore": r'''
        __pycache__/
        *.py[cod]
        *.egg-info/
        .pytest_cache/
        .coverage
        htmlcov/
        .venv/
        build/
        dist/
        wheelhouse/
        *.sqlite
        .DS_Store
        .env
        .env.*
        !.env.example
        local-inputs/
        private-runs/
        ci-output/
        tmp-output/
    ''',
}


for relative_path, file_content in FILES.items():
    write(relative_path, file_content)

print(f"generated {len(FILES)} core files")

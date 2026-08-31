from __future__ import annotations

import json
from pathlib import Path
from textwrap import dedent

ROOT = Path(__file__).resolve().parents[1]


def write(path: str, content: str) -> None:
    destination = ROOT / path
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(dedent(content).lstrip("\n"), encoding="utf-8")


def dump(path: str, payload: object) -> None:
    destination = ROOT / path
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )


BASELINE = {
    "schema_version": "1.0",
    "scenario_id": "SYN-CIF-BASELINE",
    "as_of": "2026-08-31",
    "data_classification": "synthetic",
    "assumption_status": "fictional values for software demonstration; not current prices or legal rates",
    "source_registry": [
        {
            "source_id": "SYN-MASS-001",
            "uri": "synthetic://mass-and-packaging-fixture",
            "checked_at": "2026-08-31",
            "status": "synthetic",
        },
        {
            "source_id": "SYN-COST-001",
            "uri": "synthetic://cost-and-fx-fixture",
            "checked_at": "2026-08-31",
            "status": "synthetic",
        },
    ],
    "currencies": {
        "model_currency": "USD",
        "fx_to_model": {"USD": "1", "CNY": "0.14", "SGD": "0.74"},
        "fx_note": "fictional conversion factors for deterministic tests",
    },
    "product": {
        "species_label": "Synthetic golden pompano",
        "product_form": "whole-round-frozen",
        "target_net_fish_kg": "18000",
        "glaze_fraction_of_glazed_product": "0.10",
        "declared_product_kg_per_carton": "20",
        "packaging_tare_kg_per_carton": "1.10",
        "cartons_per_pallet": "50",
        "pallet_tare_kg": "25",
        "container_payload_limit_kg": "27000",
        "size_mix": [
            {"id": "SYN-350-400G", "min_grams": "350", "max_grams": "400", "share_of_net_fish": "0.25"},
            {"id": "SYN-400-500G", "min_grams": "400", "max_grams": "500", "share_of_net_fish": "0.50"},
            {"id": "SYN-500-600G", "min_grams": "500", "max_grams": "600", "share_of_net_fish": "0.25"},
        ],
    },
    "quote": {
        "currency": "USD",
        "price_basis": "per_glazed_product_kg",
        "unit_price": "5.55",
        "payment": {
            "deposit_fraction": "0.30",
            "deposit_day_relative_to_shipment": -20,
            "balance_day_relative_to_shipment": 30,
        },
    },
    "contract_profile": {
        "incoterm_label": "CIF",
        "named_place": "Synthetic destination port",
        "edition_note": "label only; operator must confirm the governing contract and edition",
        "cost_responsibility_overrides": {},
    },
    "customs_value": {"method": "invoice"},
    "costs": [
        {"id": "raw_fish", "label": "Synthetic farm-gate fish cost", "stage": "raw_material", "payer": "auto", "basis": "per_net_fish_kg", "rate": "24.00", "currency": "CNY", "cash_day_relative_to_shipment": -35},
        {"id": "processing", "label": "Synthetic processing cost", "stage": "processing", "payer": "auto", "basis": "per_net_fish_kg", "rate": "2.80", "currency": "CNY", "cash_day_relative_to_shipment": -15},
        {"id": "glazing", "label": "Synthetic glazing cost", "stage": "glazing", "payer": "auto", "basis": "per_glazed_product_kg", "rate": "0.25", "currency": "CNY", "cash_day_relative_to_shipment": -12},
        {"id": "packaging", "label": "Synthetic carton and liner cost", "stage": "packaging", "payer": "auto", "basis": "per_carton", "rate": "42.00", "currency": "CNY", "cash_day_relative_to_shipment": -18},
        {"id": "inspection", "label": "Synthetic quality inspection", "stage": "quality_inspection", "payer": "auto", "basis": "per_shipment", "rate": "2800", "currency": "CNY", "cash_day_relative_to_shipment": -8},
        {"id": "origin_inland", "label": "Synthetic origin inland cold-chain", "stage": "origin_inland", "payer": "auto", "basis": "per_shipment", "rate": "6500", "currency": "CNY", "cash_day_relative_to_shipment": -3},
        {"id": "export_clearance", "label": "Synthetic export documentation", "stage": "export_clearance", "payer": "auto", "basis": "per_shipment", "rate": "3500", "currency": "CNY", "cash_day_relative_to_shipment": -2},
        {"id": "origin_terminal", "label": "Synthetic origin terminal charges", "stage": "origin_terminal", "payer": "auto", "basis": "per_shipment", "rate": "5200", "currency": "CNY", "cash_day_relative_to_shipment": 0},
        {"id": "main_carriage", "label": "Synthetic ocean freight", "stage": "main_carriage", "payer": "auto", "basis": "per_container", "rate": "5200", "currency": "USD", "cash_day_relative_to_shipment": 0},
        {"id": "cargo_insurance", "label": "Synthetic cargo insurance", "stage": "cargo_insurance", "payer": "auto", "basis": "percent_invoice", "rate": "0.0025", "currency": "USD", "cash_day_relative_to_shipment": 0},
        {"id": "destination_terminal", "label": "Synthetic destination terminal charges", "stage": "destination_terminal", "payer": "auto", "basis": "per_container", "rate": "1100", "currency": "USD", "cash_day_relative_to_shipment": 18},
        {"id": "import_clearance", "label": "Synthetic import clearance", "stage": "import_clearance", "payer": "auto", "basis": "per_shipment", "rate": "450", "currency": "USD", "cash_day_relative_to_shipment": 19},
        {"id": "destination_inland", "label": "Synthetic destination cold-chain", "stage": "destination_inland", "payer": "auto", "basis": "per_shipment", "rate": "900", "currency": "USD", "cash_day_relative_to_shipment": 21},
        {"id": "sales_commission", "label": "Synthetic sales commission", "stage": "sales_commission", "payer": "auto", "basis": "percent_invoice", "rate": "0.012", "currency": "USD", "cash_day_relative_to_shipment": 30},
    ],
    "taxes": [
        {"id": "synthetic_import_duty", "label": "Synthetic import duty assumption", "payer": "buyer", "basis": "customs_value", "rate": "0.05", "recoverable_fraction": "0", "cash_day_relative_to_shipment": 20},
        {"id": "synthetic_import_tax", "label": "Synthetic recoverable import-tax assumption", "payer": "buyer", "basis": "customs_plus_prior_taxes", "rate": "0.09", "recoverable_fraction": "1", "cash_day_relative_to_shipment": 20, "recovery_day_relative_to_shipment": 80},
    ],
    "credits": [
        {"id": "synthetic_origin_credit", "label": "Synthetic conditional seller credit", "recipient": "seller", "basis": "per_shipment", "rate": "900", "currency": "USD", "cash_day_relative_to_shipment": 45}
    ],
    "finance": {"annual_financing_rate": "0.075"},
    "profit_share": {"fraction": "0.20", "minimum_retained_profit_model_currency": "6000"},
    "targets": {"seller_margin_fraction": "0.12"},
    "analysis": {
        "one_way": [
            {"path": "quote.unit_price", "deltas": ["-0.10", "-0.05", "0", "0.05", "0.10"]},
            {"path": "cost:raw_fish.rate", "deltas": ["-0.10", "-0.05", "0", "0.05", "0.10"]},
            {"path": "cost:main_carriage.rate", "deltas": ["-0.15", "-0.075", "0", "0.075", "0.15"]},
            {"path": "product.glaze_fraction_of_glazed_product", "deltas": ["-0.10", "-0.05", "0", "0.05", "0.10"]},
        ],
        "two_way": {
            "x_path": "quote.unit_price",
            "x_deltas": ["-0.10", "-0.05", "0", "0.05", "0.10"],
            "y_path": "cost:raw_fish.rate",
            "y_deltas": ["-0.10", "-0.05", "0", "0.05", "0.10"],
        },
    },
}

RESILIENT = json.loads(json.dumps(BASELINE))
RESILIENT["scenario_id"] = "SYN-CIF-RESILIENT"
RESILIENT["quote"]["unit_price"] = "5.65"
RESILIENT["quote"]["payment"]["balance_day_relative_to_shipment"] = 15
for line in RESILIENT["costs"]:
    if line["id"] == "raw_fish":
        line["rate"] = "23.50"
    elif line["id"] == "main_carriage":
        line["rate"] = "4700"
    elif line["id"] == "packaging":
        line["rate"] = "40.00"
RESILIENT["finance"]["annual_financing_rate"] = "0.065"
RESILIENT["assumption_status"] = "fictional improved-assumption case for deterministic comparison"

for target in (
    "examples/synthetic_baseline/scenario.json",
    "src/golden_pompano_export_simulator/package_data/starter_scenario.json",
):
    dump(target, BASELINE)
dump("examples/synthetic_resilient/scenario.json", RESILIENT)

SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "https://example.invalid/gpes/scenario.schema.json",
    "title": "Golden Pompano Export Simulator scenario",
    "type": "object",
    "required": [
        "schema_version",
        "scenario_id",
        "as_of",
        "data_classification",
        "currencies",
        "product",
        "quote",
        "contract_profile",
        "costs",
        "taxes",
        "finance",
        "profit_share",
        "targets",
    ],
    "properties": {
        "schema_version": {"const": "1.0"},
        "scenario_id": {"type": "string", "minLength": 2},
        "as_of": {"type": "string", "format": "date"},
        "data_classification": {"enum": ["synthetic", "private", "licensed"]},
        "product": {"type": "object"},
        "quote": {"type": "object"},
        "contract_profile": {"type": "object"},
        "costs": {"type": "array", "minItems": 1},
        "taxes": {"type": "array"},
    },
    "additionalProperties": True,
}
dump("schemas/scenario.schema.json", SCHEMA)

FILES = {
    "README.md": r'''
        # Golden Pompano Export Simulator

        **Assumption-driven export quotation, mass-balance and landed-cost modelling with explicit unit bases.**

        Golden Pompano Export Simulator (`gpes`) turns a versioned JSON scenario into an auditable seller-and-buyer decision bundle. It keeps five quantities separate:

        ```text
        net fish mass
        + ice glaze mass
        = glazed product mass
        + packaging tare
        = packaged gross shipment mass
        ```

        That separation prevents the most common export-quotation error: treating “price per tonne” as meaningful without saying which tonne.

        > **Public boundary:** all committed values, routes, counterparties, FX rates, duties, taxes, costs and margins are fictional. The software performs no live tariff lookup and makes no legal or customs determination.

        ## What the simulator answers

        - How many integer cartons, pallets and containers are required for a target net-fish mass?
        - How much of the shipment is fish, ice, cartons and pallet tare?
        - What is the seller's invoice, working-capital need, financing cost, profit share and margin?
        - What is the buyer's landed cash cost versus economic cost after modelled recoverable tax?
        - What is every result per net-fish kg, glazed-product kg, packaged-gross kg, carton, container and shipment?
        - What unit price produces break-even or a declared target margin?
        - Which assumptions create the largest one-way and two-way sensitivity?
        - Can the generated run be verified against its input snapshot, hash chain, SQLite content and artifact manifest?

        ## Quick start

        Requires Python 3.11 or newer. Runtime dependencies: **zero**.

        ```bash
        git clone https://github.com/JINGJAYHUANG/golden-pompano-export-simulator.git
        cd golden-pompano-export-simulator
        python -m pip install --no-deps -e .
        ```

        Validate the committed synthetic fixture:

        ```bash
        gpes validate examples/synthetic_baseline/scenario.json --public-fixture
        ```

        Generate an auditable run:

        ```bash
        gpes simulate examples/synthetic_baseline/scenario.json \
          --output-dir demo-run \
          --fixed-time 2026-08-31T00:00:00Z
        ```

        Verify it after generation or transfer:

        ```bash
        gpes verify demo-run
        ```

        Compare two assumption sets:

        ```bash
        gpes compare \
          --baseline examples/synthetic_baseline/scenario.json \
          --candidate examples/synthetic_resilient/scenario.json
        ```

        Calculate break-even and target-margin quote prices:

        ```bash
        gpes quote-targets examples/synthetic_baseline/scenario.json
        ```

        ## Output bundle

        | Artifact | Purpose |
        |---|---|
        | `scenario_snapshot.json` | Exact input used for the run |
        | `summary.json` | Full seller, buyer, mass, tax and unit-economics result |
        | `mass_balance.csv` | Fish, glaze, packaging, gross mass and utilization |
        | `size_grades.csv` | Synthetic grade mix and estimated fish counts |
        | `cost_lines.csv` | Every modelled cost, basis, payer and amount |
        | `tax_lines.csv` | Cash tax, recoverable amount and economic amount |
        | `cash_timeline.csv` | Seller receipts, outflows, cash deficit and financing accrual |
        | `sensitivity.csv` | One-way sensitivity rows |
        | `two_way_grid.csv` | Quote-price × input-cost grid |
        | `report.md` / `report.html` | Human-readable decision reports |
        | `audit.sqlite` | Queryable relational output |
        | `events.jsonl` | Hash-chained execution events |
        | `artifact_manifest.json` | Declared outputs and content digests |
        | `run_manifest.json` | Scenario identity, final event hash and run identity |

        ## Three price denominators that must not be mixed

        For a 10% glaze fraction defined as **ice / glazed product mass**:

        ```text
        glazed product mass = net fish mass / (1 - 0.10)
        ```

        Therefore:

        ```text
        1,000 kg net fish
        = 1,111.111... kg glazed product
        = more than 1,111.111... kg packaged gross shipment
        ```

        A quote of `5.00 per net-fish kg` is economically different from `5.00 per glazed-product kg`. `gpes` requires the basis to be explicit and reports all major results on every supported basis.

        See [Mass and price bases](docs/mass-and-price-bases.md).

        ## Cost responsibility, not legal interpretation

        The built-in `EXW`, `FCA`, `FOB`, `CFR`, `CIF`, `DAP` and `DDP` profiles are **illustrative calculation templates**. They assign modelled cost stages between seller and buyer, then allow contract-specific overrides.

        They do **not** determine:

        - legal risk transfer;
        - title transfer;
        - customs valuation;
        - importer/exporter eligibility;
        - licensing, health-certificate or labelling compliance;
        - tariff classification;
        - tax recoverability;
        - liability under a real contract.

        The contract, route, destination rules and qualified professional review control those matters. See [Contract and Incoterms boundary](docs/contract-and-incoterms-boundary.md).

        ## Seller and buyer are modelled separately

        Seller economics include:

        ```text
        invoice revenue
        + modelled seller credits
        + modelled recoverable seller tax
        - seller-paid costs
        - seller tax cash outflow
        - working-capital financing cost
        - conditional profit share
        ```

        Buyer economics distinguish:

        ```text
        landed cash cost
        = invoice + buyer-paid costs + tax cash outflow

        landed economic cost
        = landed cash cost - recoverable tax - buyer credits
        ```

        Recoverability is only an assumption supplied by the operator. It is not inferred by the package.

        ## Determinism and auditability

        Monetary arithmetic uses `decimal.Decimal`, not binary floats. Fixed-time runs are deterministic for JSON, CSV, Markdown and HTML. SQLite is verified through a semantic table digest rather than database-page bytes, because SQLite library versions may lay out identical tables differently.

        The verifier fails when it detects:

        - an altered scenario snapshot;
        - a changed result or report;
        - a modified SQLite table;
        - a deleted or reordered event;
        - a missing artifact;
        - an undeclared artifact;
        - an inconsistent final hash or file count.

        ## Scope and limitations

        - This is a deterministic scenario model, not a forecast.
        - Synthetic examples are not evidence of any current market price, tariff, freight rate or margin.
        - A mathematically profitable scenario may be commercially, legally or operationally infeasible.
        - Integer packaging can create small shipment overfill relative to target net-fish mass.
        - Size-grade fish counts use band midpoints and are planning estimates only.
        - Container payload does not represent volume, axle, reefer, stowage or route-specific limits.
        - Customs, tax, sanctions, food-safety, veterinary, insurance and Incoterms questions require current primary sources and professional review.
        - The model does not certify product quality, buyer creditworthiness, payment collection or regulatory compliance.

        ## Repository map

        ```text
        src/golden_pompano_export_simulator/  Package and CLI
        examples/                             Fictional deterministic scenarios
        schemas/                              Machine-readable scenario contract
        tests/                                Unit, matrix, security and integrity tests
        scripts/                              Public audit, reproducibility and release gates
        docs/                                 Methodology and boundary documentation
        .github/workflows/                    CI and release automation
        ```

        ## Project status

        **v0.1.0 — public alpha.** Mass balance, seller/buyer economics, financing, profit share, quote targets, sensitivity, SQLite export and evidence verification are implemented against synthetic fixtures.

        ## License

        MIT. See [LICENSE](LICENSE).
    ''',
    "docs/README.zh-CN.md": r'''
        # 金鲳鱼出口报价与利润模拟器

        这个项目不是“替你报一个价格”，而是强迫所有参与者先把口径说清楚，再计算。

        ## 它解决的核心误区

        外贸沟通中常见一句话：

        ```text
        每吨多少钱？
        ```

        但这里至少可能指：

        1. 每吨净鱼；
        2. 每吨含冰衣产品；
        3. 每吨连纸箱、内袋和托盘的运输毛重；
        4. 每个整柜；
        5. 每票货。

        如果冰衣率是含冰衣产品重量的 10%，那么 18,000 千克净鱼并不是 19,800 千克含冰衣产品，而是：

        ```text
        18,000 / (1 - 10%) = 20,000 千克含冰衣产品
        ```

        再加入纸箱和托盘后，运输毛重继续增加。因此所有报价、成本和到岸成本都必须绑定明确分母。

        ## 一票货同时看两张表

        ### 卖方利润表

        - 发票收入；
        - 生产、加工、冰衣、包装和物流成本；
        - 税费现金流与可回收部分；
        - 收款节奏；
        - 峰值垫资；
        - 融资成本；
        - 利润分成；
        - 最终利润和利润率。

        ### 买方到岸表

        - 发票金额；
        - 买方承担的港杂、清关和内陆运输；
        - 关税和进口税现金支出；
        - 可回收税额；
        - 到岸现金成本；
        - 到岸经济成本；
        - 按净鱼、含冰衣产品、运输毛重、纸箱和整柜换算的单位成本。

        ## Incoterms 边界

        软件只使用可编辑的成本责任模板，不判断真实合同的风险转移、所有权、进口资格、关税归类、食品与动物卫生要求或税额可抵扣性。任何真实业务都必须按合同、路线、日期和目的国重新核验。

        ## 快速运行

        ```bash
        python -m pip install --no-deps -e .
        gpes validate examples/synthetic_baseline/scenario.json --public-fixture
        gpes simulate examples/synthetic_baseline/scenario.json \
          --output-dir demo-run \
          --fixed-time 2026-08-31T00:00:00Z
        gpes verify demo-run
        ```

        ## 公开边界

        仓库中的价格、汇率、客户、航线、税率、成本和利润全部是虚构测试值，不对应任何真实公司、买家、供应商、养殖场、合同或当前市场。
    ''',
    "docs/mass-and-price-bases.md": r'''
        # Mass and price bases

        ## Definitions

        Let:

        - `N` = net fish mass;
        - `g` = ice glaze as a fraction of glazed product mass;
        - `P` = glazed product mass;
        - `I` = ice mass;
        - `T` = packaging tare;
        - `G` = packaged gross shipment mass.

        Then:

        ```text
        P = N / (1 - g)
        I = P × g
        G = P + T
        ```

        The simulator deliberately does not support an unlabeled `per_kg` price basis. Every quote must use one of:

        - `per_net_fish_kg`;
        - `per_glazed_product_kg`;
        - `per_packaged_gross_kg`;
        - `per_carton`;
        - `per_container`;
        - `per_shipment`.

        ## Integer packaging

        Cartons are indivisible. The minimum carton count is:

        ```text
        ceil(target net fish / net fish per carton)
        ```

        Consequently the shipped net-fish mass can exceed the target. The model reports this as `net_fish_overfill_kg`; it does not silently reduce a carton.

        ## Size grades

        Size-grade shares allocate shipped net-fish mass. Estimated fish counts divide each allocation by the band midpoint. They are planning approximations, not sorting or yield guarantees.

        ## Capacity warning

        Payload utilization uses weight only. Reefer volume, airflow, pallet geometry, axle limits, road limits, route restrictions and carrier practice remain outside scope.
    ''',
    "docs/contract-and-incoterms-boundary.md": r'''
        # Contract and Incoterms boundary

        The simulator stores an `incoterm_label` and an editable stage-to-payer map. This is useful for cost modelling, but it is intentionally narrower than a legal Incoterms analysis.

        ## Modelled

        - which party pays each declared cost line;
        - the effect of that allocation on seller profit and buyer landed cost;
        - explicit contract-specific overrides;
        - a named place as scenario metadata.

        ## Not modelled

        - transfer of risk;
        - title or beneficial ownership;
        - export/import eligibility;
        - customs representation;
        - tariff classification;
        - sanctions and restricted-party screening;
        - food, animal-health or labelling compliance;
        - insurance adequacy or claims handling;
        - legal enforceability;
        - destination tax recoverability.

        ## Why profiles are illustrative

        Real cost allocation may be changed by freight contracts, terminal practice, surcharges, demurrage, detention, inspection, cold-chain incidents, customs examinations, local taxes, contract clauses or side agreements. The operator must replace the template with the signed commercial allocation before using the output for a transaction.
    ''',
    "docs/tax-finance-and-cashflow.md": r'''
        # Tax, finance and cash-flow model

        ## Tax cash versus tax economics

        Each tax line has:

        ```text
        cash amount
        recoverable fraction
        recoverable amount
        non-recoverable amount
        ```

        Buyer landed cash cost includes the full tax cash outflow. Buyer landed economic cost subtracts the assumed recoverable portion. Recoverability is never inferred.

        ## Seller working capital

        Seller receipts and payments are placed on a timeline relative to shipment day. Between consecutive events, a negative running cash balance accrues simple financing cost:

        ```text
        financing cost
        = cash deficit × annual financing rate × days / 365
        ```

        This is a planning approximation. It does not model compounding, bank fees, credit limits, collateral, currency forward points or default risk.

        ## Profit share

        The synthetic model supports a share applied only to positive profit above a retained-profit floor:

        ```text
        share base = max(0, profit before share - retained floor)
        profit share = share base × share fraction
        ```

        Actual partnership, agency, referral or joint-venture terms require a written agreement and professional review.
    ''',
    "docs/methodology.md": r'''
        # Methodology

        ## Calculation order

        1. Validate version, dates, IDs, units, rates, parties and source classification.
        2. Convert target net-fish mass into integer cartons, pallets and containers.
        3. Calculate fish, ice, product, packaging and gross shipment mass.
        4. Convert the quote basis into an invoice.
        5. Resolve cost responsibility from the illustrative profile plus overrides.
        6. Calculate customs-value assumptions, taxes and recoverable amounts.
        7. Build the seller cash timeline and financing cost.
        8. Calculate seller profit before and after profit share.
        9. Calculate buyer landed cash and economic cost.
        10. Express results on six explicit unit bases.
        11. Solve break-even and target-margin quote prices by deterministic bisection.
        12. Run one-way and two-way sensitivity.
        13. Export reports, SQLite, hash-chained events and manifests.

        ## Decimal arithmetic

        All model arithmetic uses `decimal.Decimal`. Monetary outputs are rounded to two decimal places at cash-line boundaries. Mass is retained to four decimal places. The quote solver retains additional precision before display.

        ## Scenario analysis, not probability

        A sensitivity row answers “what changes under this declared input change?” It is not a probability-weighted forecast. The software does not estimate demand, price distributions, counterparty default or regulatory outcomes.

        ## Break-even interpretation

        Break-even is conditional on every supplied assumption, including cost responsibility, tax recovery, payment timing, financing rate and profit-share formula. It should be treated as a model output to challenge, not an offer price.
    ''',
    "docs/decision-guide.md": r'''
        # Decision guide

        Use the outputs in this order:

        1. **Check mass basis.** Confirm the glaze definition and carton declaration.
        2. **Check responsibility.** Replace illustrative stage allocation with the contract.
        3. **Check cash.** Seller profit can be positive while peak funding is unaffordable.
        4. **Check buyer economics.** Separate recoverable tax from cash paid at import.
        5. **Check unit denominator.** Compare competing quotes only on the same basis.
        6. **Check sensitivity.** Identify assumptions capable of reversing the decision.
        7. **Check evidence date.** FX, freight, duty and tax inputs expire quickly.
        8. **Check operational feasibility.** Product quality, delivery, documents and payment collection remain outside the arithmetic.

        ## Minimum commercial handoff

        Before turning a scenario into a real quotation, a human reviewer should confirm:

        - product specification and tolerance;
        - glaze test method and labelling basis;
        - carton declaration and net/gross weights;
        - quantity tolerance and integer carton policy;
        - named Incoterms place and edition;
        - responsibility for every origin and destination charge;
        - customs value and tariff classification;
        - tax recoverability and timing;
        - payment security and credit terms;
        - freight validity, surcharges and free time;
        - inspection, rejection, claim and dispute clauses;
        - currency, quote expiry and adjustment rules.
    ''',
    "docs/architecture.md": r'''
        # Architecture

        ```mermaid
        flowchart LR
          A[Versioned scenario JSON] --> V[Validation]
          V --> M[Mass and packaging engine]
          M --> Q[Quote basis and invoice]
          Q --> R[Cost responsibility resolver]
          R --> T[Tax and customs assumptions]
          T --> C[Seller cash timeline]
          C --> S[Seller P&L]
          T --> B[Buyer landed cost]
          S --> P[Break-even and target-price solver]
          B --> X[Sensitivity engine]
          P --> X
          X --> O[JSON / CSV / Markdown / HTML / SQLite]
          O --> H[Hash chain and artifact manifest]
        ```

        The package is local-first and dependency-free at runtime. No network adapter is included in v0.1.0. Current prices, tariff schedules and legal rules must be supplied and verified outside the package.
    ''',
    "docs/privacy-and-publication-boundary.md": r'''
        # Privacy and publication boundary

        ## Allowed in the public repository

        - fictional routes and counterparties;
        - synthetic prices, costs, exchange rates and tax assumptions;
        - generic cost categories;
        - software tests and deterministic reports;
        - public methodology and calculation contracts.

        ## Never commit

        - buyer, supplier, factory or employee contact details;
        - real negotiation history;
        - real farm-gate prices, inventory, harvest schedules or margins;
        - contracts, invoices, bank evidence or customs documents;
        - account credentials, API keys, cookies or webhooks;
        - local absolute paths or private repository references;
        - health, identity, immigration or personal-finance records;
        - licensed market or trade data without redistribution rights.

        The included scanner is a guardrail, not a guarantee. Human review remains mandatory before publication.
    ''',
    "docs/release-verification.md": r'''
        # Release verification

        A valid v0.1.0 release must pass:

        - Python 3.11, 3.12 and 3.13 installation and compilation;
        - the exact 523-test floor;
        - public-fixture validation;
        - deterministic baseline and resilient scenario generation;
        - run-bundle verification;
        - comparison of regenerated outputs with committed Golden summaries;
        - nine tamper attacks;
        - public-boundary scanning;
        - Markdown-link validation;
        - byte-identical Wheel construction under a fixed build epoch;
        - clean-environment Wheel installation and CLI smoke tests.

        Passing these gates validates the software protocol and synthetic fixtures. It does not validate any real commercial assumption.
    ''',
    "MODEL_CARD.md": r'''
        # Model Card

        ## Intended use

        Structured scenario analysis for frozen whole-fish export quotations, working capital and landed cost.

        ## Not intended for

        Legal advice, customs classification, tax advice, food-safety approval, veterinary advice, buyer credit approval, live pricing or profit guarantees.

        ## Core assumptions

        - glaze is expressed as ice divided by glazed-product mass;
        - cartons and containers are integer quantities;
        - costs are supplied by the operator and converted through explicit FX factors;
        - financing is a simple annual rate over negative cash-balance intervals;
        - tax recoverability is user-declared;
        - cost responsibility is an editable calculation profile;
        - sensitivity is deterministic, not probabilistic.

        ## Failure modes

        Wrong mass basis, stale freight, incorrect customs value, incorrect tax recovery, hidden destination charges, invalid payment assumptions, quality claims, volume constraints and counterparty default can all invalidate a commercially attractive result.
    ''',
    "DATA_CARD.md": r'''
        # Data Card

        All committed example rows are synthetic. They use `synthetic://` source identifiers and fictional exchange rates, tax rates, freight, costs, margins, route names and counterparties.

        The package does not include live trade, customs, tariff, freight, buyer, supplier, farm, vessel or market datasets.

        Private users are responsible for source rights, freshness, field definitions, currency conversion, date alignment, confidentiality and retention policy.
    ''',
    "SECURITY.md": r'''
        # Security Policy

        Report vulnerabilities through a private GitHub security advisory when available. Do not place credentials, contracts, commercial data or personal information in a public issue.

        The CLI reads local JSON and writes a new output directory. It performs no network request. Treat externally supplied scenarios as untrusted data and run the package in an appropriately restricted environment when provenance is unknown.
    ''',
    "CONTRIBUTING.md": r'''
        # Contributing

        1. Use synthetic fixtures only.
        2. Preserve explicit mass, currency, time and price bases.
        3. Add tests for every new calculation path and failure mode.
        4. Do not present an illustrative responsibility profile as legal advice.
        5. Keep runtime dependencies at zero unless a documented capability requires otherwise.
        6. Run `make all` before opening a pull request.
        7. Update the model/data cards when scope or assumptions change.
    ''',
    "AGENTS.md": r'''
        # Agent Instructions

        - Read README, MODEL_CARD, DATA_CARD and the relevant methodology document before changing calculations.
        - Never insert real buyers, contacts, prices, contracts, farm data, account data or credentials.
        - Use `Decimal`; do not replace commercial arithmetic with binary floats.
        - Never introduce an unlabeled `per_kg` field.
        - Cost responsibility and legal risk transfer must remain separate concepts.
        - Missing legal, tariff or tax evidence must remain an explicit assumption, not be inferred.
        - A negative or commercially unattractive result is valid output and must not be hidden.
        - Update tests, Golden fixtures and release notes together.
        - Do not hand-edit generated example outputs; regenerate and verify them.
    ''',
    "CHANGELOG.md": r'''
        # Changelog

        ## 0.1.0 — 2026-08-31

        - explicit net-fish, glaze, product, packaging and shipment mass balance;
        - integer carton, pallet and container calculation;
        - seller P&L, buyer landed cash/economic cost and multi-basis unit economics;
        - editable illustrative cost-responsibility profiles;
        - customs, tax recovery, credits and working-capital timeline;
        - profit sharing, break-even and target-margin quote solver;
        - one-way and two-way sensitivity;
        - JSON, CSV, Markdown, HTML and SQLite outputs;
        - hash-chained events, artifact manifest and tamper verification;
        - synthetic public fixtures, 523 tests, CI and release automation.
    ''',
    "ROADMAP.md": r'''
        # Roadmap

        ## v0.1 — complete

        Core deterministic mass, quotation, landed-cost, sensitivity and audit engine.

        ## Candidate v0.2

        - multi-SKU and multi-container allocation;
        - volume and pallet-geometry constraints;
        - configurable payment instruments and counterparty-credit scenarios;
        - probabilistic Monte Carlo layer with explicit distributions;
        - optional spreadsheet export without changing the calculation source of truth.

        ## Candidate v0.3

        - signed private assumption packs;
        - pluggable current-data adapters with provenance and cache expiry;
        - route-specific document and compliance checklist integration.

        ## Non-goals

        Automated legal conclusions, tariff classification, buyer outreach, contract acceptance, payment execution, customs filing or shipment booking.
    ''',
    "CITATION.cff": r'''
        cff-version: 1.2.0
        message: "If you use this software, cite the repository and version."
        title: "Golden Pompano Export Simulator"
        version: 0.1.0
        date-released: 2026-08-31
        authors:
          - family-names: "Huang"
            given-names: "Jingjie"
        repository-code: "https://github.com/JINGJAYHUANG/golden-pompano-export-simulator"
        license: MIT
    ''',
    "LICENSE": r'''
        MIT License

        Copyright (c) 2026 JINGJAYHUANG

        Permission is hereby granted, free of charge, to any person obtaining a copy
        of this software and associated documentation files (the "Software"), to deal
        in the Software without restriction, including without limitation the rights
        to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
        copies of the Software, and to permit persons to whom the Software is
        furnished to do so, subject to the following conditions:

        The above copyright notice and this permission notice shall be included in all
        copies or substantial portions of the Software.

        THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
        IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
        FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
        AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
        LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
        OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
        SOFTWARE.
    ''',
    "Makefile": r'''
        .PHONY: install test demo verify audit links all

        install:
        	python -m pip install --no-deps -e .

        test:
        	python scripts/verify_test_count.py
        	python -m unittest discover -s tests -v

        demo:
        	rm -rf tmp-output
        	gpes simulate examples/synthetic_baseline/scenario.json --output-dir tmp-output --fixed-time 2026-08-31T00:00:00Z

        verify:
        	gpes verify tmp-output

        audit:
        	python scripts/public_audit.py .

        links:
        	python scripts/check_markdown_links.py .

        all: install test demo verify audit links
    ''',
    ".env.example": r'''
        # The v0.1.0 package needs no environment variables or credentials.
        # Keep private commercial inputs outside the repository.
    ''',
}

for relative_path, content in FILES.items():
    write(relative_path, content)

print(f"generated {len(FILES)} documentation files and 2 fixtures")

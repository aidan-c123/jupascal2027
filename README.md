# JUPAS 2027 Calculator

**Live Site:** [https://jupascal.pages.dev](https://jupascal.pages.dev)

An interactive client-side JUPAS 2027 admissions score calculator, A1–E20 band choice planner, and risk diagnostic dashboard, backed by normalized 3NF CSV data tables.

## Key Features

* **HKDSE Score & Eligibility Engine:** Calculates programme-specific scores (`BEST_5`, `BEST_6`, `3C2X`, `4C2X`, subject weightings, and extra elective bonuses), checks core/elective/language/CSD/compulsory-elective eligibility rules across all Category A and Category C subjects, and provides an interactive formula breakdown (`Base + Weightings + Extra Bonus = Total`).
* **A1–E20 Choice Planner & Risk Diagnostics:** Supports adding, dragging/reordering, moving up/down, and importing/exporting choices across Bands A–E, with band-adjusted risk tiers (`Safe`, `Low Risk`, `Moderate Danger`, `High Danger`, `Ineligible`, `No Data`), an **Analysis** tab for diagnostics and safer same-direction backups, a sticky **Quick Tweak** bar, and one-click sample demo loading.
* **Persistence, Sharing & Theme Controls:** Automatically saves grades and choices to `localStorage`, encodes state into shareable `#s=...` URL hashes, includes a responsive mobile card view (`< 768px`) alongside the desktop table, supports Dark and Light mode toggling, and provides CSV integrity validation via `validate_csv.py`.

## Repository Structure

* `index.html` — Single-file frontend application (HTML, Tailwind CSS, and vanilla JavaScript with PapaParse).
* `validate_csv.py` — Python validation script checking foreign keys, formula types, weights, grades, and `compulsory_electives` syntax across the data tables.
* `.github/workflows/validate-csv.yml` — GitHub Actions workflow that runs CSV integrity checks on pushes and pull requests touching `data/*.csv` or `validate_csv.py`.
* `data/programmes.csv` — 312 UGC programmes with formula types, subject/language overrides, compulsory elective rules, `intake_2026`, and `interview_req`.
* `data/programme_weights.csv` — 1,034 programme–subject weighting, mandatory-subject, and minimum-grade rules.
* `data/admissions_history.csv` — Historical admission score benchmarks (`score_uq`, `score_median`, `score_lq`, and notes), including 2026 reference figures.
* `data/institutions.csv` — 8 UGC institutions (`HKU`, `CUHK`, `HKUST`, `PolyU`, `CityUHK`, `HKBU`, `Lingnan University`, and `EdUHK`) and default baseline requirements.
* `data/grade_scales.csv` — Point mappings across grade scales (including 7.0 and 8.5 scales).
* `data/subjects.csv` — All HKDSE Category A (Core, Math Extended `M1`/`M2`, and Electives) and Category C (Other Languages) subjects.

## Data Provenance & Disclaimer

* **Data Source:** 2026 JUPAS admission figures and 2027 UGC programme weightings (data as of 24 Nov 2026).
* **Estimates Only:** All calculated scores, cut-off comparisons, and band risk indicators are unofficial estimates for reference only. Always verify official JUPAS and university brochures before locking in choices by **December 2, 2026** (a **HK$100** amendment fee applies afterward).
* **Report Data Errors:** Submit issues or corrections via [https://github.com/aidan-c123/jupascal2027/issues](https://github.com/aidan-c123/jupascal2027/issues).
* **Author:** Created by [@aidan.choi_](https://www.instagram.com/aidan.choi_/).
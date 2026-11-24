# JUPAS 2027 Score Calculator (GitHub Pages)

A zero-backend static web app powered directly by normalized 3NF CSV files in `data/`.

## How to Deploy on GitHub Pages
1. Create a new public repository on GitHub (e.g. `jupas-2027-calculator`).
2. Upload `index.html`, `README.md`, and the entire `data/` folder to the repository root.
3. Go to **Settings → Pages**, set Source to **Deploy from a branch**, select `main` and `/ (root)`, and click **Save**.

## How to Test Locally
Browsers block `fetch()` on `file://` URLs. Run a one-line local server inside this folder:
```bash
python -m http.server 8000
```
Then open `http://localhost:8000`.

## Updating Scores Next Year
Simply edit or append rows in `data/programmes.csv`, `data/programme_weights.csv`, or `data/admissions_history.csv` and commit to GitHub. The live site updates automatically.

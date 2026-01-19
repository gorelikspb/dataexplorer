# Deployment Guide

## Quick Start (Local)

```bash
# 1. Clone repository
git clone https://github.com/gorelikspb/dataexplorer.git
cd konstanz_data

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run app
streamlit run streamlit_app.py
```

## Streamlit Cloud Deployment

### Step 1: GitHub Repository

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/gorelikspb/dataexplorer.git
git push -u origin main
```

### Step 2: Streamlit Cloud

1. Go to https://streamlit.io/cloud
2. Sign in with GitHub
3. Click "New app"
4. Select repository: `gorelikspb/dataexplorer`
5. Branch: `main`
6. Main file: `streamlit_app.py`
7. Python version: 3.9+
8. Click "Deploy!"

The CSV data file is already included in the repository, so no additional file upload is needed.

## What Gets Deployed

Code:
- `streamlit_app.py` (Main app)
- `src/visualizer.py` (Visualization logic)
- `requirements.txt` (Dependencies)

Data:
- `data/raw/Aussenwanderung_nach_Herkunfts_Ziel-Staat_2010-2023_0_0.csv` (Migration data)

Configuration:
- `.gitignore`
- `.streamlit/config.toml` (if present)

Not deployed:
- `venv/` (Virtual environment)
- `archive/` (Old files)

## Troubleshooting

Problem: App doesn't load data
- Solution: Check that the CSV file is present in the repository at `data/raw/Aussenwanderung_nach_Herkunfts_Ziel-Staat_2010-2023_0_0.csv`

Problem: Missing dependencies
- Solution: Check `requirements.txt`, are all packages installed?

Problem: Python version
- Solution: Streamlit Cloud supports Python 3.9-3.11

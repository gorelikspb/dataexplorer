# Deployment Guide

## 🚀 Schnellstart (Lokal)

```bash
# 1. Repository klonen
git clone <your-repo-url>
cd konstanz_data

# 2. Virtual Environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 3. Dependencies installieren
pip install -r requirements.txt

# 4. Daten herunterladen (optional)
python scripts/download_direct.py

# 5. App starten
streamlit run app.py
```

## ☁️ Streamlit Cloud Deployment

### Schritt 1: GitHub Repository

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-github-repo-url>
git push -u origin main
```

### Schritt 2: Streamlit Cloud

1. Gehe zu https://streamlit.io/cloud
2. Mit GitHub anmelden
3. "New app" klicken
4. Repository auswählen
5. **Main file:** `app.py`
6. **Python version:** 3.9+
7. "Deploy!" klicken

### Schritt 3: Daten hochladen

Nach dem Deployment:

1. In Streamlit Cloud: "⋮" → "Manage app" → "Files"
2. Navigiere zu `data/raw/`
3. Lade `Aussenwanderung_nach_Herkunfts_Ziel-Staat_2010-2023_0_0.csv` hoch

**Oder:** Datei direkt in GitHub Repository committen (wenn < 10MB).

## 📦 Was wird deployed?

✅ **Code:**
- `app.py` (Haupt-App)
- `src/visualizer.py` (Visualisierungslogik)
- `requirements.txt` (Dependencies)

✅ **Konfiguration:**
- `.gitignore`
- `.streamlit/config.toml` (falls vorhanden)

❌ **Nicht deployed:**
- `venv/` (Virtual Environment)
- `data/raw/*.csv` (große Dateien - manuell hochladen)
- `archive/` (alte Dateien)

## 🔧 Troubleshooting

**Problem:** App lädt keine Daten
- **Lösung:** CSV-Datei in `data/raw/` hochladen (siehe Schritt 3)

**Problem:** Dependencies fehlen
- **Lösung:** `requirements.txt` prüfen, alle Pakete installiert?

**Problem:** Python-Version
- **Lösung:** Streamlit Cloud unterstützt Python 3.9-3.11



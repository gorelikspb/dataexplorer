# GitHub Setup Checklist

## ✅ Vorbereitung abgeschlossen

### Struktur bereinigt:
- ✅ Alte/Test-Dateien nach `archive/` verschoben
- ✅ Nur notwendige Dependencies in `requirements.txt`
- ✅ `.gitignore` konfiguriert
- ✅ README.md aktualisiert
- ✅ DEPLOY.md für Deployment-Anleitung erstellt

### Wichtige Dateien für GitHub:

**Hauptdateien:**
- `app.py` - Streamlit App
- `requirements.txt` - Dependencies (minimal)
- `README.md` - Projektbeschreibung
- `DEPLOY.md` - Deployment-Anleitung
- `ANLEITUNG.md` - Anleitung für andere Datenquellen

**Code:**
- `src/` - Alle Source-Module
- `scripts/download_direct.py` - Daten-Download-Script

**Konfiguration:**
- `.gitignore` - Git-Ignore-Regeln
- `.streamlit/config.toml` - Streamlit-Konfiguration

**Datenstruktur:**
- `data/raw/.gitkeep` - Verzeichnisstruktur (Daten werden ignoriert)
- `data/processed/.gitkeep`
- `output/.gitkeep`

## 🚀 Nächste Schritte

### 1. GitHub Repository erstellen

```bash
# Initialisiere Git (falls noch nicht geschehen)
git init

# Füge alle Dateien hinzu
git add .

# Erster Commit
git commit -m "Initial commit: Konstanz Open Data Explorer"

# Erstelle Repository auf GitHub und verbinde
git remote add origin <your-repo-url>
git branch -M main
git push -u origin main
```

### 2. Streamlit Cloud Deployment

1. Gehe zu https://streamlit.io/cloud
2. "New app" klicken
3. Repository auswählen
4. Main file: `app.py`
5. Python version: 3.9+
6. Deploy!

### 3. Daten für Deployment

**Wichtig:** Die App benötigt mindestens eine CSV-Datei:
- `data/raw/Aussenwanderung_nach_Herkunfts_Ziel-Staat_2010-2023_0_0.csv`

**Optionen:**
1. Datei manuell herunterladen und in Repository committen (nicht empfohlen für große Dateien)
2. Datei nach Deployment hochladen (Streamlit Cloud File Browser)
3. Script `scripts/download_direct.py` nach Deployment ausführen

**Empfehlung:** Für Portfolio-Zwecke kann die Datei direkt ins Repository (wenn < 10MB), oder nach Deployment hochladen.

## 📝 Hinweise

- `venv/` wird automatisch ignoriert (in .gitignore)
- `archive/` wird ignoriert (alte Dateien)
- Daten-Dateien werden ignoriert (nur Struktur bleibt)
- `__pycache__/` wird ignoriert

## 🔍 Was wird auf GitHub hochgeladen?

✅ Code (app.py, src/, scripts/)
✅ Konfiguration (.gitignore, .streamlit/)
✅ Dokumentation (README.md, DEPLOY.md, ANLEITUNG.md)
✅ Requirements (requirements.txt)
✅ Verzeichnisstruktur (.gitkeep Dateien)

❌ Virtual Environment (venv/)
❌ Daten-Dateien (data/raw/*.csv)
❌ Archive-Dateien
❌ Output-Dateien
❌ Cache-Dateien




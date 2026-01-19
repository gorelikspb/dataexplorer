# Konstanz Open Data Explorer

**Portfolio-Projekt: Interaktive Visualisierung von Open Data**

Eine einfache Streamlit-App zur Visualisierung von Migrationsdaten der Stadt Konstanz (2010-2023).

## 📊 Live Demo

👉 **[Streamlit Cloud Deployment](https://your-app-name.streamlit.app)** (Link nach Deployment)

## 🎯 Projekt-Überblick

Dieses Projekt demonstriert:
- **Datenvisualisierung** mit Plotly
- **Web-App Entwicklung** mit Streamlit
- **Datenverarbeitung** mit Pandas
- **Open Data Integration** (CKAN API)

### Features

- 📈 **5 interaktive Visualisierungen:**
  - Gesamtmigration nach Jahren (Zuzug/Wegzug)
  - Migrationssaldo über Zeit
  - Top 10 Länder nach Zuzug (mit Jahresauswahl)
  - Top 10 Länder nach Wegzug (mit Jahresauswahl)
  - Migrationssaldo der Top 5 Länder (2010-2023)
- 📋 **Rohdaten-Export** für jeden Graphen
- 📊 **Automatische Datenladung** beim Start

## 🚀 Quick Start

### Lokale Installation

1. Repository klonen:
```bash
git clone <repository-url>
cd konstanz_data
```

2. Virtual Environment erstellen:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# oder
source venv/bin/activate  # Linux/Mac
```

3. Dependencies installieren:
```bash
pip install -r requirements.txt
```

4. Daten herunterladen (optional):
```bash
python scripts/download_direct.py
```

**Hinweis:** Die App lädt automatisch `Aussenwanderung_nach_Herkunfts_Ziel-Staat_2010-2023_0_0.csv` beim Start, falls vorhanden.

5. App starten:
```bash
streamlit run app.py
```

Die App öffnet sich automatisch im Browser unter `http://localhost:8501`

## 📁 Projektstruktur

```
konstanz_data/
├── app.py                    # Haupt-Streamlit-App (200 Zeilen)
├── src/
│   └── visualizer.py        # Visualisierungslogik (400 Zeilen)
├── scripts/
│   └── download_direct.py  # Optional: Daten-Download-Script
├── data/
│   └── raw/                 # CSV-Dateien (nicht in Git)
├── requirements.txt         # 3 Dependencies
├── README.md               # Diese Datei
├── DEPLOY.md               # Deployment-Anleitung
└── .gitignore             # Git-Konfiguration
```

## 📊 Datenquelle

**Open Data Konstanz**: https://offenedaten-konstanz.de/

Aktueller Datensatz: Außenwanderung nach Herkunfts- und Zielgebiet (2010-2023)

## 🔧 Technologie-Stack

- **Python 3.9+**
- **Streamlit** - Web-App Framework (UI)
- **Pandas** - Datenverarbeitung
- **Plotly** - Interaktive Visualisierungen

**Nur 3 Dependencies** - minimalistisch und schnell zu deployen.

## 📝 Verwendung

1. Die App lädt automatisch die Migrationsdaten beim Start
2. Wählen Sie ein Jahr aus dem Dropdown für Top-10-Länder-Grafiken
3. Klicken Sie auf "📋 Rohdaten" Expander, um die zugrundeliegenden Daten zu sehen

## 🌐 Deployment

Siehe [DEPLOY.md](DEPLOY.md) für detaillierte Anweisungen zur Deployment auf Streamlit Cloud oder anderen Plattformen.

## 📚 Weitere Informationen

- [ANLEITUNG.md](ANLEITUNG.md) - Anleitung für andere Datenquellen
- [DEPLOY.md](DEPLOY.md) - Deployment-Anleitung

## 🚀 Deployment

1. **GitHub Repository** erstellen
2. **Streamlit Cloud** verbinden: https://streamlit.io/cloud
3. Repository auswählen → Main file: `app.py` → Deploy!

Siehe [DEPLOY.md](DEPLOY.md) für Details.

## 📄 Lizenz

Portfolio-Projekt - frei verwendbar für Lernzwecke.

## 👤 Kontakt

Für Fragen oder weitere Analysen: [gorelikgo@gmail.com](mailto:gorelikgo@gmail.com)

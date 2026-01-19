# Anleitung: Datenquellen für andere Städte

Diese Anleitung zeigt, wie Sie dieses Tool für Daten aus anderen Open Data Portalen verwenden können.

## Schritte

### 1. Daten herunterladen
- Besuchen Sie ein Open Data Portal (z.B. [GovData](https://www.govdata.de/), [Daten.BW](https://www.daten-bw.de/))
- Suchen Sie nach CSV/Excel-Dateien mit statistischen Daten
- Laden Sie die Datei herunter

### 2. Daten vorbereiten
- Speichern Sie die Datei im Ordner `data/raw/`
- Stellen Sie sicher, dass das Format unterstützt wird:
  - **CSV**: Mit Komma oder Semikolon getrennt
  - **Excel**: XLS oder XLSX
  - **PDF**: Mit Tabellen (wird automatisch extrahiert)

### 3. Daten laden
- Öffnen Sie die App
- Gehen Sie zur Seite "Daten abrufen"
- Wählen Sie die Datei aus der Liste aus
- Die Daten werden automatisch geladen

### 4. Visualisierung anpassen
- Die App erkennt automatisch verschiedene Datentypen
- Für Migrationsdaten: Erwartet Spalte "herkunftsgebiet_wegzugsgebiet"
- Für Bevölkerungsdaten: Erwartet Spalten "jahr" und "einwohner"
- Passen Sie `src/visualizer.py` an, um neue Visualisierungen hinzuzufügen

## Unterstützte Portale

- **Open Data Konstanz**: https://offenedaten-konstanz.de/
- **Daten.BW**: https://www.daten-bw.de/ (Baden-Württemberg)
- **GovData**: https://www.govdata.de/ (Deutschland)
- **Open Data Berlin**: https://daten.berlin.de/
- **Open Data Hamburg**: https://suche.transparenz.hamburg.de/

## Technische Details

### CSV-Format
- Deutsche CSV-Dateien verwenden oft Semikolon (`;`) als Trennzeichen
- Die App erkennt automatisch das Trennzeichen
- Encoding: UTF-8 wird bevorzugt

### Datenstruktur
- Erste Zeile sollte Spaltenüberschriften enthalten
- Numerische Daten sollten als Zahlen (nicht Text) vorliegen
- Datumsspalten werden automatisch erkannt und normalisiert

### Anpassungen
- **Neue Visualisierungen**: Fügen Sie Funktionen in `src/visualizer.py` hinzu
- **Datenbereinigung**: Passen Sie `src/standardizer.py` an
- **Analyse**: Erweitern Sie `src/analyzer.py`

## Beispiel: Eigene Visualisierung

```python
# In src/visualizer.py
def plot_custom_data(self):
    """Erstellt eine benutzerdefinierte Visualisierung"""
    fig = go.Figure()
    # ... Ihr Code ...
    return fig
```

Dann in `app.py`:
```python
if 'custom_column' in df.columns:
    fig = visualizer.plot_custom_data()
    st.plotly_chart(fig, use_container_width=True)
```




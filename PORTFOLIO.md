# Portfolio-Projekt: Konstanz Open Data Explorer

## 🎯 Projekt-Zusammenfassung

**Ziel:** Demonstration von Datenvisualisierung mit Python und Streamlit

**Dauer:** Portfolio-Projekt (1-2 Tage)

**Technologien:** Python, Streamlit, Pandas, Plotly

## 📊 Was wurde demonstriert?

### 1. Datenverarbeitung
- CSV-Parsing mit Pandas (semicolon-delimited)
- Datenaggregation und -transformation
- Extraktion von Zeitreihendaten

### 2. Datenvisualisierung
- 5 interaktive Plotly-Grafiken
- Responsive Design für Desktop und Mobile
- Rohdaten-Export für Transparenz

### 3. Web-App Entwicklung
- Streamlit für schnelle Prototypen
- Session State Management
- Sidebar-Navigation

### 4. Open Data Integration
- CKAN API Integration (optional)
- Automatischer Daten-Download
- Datenstandardisierung

## 📁 Code-Struktur

```
app.py (200 Zeilen)
├── Streamlit UI
├── Datenladung
└── Visualisierungs-Integration

src/visualizer.py (400 Zeilen)
├── DataVisualizer Klasse
├── plot_migration_data() - 3 Hauptgrafiken
└── plot_top_countries_by_year() - 2 Jahresgrafiken
```

## 🚀 Deployment

- **Plattform:** Streamlit Cloud (kostenlos)
- **Deployment-Zeit:** < 5 Minuten
- **Dependencies:** Nur 3 Pakete (pandas, plotly, streamlit)

## 📈 Metriken

- **Code-Zeilen:** ~600 Zeilen (ohne Kommentare)
- **Dependencies:** 3 Pakete
- **Grafiken:** 5 interaktive Visualisierungen
- **Datenquelle:** Open Data Konstanz (2010-2023)

## 💡 Lessons Learned

1. **Streamlit ist ideal für Portfolio-Projekte:**
   - Schnelle Entwicklung
   - Keine Frontend-Kenntnisse nötig
   - Einfaches Deployment

2. **Plotly für interaktive Visualisierungen:**
   - Bessere UX als statische Grafiken
   - Einfache Integration in Streamlit

3. **Minimalistische Dependencies:**
   - Weniger = besser für Deployment
   - Schnellere Installation

## 🔗 Links

- **GitHub:** [Repository-Link]
- **Live Demo:** [Streamlit Cloud Link]
- **Datenquelle:** https://offenedaten-konstanz.de/

## 📝 Nächste Schritte (Optional)

- [ ] Weitere Datensätze hinzufügen
- [ ] Machine Learning Integration
- [ ] Export-Funktionalität (PDF, Excel)
- [ ] Multi-Language Support



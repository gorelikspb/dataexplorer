"""
Streamlit App für Konstanz Open Data Explorer
Mini-Web-App zur Analyse und Visualisierung von Statistikdaten
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import sys

# Füge src zum Pfad hinzu
sys.path.append(str(Path(__file__).parent))

from src.visualizer import DataVisualizer

# Konfiguration
st.set_page_config(
    page_title="Konstanz Open Data Explorer",
    page_icon="📊",
    layout="wide"
)

# Titel
st.title("📊 Konstanz Open Data Explorer")
st.markdown("**Prototyp eines Werkzeugs zur Analyse und Strukturierung offener Statistikdaten der Stadt Konstanz**")

# Sidebar - app information (visible on desktop)
with st.sidebar:
    st.title("Konstanz Open Data Explorer")
    st.markdown("**Version 0.1.0**")
    st.markdown("---")
    
    st.markdown("### 📊 Datenquelle")
    st.markdown("**Datenquelle:** [Open Data Konstanz](https://offenedaten-konstanz.de/)")
    st.markdown("**Aktueller Datensatz:** Außenwanderung nach Herkunfts- und Zielgebiet (2010-2023)")
    
    with st.expander("🔧 Technische Umsetzung", expanded=False):
        st.markdown("""
        **Implementierung:**
        - **Backend:** Python 3.9+ mit Pandas für Datenverarbeitung
        - **Visualisierung:** Plotly für interaktive Grafiken
        - **Web-Framework:** Streamlit für die Benutzeroberfläche
        - **Datenquelle:** CKAN API von Open Data Konstanz
        
        **Funktionalitäten:**
        - Automatische Erkennung von Migrationsdaten
        - Dynamische Visualisierung mit Jahresauswahl
        - Export von Rohdaten für jeden Graphen
        - Responsive Design für Desktop und Mobile
        """)
    
    st.markdown("---")
    st.markdown("### 📧 Weitere Analysen")
    st.markdown("""
    Für andere Datenquellen: [gorelikgo@gmail.com](mailto:gorelikgo@gmail.com)
    """)

# Session State
if 'current_data' not in st.session_state:
    st.session_state.current_data = None
if 'current_file' not in st.session_state:
    st.session_state.current_file = None

# Automatically load migration file on startup
if st.session_state.current_data is None:
    migration_file = Path("data/raw/Aussenwanderung_nach_Herkunfts_Ziel-Staat_2010-2023_0_0.csv")
    if migration_file.exists():
        try:
            df = pd.read_csv(migration_file, sep=';', encoding='utf-8')
            st.session_state.current_data = df
            st.session_state.current_file = migration_file.name
        except:
            pass

# Main content - visualization only
st.header("📊 Visualisierung")

if st.session_state.current_data is None:
    st.info("Daten werden automatisch geladen...")
else:
    df = st.session_state.current_data
    
    # Prüfe Datentyp und zeige passende Visualisierungen
    visualizer = DataVisualizer(df)
    
    # Spezielle Visualisierung für Migrationsdaten
    if 'herkunftsgebiet_wegzugsgebiet' in df.columns:
        st.subheader("Außenwanderung Konstanz 2010-2023")
        
        # Interesting facts and patterns
        with st.expander("🔍 Interessante Fakten und Muster", expanded=False):
            st.markdown("""
            **Wichtige Erkenntnisse aus der Analyse:**
            
            **1. Ukraine-Krise 2022:**
            - Im Jahr 2022 gab es einen dramatischen Anstieg der Zuzüge aus der Ukraine: **1.478 Personen** (vs. durchschnittlich ~20-50 in den Vorjahren)
            - Das Migrationssaldo betrug **+1.253** (1.478 Zuzug - 225 Wegzug), was den größten Einzeljahreseffekt für ein Land darstellt
            - Dies spiegelt die Fluchtbewegungen nach dem Beginn des Krieges wider
            
            **2. Geografische Nähe zu Schweiz:**
            - Die Schweiz ist durchgehend das Land mit den höchsten Wegzügen (813 in 2023, 799 in 2022)
            - Dies ist logisch, da Konstanz direkt an der Schweizer Grenze liegt und viele Menschen für Arbeit oder Lebensqualität in die Schweiz ziehen
            
            **3. Regionale Migration innerhalb Deutschlands:**
            - **Baden-Württemberg** ist der größte Zuzugsquelle (4.482 in 2023, 4.577 in 2022)
            - **Deutschland (ohne BW)** folgt als zweitgrößte Quelle (1.737 in 2023)
            - Dies zeigt die Bedeutung der Binnenmigration innerhalb Deutschlands
            
            **4. Stabile europäische Migration:**
            - Länder wie **Italien**, **Polen**, **Rumänien** und **Kroatien** zeigen kontinuierlich hohe Migrationszahlen
            - Diese spiegeln die EU-Freizügigkeit und Arbeitsmigration wider
            
            **5. Langfristige Trends:**
            - Die Gesamtzahl der Zuzüge schwankt zwischen ~6.000-7.000 Personen pro Jahr
            - Das Migrationssaldo ist meist positiv, was auf ein Bevölkerungswachstum durch Migration hinweist
            - Die COVID-19-Pandemie (2020-2021) zeigt leichte Rückgänge in der Migration
            """)
        
        with st.spinner("Erstelle Visualisierungen..."):
            figures, available_years = visualizer.plot_migration_data()
            
            if figures:
                # Chart 1: Time series
                if len(figures) > 0:
                    st.plotly_chart(figures[0], use_container_width=True)
                    
                    # Show raw data for this chart
                    with st.expander("📋 Rohdaten: Gesamtmigration nach Jahren", expanded=False):
                        # Extract data from chart
                        years_data = figures[0].data[0].x
                        zuzug_data = figures[0].data[0].y
                        wegzug_data = figures[0].data[1].y
                        
                        summary_df = pd.DataFrame({
                            'Jahr': years_data,
                            'Zuzug': zuzug_data,
                            'Wegzug': wegzug_data,
                            'Saldo': [z - w for z, w in zip(zuzug_data, wegzug_data)]
                        })
                        st.dataframe(summary_df, use_container_width=True)
                
                # Chart 2: Migration balance
                if len(figures) > 1:
                    st.plotly_chart(figures[1], use_container_width=True)
                
                # Charts 3 and 4: Top 10 countries by Zuzug and Wegzug (with year selection)
                st.subheader("Top 10 Länder nach Zuzug und Wegzug")
                
                # Dropdown for year selection
                if available_years:
                    selected_year = st.selectbox(
                        "Jahr auswählen:",
                        available_years,
                        index=len(available_years) - 1  # Default to last year
                    )
                    
                    if selected_year:
                        try:
                            fig_zuzug, fig_wegzug = visualizer.plot_top_countries_by_year(selected_year)
                            
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                if fig_zuzug is not None:
                                    st.plotly_chart(fig_zuzug, use_container_width=True)
                                    
                                    with st.expander("📋 Rohdaten: Top 10 Zuzug", expanded=False):
                                        countries_z = fig_zuzug.data[0].y
                                        values_z = fig_zuzug.data[0].x
                                        zuzug_df = pd.DataFrame({
                                            'Land': countries_z,
                                            f'Zuzug {selected_year}': values_z
                                        })
                                        st.dataframe(zuzug_df, use_container_width=True)
                                        st.caption(f"Anzahl der Zuzüge (Ankünfte) aus jedem Land im Jahr {selected_year}")
                                else:
                                    st.warning("Keine Zuzug-Daten verfügbar für dieses Jahr")
                            
                            with col2:
                                if fig_wegzug is not None:
                                    st.plotly_chart(fig_wegzug, use_container_width=True)
                                    
                                    with st.expander("📋 Rohdaten: Top 10 Wegzug", expanded=False):
                                        countries_w = fig_wegzug.data[0].y
                                        values_w = fig_wegzug.data[0].x
                                        wegzug_df = pd.DataFrame({
                                            'Land': countries_w,
                                            f'Wegzug {selected_year}': values_w
                                        })
                                        st.dataframe(wegzug_df, use_container_width=True)
                                        st.caption(f"Anzahl der Fortzüge (Abgänge) in jedes Land im Jahr {selected_year}")
                                else:
                                    st.warning("Keine Wegzug-Daten verfügbar für dieses Jahr")
                        except Exception as e:
                            st.error(f"Fehler beim Erstellen der Grafiken: {e}")
                            st.exception(e)
                else:
                    st.warning("Keine Jahre verfügbar")
                
                # Chart 5: Top countries dynamics
                if len(figures) > 2:
                    st.plotly_chart(figures[2], use_container_width=True)
                    st.caption("**Hinweis:** Migrationssaldo = Zuzug - Wegzug. Positive Werte bedeuten Netto-Zuzug (mehr Menschen ziehen zu als weg), negative Werte bedeuten Netto-Wegzug.")
                    
                    # Show raw data for dynamics chart
                    with st.expander("📋 Rohdaten: Migrationssaldo Top 5 Länder nach Jahren", expanded=False):
                        # Extract data from chart
                        years_dyn = figures[2].data[0].x
                        countries_dyn = [trace.name for trace in figures[2].data]
                        saldo_data = {country: trace.y for country, trace in zip(countries_dyn, figures[2].data)}
                        
                        dyn_df = pd.DataFrame({
                            'Jahr': years_dyn,
                            **{country: saldo_data[country] for country in countries_dyn}
                        })
                        st.dataframe(dyn_df, use_container_width=True)
                        st.caption("Migrationssaldo = Zuzug - Wegzug. Beispiel: Ukraine 2022: 1478 Zuzug - 225 Wegzug = 1253 Saldo")
            else:
                st.warning("Konnte keine Visualisierungen erstellen")


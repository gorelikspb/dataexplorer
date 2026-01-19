"""
Modul zur Visualisierung von Migrationsdaten
Spezialisiert auf Außenwanderung nach Herkunfts- und Zielgebiet
"""

import pandas as pd
import plotly.graph_objects as go
from typing import Optional, List, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataVisualizer:
    """Klasse zur Visualisierung von Migrationsdaten"""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
    
    def _clean_country_name(self, name: str) -> str:
        """Bereinigt Ländernamen (entfernt Präfixe wie '121_')"""
        parts = name.split('_', 1)
        if len(parts) > 1 and parts[0].isdigit():
            return parts[1].replace('_', ' ').title()
        return name.replace('_', ' ').title()

    def plot_migration_data(self) -> Tuple[List[go.Figure], List[int]]:
        """
        Spezielle Visualisierung für Migrationsdaten (Aussenwanderung)
        Erstellt mehrere Grafiken: Zeitreihe, Migrationssaldo, Dynamik Top-Länder
        
        Returns:
            Tuple von (Liste von Figuren, Liste von verfügbaren Jahren)
        """
        figures = []
        
        # Check if this is migration data
        if 'herkunftsgebiet_wegzugsgebiet' not in self.df.columns:
            logger.warning("Keine Migrationsdaten erkannt")
            return figures, []
        
        # Extrahiere Daten
        key_col = 'herkunftsgebiet_wegzugsgebiet'
        
        # Finde Zeile mit Kontinenten (für Filterung)
        continent_row = None
        for idx, val in enumerate(self.df[key_col]):
            if 'Kontinent' in str(val):
                continent_row = idx
                break
        
        # Extrahiere Jahre und Typen (Zuzug/Wegzug)
        years = []
        zuzug_data = {}
        wegzug_data = {}
        
        for idx, row_key in enumerate(self.df[key_col]):
            if pd.isna(row_key):
                continue
            
            row_key_str = str(row_key).strip()
            
            # Parse Jahr und Typ
            if '_ Zuzug' in row_key_str:
                year = int(row_key_str.split('_')[0])
                years.append(year)
                
                # Extrahiere Daten nach Ländern (überspringe Kontinente)
                row_data = self.df.iloc[idx]
                for col in self.df.columns:
                    if col == key_col or col == 'quelle':
                        continue
                    
                    # Überspringe wenn Kontinent
                    if continent_row is not None:
                        continent_val = str(self.df.iloc[continent_row][col])
                        if continent_val in ['Europa', 'Afrika', 'Amerika', 'Asien', 'Australien Ozeanien', '.']:
                            continue
                    
                    country = col
                    value = row_data[col]
                    
                    # Versuche in Zahl zu konvertieren
                    try:
                        if pd.notna(value) and str(value).strip() != '':
                            val = float(str(value).replace(',', '.'))
                            if country not in zuzug_data:
                                zuzug_data[country] = {}
                            zuzug_data[country][year] = val
                    except:
                        pass
            
            elif '_ Wegzug' in row_key_str:
                year = int(row_key_str.split('_')[0])
                
                row_data = self.df.iloc[idx]
                for col in self.df.columns:
                    if col == key_col or col == 'quelle':
                        continue
                    
                    if continent_row is not None:
                        continent_val = str(self.df.iloc[continent_row][col])
                        if continent_val in ['Europa', 'Afrika', 'Amerika', 'Asien', 'Australien Ozeanien', '.']:
                            continue
                    
                    country = col
                    value = row_data[col]
                    
                    try:
                        if pd.notna(value) and str(value).strip() != '':
                            val = float(str(value).replace(',', '.'))
                            if country not in wegzug_data:
                                wegzug_data[country] = {}
                            wegzug_data[country][year] = val
                    except:
                        pass
        
        years = sorted(set(years))
        
        if not years:
            logger.warning("Keine Jahresdaten gefunden")
            return figures, []
        
        # Chart 1: Time series of total migration
        # Sum directly from rows
        total_zuzug = []
        total_wegzug = []
        
        for year in years:
            z_sum = 0
            w_sum = 0
            
            # Finde Zeile für Zuzug
            for idx, row_key in enumerate(self.df[key_col]):
                row_key_str = str(row_key).strip()
                if f'{year}_ Zuzug' in row_key_str:
                    row_data = self.df.iloc[idx]
                    # Summiere alle numerischen Werte in der Zeile (außer erste Spalte)
                    for col in self.df.columns:
                        if col == key_col or col == 'quelle':
                            continue
                        try:
                            val = row_data[col]
                            if pd.notna(val) and str(val).strip() != '':
                                num_val = float(str(val).replace(',', '.'))
                                z_sum += num_val
                        except:
                            pass
                    break
            
            # Finde Zeile für Wegzug
            for idx, row_key in enumerate(self.df[key_col]):
                row_key_str = str(row_key).strip()
                if f'{year}_ Wegzug' in row_key_str:
                    row_data = self.df.iloc[idx]
                    for col in self.df.columns:
                        if col == key_col or col == 'quelle':
                            continue
                        try:
                            val = row_data[col]
                            if pd.notna(val) and str(val).strip() != '':
                                num_val = float(str(val).replace(',', '.'))
                                w_sum += num_val
                        except:
                            pass
                    break
            
            total_zuzug.append(z_sum)
            total_wegzug.append(w_sum)
        
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(
            x=years,
            y=total_zuzug,
            mode='lines+markers',
            name='Zuzug (Ankunft)',
            line=dict(color='#2ecc71', width=3),
            marker=dict(size=8)
        ))
        fig1.add_trace(go.Scatter(
            x=years,
            y=total_wegzug,
            mode='lines+markers',
            name='Wegzug (Abgang)',
            line=dict(color='#e74c3c', width=3),
            marker=dict(size=8)
        ))
        fig1.update_layout(
            title='Außenwanderung Konstanz 2010-2023',
            xaxis_title='Jahr',
            yaxis_title='Anzahl Personen',
            template='plotly_white',
            hovermode='x unified',
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
            margin=dict(l=60, r=60, t=60, b=100),  # Increase bottom margin
            xaxis=dict(
                title_standoff=15  # X-axis title offset
            ),
            annotations=[
                dict(
                    text="<b>Berechnung:</b> Summe aller Zu- und Fortzüge pro Jahr. Daten aus Zeilen 'Jahr_ Zuzug' und 'Jahr_ Wegzug'",
                    xref="paper", yref="paper",
                    x=0.5, y=-0.18,  # Increase bottom offset to avoid overlapping with axis label
                    xanchor="center", yanchor="top",
                    showarrow=False,
                    font=dict(size=9, color="gray")
                )
            ]
        )
        figures.append(fig1)
        
        # Chart 2: Migration balance by year
        saldo = [z - w for z, w in zip(total_zuzug, total_wegzug)]
        
        colors = ['#2ecc71' if s > 0 else '#e74c3c' for s in saldo]
        
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=years,
            y=saldo,
            name='Migrationssaldo',
            marker_color=colors,
            text=[f'+{s:.0f}' if s > 0 else f'{s:.0f}' for s in saldo],
            textposition='outside'
        ))
        fig2.add_hline(y=0, line_dash="dash", line_color="gray")
        fig2.update_layout(
            title='Migrationssaldo (Zuzug - Wegzug)',
            xaxis_title='Jahr',
            yaxis_title='Saldo',
            template='plotly_white',
            showlegend=False,
            margin=dict(b=100),  # Increase bottom margin
            xaxis=dict(title_standoff=15),  # X-axis title offset
            annotations=[
                dict(
                    text="<b>Berechnung:</b> Migrationssaldo = Zuzug - Wegzug. Positive Werte = mehr Zuzüge, negative = mehr Fortzüge",
                    xref="paper", yref="paper",
                    x=0.5, y=-0.18,  # Move annotation lower to avoid overlapping with axis label
                    xanchor="center", yanchor="top",
                    showarrow=False,
                    font=dict(size=9, color="gray")  # Slightly smaller font
                )
            ]
        )
        figures.append(fig2)
        
        # Chart 3: Top countries dynamics over years
        if len(years) > 1:
            # Determine top countries (based on max absolute saldo across all years)
            # This ensures countries with significant migration peaks (like Ukraine 2022) are included
            country_max_abs_saldo = {}
            for year in years:
                zuzug_row_idx = None
                wegzug_row_idx = None
                for idx, row_key in enumerate(self.df[key_col]):
                    row_key_str = str(row_key).strip()
                    if f'{year}_ Zuzug' in row_key_str:
                        zuzug_row_idx = idx
                    elif f'{year}_ Wegzug' in row_key_str:
                        wegzug_row_idx = idx
                
                if zuzug_row_idx is not None and wegzug_row_idx is not None:
                    zuzug_data_row = self.df.iloc[zuzug_row_idx]
                    wegzug_data_row = self.df.iloc[wegzug_row_idx]
                    
                    for col in self.df.columns:
                        if col == key_col or col == 'quelle' or col in ['sonstige_staaten', 'unbekannt_ohne_angaben']:
                            continue
                        try:
                            z_val = zuzug_data_row[col]
                            w_val = wegzug_data_row[col]
                            z = float(str(z_val).replace(',', '.')) if pd.notna(z_val) and str(z_val).strip() != '' and str(z_val).strip() != 'nan' else 0
                            w = float(str(w_val).replace(',', '.')) if pd.notna(w_val) and str(w_val).strip() != '' and str(w_val).strip() != 'nan' else 0
                            abs_saldo = abs(z - w)
                            # Keep maximum absolute saldo for each country
                            if col not in country_max_abs_saldo or abs_saldo > country_max_abs_saldo[col]:
                                country_max_abs_saldo[col] = abs_saldo
                        except:
                            pass

            sorted_countries_by_saldo = sorted(country_max_abs_saldo.items(), key=lambda x: x[1], reverse=True)
            top_countries = [c[0] for c in sorted_countries_by_saldo[:5]]  # Top-5 by max absolute saldo
            
            # Collect yearly data for these countries
            country_yearly_data = {country: {'zuzug': [], 'wegzug': [], 'saldo': []} for country in top_countries}
            
            for year in years:
                # Find rows for this year
                zuzug_row_idx = None
                wegzug_row_idx = None
                
                for idx, row_key in enumerate(self.df[key_col]):
                    row_key_str = str(row_key).strip()
                    if f'{year}_ Zuzug' in row_key_str:
                        zuzug_row_idx = idx
                    elif f'{year}_ Wegzug' in row_key_str:
                        wegzug_row_idx = idx
                
                if zuzug_row_idx is not None and wegzug_row_idx is not None:
                    zuzug_row = self.df.iloc[zuzug_row_idx]
                    wegzug_row = self.df.iloc[wegzug_row_idx]
                    
                    for country_col in top_countries:
                        try:
                            z_val = zuzug_row[country_col]
                            w_val = wegzug_row[country_col]
                            
                            z = 0
                            w = 0
                            
                            if pd.notna(z_val) and str(z_val).strip() != '' and str(z_val).strip() != 'nan':
                                z = float(str(z_val).replace(',', '.'))
                            if pd.notna(w_val) and str(w_val).strip() != '' and str(w_val).strip() != 'nan':
                                w = float(str(w_val).replace(',', '.'))
                            
                            country_yearly_data[country_col]['zuzug'].append(z)
                            country_yearly_data[country_col]['wegzug'].append(w)
                            country_yearly_data[country_col]['saldo'].append(z - w)
                        except:
                            country_yearly_data[country_col]['zuzug'].append(0)
                            country_yearly_data[country_col]['wegzug'].append(0)
                            country_yearly_data[country_col]['saldo'].append(0)
            
            # Create chart
            fig3 = go.Figure()
            
            # Add lines for top-5 countries
            colors = ['#3498db', '#2ecc71', '#e74c3c', '#f39c12', '#9b59b6']
            for idx, country_col in enumerate(top_countries):
                country_name = self._clean_country_name(country_col)
                saldo_data = country_yearly_data[country_col]['saldo']
                
                fig3.add_trace(go.Scatter(
                    x=years,
                    y=saldo_data,
                    mode='lines+markers',
                    name=country_name,
                    line=dict(color=colors[idx % len(colors)], width=2),
                    marker=dict(size=6)
                ))
            
            fig3.update_layout(
                title='Migrationssaldo der Top 5 Länder (2010-2023)',
                xaxis_title='Jahr',
                yaxis_title='Migrationssaldo (Zuzug - Wegzug)',
                template='plotly_white',
                hovermode='x unified',
                legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
                height=400,
                margin=dict(b=100),
                xaxis=dict(title_standoff=15),
                annotations=[
                    dict(
                        text="<b>Berechnung:</b> Migrationssaldo = Zuzug - Wegzug (positive Werte = Netto-Zuzug, negative = Netto-Wegzug)<br><b>Datenquelle:</b> Zeilen 'Jahr_ Zuzug' und 'Jahr_ Wegzug' aus dem Datensatz",
                        xref="paper", yref="paper",
                        x=0.5, y=-0.18,
                        xanchor="center", yanchor="top",
                        showarrow=False,
                        font=dict(size=9, color="gray")
                    )
                ]
            )
            fig3.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
            figures.append(fig3)
        
        return figures, years
    
    def plot_top_countries_by_year(self, selected_year: int):
        """
        Erstellt zwei Grafiken: Top 10 Länder nach Zuzug und Top 10 Länder nach Wegzug für ein bestimmtes Jahr
        
        Args:
            selected_year: Das ausgewählte Jahr
            
        Returns:
            Tuple von (fig_zuzug, fig_wegzug) oder (None, None) wenn keine Daten
        """
        key_col = 'herkunftsgebiet_wegzugsgebiet'
        
        if key_col not in self.df.columns:
            return None, None
        
        # Finde Zeilen für das ausgewählte Jahr
        zuzug_row = None
        wegzug_row = None
        
        for idx, row_key in enumerate(self.df[key_col]):
            row_key_str = str(row_key).strip()
            if f'{selected_year}_ Zuzug' in row_key_str:
                zuzug_row = idx
            elif f'{selected_year}_ Wegzug' in row_key_str:
                wegzug_row = idx
        
        if zuzug_row is None or wegzug_row is None:
            return None, None
        
        zuzug_data_row = self.df.iloc[zuzug_row]
        wegzug_data_row = self.df.iloc[wegzug_row]
        
        # Sammle Daten für Zuzug
        zuzug_totals = {}
        for col in self.df.columns:
            if col == key_col or col == 'quelle':
                continue
            if col in ['sonstige_staaten', 'unbekannt_ohne_angaben']:
                continue
            
            try:
                z_val = zuzug_data_row[col]
                z = 0
                if pd.notna(z_val) and str(z_val).strip() != '' and str(z_val).strip() != 'nan':
                    z = float(str(z_val).replace(',', '.'))
                if z > 0:
                    zuzug_totals[col] = z
            except:
                pass
        
        # Sammle Daten für Wegzug
        wegzug_totals = {}
        for col in self.df.columns:
            if col == key_col or col == 'quelle':
                continue
            if col in ['sonstige_staaten', 'unbekannt_ohne_angaben']:
                continue
            
            try:
                w_val = wegzug_data_row[col]
                w = 0
                if pd.notna(w_val) and str(w_val).strip() != '' and str(w_val).strip() != 'nan':
                    w = float(str(w_val).replace(',', '.'))
                if w > 0:
                    wegzug_totals[col] = w
            except:
                pass
        
        # Erstelle Grafik für Zuzug
        fig_zuzug = None
        if zuzug_totals:
            sorted_zuzug = sorted(zuzug_totals.items(), key=lambda x: x[1], reverse=True)[:10]
            countries_z = [self._clean_country_name(c[0]) for c in sorted_zuzug]
            values_z = [float(c[1]) for c in sorted_zuzug]
            
            fig_zuzug = go.Figure()
            fig_zuzug.add_trace(go.Bar(
                x=values_z,
                y=countries_z,
                orientation='h',
                marker_color='#2ecc71',
                text=[f'{v:.0f}' for v in values_z],
                textposition='outside',
                textfont=dict(size=11)
            ))
            fig_zuzug.update_layout(
                title=f'Top 10 Länder nach Zuzug {selected_year}',
                xaxis_title='Anzahl Personen (Zuzug)',
                yaxis_title='Land',
                template='plotly_white',
                height=500,
                yaxis=dict(autorange='reversed'),
                margin=dict(l=120, r=100, t=60, b=120),  # Increase margins: right for numbers, bottom for annotations
                xaxis=dict(
                    title_standoff=15  # X-axis title offset
                ),
                annotations=[
                    dict(
                        text=f"<b>Berechnung:</b> Anzahl der Zuzüge (Ankünfte) aus jedem Land im Jahr {selected_year}",
                        xref="paper", yref="paper",
                        x=0.5, y=-0.20,  # Increase bottom offset to avoid overlapping with axis label
                        xanchor="center", yanchor="top",
                        showarrow=False,
                        font=dict(size=9, color="gray")
                    )
                ]
            )
        
        # Erstelle Grafik für Wegzug
        fig_wegzug = None
        if wegzug_totals:
            sorted_wegzug = sorted(wegzug_totals.items(), key=lambda x: x[1], reverse=True)[:10]
            countries_w = [self._clean_country_name(c[0]) for c in sorted_wegzug]
            values_w = [float(c[1]) for c in sorted_wegzug]
            
            fig_wegzug = go.Figure()
            fig_wegzug.add_trace(go.Bar(
                x=values_w,
                y=countries_w,
                orientation='h',
                marker_color='#e74c3c',
                text=[f'{v:.0f}' for v in values_w],
                textposition='outside',
                textfont=dict(size=11)
            ))
            fig_wegzug.update_layout(
                title=f'Top 10 Länder nach Wegzug {selected_year}',
                xaxis_title='Anzahl Personen (Wegzug)',
                yaxis_title='Land',
                template='plotly_white',
                height=500,
                yaxis=dict(autorange='reversed'),
                margin=dict(l=120, r=100, t=60, b=120),  # Increase margins: right for numbers, bottom for annotations
                xaxis=dict(
                    title_standoff=15  # X-axis title offset
                ),
                annotations=[
                    dict(
                        text=f"<b>Berechnung:</b> Anzahl der Fortzüge (Abgänge) in jedes Land im Jahr {selected_year}",
                        xref="paper", yref="paper",
                        x=0.5, y=-0.20,  # Increase bottom offset to avoid overlapping with axis label
                        xanchor="center", yanchor="top",
                        showarrow=False,
                        font=dict(size=9, color="gray")
                    )
                ]
            )
        
        return fig_zuzug, fig_wegzug


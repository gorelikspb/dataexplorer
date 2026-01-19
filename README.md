# Konstanz Open Data Explorer

Portfolio project: Interactive visualization of open data from the city of Konstanz.

A simple Streamlit app for visualizing migration data from Konstanz (2010-2023).

## Quick Start

### Local Installation

1. Clone repository:
```bash
git clone https://github.com/gorelikspb/dataexplorer.git
cd konstanz_data
```

2. Create virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # Linux/Mac
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run app:
```bash
streamlit run streamlit_app.py
```

The app automatically loads `Aussenwanderung_nach_Herkunfts_Ziel-Staat_2010-2023_0_0.csv` on startup if present.

## Project Structure

```
konstanz_data/
├── streamlit_app.py      # Main Streamlit app
├── src/
│   └── visualizer.py     # Visualization logic
├── data/
│   └── raw/              # CSV files (not in Git)
├── requirements.txt      # Dependencies
└── README.md
```

## Data Source

Open Data Konstanz: https://offenedaten-konstanz.de/

Current dataset: Migration by origin and destination (2010-2023)

## Technology Stack

- Python 3.9+
- Streamlit - Web app framework
- Pandas - Data processing
- Plotly - Interactive visualizations

## Features

- 5 interactive visualizations:
  - Total migration by year (immigration/emigration)
  - Migration balance over time
  - Top 10 countries by immigration (with year selection)
  - Top 10 countries by emigration (with year selection)
  - Migration balance of top 5 countries (2010-2023)
- Raw data export for each chart
- Automatic data loading on startup

## Deployment

See [DEPLOY.md](DEPLOY.md) for deployment instructions.

## Contact

For questions or other data sources: gorelikgo@gmail.com

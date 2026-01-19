"""
Direktes Herunterladen von bekannten CSV-Dateien von Open Data Konstanz
"""

import requests
from pathlib import Path
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "https://offenedaten-konstanz.de"
DATA_DIR = Path(__file__).parent.parent / "data" / "raw"

# Bekannte Datensätze mit direkten CSV-Links
KNOWN_DATASETS = [
    {
        'name': 'einwohner-nach-stadtviertel',
        'title': 'Einwohner nach Stadtviertel',
        'url': 'https://offenedaten-konstanz.de/dataset/einwohner-nach-stadtviertel',
        'csv_urls': [
            'https://offenedaten-konstanz.de/dataset/einwohner-nach-stadtviertel/resource/einwohner-nach-stadtviertel/download/einwohner-nach-stadtviertel.csv'
        ]
    },
    {
        'name': 'geschwindigkeits-berwachung-jahresstatistik',
        'title': 'Geschwindigkeitsüberwachung Jahresstatistik',
        'url': 'https://offenedaten-konstanz.de/dataset/geschwindigkeits-berwachung-jahresstatistik',
        'csv_urls': []
    },
    {
        'name': 'wetterstationen',
        'title': 'Wetterstationen Smart Green City',
        'url': 'https://offenedaten-konstanz.de/dataset/wetterstationen-programm-smart-green-city',
        'csv_urls': []
    }
]


def get_resource_urls_from_api(dataset_id):
    """
    Ruft URLs von Ressourcen über API ab
    Gibt zurück: (csv_urls, dataset_info)
    """
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    
    api_url = f"{BASE_URL}/api/3/action/package_show"
    
    try:
        response = session.get(api_url, params={'id': dataset_id}, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get('success'):
            result = data.get('result')
            # API kann Dict oder List zurückgeben
            if isinstance(result, list) and len(result) > 0:
                result = result[0]
            
            if isinstance(result, dict):
                resources = result.get('resources', [])
                
                # Extrahiere Metadaten
                dataset_info = {
                    'title': result.get('title', dataset_id),
                    'description': result.get('notes', ''),
                    'url': result.get('url', ''),
                    'tags': [tag.get('name', '') if isinstance(tag, dict) else tag for tag in result.get('tags', [])]
                }
                
                # Suche nach CSV/JSON Ressourcen, priorisiere CSV
                csv_resources = []
                json_resources = []
                
                for resource in resources:
                    if isinstance(resource, dict):
                        url = resource.get('url', '')
                        format_type = resource.get('format', '').upper()
                        name = resource.get('name', '')
                        
                        # Filter: nur 2022
                        if '2022' not in name and '2022' not in url:
                            continue
                        
                        if format_type == 'CSV' or url.endswith('.csv'):
                            csv_resources.append({
                                'url': url,
                                'name': name,
                                'description': resource.get('description', '')
                            })
                        elif format_type == 'JSON' or url.endswith('.json'):
                            json_resources.append({
                                'url': url,
                                'name': name,
                                'description': resource.get('description', '')
                            })
                
                # Priorisiere CSV, sonst JSON
                if csv_resources:
                    return csv_resources, dataset_info
                elif json_resources:
                    return json_resources, dataset_info
        
        return [], {}
    except Exception as e:
        logger.error(f"Fehler beim Abrufen von {dataset_id}: {e}")
        return [], {}


def download_file(url, filename, data_dir):
    """
    Lädt eine Datei herunter
    """
    filepath = data_dir / filename
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    # Überspringe wenn bereits vorhanden
    if filepath.exists():
        logger.info(f"Überspringe (bereits vorhanden): {filename}")
        return filepath
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    
    try:
        logger.info(f"Lade herunter: {url}")
        response = session.get(url, timeout=30, stream=True)
        response.raise_for_status()
        
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        logger.info(f"✓ Erfolgreich: {filepath}")
        return filepath
    except Exception as e:
        logger.error(f"✗ Fehler beim Herunterladen von {url}: {e}")
        return None


def main():
    """
    Lädt bekannte CSV-Dateien herunter
    """
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    downloaded_files = []
    
    # Hole alle Datensätze von API
    logger.info("Hole Liste aller Datensätze...")
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    
    try:
        response = session.get(f"{BASE_URL}/api/3/action/package_list", timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get('success'):
            all_datasets = data.get('result', [])
            logger.info(f"Gefunden: {len(all_datasets)} Datensätze")
            
            # Durchsuche alle Datensätze nach CSV/JSON für 2022
            for dataset_id in all_datasets:
                logger.info(f"Prüfe: {dataset_id}")
                resources, dataset_info = get_resource_urls_from_api(dataset_id)
                
                if resources:
                    logger.info(f"  → {len(resources)} Dateien für 2022 gefunden")
                    
                    # Nimm nur die erste (beste) Ressource
                    resource = resources[0]
                    csv_url = resource['url']
                    
                    # Erstelle Dateiname
                    filename = csv_url.split('/')[-1]
                    if not filename or filename == 'download':
                        filename = f"{dataset_id}.csv"
                    
                    # Lade herunter
                    filepath = download_file(csv_url, filename, DATA_DIR)
                    if filepath:
                        downloaded_files.append({
                            'dataset_id': dataset_id,
                            'filename': filename,
                            'url': csv_url,
                            'title': dataset_info.get('title', dataset_id),
                            'description': dataset_info.get('description', ''),
                            'tags': dataset_info.get('tags', []),
                            'dataset_url': dataset_info.get('url', '')
                        })
    except Exception as e:
        logger.error(f"Fehler: {e}")
    
    # Speichere Metadaten
    metadata_file = DATA_DIR / 'download_metadata.json'
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump(downloaded_files, f, indent=2, ensure_ascii=False)
    
    logger.info(f"\n{'='*60}")
    logger.info(f"Zusammenfassung:")
    logger.info(f"  Heruntergeladen: {len(downloaded_files)} CSV-Dateien")
    logger.info(f"  Speicherort: {DATA_DIR}")
    logger.info(f"  Metadaten: {metadata_file}")
    
    if downloaded_files:
        logger.info(f"\nHeruntergeladene Dateien:")
        for item in downloaded_files:
            logger.info(f"  - {item['filename']} ({item['dataset_id']})")
    
    return downloaded_files


if __name__ == "__main__":
    main()


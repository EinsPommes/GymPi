# GymPi Cloud API

Eine einfache REST-API für die Synchronisation und Verwaltung von GymPi Trainingsdaten.

## Installation

1. Erstelle eine virtuelle Umgebung:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. Installiere die Abhängigkeiten:
```bash
pip install -r requirements.txt
```

## Start der API

```bash
python main.py
```

Die API ist dann unter `http://localhost:8000` erreichbar.

## API-Endpunkte

### POST /workout/sync
Synchronisiert Workout-Daten von einem GymPi-Gerät.

### GET /workout/history/{device_id}
Ruft den Workout-Verlauf für ein bestimmtes Gerät ab.

### GET /workout/stats/{device_id}
Berechnet Trainingsstatistiken für ein Gerät.

## Swagger Dokumentation

Die vollständige API-Dokumentation ist unter `http://localhost:8000/docs` verfügbar.

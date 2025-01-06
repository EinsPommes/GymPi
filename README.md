# GymPi - Tragbares Trainingssystem

Ein tragbares Trainingssystem basierend auf dem Raspberry Pi Zero 2 W mit E-Paper-Display und Pulssensor.

## Hardware-Anforderungen

- Raspberry Pi Zero 2 W
- E-Paper Display (2.9" oder größer)
- MAX30102 Pulssensor
- MPU6050 Bewegungssensor (optional)
- 3.7V Li-Ion Akku mit PowerBoost 1000C

## Installation

1. Installiere die Abhängigkeiten:
```bash
pip install -r requirements.txt
```

2. Aktiviere SPI und I2C auf dem Raspberry Pi:
```bash
sudo raspi-config
```
Navigiere zu "Interface Options" und aktiviere SPI sowie I2C.

## Projektstruktur

- `src/` - Hauptquellcode
  - `display/` - E-Paper Display Funktionen
  - `sensors/` - Sensoren (Puls, Bewegung)
  - `workout/` - Trainingsplan-Management
  - `utils/` - Hilfsfunktionen
  - `cloud/` - Cloud-Synchronisation
    - `api/` - Cloud-API Server
- `config/` - Konfigurationsdateien
- `data/` - Trainingspläne und -daten

## Cloud-API Setup

Die Cloud-API ermöglicht die Synchronisation und Analyse von Trainingsdaten.

### Installation der API

1. Wechsle in das API-Verzeichnis:
```bash
cd src/cloud/api
```

2. Installiere die API-Abhängigkeiten:
```bash
pip install -r requirements.txt
```

3. Starte den API-Server:
```bash
python main.py
```

Die API ist dann unter `http://localhost:8000` erreichbar.

### API-Konfiguration

Setze die Umgebungsvariable für die GymPi-Geräte:
```bash
GYMPI_API_URL=http://localhost:8000
```

### API-Endpunkte

- `POST /workout/sync` - Synchronisiert Workout-Daten
- `GET /workout/history/{device_id}` - Zeigt Trainingshistorie
- `GET /workout/stats/{device_id}` - Zeigt Trainingsstatistiken

Die vollständige API-Dokumentation ist unter `http://localhost:8000/docs` verfügbar.

## Verwendung

1. Starte das Hauptprogramm:
```bash
python src/main.py
```

2. Folge den Anweisungen auf dem E-Paper Display

## Features

- Anzeige von Trainingsplänen
- Echtzeit-Herzfrequenzüberwachung
- Automatische Fortschrittsverfolgung
- Cloud-Synchronisation
- Bewegungserkennung (optional)

## Lizenz

MIT

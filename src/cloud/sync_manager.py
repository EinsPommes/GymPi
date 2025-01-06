import requests
import json
import os
from datetime import datetime
from pathlib import Path
import threading
import queue
import time

class CloudSync:
    def __init__(self, api_url=None):
        self.api_url = api_url or os.getenv('GYMPI_API_URL')
        self.sync_queue = queue.Queue()
        self.sync_thread = None
        self.running = False
        
        # Erstelle einen Ordner für offline Daten
        self.offline_dir = Path(__file__).parent.parent.parent / 'data' / 'offline_data'
        self.offline_dir.mkdir(parents=True, exist_ok=True)
        
    def start_sync_thread(self):
        """Startet den Synchronisations-Thread"""
        self.running = True
        self.sync_thread = threading.Thread(target=self._sync_worker)
        self.sync_thread.daemon = True
        self.sync_thread.start()
        
    def stop_sync_thread(self):
        """Stoppt den Synchronisations-Thread"""
        self.running = False
        if self.sync_thread:
            self.sync_thread.join()
            
    def _sync_worker(self):
        """Worker-Thread für die Synchronisation"""
        while self.running:
            try:
                # Versuche, Daten aus der Queue zu holen
                data = self.sync_queue.get(timeout=1)
                self._send_to_cloud(data)
                self.sync_queue.task_done()
            except queue.Empty:
                # Versuche, offline gespeicherte Daten zu synchronisieren
                self._sync_offline_data()
            except Exception as e:
                print(f"Fehler bei der Synchronisation: {e}")
            time.sleep(1)
            
    def _send_to_cloud(self, data):
        """Sendet Daten an die Cloud"""
        if not self.api_url:
            self._save_offline(data)
            return
            
        try:
            response = requests.post(
                f"{self.api_url}/workout/sync",
                json=data,
                timeout=5
            )
            if response.status_code != 200:
                self._save_offline(data)
        except requests.exceptions.RequestException:
            self._save_offline(data)
            
    def _save_offline(self, data):
        """Speichert Daten lokal für spätere Synchronisation"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = self.offline_dir / f"workout_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(data, f)
            
    def _sync_offline_data(self):
        """Synchronisiert offline gespeicherte Daten"""
        if not self.api_url:
            return
            
        for file in self.offline_dir.glob("workout_*.json"):
            try:
                with open(file, 'r') as f:
                    data = json.load(f)
                
                response = requests.post(
                    f"{self.api_url}/workout/sync",
                    json=data,
                    timeout=5
                )
                
                if response.status_code == 200:
                    os.remove(file)
            except Exception as e:
                print(f"Fehler beim Synchronisieren von {file}: {e}")
                
    def sync_workout_data(self, workout_data):
        """
        Fügt Workout-Daten zur Synchronisations-Queue hinzu
        
        Args:
            workout_data: Dict mit Workout-Informationen
        """
        self.sync_queue.put({
            'timestamp': datetime.now().isoformat(),
            'data': workout_data
        })

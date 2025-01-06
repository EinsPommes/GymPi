import json
import os
from datetime import datetime

class WorkoutManager:
    def __init__(self):
        self.current_workout = None
        self.current_exercise_index = 0
        self.current_set = 1
        self.workout_data_dir = os.path.join(os.path.dirname(__file__), '../../data/workouts')
        os.makedirs(self.workout_data_dir, exist_ok=True)
        
    def load_workout(self, workout_name):
        """Lädt einen Trainingsplan"""
        try:
            file_path = os.path.join(self.workout_data_dir, f"{workout_name}.json")
            with open(file_path, 'r') as f:
                self.current_workout = json.load(f)
            self.current_exercise_index = 0
            self.current_set = 1
            return True
        except Exception as e:
            print(f"Fehler beim Laden des Workouts: {e}")
            return False
            
    def get_current_exercise(self):
        """Gibt die aktuelle Übung zurück"""
        if not self.current_workout:
            return None
        return self.current_workout['exercises'][self.current_exercise_index]
        
    def next_set(self):
        """Geht zum nächsten Satz über"""
        exercise = self.get_current_exercise()
        if not exercise:
            return False
            
        if self.current_set < exercise['sets']:
            self.current_set += 1
            return True
        else:
            return self.next_exercise()
            
    def next_exercise(self):
        """Geht zur nächsten Übung über"""
        if not self.current_workout:
            return False
            
        if self.current_exercise_index < len(self.current_workout['exercises']) - 1:
            self.current_exercise_index += 1
            self.current_set = 1
            return True
        return False
        
    def save_progress(self, heart_rate_data):
        """Speichert den Trainingsfortschritt"""
        if not self.current_workout:
            return
            
        progress = {
            'date': datetime.now().isoformat(),
            'workout_name': self.current_workout['name'],
            'completed_exercises': self.current_exercise_index + 1,
            'heart_rate_data': heart_rate_data
        }
        
        # Speichere in JSON-Datei
        progress_file = os.path.join(self.workout_data_dir, 'progress.json')
        try:
            if os.path.exists(progress_file):
                with open(progress_file, 'r') as f:
                    history = json.load(f)
            else:
                history = []
                
            history.append(progress)
            
            with open(progress_file, 'w') as f:
                json.dump(history, f, indent=2)
                
        except Exception as e:
            print(f"Fehler beim Speichern des Fortschritts: {e}")

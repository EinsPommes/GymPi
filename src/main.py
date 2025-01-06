import time
from display.epaper import EpaperDisplay
from sensors.heart_rate import HeartRateSensor
from sensors.motion import MotionSensor
from workout.workout_manager import WorkoutManager
from cloud.sync_manager import CloudSync

def main():
    try:
        # Initialisiere Komponenten
        display = EpaperDisplay()
        heart_sensor = HeartRateSensor()
        motion_sensor = MotionSensor()
        workout_manager = WorkoutManager()
        cloud_sync = CloudSync()
        
        # Starte Cloud-Sync Thread
        cloud_sync.start_sync_thread()
        
        # Lade Standard-Workout
        if not workout_manager.load_workout("default_workout"):
            display.show_message("Kein Workout gefunden!")
            return
            
        heart_rate_data = []
        rep_count = 0
        last_rep_time = time.time()
        
        while True:
            # Aktuelle Übung holen
            exercise = workout_manager.get_current_exercise()
            if not exercise:
                break
                
            # Herzfrequenz messen
            heart_rate = heart_sensor.read_heart_rate()
            if heart_rate:
                heart_rate_data.append({
                    'timestamp': time.time(),
                    'value': heart_rate
                })
                
            # Bewegungserkennung
            if motion_sensor.detect_rep():
                current_time = time.time()
                # Prüfe auf Mindestzeit zwischen Wiederholungen (0.5 Sekunden)
                if current_time - last_rep_time > 0.5:
                    rep_count += 1
                    last_rep_time = current_time
                    
                    # Wenn alle Wiederholungen eines Satzes gemacht wurden
                    if rep_count >= exercise['reps']:
                        rep_count = 0
                        workout_manager.next_set()
                
            # Display aktualisieren
            display.show_workout(
                exercise['name'],
                exercise['sets'],
                exercise['reps'],
                workout_manager.current_set,
                heart_rate
            )
            display.update()
            
            # Warte kurz
            time.sleep(0.1)
            
        # Workout beendet
        display.show_message("Workout beendet!")
        
        # Speichere und synchronisiere Fortschritt
        workout_data = workout_manager.save_progress(heart_rate_data)
        cloud_sync.sync_workout_data(workout_data)
        
    except KeyboardInterrupt:
        print("\nProgramm beendet")
    finally:
        heart_sensor.close()
        cloud_sync.stop_sync_thread()

if __name__ == "__main__":
    main()

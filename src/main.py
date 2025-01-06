import time
from datetime import datetime
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
        
        # Zeige Startbildschirm
        display.show_message("GymPi", "Bereit zum Training")
        display.update()
        time.sleep(2)
        
        # Zeige letzte Workouts
        history = workout_manager.get_workout_history()
        if history:
            display.show_workout_history(history)
            display.update()
            time.sleep(3)
        
        # Lade Standard-Workout
        if not workout_manager.load_workout("default_workout"):
            display.show_message("Kein Workout gefunden!")
            return
            
        workout_start_time = time.time()
        heart_rate_data = []
        rep_count = 0
        last_rep_time = time.time()
        total_reps = 0
        total_sets = 0
        
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
                # Prüfe auf Mindestzeit zwischen Wiederholungen
                if current_time - last_rep_time > 0.5:
                    rep_count += 1
                    total_reps += 1
                    last_rep_time = current_time
                    
                    # Wenn alle Wiederholungen eines Satzes gemacht wurden
                    if rep_count >= exercise['reps']:
                        rep_count = 0
                        total_sets += 1
                        
                        # Zeige Pause-Timer
                        rest_time = exercise.get('rest_time', 60)
                        for remaining in range(rest_time, 0, -1):
                            display.show_rest_timer(remaining)
                            display.update()
                            time.sleep(1)
                        
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
            
            # Kurze Pause
            time.sleep(0.1)
            
        # Workout beendet
        workout_duration = int((time.time() - workout_start_time) / 60)  # in Minuten
        
        # Berechne durchschnittliche Herzfrequenz
        avg_heart_rate = 0
        if heart_rate_data:
            avg_heart_rate = sum(d['value'] for d in heart_rate_data) / len(heart_rate_data)
        
        # Zeige Zusammenfassung
        display.show_workout_summary(
            total_sets,
            total_reps,
            workout_duration,
            int(avg_heart_rate)
        )
        display.update()
        time.sleep(5)
        
        # Speichere und synchronisiere Fortschritt
        workout_data = workout_manager.save_progress(heart_rate_data)
        cloud_sync.sync_workout_data(workout_data)
        
        display.show_message("Workout beendet!", "Daten synchronisiert")
        display.update()
        
    except KeyboardInterrupt:
        print("\nProgramm beendet")
    finally:
        heart_sensor.close()
        cloud_sync.stop_sync_thread()

if __name__ == "__main__":
    main()

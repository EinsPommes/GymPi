from PIL import Image, ImageDraw, ImageFont
import os
from datetime import datetime

class EpaperDisplay:
    def __init__(self, width=296, height=128):  # 2.9 inch display
        self.width = width
        self.height = height
        self.image = Image.new('1', (width, height), 255)  # 255: white
        self.draw = ImageDraw.Draw(self.image)
        self.font_dir = os.path.join(os.path.dirname(__file__), '../../assets/fonts')
        self.font = ImageFont.load_default()  # Standardschriftart als Fallback
        self.small_font = ImageFont.load_default()
        
    def clear(self):
        """Löscht den Display-Inhalt"""
        self.image = Image.new('1', (self.width, self.height), 255)
        self.draw = ImageDraw.Draw(self.image)
        
    def show_workout(self, exercise, sets, reps, current_set, heart_rate):
        """Zeigt die aktuelle Übung und Herzfrequenz an"""
        self.clear()
        
        # Übungsname (groß, oben)
        self.draw.text((10, 5), exercise, font=self.font, fill=0)
        
        # Sets und Wiederholungen
        progress = f"Set {current_set}/{sets}"
        self.draw.text((10, 30), progress, font=self.font, fill=0)
        
        # Wiederholungen
        reps_text = f"Wiederholungen: {reps}"
        self.draw.text((self.width//2 + 10, 30), reps_text, font=self.font, fill=0)
        
        # Fortschrittsbalken für Sets
        progress_width = int((self.width - 20) * (current_set / sets))
        self.draw.rectangle([(10, 50), (self.width-10, 60)], outline=0)
        self.draw.rectangle([(10, 50), (10 + progress_width, 60)], fill=0)
        
        # Herzfrequenz mit Symbol
        if heart_rate:
            hr_text = f"♥ {heart_rate} BPM"
            self.draw.text((10, 70), hr_text, font=self.font, fill=0)
            
        # Zeit
        current_time = datetime.now().strftime("%H:%M")
        self.draw.text((self.width-50, 5), current_time, font=self.small_font, fill=0)
        
    def show_rest_timer(self, seconds_left):
        """Zeigt einen Ruhetimer an"""
        self.clear()
        
        # Großer Timer in der Mitte
        timer_text = f"{seconds_left}s"
        self.draw.text((self.width//2-20, self.height//2-15), 
                      timer_text, font=self.font, fill=0)
        
        # Hinweistext
        self.draw.text((10, 10), "Pause", font=self.font, fill=0)
        
    def show_workout_summary(self, total_sets, total_reps, duration_mins, avg_heart_rate):
        """Zeigt eine Zusammenfassung des Workouts"""
        self.clear()
        
        self.draw.text((10, 5), "Workout Zusammenfassung", font=self.font, fill=0)
        
        # Statistiken
        stats = [
            f"Sets: {total_sets}",
            f"Wdh: {total_reps}",
            f"Zeit: {duration_mins}min",
            f"Ø Puls: {avg_heart_rate}bpm"
        ]
        
        for i, stat in enumerate(stats):
            self.draw.text((10, 30 + i*20), stat, font=self.font, fill=0)
            
    def show_workout_history(self, history_data):
        """Zeigt die letzten Workouts an"""
        self.clear()
        
        self.draw.text((10, 5), "Letzte Workouts", font=self.font, fill=0)
        
        y_pos = 30
        for workout in history_data[:3]:  # Zeige die letzten 3 Workouts
            date = datetime.fromisoformat(workout['timestamp']).strftime("%d.%m")
            text = f"{date}: {workout['workout_name']} ({workout['completed_exercises']} Übungen)"
            self.draw.text((10, y_pos), text, font=self.small_font, fill=0)
            y_pos += 20
            
    def show_message(self, message, subtitle=None):
        """Zeigt eine Nachricht auf dem Display an"""
        self.clear()
        
        # Hauptnachricht
        text_width = self.draw.textlength(message, font=self.font)
        x = (self.width - text_width) // 2
        self.draw.text((x, self.height//3), message, font=self.font, fill=0)
        
        # Untertitel (optional)
        if subtitle:
            text_width = self.draw.textlength(subtitle, font=self.small_font)
            x = (self.width - text_width) // 2
            self.draw.text((x, self.height//2), subtitle, font=self.small_font, fill=0)
        
    def update(self):
        """
        Aktualisiert das physische Display
        In der Praxis würde hier der spezifische Code für das
        verwendete E-Paper Display implementiert
        """
        # Hier würde der tatsächliche Code zur Aktualisierung des Displays kommen
        pass

from PIL import Image, ImageDraw, ImageFont
import os
from datetime import datetime

class EpaperDisplay:
    def __init__(self, width=296, height=128):  # 2.9 inch display
        self.width = width
        self.height = height
        self.image = Image.new('1', (width, height), 255)  # 255: white
        self.draw = ImageDraw.Draw(self.image)
        
        # Lade Schriftarten
        self.font_dir = os.path.join(os.path.dirname(__file__), '../../assets/fonts')
        self.font = ImageFont.load_default()  # Standardschriftart als Fallback
        self.small_font = ImageFont.load_default()
        
        # Pfad zu Übungsbildern
        self.exercise_dir = os.path.join(os.path.dirname(__file__), '../../data/exercises')
        
    def clear(self):
        """Löscht den Display-Inhalt"""
        self.image = Image.new('1', (self.width, self.height), 255)
        self.draw = ImageDraw.Draw(self.image)
        
    def _load_exercise_image(self, exercise_name):
        """Lädt das Bild für eine bestimmte Übung"""
        # Normalisiere den Dateinamen
        filename = exercise_name.lower().replace(' ', '_') + '.bmp'
        image_path = os.path.join(self.exercise_dir, filename)
        
        try:
            if os.path.exists(image_path):
                # Lade und konvertiere das Bild
                img = Image.open(image_path)
                # Konvertiere zu 1-bit Schwarz/Weiß
                img = img.convert('1')
                return img
        except Exception as e:
            print(f"Fehler beim Laden des Übungsbildes: {e}")
        return None
        
    def show_workout(self, exercise, sets, reps, current_set, heart_rate):
        """Zeigt die aktuelle Übung und Herzfrequenz an"""
        self.clear()
        
        # Übungsname (oben)
        self.draw.text((10, 5), exercise, font=self.font, fill=0)
        
        # Lade und zeige Übungsbild
        exercise_image = self._load_exercise_image(exercise)
        if exercise_image:
            # Bild auf der linken Seite
            image_width = 128  # Fixe Breite für Übungsbilder
            image_height = 64  # Fixe Höhe für Übungsbilder
            image_x = 10
            image_y = 25
            
            # Füge das Bild ein
            self.image.paste(exercise_image, (image_x, image_y))
            
            # Verschiebe die restlichen Elemente nach rechts
            info_x = image_x + image_width + 10
        else:
            info_x = 10
            
        # Sets und Wiederholungen
        progress = f"Set {current_set}/{sets}"
        self.draw.text((info_x, 30), progress, font=self.font, fill=0)
        
        # Wiederholungen
        reps_text = f"{reps} Wdh."
        self.draw.text((info_x, 50), reps_text, font=self.font, fill=0)
        
        # Fortschrittsbalken für Sets
        bar_width = 100
        progress_width = int(bar_width * (current_set / sets))
        self.draw.rectangle([(info_x, 70), (info_x + bar_width, 80)], outline=0)
        self.draw.rectangle([(info_x, 70), (info_x + progress_width, 80)], fill=0)
        
        # Herzfrequenz mit Symbol
        if heart_rate:
            hr_text = f"♥ {heart_rate} BPM"
            self.draw.text((info_x, 90), hr_text, font=self.font, fill=0)
            
        # Zeit
        current_time = datetime.now().strftime("%H:%M")
        self.draw.text((self.width-50, 5), current_time, font=self.small_font, fill=0)
        
    def show_exercise_preview(self, exercise_name):
        """Zeigt eine Vorschau der Übung mit großem Bild"""
        self.clear()
        
        # Übungsname oben
        self.draw.text((10, 5), exercise_name, font=self.font, fill=0)
        
        # Lade und zeige Übungsbild
        exercise_image = self._load_exercise_image(exercise_name)
        if exercise_image:
            # Zentriere das Bild
            image_x = (self.width - exercise_image.width) // 2
            image_y = (self.height - exercise_image.height) // 2
            self.image.paste(exercise_image, (image_x, image_y))
        else:
            self.draw.text((10, self.height//2), "Kein Bild verfügbar", font=self.font, fill=0)
        
    def show_rest_timer(self, seconds_left):
        """Zeigt einen Ruhetimer an"""
        self.clear()
        
        # Großer Timer in der Mitte
        timer_text = f"{seconds_left}s"
        text_width = self.draw.textlength(timer_text, font=self.font)
        x = (self.width - text_width) // 2
        self.draw.text((x, self.height//2-15), timer_text, font=self.font, fill=0)
        
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

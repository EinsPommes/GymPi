from PIL import Image, ImageDraw, ImageFont
import os

class EpaperDisplay:
    def __init__(self, width=296, height=128):  # 2.9 inch display
        self.width = width
        self.height = height
        self.image = Image.new('1', (width, height), 255)  # 255: white
        self.draw = ImageDraw.Draw(self.image)
        self.font_dir = os.path.join(os.path.dirname(__file__), '../../assets/fonts')
        self.font = ImageFont.load_default()  # Standardschriftart als Fallback
        
    def clear(self):
        """Löscht den Display-Inhalt"""
        self.image = Image.new('1', (self.width, self.height), 255)
        self.draw = ImageDraw.Draw(self.image)
        
    def show_workout(self, exercise, sets, reps, current_set, heart_rate):
        """Zeigt die aktuelle Übung und Herzfrequenz an"""
        self.clear()
        
        # Übungsname
        self.draw.text((10, 10), exercise, font=self.font, fill=0)
        
        # Sets und Wiederholungen
        progress = f"Set {current_set}/{sets} - {reps} Wdh."
        self.draw.text((10, 40), progress, font=self.font, fill=0)
        
        # Fortschrittsbalken
        progress_width = int((self.width - 20) * (current_set / sets))
        self.draw.rectangle([(10, 60), (self.width-10, 70)], outline=0)
        self.draw.rectangle([(10, 60), (10 + progress_width, 70)], fill=0)
        
        # Herzfrequenz
        if heart_rate:
            hr_text = f"♥ {heart_rate} BPM"
            self.draw.text((10, 90), hr_text, font=self.font, fill=0)
            
    def show_message(self, message):
        """Zeigt eine Nachricht auf dem Display an"""
        self.clear()
        self.draw.text((10, self.height//2), message, font=self.font, fill=0)
        
    def update(self):
        """
        Aktualisiert das physische Display
        In der Praxis würde hier der spezifische Code für das
        verwendete E-Paper Display implementiert
        """
        # Hier würde der tatsächliche Code zur Aktualisierung des Displays kommen
        pass

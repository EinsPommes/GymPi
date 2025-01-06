import time
import board
import busio
import adafruit_max30102

class HeartRateSensor:
    def __init__(self):
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.sensor = adafruit_max30102.MAX30102(self.i2c)
        self.sensor.setup_sensor()
        self.sensor.set_pulse_amplitude_red(0x0A)
        self.sensor.set_pulse_amplitude_ir(0x0A)
        
    def read_heart_rate(self):
        """Liest die aktuelle Herzfrequenz"""
        try:
            red_reading = self.sensor.red
            ir_reading = self.sensor.ir
            
            if ir_reading > 50000:  # Schwellenwert für gültige Messung
                # Vereinfachte Herzfrequenzberechnung
                # In der Praxis würde hier ein komplexerer Algorithmus verwendet
                heart_rate = self._calculate_heart_rate(red_reading, ir_reading)
                return heart_rate
            return None
            
        except Exception as e:
            print(f"Fehler beim Lesen der Herzfrequenz: {e}")
            return None
            
    def _calculate_heart_rate(self, red, ir):
        """
        Berechnet die Herzfrequenz aus den Rohdaten
        Dies ist eine vereinfachte Version - in der Praxis würde man
        einen komplexeren Algorithmus verwenden
        """
        # Beispielhafte Berechnung
        if ir == 0:
            return 0
        ratio = red / ir
        # Vereinfachte Formel - muss in der Praxis kalibriert werden
        heart_rate = int(60 * ratio)
        return min(max(heart_rate, 40), 200)  # Begrenzt auf realistische Werte
        
    def close(self):
        """Schließt die Verbindung zum Sensor"""
        self.i2c.deinit()

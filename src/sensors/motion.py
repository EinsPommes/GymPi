from mpu6050 import mpu6050
import numpy as np
from time import sleep

class MotionSensor:
    def __init__(self, address=0x68):
        self.sensor = mpu6050(address)
        self.calibrate()
        self.movement_threshold = 2.0  # m/s²
        self.rep_threshold = 0.8  # Schwellenwert für Wiederholungserkennung
        
    def calibrate(self):
        """Kalibriert den Sensor durch Sammeln von Grundwerten"""
        print("Kalibriere Bewegungssensor...")
        accel_data = []
        for _ in range(100):
            data = self.sensor.get_accel_data()
            accel_data.append([data['x'], data['y'], data['z']])
            sleep(0.01)
        
        self.baseline = np.mean(accel_data, axis=0)
        print("Kalibrierung abgeschlossen")
        
    def detect_movement(self):
        """Erkennt signifikante Bewegungen"""
        data = self.sensor.get_accel_data()
        current = np.array([data['x'], data['y'], data['z']])
        diff = np.abs(current - self.baseline)
        return np.any(diff > self.movement_threshold)
        
    def detect_rep(self):
        """
        Erkennt eine einzelne Wiederholung einer Übung
        Basiert auf der Bewegungsamplitude und -muster
        """
        readings = []
        for _ in range(10):  # Sammle Daten über kurzen Zeitraum
            data = self.sensor.get_accel_data()
            readings.append([data['x'], data['y'], data['z']])
            sleep(0.05)
            
        readings = np.array(readings)
        max_amplitude = np.max(np.abs(readings - self.baseline), axis=0)
        
        # Prüfe ob die Amplitude über dem Schwellenwert liegt
        return np.any(max_amplitude > self.rep_threshold)
        
    def get_orientation(self):
        """Ermittelt die aktuelle Orientierung des Geräts"""
        data = self.sensor.get_accel_data()
        
        # Vereinfachte Orientierungserkennung
        if abs(data['z']) > abs(data['x']) and abs(data['z']) > abs(data['y']):
            return 'horizontal' if data['z'] > 0 else 'invertiert'
        elif abs(data['y']) > abs(data['x']):
            return 'vertikal' if data['y'] > 0 else 'verkehrt'
        else:
            return 'seitlich'

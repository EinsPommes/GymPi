from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
import json
from typing import List, Optional
import os
from pathlib import Path

# Datenbank Setup
DATABASE_URL = "sqlite:///./gympi.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modelle
class WorkoutData(Base):
    __tablename__ = "workout_data"
    
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    workout_name = Column(String)
    completed_exercises = Column(Integer)
    heart_rate_data = Column(JSON)
    
# Datenbank erstellen
Base.metadata.create_all(bind=engine)

# FastAPI App
app = FastAPI(title="GymPi Cloud API")

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Datenbank-Session Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/workout/sync")
async def sync_workout(data: dict, db: Session = Depends(get_db)):
    """
    Synchronisiert Workout-Daten von einem GymPi-Gerät
    """
    try:
        workout_data = WorkoutData(
            device_id=data.get('device_id', 'unknown'),
            workout_name=data['data'].get('workout_name'),
            completed_exercises=data['data'].get('completed_exercises', 0),
            heart_rate_data=json.dumps(data['data'].get('heart_rate_data', []))
        )
        
        db.add(workout_data)
        db.commit()
        return {"status": "success", "message": "Daten erfolgreich synchronisiert"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/workout/history/{device_id}")
async def get_workout_history(device_id: str, db: Session = Depends(get_db)):
    """
    Ruft den Workout-Verlauf für ein bestimmtes Gerät ab
    """
    workouts = db.query(WorkoutData).filter(
        WorkoutData.device_id == device_id
    ).order_by(WorkoutData.timestamp.desc()).all()
    
    return [{
        "id": w.id,
        "timestamp": w.timestamp,
        "workout_name": w.workout_name,
        "completed_exercises": w.completed_exercises,
        "heart_rate_data": json.loads(w.heart_rate_data)
    } for w in workouts]

@app.get("/workout/stats/{device_id}")
async def get_workout_stats(device_id: str, db: Session = Depends(get_db)):
    """
    Berechnet Trainingsstatistiken für ein Gerät
    """
    workouts = db.query(WorkoutData).filter(
        WorkoutData.device_id == device_id
    ).all()
    
    total_workouts = len(workouts)
    total_exercises = sum(w.completed_exercises for w in workouts)
    
    # Berechne durchschnittliche Herzfrequenz
    all_hr_data = []
    for w in workouts:
        hr_data = json.loads(w.heart_rate_data)
        all_hr_data.extend([d['value'] for d in hr_data if 'value' in d])
    
    avg_heart_rate = sum(all_hr_data) / len(all_hr_data) if all_hr_data else 0
    
    return {
        "total_workouts": total_workouts,
        "total_exercises": total_exercises,
        "average_heart_rate": round(avg_heart_rate, 1)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

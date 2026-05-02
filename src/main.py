from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database import SessionLocal, engine, Base
from src.models import User, Batch, Session as SessionModel, Attendance
from src.auth import create_token, get_current_user

app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return {"message": "API is running"}

@app.post("/auth/signup")
def signup(name: str, email: str, password: str, role: str, db: Session = Depends(get_db)):
    user = User(name=name, email=email, password=password, role=role)
    db.add(user)
    db.commit()
    db.refresh(user)
    token = create_token({"user_id": user.id, "role": role})
    return {"token": token}

@app.post("/auth/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user or user.password != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_token({"user_id": user.id, "role": user.role})
    return {"token": token}

@app.post("/batches")
def create_batch(name: str, user=Depends(get_current_user), db: Session = Depends(get_db)):
    if user["role"] not in ["trainer", "institution"]:
        raise HTTPException(status_code=403, detail="Not allowed")
    batch = Batch(name=name)
    db.add(batch)
    db.commit()
    db.refresh(batch)
    return batch

@app.post("/sessions")
def create_session(title: str, batch_id: int, user=Depends(get_current_user), db: Session = Depends(get_db)):
    if user["role"] != "trainer":
        raise HTTPException(status_code=403, detail="Not allowed")
    session = SessionModel(title=title, batch_id=batch_id, trainer_id=user["user_id"])
    db.add(session)
    db.commit()
    db.refresh(session)
    return session

@app.post("/attendance/mark")
def mark_attendance(session_id: int, status: str, user=Depends(get_current_user), db: Session = Depends(get_db)):
    if user["role"] != "student":
        raise HTTPException(status_code=403, detail="Not allowed")
    attendance = Attendance(session_id=session_id, student_id=user["user_id"], status=status)
    db.add(attendance)
    db.commit()
    db.refresh(attendance)
    return attendance

@app.get("/monitoring/attendance")
def monitoring(user=Depends(get_current_user)):
    if user["role"] != "monitoring_officer":
        raise HTTPException(status_code=403, detail="Not allowed")
    return {"data": "Read-only attendance"}

from sqlalchemy import Column, Integer, String, ForeignKey
from src.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    role = Column(String)

class Batch(Base):
    __tablename__ = "batches"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    institution_id = Column(Integer, nullable=True)

class Session(Base):
    __tablename__ = "sessions"
    id = Column(Integer, primary_key=True)
    batch_id = Column(Integer, ForeignKey("batches.id"))
    trainer_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)

class Attendance(Base):
    __tablename__ = "attendance"
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey("sessions.id"))
    student_id = Column(Integer, ForeignKey("users.id"))
    status = Column(String)

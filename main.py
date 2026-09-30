from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from database import engine, Base, get_db
from models import JobDB, User
from schemas import UserCreate
from auth import hash_password, verify_password, create_access_token, get_current_user

Base.metadata.create_all(bind=engine)

app = FastAPI(title="JobTrack API")


class Job(BaseModel):
    title: str = Field(min_length=2, max_length=100)
    company: str = Field(min_length=2, max_length=100)
    location: str = Field(min_length=2, max_length=100)
    salary: int = Field(gt=0)


@app.get("/")
def home():
    return {"message": "JobTrack API"}


@app.get("/jobs", dependencies=[Depends(get_current_user)])
def get_jobs(
    search: str = None,
    location: str = None,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    query = db.query(JobDB)

    if search:
        query = query.filter(
            JobDB.title.ilike(f"%{search}%") | JobDB.company.ilike(f"%{search}%")
        )
    if location:
        query = query.filter(JobDB.location.ilike(f"%{location}%"))

    return query.offset((page - 1) * limit).limit(limit).all()


@app.get("/jobs/{job_id}", dependencies=[Depends(get_current_user)])
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(JobDB).filter(JobDB.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@app.post("/jobs", dependencies=[Depends(get_current_user)])
def create_job(job: Job, db: Session = Depends(get_db)):
    new_job = JobDB(**job.model_dump())
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return new_job


@app.put("/jobs/{job_id}", dependencies=[Depends(get_current_user)])
def update_job(job_id: int, job: Job, db: Session = Depends(get_db)):
    existing = db.query(JobDB).filter(JobDB.id == job_id).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Job not found")
    for key, value in job.model_dump().items():
        setattr(existing, key, value)
    db.commit()
    db.refresh(existing)
    return existing


@app.delete("/jobs/{job_id}", dependencies=[Depends(get_current_user)])
def delete_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(JobDB).filter(JobDB.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    db.delete(job)
    db.commit()
    return {"message": "Job deleted successfully"}


@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = User(email=user.email, hashed_password=hash_password(user.password))
    db.add(new_user)
    db.commit()
    return {"message": "Registered"}


@app.post("/login")
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Wrong email or password")
    return {"access_token": create_access_token({"sub": db_user.email})}
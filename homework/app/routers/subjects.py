from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.subject import SubjectCreate, SubjectResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.subject import Subject
from app.schemas.student import StudentResponse

router = APIRouter(prefix="/subjects", tags=["subjects"])

@router.post("/", response_model=SubjectResponse, status_code=status.HTTP_201_CREATED)
def create_subject(subject: SubjectCreate, db: Session = Depends(get_db)):
    existing_subject = db.query(Subject).filter(Subject.name == subject.name).first()
    if existing_subject:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Subject already exists")

    new_subject = Subject(**subject.model_dump())
    db.add(new_subject)
    db.commit()
    db.refresh(new_subject)

    return new_subject

@router.get("/", response_model=list[SubjectResponse])
def get_all_subjects(db: Session = Depends(get_db)):
    subjects = db.query(Subject).all()
    return subjects

@router.get("/{subject_id}", response_model=SubjectResponse)
def get_subject(subject_id: int, db: Session = Depends(get_db)):
    subject = db.query(Subject).filter(Subject.id == subject_id).first()

    if not subject:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subject not found")

    return subject

@router.delete("/{subject_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_subject(subject_id: int, db: Session = Depends(get_db)):
    subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if not subject:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subject not found")

    db.delete(subject)
    db.commit()

    return None

@router.get("/{subject_id}/students", response_model=list[StudentResponse])
def get_subject_students(subject_id: int, db: Session = Depends(get_db)):
    subject = db.query(Subject).filter(Subject.id == subject_id).first()

    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")

    students = [i.student for i in subject.student_associations]
    return students
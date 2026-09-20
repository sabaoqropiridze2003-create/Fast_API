from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.student import Student, StudentSubject
from app.models.subject import Subject
from app.schemas.student import StudentCreate, StudentResponse
from app.schemas.subject import SubjectResponse

router = APIRouter(prefix="/students", tags=["students"])

@router.post("/", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    db_student = db.query(Student).filter(Student.email == student.email).first()
    if db_student:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    new_student = Student(**student.model_dump())

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student


@router.get("/", response_model=list[StudentResponse])
def get_all_students(db: Session = Depends(get_db)):
    students = db.query(Student).all()
    return students


@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()

    if not student_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

    return student

@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()

    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

    db.delete(student)
    db.commit
    return None


@router.post("/{student_id}/subjects/{subject_id}", status_code=status.HTTP_201_CREATED)
def enroll_student_in_subject(student_id: int, subject_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")

    existing_enrollment = db.query(StudentSubject).filter(
        StudentSubject.student_id == student_id,
        StudentSubject.subject_id == subject_id
    ).first()

    if existing_enrollment:
        raise HTTPException(status_code=400, detail="Student is already enrolled in this subject")

    enrollment = StudentSubject(student_id=student_id, subject_id=subject_id)
    db.add(enrollment)
    db.commit()

    return {"message": "successfully enrolled"}

@router.get("/{student_id}/subjects", response_model=list[SubjectResponse])
def get_student_subjects(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    subjects = [i.subject for i in student.subject_associations]
    return subjects

@router.delete("/{student_id}/subjects/{subject_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student_from_subject(student_id: int, subject_id, db: Session = Depends(get_db)):
    enrollment = db.query(StudentSubject).filter(
        StudentSubject.student_id == student_id,
        StudentSubject.subject_id == subject_id
    ).first()

    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment record not found")


    db.delete(enrollment)
    db.commit()

    return None




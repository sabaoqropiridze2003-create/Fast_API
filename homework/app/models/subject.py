from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class Subject(Base):
    __tablename__ = "subjects"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    duration: Mapped[int] = mapped_column(Integer)

    student_associations: Mapped[list["StudentSubject"]] = relationship(
        back_populates="subject", cascade="all, delete"
    )

    def __str__(self):
        return self.name
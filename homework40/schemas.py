from pydantic import BaseModel, Field


class MovieCreate(BaseModel):
    title: str = Field(min_length=1, max_length=150)
    genre: str = Field(min_length=1, max_length=50)
    year: int = Field(gt=1800, le=2100)
    rating: float = Field(ge=0.0, le=10.0)
    description: str | None = None


class MovieUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=150)
    genre: str | None = Field(default=None, min_length=1, max_length=50)
    year: int | None = Field(default=None, gt=1800, le=2100)
    rating: float | None = Field(default=None, ge=0.0, le=10.0)
    description: str | None = None


class MovieResponse(BaseModel):
    id: int
    title: str
    genre: str
    year: int
    rating: float
    description: str | None = None

    class Config:
        from_attributes = True

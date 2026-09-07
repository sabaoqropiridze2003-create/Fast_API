from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator


class ProductCreateRequest(BaseModel):
    name: str = Field(min_length=3, max_length=100)
    price: float = Field(gt=0)
    discount_price: float | None = None
    quantity: int = Field(ge=0)
    category: str
    sku: str = Field(min_length=5, max_length=20)
    email: EmailStr
    stock: bool = True

    @field_validator("name")
    @classmethod
    def clean_name(cls, value: str):
        return value.strip()

    @field_validator("sku")
    @classmethod
    def validate_sku(cls, value: str):
        if " " in value:
            raise ValueError("SKU must not contain spaces")
        return value.upper()

    @model_validator(mode="after")
    def check_discount_price(self):
        if self.discount_price is not None and self.discount_price >= self.price:
            raise ValueError("discount_price must be less than price")
        return self

class ProductResponse(BaseModel):
    id: int
    name: str
    price: float
    discount_price: float | None = None
    quantity: int
    category: str
    stock: bool
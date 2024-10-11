from pydantic import BaseModel, EmailStr


class UserBasic(BaseModel):
    username: str
    full_name: str
    email: EmailStr


class UserInput(UserBasic):
    password: str


class PatchUserInput(BaseModel):
    username: str | None = None
    full_name: str | None = None
    email: EmailStr | None = None


class ProductInput(BaseModel):
    product_code: int
    product_name: str
    product_category: str
    product_brand: str
    product_unit_presentation: str
    product_quantity_presentation: int
    product_price: float
    supplier_name: str


class PatchProductInput(BaseModel):
    product_code: int | None = None
    product_name: str | None = None
    product_category: str | None = None
    product_brand: str | None = None
    product_unit_presentation: str | None = None
    product_quantity_presentation: int | None = None
    product_price: float | None = None
    supplier_name: str | None = None

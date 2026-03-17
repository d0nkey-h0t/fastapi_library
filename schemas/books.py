from pydantic import BaseModel, ConfigDict, Field


class SBookAdd(BaseModel):
    title: str
    author: str
    year: int
    pages: int = Field(..., ge=10)
    is_read: bool = Field(default=False)

class SBook (SBookAdd):
    id: int

    # 2. Включаем поддержку ORM
    model_config = ConfigDict(from_attributes=True)
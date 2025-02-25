from typing import Optional

from sqlmodel import Field, SQLModel

class CustomerBase(SQLModel):
    name: str = Field(min_length=1, max_length=32, index=True)

class Customer(CustomerBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

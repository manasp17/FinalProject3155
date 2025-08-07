from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class PromoCodeBase(BaseModel):
    code: str
    discount_percent: int
    expires_at: Optional[datetime] = None
    active: Optional[bool] = True

class PromoCodeCreate(PromoCodeBase):
    pass

class PromoCodeUpdate(BaseModel):
    code: Optional[str] = None
    discount_percent: Optional[int] = None
    expires_at: Optional[datetime] = None
    active: Optional[bool] = None

class PromoCode(PromoCodeBase):
    id: int

    class Config:
        orm_mode = True

from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime
from ..dependencies.database import Base

class PromoCode(Base):
    __tablename__ = "promo_codes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    code = Column(String(50), unique=True, nullable=False)
    discount_percent = Column(Integer, nullable=False)  # e.g., 10 for 10% off
    expires_at = Column(DateTime, nullable=True)
    active = Column(Boolean, default=True, nullable=False)

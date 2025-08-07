from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..models import promo_codes as model
from ..schemas import promo_codes as schema
from datetime import datetime

def create(db: Session, request: schema.PromoCodeCreate):
    existing = db.query(model.PromoCode).filter(model.PromoCode.code == request.code).first()
    if existing:
        raise HTTPException(status_code=400, detail="Promo code already exists")
    promo = model.PromoCode(
        code=request.code,
        discount_percent=request.discount_percent,
        expires_at=request.expires_at,
        active=request.active if request.active is not None else True
    )
    db.add(promo)
    db.commit()
    db.refresh(promo)
    return promo

def read_all(db: Session):
    return db.query(model.PromoCode).all()

def read_one(db: Session, promo_id: int):
    promo = db.query(model.PromoCode).filter(model.PromoCode.id == promo_id).first()
    if not promo:
        raise HTTPException(status_code=404, detail="Promo code not found")
    return promo

def update(db: Session, promo_id: int, request: schema.PromoCodeUpdate):
    promo = db.query(model.PromoCode).filter(model.PromoCode.id == promo_id).first()
    if not promo:
        raise HTTPException(status_code=404, detail="Promo code not found")
    if request.code is not None:
        promo.code = request.code
    if request.discount_percent is not None:
        promo.discount_percent = request.discount_percent
    if request.expires_at is not None:
        promo.expires_at = request.expires_at
    if request.active is not None:
        promo.active = request.active
    db.commit()
    db.refresh(promo)
    return promo

def delete(db: Session, promo_id: int):
    promo = db.query(model.PromoCode).filter(model.PromoCode.id == promo_id).first()
    if not promo:
        raise HTTPException(status_code=404, detail="Promo code not found")
    db.delete(promo)
    db.commit()
    return {"detail": "Promo code deleted"}

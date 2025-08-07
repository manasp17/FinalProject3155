from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..controllers import promo_codes as controller
from ..schemas import promo_codes as schema
from ..dependencies.database import get_db

router = APIRouter(
    prefix="/promocodes",
    tags=["Promo Codes"]
)

@router.post("/", response_model=schema.PromoCode)
def create_promo(request: schema.PromoCodeCreate, db: Session = Depends(get_db)):
    return controller.create(db, request)

@router.get("/", response_model=list[schema.PromoCode])
def get_all_promos(db: Session = Depends(get_db)):
    return controller.read_all(db)

@router.get("/{promo_id}", response_model=schema.PromoCode)
def get_promo(promo_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, promo_id)

@router.put("/{promo_id}", response_model=schema.PromoCode)
def update_promo(promo_id: int, request: schema.PromoCodeUpdate, db: Session = Depends(get_db)):
    return controller.update(db, promo_id, request)

@router.delete("/{promo_id}")
def delete_promo(promo_id: int, db: Session = Depends(get_db)):
    return controller.delete(db, promo_id)

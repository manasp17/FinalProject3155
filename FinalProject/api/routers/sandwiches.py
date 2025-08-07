from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..models.sandwiches import Sandwich as SandwichModel
from ..schemas.sandwiches import SandwichCreate, SandwichUpdate, Sandwich
from ..dependencies.database import get_db

router = APIRouter(
    prefix="/sandwiches",
    tags=["Sandwiches"]
)


# CREATE
@router.post("/", response_model=Sandwich)
def create_sandwich(sandwich: SandwichCreate, db: Session = Depends(get_db)):
    db_sandwich = SandwichModel(**sandwich.dict())
    db.add(db_sandwich)
    db.commit()
    db.refresh(db_sandwich)
    return db_sandwich


# READ ALL
@router.get("/", response_model=List[Sandwich])
def read_sandwiches(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(SandwichModel).offset(skip).limit(limit).all()


# READ ONE
@router.get("/{sandwich_id}", response_model=Sandwich)
def read_sandwich(sandwich_id: int, db: Session = Depends(get_db)):
    sandwich = db.query(SandwichModel).filter(SandwichModel.id == sandwich_id).first()
    if sandwich is None:
        raise HTTPException(status_code=404, detail="Sandwich not found")
    return sandwich


# UPDATE
@router.put("/{sandwich_id}", response_model=Sandwich)
def update_sandwich(sandwich_id: int, sandwich_update: SandwichUpdate, db: Session = Depends(get_db)):
    sandwich = db.query(SandwichModel).filter(SandwichModel.id == sandwich_id).first()
    if sandwich is None:
        raise HTTPException(status_code=404, detail="Sandwich not found")

    for key, value in sandwich_update.dict(exclude_unset=True).items():
        setattr(sandwich, key, value)

    db.commit()
    db.refresh(sandwich)
    return sandwich


# DELETE
@router.delete("/{sandwich_id}")
def delete_sandwich(sandwich_id: int, db: Session = Depends(get_db)):
    sandwich = db.query(SandwichModel).filter(SandwichModel.id == sandwich_id).first()
    if sandwich is None:
        raise HTTPException(status_code=404, detail="Sandwich not found")
    db.delete(sandwich)
    db.commit()
    return {"message": "Sandwich deleted"}

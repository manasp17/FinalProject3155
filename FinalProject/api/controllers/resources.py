from sqlalchemy.orm import Session
from ..models import resources as models
from ..schemas import resources as schemas

def create(db: Session, request: schemas.ResourceCreate):
    new_resource = models.Resource(**request.dict())
    db.add(new_resource)
    db.commit()
    db.refresh(new_resource)
    return new_resource

def read_all(db: Session):
    return db.query(models.Resource).all()

def read_one(db: Session, item_id: int):
    return db.query(models.Resource).filter(models.Resource.id == item_id).first()

def update(db: Session, item_id: int, request: schemas.ResourceUpdate):
    resource = db.query(models.Resource).filter(models.Resource.id == item_id).first()
    if not resource:
        return None
    for key, value in request.dict(exclude_unset=True).items():
        setattr(resource, key, value)
    db.commit()
    db.refresh(resource)
    return resource

def delete(db: Session, item_id: int):
    resource = db.query(models.Resource).filter(models.Resource.id == item_id).first()
    if not resource:
        return None
    db.delete(resource)
    db.commit()
    return True

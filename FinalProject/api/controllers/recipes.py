from sqlalchemy.orm import Session
from ..models import recipes as models
from ..schemas import recipes as schemas

def create(db: Session, request: schemas.RecipeCreate):
    new_recipe = models.Recipe(**request.dict())
    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)
    return new_recipe

def read_all(db: Session):
    return db.query(models.Recipe).all()

def read_one(db: Session, item_id: int):
    return db.query(models.Recipe).filter(models.Recipe.id == item_id).first()

def update(db: Session, item_id: int, request: schemas.RecipeUpdate):
    recipe = db.query(models.Recipe).filter(models.Recipe.id == item_id).first()
    if not recipe:
        return None
    for key, value in request.dict(exclude_unset=True).items():
        setattr(recipe, key, value)
    db.commit()
    db.refresh(recipe)
    return recipe

def delete(db: Session, item_id: int):
    recipe = db.query(models.Recipe).filter(models.Recipe.id == item_id).first()
    if not recipe:
        return None
    db.delete(recipe)
    db.commit()
    return True

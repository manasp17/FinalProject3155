from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from ..controllers import recipes as controller
from ..schemas import recipes as schema
from ..dependencies.database import get_db

router = APIRouter(
    prefix="/recipes",
    tags=["Recipes"]
)

@router.post("/", response_model=schema.Recipe, status_code=status.HTTP_201_CREATED)
def create_recipe(request: schema.RecipeCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)

@router.get("/", response_model=list[schema.Recipe])
def get_all_recipes(db: Session = Depends(get_db)):
    return controller.read_all(db)

@router.get("/{recipe_id}", response_model=schema.Recipe)
def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = controller.read_one(db, item_id=recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe

@router.put("/{recipe_id}", response_model=schema.Recipe)
def update_recipe(recipe_id: int, request: schema.RecipeUpdate, db: Session = Depends(get_db)):
    updated = controller.update(db=db, item_id=recipe_id, request=request)
    if not updated:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return updated

@router.delete("/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recipe(recipe_id: int, db: Session = Depends(get_db)):
    deleted = controller.delete(db=db, item_id=recipe_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

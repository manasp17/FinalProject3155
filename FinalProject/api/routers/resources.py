from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from ..controllers import resources as controller
from ..schemas import resources as schema
from ..dependencies.database import get_db

router = APIRouter(
    prefix="/resources",
    tags=["Resources"]
)

@router.post("/", response_model=schema.Resource, status_code=status.HTTP_201_CREATED)
def create_resource(request: schema.ResourceCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)

@router.get("/", response_model=list[schema.Resource])
def get_all_resources(db: Session = Depends(get_db)):
    return controller.read_all(db)

@router.get("/{resource_id}", response_model=schema.Resource)
def get_resource(resource_id: int, db: Session = Depends(get_db)):
    resource = controller.read_one(db, item_id=resource_id)
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    return resource

@router.put("/{resource_id}", response_model=schema.Resource)
def update_resource(resource_id: int, request: schema.ResourceUpdate, db: Session = Depends(get_db)):
    updated = controller.update(db=db, item_id=resource_id, request=request)
    if not updated:
        raise HTTPException(status_code=404, detail="Resource not found")
    return updated

@router.delete("/{resource_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_resource(resource_id: int, db: Session = Depends(get_db)):
    deleted = controller.delete(db=db, item_id=resource_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Resource not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

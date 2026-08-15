from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.master import Color, Material, Size
from app.models.user import User
from app.schemas.schemas import (
    ColorCreate,
    ColorOut,
    MaterialCreate,
    MaterialOut,
    MaterialUpdate,
    SizeCreate,
    SizeOut,
)

router = APIRouter(tags=["Master Data"])

material_router = APIRouter(prefix="/materials", tags=["Materials"])
color_router = APIRouter(prefix="/colors", tags=["Colors"])
size_router = APIRouter(prefix="/sizes", tags=["Sizes"])


# ---------- Materials ----------
@material_router.get("", response_model=list[MaterialOut])
def list_materials(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(Material).all()


@material_router.post("", response_model=MaterialOut, status_code=201)
def create_material(payload: MaterialCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    existing = db.query(Material).filter(Material.code == payload.code).first()
    if existing:
        raise HTTPException(status_code=400, detail="Material code already exists")
    material = Material(**payload.model_dump())
    db.add(material)
    db.commit()
    db.refresh(material)
    return material


@material_router.get("/{material_id}", response_model=MaterialOut)
def get_material(material_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    material = db.query(Material).filter(Material.id == material_id).first()
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")
    return material


@material_router.put("/{material_id}", response_model=MaterialOut)
def update_material(
    material_id: int,
    payload: MaterialUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    material = db.query(Material).filter(Material.id == material_id).first()
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(material, key, value)
    db.commit()
    db.refresh(material)
    return material


@material_router.delete("/{material_id}", status_code=204)
def delete_material(material_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    material = db.query(Material).filter(Material.id == material_id).first()
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")
    db.delete(material)
    db.commit()


# ---------- Colors ----------
@color_router.get("", response_model=list[ColorOut])
def list_colors(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(Color).all()


@color_router.post("", response_model=ColorOut, status_code=201)
def create_color(payload: ColorCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    existing = db.query(Color).filter(Color.name == payload.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Color already exists")
    color = Color(**payload.model_dump())
    db.add(color)
    db.commit()
    db.refresh(color)
    return color


@color_router.delete("/{color_id}", status_code=204)
def delete_color(color_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    color = db.query(Color).filter(Color.id == color_id).first()
    if not color:
        raise HTTPException(status_code=404, detail="Color not found")
    db.delete(color)
    db.commit()


# ---------- Sizes ----------
@size_router.get("", response_model=list[SizeOut])
def list_sizes(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(Size).all()


@size_router.post("", response_model=SizeOut, status_code=201)
def create_size(payload: SizeCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    existing = db.query(Size).filter(Size.name == payload.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Size already exists")
    size = Size(**payload.model_dump())
    db.add(size)
    db.commit()
    db.refresh(size)
    return size


@size_router.delete("/{size_id}", status_code=204)
def delete_size(size_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    size = db.query(Size).filter(Size.id == size_id).first()
    if not size:
        raise HTTPException(status_code=404, detail="Size not found")
    db.delete(size)
    db.commit()
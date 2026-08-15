from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.bom import GarmentBom, GarmentBomItem, BomStatus
from app.models.master import Material, Style
from app.models.user import User
from app.schemas.schemas import (
    GarmentBomCreate,
    GarmentBomItemOut,
    GarmentBomOut,
)

router = APIRouter(prefix="/boms", tags=["Garment BOM"])


def _to_bom_out(db: Session, bom: GarmentBom) -> GarmentBomOut:
    out = GarmentBomOut.model_validate(bom)
    style = db.query(Style).filter(Style.id == bom.style_id).first()
    out.style_no = style.style_no if style else None

    items = []
    for item in bom.items:
        item_out = GarmentBomItemOut.model_validate(item)
        material = db.query(Material).filter(Material.id == item.material_id).first()
        if material:
            item_out.material_code = material.code
            item_out.material_name = material.name
        items.append(item_out)
    out.items = items
    return out


@router.get("", response_model=list[GarmentBomOut])
def list_boms(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    boms = db.query(GarmentBom).all()
    return [_to_bom_out(db, b) for b in boms]


@router.post("", response_model=GarmentBomOut, status_code=201)
def create_bom(payload: GarmentBomCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    style = db.query(Style).filter(Style.id == payload.style_id).first()
    if not style:
        raise HTTPException(status_code=404, detail="Style not found")

    existing = (
        db.query(GarmentBom)
        .filter(GarmentBom.style_id == payload.style_id, GarmentBom.version == payload.version)
        .first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="BOM version already exists for this style")

    bom = GarmentBom(
        style_id=payload.style_id,
        bom_name=payload.bom_name,
        version=payload.version,
        notes=payload.notes,
    )
    db.add(bom)
    db.flush()

    for item_data in payload.items:
        material = db.query(Material).filter(Material.id == item_data.material_id).first()
        if not material:
            raise HTTPException(status_code=400, detail=f"Material {item_data.material_id} not found")
        bom_item = GarmentBomItem(
            bom_id=bom.id,
            material_id=item_data.material_id,
            quantity_per_garment=item_data.quantity_per_garment,
            uom=item_data.uom or material.uom,
            wastage_percent=item_data.wastage_percent,
            is_mandatory=item_data.is_mandatory,
            color_id=item_data.color_id,
            size_id=item_data.size_id,
            notes=item_data.notes,
        )
        db.add(bom_item)

    db.commit()
    db.refresh(bom)
    return _to_bom_out(db, bom)


@router.get("/{bom_id}", response_model=GarmentBomOut)
def get_bom(bom_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    bom = db.query(GarmentBom).filter(GarmentBom.id == bom_id).first()
    if not bom:
        raise HTTPException(status_code=404, detail="BOM not found")
    return _to_bom_out(db, bom)


@router.post("/{bom_id}/activate", response_model=GarmentBomOut)
def activate_bom(bom_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    bom = db.query(GarmentBom).filter(GarmentBom.id == bom_id).first()
    if not bom:
        raise HTTPException(status_code=404, detail="BOM not found")

    # Deactivate all other BOMs for the same style
    db.query(GarmentBom).filter(
        GarmentBom.style_id == bom.style_id,
        GarmentBom.id != bom.id,
    ).update({"is_active": False})

    bom.is_active = True
    bom.status = BomStatus.ACTIVE
    db.commit()
    db.refresh(bom)
    return _to_bom_out(db, bom)


@router.delete("/{bom_id}", status_code=204)
def delete_bom(bom_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    bom = db.query(GarmentBom).filter(GarmentBom.id == bom_id).first()
    if not bom:
        raise HTTPException(status_code=404, detail="BOM not found")
    db.delete(bom)
    db.commit()
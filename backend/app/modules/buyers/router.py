from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.master import Buyer
from app.models.user import User
from app.schemas.schemas import BuyerCreate, BuyerOut, BuyerUpdate

router = APIRouter(prefix="/buyers", tags=["Buyers"])


@router.get("", response_model=list[BuyerOut])
def list_buyers(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(Buyer).all()


@router.post("", response_model=BuyerOut, status_code=201)
def create_buyer(payload: BuyerCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    existing = db.query(Buyer).filter(Buyer.code == payload.code).first()
    if existing:
        raise HTTPException(status_code=400, detail="Buyer code already exists")
    buyer = Buyer(**payload.model_dump())
    db.add(buyer)
    db.commit()
    db.refresh(buyer)
    return buyer


@router.get("/{buyer_id}", response_model=BuyerOut)
def get_buyer(buyer_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    buyer = db.query(Buyer).filter(Buyer.id == buyer_id).first()
    if not buyer:
        raise HTTPException(status_code=404, detail="Buyer not found")
    return buyer


@router.put("/{buyer_id}", response_model=BuyerOut)
def update_buyer(
    buyer_id: int,
    payload: BuyerUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    buyer = db.query(Buyer).filter(Buyer.id == buyer_id).first()
    if not buyer:
        raise HTTPException(status_code=404, detail="Buyer not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(buyer, key, value)
    db.commit()
    db.refresh(buyer)
    return buyer


@router.delete("/{buyer_id}", status_code=204)
def delete_buyer(buyer_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    buyer = db.query(Buyer).filter(Buyer.id == buyer_id).first()
    if not buyer:
        raise HTTPException(status_code=404, detail="Buyer not found")
    db.delete(buyer)
    db.commit()
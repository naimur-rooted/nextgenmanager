from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.quality import Defect, QualityInspection, QCStatus
from app.models.user import User
from app.schemas.schemas import DefectOut, QualityInspectionCreate, QualityInspectionOut

router = APIRouter(prefix="/quality", tags=["Quality Control"])


def _to_out(db: Session, qc: QualityInspection) -> QualityInspectionOut:
    out = QualityInspectionOut.model_validate(qc)
    defects = []
    for d in qc.defects:
        defects.append(DefectOut.model_validate(d))
    out.defects = defects
    return out


@router.get("/inspections", response_model=list[QualityInspectionOut])
def list_inspections(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return [_to_out(db, q) for q in db.query(QualityInspection).all()]


@router.post("/inspections", response_model=QualityInspectionOut, status_code=201)
def create_inspection(
    payload: QualityInspectionCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    existing = db.query(QualityInspection).filter(
        QualityInspection.inspection_number == payload.inspection_number
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Inspection number already exists")

    qc = QualityInspection(
        inspection_number=payload.inspection_number,
        qc_type=payload.qc_type,
        work_order_id=payload.work_order_id,
        order_id=payload.order_id,
        style_variant_id=payload.style_variant_id,
        material_id=payload.material_id,
        inspected_qty=payload.inspected_qty,
        passed_qty=payload.passed_qty,
        rejected_qty=payload.rejected_qty,
        inspector=payload.inspector,
        inspection_date=payload.inspection_date,
        remarks=payload.remarks,
    )
    # Auto-set status
    if payload.rejected_qty > 0 and payload.passed_qty > 0:
        qc.status = QCStatus.REWORK
    elif payload.rejected_qty > 0:
        qc.status = QCStatus.REJECTED
    else:
        qc.status = QCStatus.PASSED

    db.add(qc)
    db.flush()

    for defect_data in payload.defects:
        db.add(
            Defect(
                inspection_id=qc.id,
                defect_type=defect_data.defect_type,
                quantity=defect_data.quantity,
                remarks=defect_data.remarks,
            )
        )

    db.commit()
    db.refresh(qc)
    return _to_out(db, qc)


@router.get("/inspections/{qc_id}", response_model=QualityInspectionOut)
def get_inspection(qc_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    qc = db.query(QualityInspection).filter(QualityInspection.id == qc_id).first()
    if not qc:
        raise HTTPException(status_code=404, detail="Inspection not found")
    return _to_out(db, qc)


DEFECT_TYPES = [
    "Fabric Defect",
    "Stitching Defect",
    "Measurement Defect",
    "Color Issue",
    "Printing Issue",
    "Button Issue",
    "Finishing Issue",
    "Packing Issue",
]


@router.get("/defects/types")
def list_defect_types(_: User = Depends(get_current_user)):
    return DEFECT_TYPES
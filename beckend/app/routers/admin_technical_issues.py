from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas
from app.crud.technical_issues import create_technical_issue, delete_technical_issue, get_all_technical_issues, update_technical_issue
from app.db import get_db
from app.dependencies import get_current_admin

router = APIRouter(prefix="/admin/technical-issues", tags=["Admin Technical Issues"])


@router.get("/", response_model=list[schemas.TechnicalIssueRead])
def list_technical_issues(db: Session = Depends(get_db), current_admin=Depends(get_current_admin)):
    return get_all_technical_issues(db)


@router.post("/", response_model=schemas.TechnicalIssueRead, status_code=status.HTTP_201_CREATED)
def create_technical_issue_route(
    issue_data: schemas.TechnicalIssueCreate,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    return create_technical_issue(db, issue_data)


@router.put("/{issue_id}", response_model=schemas.TechnicalIssueRead)
def update_technical_issue_route(
    issue_id: int,
    issue_data: schemas.TechnicalIssueUpdate,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    issue = update_technical_issue(db, issue_id, issue_data)
    if not issue:
        raise HTTPException(status_code=404, detail="Technical issue not found")
    return issue


@router.delete("/{issue_id}")
def delete_technical_issue_route(issue_id: int, db: Session = Depends(get_db), current_admin=Depends(get_current_admin)):
    issue = delete_technical_issue(db, issue_id)
    if not issue:
        raise HTTPException(status_code=404, detail="Technical issue not found")
    return {"message": "Technical issue deleted successfully"}

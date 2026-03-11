from sqlalchemy import or_
from sqlalchemy.orm import Session

from app import models, schemas


def create_technical_issue(db: Session, issue_data: schemas.TechnicalIssueCreate):
    issue = models.TechnicalIssue(**issue_data.model_dump())
    db.add(issue)
    db.commit()
    db.refresh(issue)
    return issue


def get_technical_issue_by_id(db: Session, issue_id: int):
    return db.query(models.TechnicalIssue).filter(models.TechnicalIssue.id == issue_id).first()


def search_technical_issues(db: Session, query: str):
    like_query = f"%{query}%"
    return (
        db.query(models.TechnicalIssue)
        .filter(
            or_(
                models.TechnicalIssue.problem.ilike(like_query),
                models.TechnicalIssue.category.ilike(like_query),
                models.TechnicalIssue.solution.ilike(like_query),
                models.TechnicalIssue.notes.ilike(like_query),
            )
        )
        .order_by(models.TechnicalIssue.problem.asc())
        .all()
    )


def get_all_technical_issues(db: Session):
    return db.query(models.TechnicalIssue).order_by(models.TechnicalIssue.problem.asc()).all()


def update_technical_issue(db: Session, issue_id: int, issue_data: schemas.TechnicalIssueUpdate):
    issue = get_technical_issue_by_id(db, issue_id)
    if not issue:
        return None
    for field, value in issue_data.model_dump(exclude_unset=True).items():
        setattr(issue, field, value)
    db.commit()
    db.refresh(issue)
    return issue


def delete_technical_issue(db: Session, issue_id: int):
    issue = get_technical_issue_by_id(db, issue_id)
    if not issue:
        return None
    db.delete(issue)
    db.commit()
    return issue

import logging

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import schemas
from app.ai_service import AITask, AIServiceError, route_ai_task
from app.db import get_db
from app.retrieval_service import get_context_by_category

router = APIRouter(tags=["Ask"])

logger = logging.getLogger(__name__)


def build_db_fallback_answer(category: str, context: str) -> str:
    if category == "exam":
        return f"I found exam information in the database:\n{context}"

    if category == "location":
        return f"I found location information in the database:\n{context}"

    if category == "office_hours":
        return f"I found office hours information in the database:\n{context}"

    if category == "general_info":
        return f"I found general campus information in the database:\n{context}"

    if category == "technical_problem":
        return f"I found technical support information in the database:\n{context}"

    return f"I found the following information in the database:\n{context}"


@router.post("/ask", response_model=schemas.AskResponse)
def ask_question(payload: schemas.AskRequest, db: Session = Depends(get_db)):
    logger.info("Received /ask request | question=%s", payload.question)

    try:
        analysis_result = route_ai_task(
            AITask.ANALYZE_QUESTION,
            question=payload.question,
        )
        category = analysis_result.get("category", "unknown")
        entities = analysis_result.get("entities", {})
        logger.info(
            "Question analysis completed | category=%s | entities=%s",
            category,
            entities,
        )
    except AIServiceError:
        logger.exception("AI service unavailable during question analysis")
        return schemas.AskResponse(
            category=None,
            answer="The AI service is currently unavailable. Please try again later.",
            source=None,
        )

    if category == "unknown":
        logger.warning("Question classification returned unknown")
        return schemas.AskResponse(
            category="unknown",
            answer="I could not understand the type of question. Please rephrase your question.",
            source=None,
        )

    context = get_context_by_category(
        db=db,
        category=category,
        question=payload.question,
        entities=entities,
    )

    if not context:
        logger.warning("No database context found | category=%s", category)
        return schemas.AskResponse(
            category=category,
            answer="The requested information is not available in the campus database.",
            source="database",
        )

    logger.info("Database context retrieved successfully | category=%s", category)

    try:
        answer = route_ai_task(
            AITask.GENERATE_ANSWER,
            question=payload.question,
            category=category,
            context=context,
        )
        logger.info("Answer generated successfully with AI | category=%s", category)
        return schemas.AskResponse(
            category=category,
            answer=answer,
            source="database + ai",
        )

    except AIServiceError:
        logger.exception("AI service unavailable during answer generation")
        return schemas.AskResponse(
            category=category,
            answer=build_db_fallback_answer(category, context),
            source="database",
        )
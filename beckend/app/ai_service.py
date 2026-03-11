import json
import os
from enum import Enum

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

ALLOWED_CATEGORIES = {
    "exam",
    "location",
    "office_hours",
    "general_info",
    "technical_problem",
    "unknown",
}


class AIServiceError(Exception):
    pass


class AITask(str, Enum):
    ANALYZE_QUESTION = "analyze_question"
    GENERATE_ANSWER = "generate_answer"


def route_ai_task(task: AITask, **kwargs):
    if task == AITask.ANALYZE_QUESTION:
        return analyze_question(kwargs["question"])

    if task == AITask.GENERATE_ANSWER:
        return generate_answer(
            question=kwargs["question"],
            category=kwargs["category"],
            context=kwargs["context"],
        )

    raise ValueError(f"Unsupported AI task: {task}")


def analyze_question(question: str) -> dict:
    """
    Returns:
    {
        "category": "exam",
        "entities": {
            "course_name": "...",
            "building_name": None,
            "room_number": None,
            "staff_name": None,
            "service_name": None,
            "technical_issue": None
        }
    }
    """
    system_prompt = """
You are an analysis assistant for a Smart Campus Assistant.

Your task is to analyze the user's question and return:
1. The most appropriate category
2. The extracted entities

Allowed categories:
- exam: questions about exam date, exam time, exam room, exam schedule
- location: questions about where a building or room is located
- office_hours: questions about office hours, staff availability, consultation hours
- general_info: questions about campus services, library, cafeteria, parking, wifi, student office, general campus information
- technical_problem: questions about technical issues such as wifi connection, portal login, Moodle access, password reset, system access problems
- unknown: if the question does not clearly fit any category

Possible entities:
- course_name
- building_name
- room_number
- staff_name
- service_name
- technical_issue

Return ONLY valid JSON in this exact format:
{
  "category": "exam",
  "entities": {
    "course_name": "Data Structures",
    "building_name": null,
    "room_number": null,
    "staff_name": null,
    "service_name": null,
    "technical_issue": null
  }
}

Rules:
- Use only one category
- If an entity does not exist, return null
- Do not add extra fields
- Do not add explanations
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            temperature=0,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question},
            ],
        )

        content = response.choices[0].message.content.strip()

        try:
            data = json.loads(content)

            category = data.get("category", "unknown")
            if category not in ALLOWED_CATEGORIES:
                category = "unknown"

            entities = data.get("entities", {})
            if not isinstance(entities, dict):
                entities = {}

            normalized_entities = {
                "course_name": entities.get("course_name"),
                "building_name": entities.get("building_name"),
                "room_number": entities.get("room_number"),
                "staff_name": entities.get("staff_name"),
                "service_name": entities.get("service_name"),
                "technical_issue": entities.get("technical_issue"),
            }

            return {
                "category": category,
                "entities": normalized_entities,
            }

        except Exception:
            return {
                "category": "unknown",
                "entities": {},
            }

    except Exception as exc:
        raise AIServiceError("Failed to analyze question") from exc


def generate_answer(question: str, category: str, context: str) -> str:
    system_prompt = """
You are a Smart Campus Assistant.
Answer only using the provided database context.
Do not invent facts.
Keep the answer short, clear, and natural.
If the context is insufficient, say that the requested information is not available in the campus database.
"""

    user_prompt = f"""
Question category: {category}

User question:
{question}

Database context:
{context}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            temperature=0.2,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )

        return response.choices[0].message.content.strip()

    except Exception as exc:
        raise AIServiceError("Failed to generate answer") from exc
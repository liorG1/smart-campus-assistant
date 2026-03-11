import json
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def extract_entities(question: str) -> dict:
    system_prompt = """
Extract relevant entities from the campus question.

Possible entities:
- course_name
- building_name
- room_number
- staff_name
- service_name
- technical_issue

Return JSON ONLY in this format:
{
  "course_name": null,
  "building_name": null,
  "room_number": null,
  "staff_name": null,
  "service_name": null,
  "technical_issue": null
}

Use null when a field is not present.
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        temperature=0,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question},
        ],
    )

    content = (response.choices[0].message.content or "").strip()

    try:
        data = json.loads(content)
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}

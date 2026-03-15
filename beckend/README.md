# Smart Campus Assistant Backend

FastAPI backend for a Smart Campus Assistant hackathon project.

## Features
- `POST /ask` endpoint
- OpenAI-based question classification
- OpenAI-based entity extraction
- Retrieval from SQLite database
- AI answer generation using database context only
- Admin authentication with JWT
- Admin CRUD routes for campus data
- Seed script for demo data

## Supported categories
- `exam`
- `location`
- `office_hours`
- `general_info`
- `technical_problem`
- `unknown`

## Project structure
```text
app/
  main.py
  db.py
  models.py
  schemas.py
  auth.py
  dependencies.py
  ai_service.py
  entity_extraction_service.py
  retrieval_service.py
  crud/
  routers/
seed_data.py
requirements.txt
.env.example
```

## Setup
```bash
python -m venv .venv
source .venv/bin/activate   # macOS / Linux
# .venv\Scripts\activate    # Windows
pip install -r requirements.txt
cp .env.example .env
```

Create a .env file in the backend folder based on .env.example
and fill in your OpenAI API key.

## Run the API
```bash
uvicorn app.main:app --reload
```

## Seed the database
```bash
python seed_data.py
```

## Useful endpoints
- `GET /`
- `POST /ask`
- `POST /admin/register`
- `POST /admin/login`
- `GET /admin/me`
- `POST /admin/buildings/`
- `POST /admin/rooms/`
- `POST /admin/courses/`
- `POST /admin/exams/`
- `POST /admin/office-hours/`
- `POST /admin/campus-info/`
- `POST /admin/technical-issues/`

## Example ask request
```json
{
  "question": "When is the Data Structures exam?"
}
```

## Notes
This package includes the backend only. Frontend and deployment can be added next.

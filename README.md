# Smart Campus Assistant

Smart Campus Assistant is an AI-powered system that helps students quickly find campus-related information such as exam schedules, office hours, campus locations, and general academic support.

The system integrates a FastAPI backend, a React frontend, and OpenAI-based AI capabilities.

---

# Features

- AI-powered question answering
- Exam schedule lookup
- Office hours lookup
- Campus information services
- Technical problem assistance
- Admin dashboard with CRUD operations
- Database integration
- Docker-based deployment

---

# Technologies Used

Backend:
- FastAPI
- Python
- SQLAlchemy
- OpenAI API
- Pydantic

Frontend:
- React
- Vite
- React Router

Deployment & DevOps:
- Docker
- Docker Compose
- Pytest
- GitHub Actions (CI)

---

# Project Structure
akaton_project
│
├── backend
│ ├── app
│ ├── tests
│ ├── requirements.txt
│ └── Dockerfile
│
├── frontend
│ ├── src
│ ├── package.json
│ └── Dockerfile
│
├── docker-compose.yml
├── experiments.md
└── README.md


---

# Running the Project Locally

## Backend
cd backend
uvicorn app.main:app --reload


Backend will run on:
http://localhost:8000


Swagger documentation:
http://localhost:8000/docs


---

## Frontend
cd frontend
npm install
npm run dev


Frontend runs on:
http://localhost:5173


---

# Running Tests
cd backend
pytest



This test verifies that the `/ask` endpoint responds correctly.

---

# Running with Docker

Build and start the system:

docker compose up --build


Services:

Backend:
http://localhost:8000/docs


Frontend:
http://localhost:5173


---

# AI Integration

The AI component uses OpenAI GPT models to:

1. Analyze student questions
2. Classify the question category
3. Extract relevant entities
4. Generate responses based on database context

The AI logic is implemented in:

backend/app/ai_service.py


---

# Admin Dashboard

The admin interface allows administrators to manage:

- Exams
- Courses
- Office hours
- Campus information

Supported operations:

- Create
- Read
- Update
- Delete

---

# AI Experiments

AI experiments and evaluation are documented in:

experiments.md


The document includes:

- 10 test questions
- prompt engineering comparison
- failure case analysis

---

## Documentation

Project documentation is located in the docs folder:

- SRS – System Requirements Specification
- Experiments – AI evaluation and testing
- Project Management – backlog, sprint, retrospective

---

# Author

Lior Getahun
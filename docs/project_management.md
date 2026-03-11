Project Backlog – Smart Campus Assistant

1. Build FastAPI backend and create the /ask endpoint
2. Integrate OpenAI API for question analysis
3. Implement question categorization (exam, location, office hours, general info, technical problems)
4. Connect backend to database for retrieving campus information
5. Implement AI answer generation based on database context
6. Build React frontend for student chat interface
7. Implement admin authentication (login/register)
8. Build admin dashboard with CRUD operations
9. Implement exam schedule management
10. Implement office hours management
11. Implement campus information management
12. Add fallback response when AI cannot find an answer
13. Write automated tests using pytest
14. Dockerize backend and frontend
15. Implement CI pipeline using GitHub Actions


User Stories:

story 1 :

As a student, I want to ask questions about exam schedules so that I can quickly know when and where my exam takes place.

story 2:

As a student, I want to ask questions about office hours so that I know when I can meet lecturers or staff members.


story 3:

As a student, I want to ask questions about campus services so that I can easily find important information such as library hours or technical support.


story 4:

As an administrator, I want to manage campus data (exams, courses, office hours, campus info) so that the AI system can provide accurate answers to students.


Definition of Done

A feature is considered complete when:

• The backend endpoint is implemented and functional.
• The frontend interface successfully communicates with the backend.
• The feature has been manually tested.
• The code runs without errors.
• Automated tests pass successfully.
• The feature is included in the Docker build.
• The CI pipeline runs successfully on GitHub.


Sprint Plan (3 days)

Day 1:
Implemented the FastAPI backend and created the /ask endpoint.
Integrated OpenAI API for question analysis and categorization.

Day 2:
Developed the React frontend and chat interface.
Connected the frontend to the backend API.

Day 3:
Implemented admin dashboard and CRUD operations.
Added Docker support and CI pipeline.



Work Log

Day 1:
Implemented the backend structure using FastAPI and integrated OpenAI API for analyzing student questions.

Day 2:
Built the React frontend chat interface and connected it to the backend API.

Day 3:
Added admin dashboard functionality, implemented CRUD operations for campus data, and integrated Docker deployment and CI pipeline.


Project Retrospective

The project successfully implemented an AI-powered campus assistant that allows students to ask natural language questions and receive accurate answers based on campus data.

One challenge during development was integrating the AI model with structured database information. It required prompt engineering and careful design of the context passed to the model.

Another difficulty was setting up Docker and CI pipelines, especially configuring environment variables for the OpenAI API.

Overall, the system works well and demonstrates a full-stack architecture combining AI, backend services, frontend UI, and DevOps tools.

If the project were extended, I would improve the AI answer accuracy further and add more automated tests for edge cases.
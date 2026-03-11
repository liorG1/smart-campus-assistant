# AI Experiments – Smart Campus Assistant

## Overview

This document presents experiments conducted to evaluate the AI component of the Smart Campus Assistant system.

The experiments aim to verify the assistant’s ability to:

- Answer campus-related questions using database information
- Provide general explanations when appropriate
- Correctly identify when a question is outside the system scope
- Avoid generating incorrect information

The AI component is implemented using **OpenAI GPT-4.1-mini** and integrated into a **FastAPI backend** through the `ai_service.py` module.

---

# System Prompt Comparison

Two versions of system prompts were evaluated.

## Prompt Version A (Basic)

You are a campus assistant.
Answer student questions.


This prompt gives minimal instructions to the model.

---

## Prompt Version B (Improved – Used in the System)
You are a Smart Campus Assistant.

Answer only using the provided database context.
Do not invent facts.
Keep the answer short, clear, and natural.

If the context is insufficient, say that the requested information
is not available in the campus database.


### Reason for choosing Prompt B

Prompt B produced better results because it:

- Reduces hallucinations
- Forces the model to rely on verified database information
- Produces shorter and clearer answers
- Provides safe fallback responses

---

# Test Questions and Results

The following questions were used to evaluate the assistant.

| # | Question | Category | Answer Returned by System |
|---|---|---|---|
| 1 | When is the English 1 exam? | Exam | The English 1 exam is scheduled for March 20 at 10:00 in room B101. |
| 2 | Where is room B101 located? | Location | Room B101 is located in Building B. |
| 3 | When are Ayelet's office hours? | Office hours | Ayelet's office hours are Monday from 10:00 to 12:00 in room A203. |
| 4 | Where is the campus library? | General info | The campus library is located in the central building near the main entrance. |
| 5 | What should I do if I miss an exam? | General academic | You should contact your course lecturer or the academic office to discuss the next steps. |
| 6 | Explain what an algorithm is. | AI knowledge | An algorithm is a step-by-step set of instructions used to solve a problem or perform a task. |
| 7 | How can I reset my student portal password? | Technical problem | You can reset your password through the student portal login page or contact IT support. |
| 8 | Is there parking available on campus? | General info | Yes, parking areas are available near the main campus entrance. |
| 9 | What services does the student office provide? | General info | The student office provides academic support, registration services, and general student assistance. |
| 10 | What is the best pizza restaurant in the city? | Out of scope | The requested information is not available in the campus database. |

---

# Failure Cases and Analysis

Although the assistant generally performed well, several failure cases were observed.

## Failure Case 1 – Ambiguous Question

**Question**

When is the exam?


**Problem**

The question is ambiguous because the course name is missing.

**AI Behavior**

The system classified the question as an exam query but could not determine which course was referenced.

**Reason**

The AI relies on entity extraction and requires a course name to identify the correct exam.

---

## Failure Case 2 – Incomplete Database Context

**Question**
Where is the cafeteria?


**Problem**

The database did not contain detailed information about the cafeteria location.

**AI Behavior**

The assistant returned a generic message stating the information was not available.

**Reason**

The system prompt prevents the AI from inventing information when the database context is missing.

---

## Failure Case 3 – Mixed Question

**Question**
 When is the English exam and where is the library?

 
**Problem**

The question contains two different intents.

**AI Behavior**

The AI focused on one part of the question and ignored the second.

**Reason**

The system is currently designed to process one intent per question.

---

# Conclusion

The experiments demonstrate that the Smart Campus Assistant performs well in answering campus-related questions and relies correctly on database information.

The improved system prompt significantly improved reliability by:

- Preventing hallucinated answers
- Enforcing the use of database context
- Providing safe fallback responses when information is unavailable

Future improvements may include better handling of ambiguous questions and multi-intent queries.
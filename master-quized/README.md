# QuizEd

A smart online quiz application with AI-powered feedback for educational assessments.

## Project Overview

QuizEd is a full-stack web application that enables educators to create and manage quizzes while providing students with personalized AI-generated feedback on their responses. The platform specializes in analyzing open-ended answers using a hybrid approach combining rule-based logic and natural language processing.

## Key Features

- **Quiz Creation and Management**: Instructors can create, edit, and manage quizzes with various question types
- **Open-Ended Question Support**: Advanced support for free-text responses with AI-powered analysis
- **Personalized Feedback**: AI-generated feedback tailored to individual student responses
- **Skill Gap Identification**: Analysis of student answers to identify knowledge gaps
- **Resource Recommendations**: Automated suggestions of learning resources based on identified skill gaps
- **Assignment Management**: Tools for creating and tracking student assignments
- **Performance Analytics**: Insights into student performance and progress

## Architecture

QuizEd consists of three main components:

### 1. Frontend (React)
- Modern React application using TypeScript, hooks, and Vite
- Component-based architecture with Chakra UI for responsive design
- Includes quiz creation, attempt handling, and feedback visualization components
- Dark mode support for accessibility

### 2. Backend (FastAPI)
- RESTful API for handling quiz data, user authentication, and business logic
- PostgreSQL database with SQLModel ORM for data persistence
- JWT authentication for secure access
- Email-based account management and password recovery

### 3. AI Feedback Service
- Dedicated microservice for analyzing student responses
- Implements a multi-stage analysis pipeline:
  - Text preprocessing and normalization
  - Rule-based feedback generation for common cases
  - ML-based deep analysis for complex responses
  - Skill gap identification and resource recommendation
- Integrates with the main backend via API calls

## Technology Stack

- ⚡ [**FastAPI**](https://fastapi.tiangolo.com) for the Python backend API.
    - 🧰 [SQLModel](https://sqlmodel.tiangolo.com) for the Python SQL database interactions (ORM).
    - 🔍 [Pydantic](https://docs.pydantic.dev), used by FastAPI, for the data validation and settings management.
    - 💾 [PostgreSQL](https://www.postgresql.org) as the SQL database.
- 🚀 [React](https://react.dev) for the frontend.
    - 💃 Using TypeScript, hooks, Vite, and other parts of a modern frontend stack.
    - 🎨 [Chakra UI](https://chakra-ui.com) for the frontend components.
    - 🤖 An automatically generated frontend client.
    - 🦇 Dark mode support.
- 🧠 AI/ML Components
    - Natural Language Processing for response analysis
    - Sentence transformers for semantic understanding
    - Rule-based logic for immediate feedback cases
- 🐋 [Docker Compose](https://www.docker.com) for development and production.
- 🔒 Secure password hashing by default.
- 🔑 JWT (JSON Web Token) authentication.
- 📫 Email based password recovery.
- ✅ Tests with [Pytest](https://pytest.org).
- 📞 [Traefik](https://traefik.io) as a reverse proxy / load balancer.
- 🚢 Deployment instructions using Docker Compose, including how to set up a frontend Traefik proxy to handle automatic HTTPS certificates.
- 🏭 CI (continuous integration) and CD (continuous deployment) based on GitHub Actions.

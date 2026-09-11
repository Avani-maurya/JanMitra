# JanMitra AI — Team Development Workflow

## Project
JanMitra AI: An Intelligent Citizen Assistance Platform

## Team Structure

### Member 1 — Team Leader + System & AI Integration
Responsibilities:
- Overall system architecture
- Requirement analysis
- AI integration strategy
- Gemini API integration
- Integration between project modules
- Code/repository coordination
- System-level testing and integration

Branch:
feature/system-ai

### Member 2 — Government Scheme & Recommendation
Responsibilities:
- Government scheme dataset
- Eligibility criteria
- Scheme matching/recommendation logic
- Scheme module APIs
- Backend Services

Branch:
feature/scheme-recommendation

### Member 3 — AI Chatbot & NLP
Responsibilities:
- AI chatbot
- Prompt design
- NLP workflow
- Gemini conversational functionality
- AI response handling

Branch:
feature/chatbot

### Member 4 — Multilingual Voice Assistant
Responsibilities:
- Speech-to-Text
- Text-to-Speech
- Hindi and English voice interaction
- Voice-to-AI workflow
- Accessibility

Branch:
feature/voice-assistant

### Member 5 — Civic Reporting  AI Assistant
Responsibilities:
- Civic issue reporting
- Complaint APIs
- Database integration
- Authentication
  
Branch:
feature/civic-ai

### Member 6 — Frontend + UI/UX + Testing
Responsibilities:
- React frontend
- UI/UX design
- Figma prototypes
- Frontend integration
- UI testing

Branch:
feature/frontend

## Git Workflow

1. `main` contains stable and integrated code.
2. Each member works on their own feature branch.
3. Members should pull the latest `main` before starting major work.
4. Members commit changes with clear commit messages.
5. Members push their feature branch to GitHub.
6. A Pull Request is created when a feature is ready.
7. The team leader reviews the changes.
8. After testing, the Pull Request is merged into `main`.

## Important Rules

- Do not push directly to `main` for normal feature development.
- Do not commit API keys, passwords, or `.env` files.
- Do not commit `node_modules`, Python virtual environments, or cache files.
- Keep commits small and meaningful.
- Do not modify another member's module without coordination.
- Test changes before creating a Pull Request.

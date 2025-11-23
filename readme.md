Interview_Practice_Partner
A web-based mock interview platform that allows candidates to practice interviews with AI-powered questions and feedback. Built with React for the frontend and FastAPI for the backend, integrated with OpenRouter (Mistral-7B-Instruct model) for intelligent interview coaching.

Features

AI-generated interview questions based on the candidate's role.

Real-time speech-to-text answer capture.

Feedback after every answer.

Automatic final interview summary after 10 questions.

Conversation history display.

Option to skip questions.

Tech Stack

Frontend: React.js, JavaScript, CSS

Backend: FastAPI, Python

AI: OpenRouter API (Mistral-7B-Instruct model)

Speech Recognition: Browser's Web Speech API

CORS Handling: FastAPI CORSMiddleware

Environment Variables: .env file with API keys

Architecture
[React Frontend] <--HTTP--> [FastAPI Backend] <--OpenAPI--> [OpenRouter AI Model]

Flow:
1. User sees a question on the frontend.
2. Candidate answers via voice or typing.
3. Frontend sends answer to FastAPI backend.
4. Backend calls OpenRouter AI for:
   - Feedback
   - Next question
   - Final summary (after 10 questions)
5. Backend sends response to frontend.
6. Frontend updates conversation history and displays AI feedback.

Setup Instructions
1. Clone Repository
git clone <your-repo-url>
cd <repo-folder>

2. Backend Setup
cd backend
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows

pip install -r requirements.txt


Create a .env file in the backend folder:

OPENROUTER_API_KEY=your_openrouter_api_key


Run FastAPI backend:

uvicorn app:app --reload --port 8000


The backend will be available at http://localhost:8000.

3. Frontend Setup
cd frontend
npm install
npm start


The frontend will run on http://localhost:3000 and communicate with the backend.

Design Decisions

Single /next endpoint: Handles both normal question flow and final summary to simplify API.

MAX_Q variable: Defines the number of questions per session (10 questions).

Feedback parsing: AI output is parsed for "FEEDBACK:" and "QUESTION:" keywords; fallback included.

Voice recorder: Uses browser Web Speech API with silence detection for automatic answer capture.

Conversation history: Stored on frontend state; allows user to review past Q&A.

CORS enabled: Backend can be accessed from any frontend domain for development purposes.

Environment variables: API key is not hardcoded; kept secure in .env.

Folder Structure
project-root/
│
├── backend/
│   ├── app.py            # FastAPI backend
│   ├── requirements.txt  # Python dependencies
│   └── .env              # API keys
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── InterviewPage.jsx
│   │   │   └── VoiceRecorder.jsx
│   │   └── utils/
│   │       └── tts.js
│   ├── package.json
│   └── public/
│
└── README.md

Usage

Start backend: uvicorn app:app --reload --port 8000

Start frontend: npm start

Open http://localhost:3000 in your browser.

Choose a role and start answering questions.

Review feedback and final summary.

Notes:
Ensure your browser supports Web Speech API for voice recording.

Adjust MAX_Q in app.py if you want longer or shorter interviews.

Final summary includes communication quality, confidence, relevance, improvement areas, and overall score.
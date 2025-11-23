from fastapi import FastAPI
from pydantic import BaseModel
import os
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OpenRouter / OpenAI client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

# Request model
class InterviewRequest(BaseModel):
    role: str
    question: str
    answer: str
    count: int = 1

MAX_Q = 10

@app.post("/next")
async def get_next_question(payload: InterviewRequest):
    """
    Handles both:
    - Normal next question flow
    - Final summary when MAX_Q is reached
    """

    # ----- Final summary -----
    if payload.count >= MAX_Q:
        summary_prompt = f"""
You are an expert HR interviewer.
Provide a **final interview summary** based on the candidate's answers so far.

Include:
- Communication quality
- Confidence
- Relevance
- Areas to improve
- Overall score (1-10)

Return ONLY the summary text.
"""
        summary_response = client.responses.create(
            model="mistralai/mistral-7b-instruct",
            input=summary_prompt
        )
        final_summary = summary_response.output_text.strip()
        return {"finished": True, "summary": final_summary}

    # ----- Normal question flow -----
    prompt = f"""
You are an expert interviewer.
Give 1–2 sentence feedback for the candidate's last answer, then generate the next question.
Last question: {payload.question}
Candidate answer: {payload.answer}
"""
    response = client.responses.create(
        model="mistralai/mistral-7b-instruct",
        input=prompt
    )

    # Parse feedback and next question
    raw = response.output_text
    try:
        if "FEEDBACK:" in raw and "QUESTION:" in raw:
            feedback = raw.split("FEEDBACK:")[1].split("QUESTION:")[0].strip()
            next_q = raw.split("QUESTION:")[1].strip()
        else:
            feedback = "Good attempt. Let's continue."
            next_q = raw.strip()
    except:
        feedback = "Good attempt. Let's continue."
        next_q = raw.strip()

    return {
        "finished": False,
        "feedback": feedback,
        "next_question": next_q,
        "next_count": payload.count + 1
    }

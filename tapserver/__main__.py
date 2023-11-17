import os
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

import dotenv

from tapserver import JoinClassRequest, AnswerSubmission

dotenv.load_dotenv()

app = FastAPI()

CLASS_CODEWORD = os.getenv("CLASS_CODEWORD")


class JoinClassRequest(BaseModel):
    username: str
    codeword: str

class AnswerSubmission(BaseModel):
    username: str
    codeword: str
    answer: str


students = {}  # Dictionary to keep track of students and their answers


@app.post("/join_class")
async def join_class(request: JoinClassRequest):
    if request.codeword != CLASS_CODEWORD:
        raise HTTPException(status_code=403, detail="Invalid codeword")
    students[request.username] = None  # Student joined but hasn't answered yet
    print("A student joined!!")
    print(students)

    return {"message": "Joined class successfully"}



@app.post("/submit_answer")
async def submit_answer(request: AnswerSubmission):
    if request.codeword != CLASS_CODEWORD or request.username not in students:
        raise HTTPException(status_code=403, detail="Invalid request")
    students[request.username] = request.answer  # Record the student's answer
    print(f"Student {request.username} answered {request.answer}")
    return {"message": "Answer submitted"}



@app.get("/class_status")
async def class_status():
    return students



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

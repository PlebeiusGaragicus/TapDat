from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class JoinClassRequest(BaseModel):
    username: str
    codeword: str

class AnswerSubmission(BaseModel):
    username: str
    codeword: str
    answer: str


codeword = "asdf"  # Set the codeword
students = {}  # Dictionary to keep track of students and their answers



@app.post("/join_class")
async def join_class(request: JoinClassRequest):
    if request.codeword != codeword:
        raise HTTPException(status_code=403, detail="Invalid codeword")
    students[request.username] = None  # Student joined but hasn't answered yet
    print("A student joined!!")
    print(students)
    return {"message": "Joined class successfully"}



@app.post("/submit_answer")
async def submit_answer(request: AnswerSubmission):
    if request.codeword != codeword or request.username not in students:
        raise HTTPException(status_code=403, detail="Invalid request")
    students[request.username] = request.answer  # Record the student's answer
    return {"message": "Answer submitted"}



@app.get("/class_status")
async def class_status():
    return students


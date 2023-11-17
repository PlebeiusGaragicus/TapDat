from pydantic import BaseModel


class JoinClassRequest(BaseModel):
    username: str
    codeword: str

class AnswerSubmission(BaseModel):
    username: str
    codeword: str
    answer: str

API_ENDPOINT = "http://192.168.5.158:8000"

from pydantic import BaseModel


class JoinClassRequest(BaseModel):
    username: str
    codeword: str

class AnswerSubmission(BaseModel):
    username: str
    codeword: str
    answer: str


class student:
    username: str
    answer: str
    answer_time: int


# API_ENDPOINT = "http://192.168.5.158:8000"
# API_ENDPOINT = "http://192.168.5.158:51924"
API_ENDPOINT = "http://0.0.0.0:8000"

import requests
from pywebio import start_server, output, input, session, pin
from pywebio.output import use_scope

from tapserver import API_ENDPOINT


question = [
    {"Q": "WHO IS YOUR DADDY AND WHAT DOES HE DO?",
    "A": "Arnold Schwarzenegger - Kindergarten Cop",
    "B": "Bruce Willis - Die Hard",
    "C": "Sylvester Stallone - Rocky",
    "D": "Jason Statham - The Transporter"},

    {"Q": "SECOND QUESTION?",
    "A": "AAA",
    "B": "BBB",
    "C": "DDD",
    "D": "DDD"}
]



question_number = 0



def refresh_students():
    response = requests.get(f"{API_ENDPOINT}/class_status") # TODO add authorization via codeword

    if response.status_code == 200:
        students = response.json()

    with use_scope("student_list", clear=True):
        output.put_markdown("## Students")
        if students == {}:
            output.put_text("No students have joined yet")
        else:
            for s in students:
                output.put_text(f"- {s}")



def check_answers():
    response = requests.get(f"{API_ENDPOINT}/class_status") # TODO add authorization via codeword

    if response.status_code == 200:
        students = response.json()

    with use_scope("results", clear=True):
        output.put_markdown("## Results")
        if students == {}:
            output.put_text("No students have joined yet")
        else:
            # talley answers for each letter
            answers = {
                "A": 0,
                "B": 0,
                "C": 0,
                "D": 0
            }

            for s in students:
                if students[s] not in answers:
                    answers[students[s]] = 1
                else:
                    answers[students[s]] += 1
            output.put_table([
                ["Answer", "Count"],
                *[[k, v] for k, v in answers.items()]
            ])
        
        output.put_button("Next question", onclick=next_question, color="success")


def next_question():
    global question_number
    # question_number += 1

    output.clear("page")
    output.clear("results")
    with use_scope("page", clear=True):

        Q = question[question_number]["Q"]
        A = question[question_number]["A"]
        B = question[question_number]["B"]
        C = question[question_number]["C"]
        D = question[question_number]["D"]
        question_number += 1

        output.put_markdown(f"{Q}")

        output.put_markdown(f"A - {A}")
        output.put_markdown(f"B - {B}")
        output.put_markdown(f"C - {C}")
        output.put_markdown(f"D - {D}")

        output.put_button("Check answers", onclick=check_answers, color="success")



def teacher_interface():
    global question_number
    question_number = 0

    output.put_html("""
    <style>
    body {
        background-color: lightblue;
    }
    </style>
    """)

    with use_scope("page", clear=True):
        output.put_button("Start quiz", onclick=next_question, color="success")
        output.put_button("Refresh student list", onclick=refresh_students, color="success")
        refresh_students()



if __name__ == "__main__":
    start_server(teacher_interface, port=8081)

import os
import json
import requests
from pywebio import start_server, output, input, session, pin
from pywebio.output import use_scope

from tapserver import API_ENDPOINT



question_number = 0



def refresh_students():
    response = requests.get(f"{API_ENDPOINT}/class_status") # TODO add authorization via codeword

    if response.status_code == 200:
        students = response.json()
    else:
        print(response)
        output.toast("Could not get class status", color="error")

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
        print(students)
    else:
        output.toast("Could not get class status", color="error")

    with use_scope("results", clear=True):
        if None in students.values():
            output.toast("Not all students have answered yet", color="warn")

            ## show the students who haven't answered yet
            output.put_markdown("## Students who haven't answered yet")
            for s in students:
                if students[s] == None:
                    output.put_text(f"- {s}")
            return

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


quiz_data = {}

def start_quiz():
    global quiz_data
    global question_number
    question_number = 0

    quiz = pin.pin['quiz']
    with open(f"quizzes/{quiz}.json", "r") as f:
        quiz_data = json.loads(f.read())

    # with use_scope("page", clear=True):
    #     output.put_markdown("## Quiz")
    #     output.put_markdown("Welcome to the quiz!")
    #     output.put_button("Start quiz", onclick=next_question, color="success")
    next_question()


def next_question():
    global question_number
    global quiz_data
    print(type(quiz_data))
    
    output.clear("page")
    output.clear("results")
    with use_scope("page", clear=True):

        print(quiz_data[question_number])
        Q = quiz_data[question_number]["questionText"]
        A = quiz_data[question_number]["options"]["A"]
        B = quiz_data[question_number]["options"]["B"]
        C = quiz_data[question_number]["options"]["C"]
        D = quiz_data[question_number]["options"]["D"]

        question_number += 1

        output.put_markdown(f"# {Q}")

        output.put_markdown(f"## A - {A}")
        output.put_markdown(f"## B - {B}")
        output.put_markdown(f"## C - {C}")
        output.put_markdown(f"## D - {D}")

        output.put_button("Check answers", onclick=check_answers, color="success")



def load_quizzes():
    """ Return a list of all JSON files inside /quizzes """

    quizzes = []
    for filename in os.listdir("quizzes"):
        if filename.endswith(".json"):
            quizzes.append(filename.removesuffix(".json"))

    return quizzes



def teacher_interface():
    output.put_html("""
    <style>
    body {
        background-color: lightblue;
    }
    </style>
    """)

    quiz_list = load_quizzes()
    print(quiz_list)

    with use_scope("page", clear=True):
        # drop down of quizzes
        pin.put_select("quiz", options=quiz_list)
        output.put_button("Start quiz", onclick=start_quiz, color="success")
        output.put_button("Refresh student list", onclick=refresh_students, color="success")
        refresh_students()



if __name__ == "__main__":
    start_server(teacher_interface, port=8081)

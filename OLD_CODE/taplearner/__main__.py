from functools import partial
from pywebio import start_server

import requests

from pywebio import output, pin
from pywebio_battery import set_cookie, get_cookie

from tapserver import API_ENDPOINT



def get_user_session():
    username = get_cookie("username")
    codeword = get_cookie("codeword")
    print("get_user_session", f"'{username}'", f"'{codeword}'")

    if None in (username, codeword) or "" in (username, codeword):
        print("no session")
        return None, None
    else:
        return username, codeword




def submit_to_join_class():
    username = pin.pin["username"]
    codeword = pin.pin["codeword"]
    print("submit_to_join_class", username, codeword)
    if None in (username, codeword):
        output.toast("Please enter the codeword to start", color="warn")
        return False

    set_cookie("username", username)
    set_cookie("codeword", codeword)

    # Send POST request with the answer
    try:
        response = requests.post(f"{API_ENDPOINT}/join_class", json={"username": username, "codeword": codeword})
    except requests.exceptions.ConnectionError:
        output.toast("Could not join class", color="error")
        return False

    if response.status_code == 200:
        # output.put_text("Answer submitted!")
        return True
    else:
        output.toast("Could not join class", color="error")
        # output.put_text("Failed to submit the answer.")
        return False



def answer(letter: str):

    username, codeword = get_user_session()
    # TODO check if session is valid
    # if None in (username, codeword):
    #     output.toast("Please enter the codeword to start", color="warn")

    # Send POST request with the answer
    try:
        response = requests.post(f"{API_ENDPOINT}/submit_answer", json={"username": username, "codeword": codeword, "answer": letter})
    except requests.exceptions.ConnectionError:
        output.toast("Could not submit answer", color="error")
        return False
    
    if response.status_code == 200:
        output.toast(f"Answer {letter} submitted!", color="success")
    else:
        output.toast("Failed to submit the answer.", color="error")





def join_class():
    if submit_to_join_class():
        output.toast("Joined class successfully!", color="success")
        pin.pin_update(name="codeword", readonly=True)
        output.clear("login")

        output.put_button("A", onclick=lambda: partial(answer, "A")(), color="success")
        output.put_button("B", onclick=lambda: partial(answer, "B")(), color="success")
        output.put_button("C", onclick=lambda: partial(answer, "C")(), color="success")
        output.put_button("D", onclick=lambda: partial(answer, "D")(), color="success")





def tap_catch():
    with output.use_scope("login", clear=True):
        # output.put_collapse("Instructions", [
        #     output.put_markdown("## Instructions"),
        #     output.put_markdown("1. Enter the codeword to start"),
        #     output.put_markdown("2. Enter your name"),
        #     output.put_markdown("3. Click on Submit")
        # ], open=False)
        output.put_markdown("## Login to Tap Class")

        pin.put_input(name="username", type="text", label="Your fake name 🧑‍🚒", value="")
        pin.put_input(name="codeword", type="text", label="The password 🤐", value="")
        output.put_button("Join class", onclick=join_class)

    username, codeword = get_user_session()
    if not None in (username, codeword):
        print("session found - trying to join with this info")
        pin.pin_update(name="username", value=username)
        pin.pin_update(name="codeword", value=codeword)
        join_class()





if __name__ == '__main__':
    start_server(tap_catch, port=8080)

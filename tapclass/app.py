import requests
from pywebio import output, pin


# API_ENDPOINT = "http://your-fastapi-server.com"
API_ENDPOINT = "http://192.168.5.158:8000"


def submit_to_join_class():
    username = pin.pin["username"]
    codeword = pin.pin["codeword"]
    if None in (username, codeword):
        output.toast("Please enter the codeword to start", color="warn")
        return False

    # Send POST request with the answer
    response = requests.post(f"{API_ENDPOINT}/join_class", json={"username": username, "codeword": codeword})

    if response.status_code == 200:
        output.put_text("Answer submitted!")
        return True
    else:
        output.put_text("Failed to submit the answer.")
        return False



def join_class():
    if submit_to_join_class():
        output.put_text("Joined class successfully!")
        pin.pin_update(name="codeword", readonly=True)
        output.clear("login")
        # output.set_scope("class")
    else:
        output.put_text("Failed to join class.")



def tap_catch():
    with output.use_scope("login", clear=True):
        output.put_collapse("Instructions", [
            output.put_markdown("## Instructions"),
            output.put_markdown("1. Enter the codeword to start"),
            output.put_markdown("2. Enter your name"),
            output.put_markdown("3. Click on Submit")
        ], open=False)

        pin.put_input(name="username", type="text", label="Your fake name 🧑‍🚒", value="")
        pin.put_input(name="codeword", type="text", label="The password 🤐", value="")
        output.put_button("Submit", onclick=join_class)


    # name = input.input("Your name:")
    # choices = ['A', 'B', 'C', 'D', 'E']

    # while True:
    #     answer = input.radio("Choose your answer", options=choices)
    #     # Send POST request with the answer
    #     response = requests.post("http://your-fastapi-server.com/submit_answer", json={"name": name, "answer": answer})
    #     if response.status_code == 200:
    #         output.put_text("Answer submitted!")
    #     else:
    #         output.put_text("Failed to submit the answer.")

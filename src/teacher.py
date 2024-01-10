import streamlit as st
import streamlit_authenticator as stauth

import yaml
from yaml.loader import SafeLoader


from src.common import Role, top_navigation





def teacher_authentication():

    if "authenticator" not in st.session_state:
        with open("./auth.yaml") as file:
            config = yaml.load(file, Loader=SafeLoader)

        # authenticator = stauth.Authenticate(
        st.session_state["authenticator"] = stauth.Authenticate(
            config["credentials"],
            config["cookie"]["name"],
            config["cookie"]["key"],
            config["cookie"]["expiry_days"],
            config["preauthorized"],
        )

    st.session_state.authenticator.login("Login as instructor", "main")

    if st.session_state["authentication_status"]:
        st.session_state["role"] = "teacher"

        st.session_state.cookie_monster.set("role", Role.TEACHER)
        return True

    elif st.session_state["authentication_status"] is False:
        st.error("Username/password is incorrect")
        return False

    # elif st.session_state["authentication_status"] is None:
    #     st.warning("Please enter your username and password")





def teacher_page():
    top_navigation()

    # if st.session_state["authentication_status"] is None:
    if not teacher_authentication():
        return

    st.write("# Teacher page")

import streamlit as st

from src.common import Role


def landing_page():
    st.write("# TapDat")

    cols = st.columns((1,2))

    with cols[0]:
        if st.button("Join a class"):
            st.session_state.cookie_monster.set(
                "role",
                Role.STUDENT,
                key="role",
                max_age=60*60*24*7)
            # st.session_state["role"] = "student"


    with cols[1]:
        if st.button("Login as instructor"):
            st.session_state.cookie_monster.set("role", Role.TEACHER)
            # st.session_state["role"] = "teacher"


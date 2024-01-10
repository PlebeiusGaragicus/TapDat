import time
import streamlit as st



class Role:
    STUDENT = "student"
    TEACHER = "teacher"


def top_navigation():
    if st.button("<- return to landing page"):
        st.session_state.cookie_monster.set("role", None)
        st.session_state["role"] = None
        time.sleep(0.2)

    
    st.write("---")

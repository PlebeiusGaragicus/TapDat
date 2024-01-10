import os
import time

import streamlit as st
import extra_streamlit_components as stx

import logging
log = logging.getLogger()

from src.VERSION import VERSION
from src.common import Role
from src.landing_page import landing_page
from src.teacher import teacher_page
from src.student import student_page





def main():
    log.debug("Starting main()")
    st.set_page_config(page_title="TapDat", layout="centered", initial_sidebar_state="auto")


    # INITIALIZATION ON FIRST-RUN
    if "cookie_monster" not in st.session_state:
        st.session_state["cookie_monster"] = stx.CookieManager()

    print(st.session_state.cookie_monster.get_all())

    # if "role" not in st.session_state:
    # if "cookies" not in st.session_state:
    st.session_state.cookies = st.session_state.cookie_monster.get_all(key="some_key")
    time.sleep(0.2)

    # if role_cookie is not None:
    if "role" in st.session_state.cookies.keys():
        log.debug("Found role cookie")
        st.session_state["role"] = st.session_state.cookies['role']
    else:
        log.debug("No role cookie found")
        st.session_state["role"] = None



    if st.session_state["role"] == Role.STUDENT:
        student_page()

    if st.session_state["role"] == Role.TEACHER:
        teacher_page()

    if st.session_state["role"] is None:
        landing_page()
        st.write("---")
        st.caption(f"TapDat v{VERSION}")

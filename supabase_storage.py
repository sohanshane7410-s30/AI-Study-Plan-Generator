"""Supabase authentication and persistence helpers for AI Study Plan Generator.

This module uses the project's Supabase Publishable Key from Streamlit Secrets.
It never contains passwords, API keys, or service-role credentials.
"""

from __future__ import annotations

from typing import Any

import streamlit as st
from supabase import Client, create_client


STUDENT_TABLE = "study_plan_students"
PLAN_TABLE = "study_plan_history"


def _get_client() -> Client:
    """Create one Supabase client per Streamlit browser session."""
    project_url = st.secrets.get("SUPABASE_URL", "")
    publishable_key = st.secrets.get("SUPABASE_KEY", "")

    if not project_url or not publishable_key:
        raise RuntimeError(
            "Supabase settings are missing. Add SUPABASE_URL and "
            "SUPABASE_KEY in Streamlit App Settings → Secrets."
        )

    if "_supabase_client" not in st.session_state:
        st.session_state["_supabase_client"] = create_client(
            project_url,
            publishable_key,
        )

    return st.session_state["_supabase_client"]


def render_login_gate() -> tuple[Client | None, str | None]:
    """Render sign-in until an authenticated Supabase user is present.

    Returns (client, user_id) when signed in; otherwise returns (None, None).
    The Supabase client is held in Streamlit session state so its Auth session
    remains available across the app's reruns for this browser session.
    """
    try:
        client = _get_client()
    except Exception as exc:
        st.error(str(exc))
        st.info(
            "Check that the Streamlit Secrets contain the correct project URL "
            "and Publishable Key. Do not put secrets in GitHub."
        )
        return None, None

    user_id = st.session_state.get("_supabase_user_id")

    if not user_id:
        st.markdown(
            "<div style='max-width:650px;margin:2rem auto 1rem;'>"
            "<h1>Learning Intelligence Studio</h1>"
            "<p>Sign in with your authorized workspace account to access "
            "student records.</p></div>",
            unsafe_allow_html=True,
        )

        left, center, right = st.columns([1, 2, 1])
        with center:
            with st.form("supabase_sign_in_form", clear_on_submit=False):
                email = st.text_input("Email address", autocomplete="email")
                password = st.text_input(
                    "Password",
                    type="password",
                    autocomplete="current-password",
                )
                submitted = st.form_submit_button(
                    "Sign in",
                    use_container_width=True,
                )

            if submitted:
                if not email.strip() or not password:
                    st.error("Enter your email address and password.")
                else:
                    try:
                        response = client.auth.sign_in_with_password(
                            {
                                "email": email.strip(),
                                "password": password,
                            }
                        )
                        if not response.user:
                            st.error("Supabase did not return a signed-in user.")
                        else:
                            st.session_state["_supabase_user_id"] = str(
                                response.user.id

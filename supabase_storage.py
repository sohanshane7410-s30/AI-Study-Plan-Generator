"""Supabase authentication and persistent storage helpers.

Compatible with older Python runtimes used by some Streamlit deployments.
Uses the Supabase Publishable Key configured in Streamlit Secrets.
Never place passwords or secret/service-role keys in this file.
"""

import streamlit as st
from supabase import create_client

STUDENT_TABLE = "study_plan_students"
PLAN_TABLE = "study_plan_history"


def _get_client():
    """Create and cache a Supabase client for this Streamlit session."""
    project_url = st.secrets.get("SUPABASE_URL", "")
    publishable_key = st.secrets.get("SUPABASE_KEY", "")

    if not project_url or not publishable_key:
        raise RuntimeError(
            "Supabase settings are missing. Add SUPABASE_URL and "
            "SUPABASE_KEY in Streamlit App Settings > Secrets."
        )

    cached = st.session_state.get("_supabase_client")
    if cached is None:
        cached = create_client(project_url, publishable_key)
        st.session_state["_supabase_client"] = cached

    return cached


def render_login_gate():
    """Render the sign-in form and return (client, user_id) when signed in."""
    try:
        client = _get_client()
    except Exception as exc:
        st.error("Supabase connection settings could not be loaded.")
        with st.expander("Connection details"):
            st.code(str(exc))
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
                email = st.text_input("Email address")
                password = st.text_input("Password", type="password")
                submitted = st.form_submit_button(
                    "Sign in", use_container_width=True
                )

            if submitted:
                if not email.strip() or not password:
                    st.error("Enter your email address and password.")
                else:
                    try:
                        response = client.auth.sign_in_with_password(
                            {"email": email.strip(), "password": password}
                        )
                        user = getattr(response, "user", None)
                        if user is None:
                            st.error("Supabase did not return a signed-in user.")
                        else:
                            st.session_state["_supabase_user_id"] = str(user.id)
                            st.session_state["_supabase_user_email"] = (
                                getattr(user, "email", None) or email.strip()
                            )
                            st.rerun()
                    except Exception as exc:
                        st.error(
                            "Sign-in failed. Check your email, password, "
                            "and Supabase Auth user status."
                        )
                        with st.expander("Sign-in details"):
                            st.code(str(exc))

        st.caption(
            "Only accounts authorized in Supabase Authentication can sign in. "
            "Public registration is not enabled in this application."
        )
        return None, None

    with st.sidebar:
        st.caption(

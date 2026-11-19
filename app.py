
import streamlit as st

st.set_page_config(
    page_title="AI Study Plan Generator",
    page_icon="📚",
    layout="wide"
)

st.title("📚 AI Study Plan Generator")
st.caption("Personalized Learning Starts Here")

st.divider()

st.header("👩‍🎓 Student Registration")

st.write("Register a student and add their academic information.")

with st.form("student_registration"):

    student_name = st.text_input(
        "Student Name",
        placeholder="Enter student name"
    )

    student_id = st.text_input(
        "Student ID",
        placeholder="Enter a unique student ID"
    )

    subject = st.selectbox(
        "Academic Subject",
        ["Mathematics", "Science", "English", "Computer Science", "Other"]
    )

    custom_subject = ""

    if subject == "Other":
        custom_subject = st.text_input(
            "Enter Subject Name",
            placeholder="Enter your subject"
        )

    submitted = st.form_submit_button(
        "Register Student",
        use_container_width=True
    )

    if submitted:

        final_subject = (
            custom_subject.strip()
            if subject == "Other"
            else subject
        )

        if not student_name.strip() or not student_id.strip():
            st.error("Please enter student name and ID.")

        elif not final_subject:
            st.error("Please enter a subject name.")

        else:
            st.session_state["student_preview"] = {
                "name": student_name.strip(),
                "id": student_id.strip(),
                "subject": final_subject
            }

            st.success("Student registration submitted!")

if "student_preview" in st.session_state:

    student = st.session_state["student_preview"]

    st.subheader("📋 Student Profile Preview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Student Name", student["name"])
    col2.metric("Student ID", student["id"])
    col3.metric("Subject", student["subject"])

    st.info(
        "Student profile is currently stored in the session. "
        "Permanent database storage will come later."
    )

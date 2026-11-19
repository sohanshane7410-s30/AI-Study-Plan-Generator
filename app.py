
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

st.write("Enter the student's academic information.")

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
        ["Mathematics", "Science", "English", "Computer Science"]
    )

    st.subheader("📊 Academic Performance")

    current_mastery = st.number_input(
        "Current Mastery (%)",
        min_value=0,
        max_value=100,
        value=42,
        step=1
    )

    target_mastery = st.number_input(
        "Target Mastery (%)",
        min_value=0,
        max_value=100,
        value=80,
        step=1
    )

    submitted = st.form_submit_button(
        "Register Student",
        use_container_width=True
    )

    if submitted:

        if not student_name.strip() or not student_id.strip():
            st.error("Please enter student name and ID.")

        else:
            st.session_state["student_preview"] = {
                "name": student_name.strip(),
                "id": student_id.strip(),
                "subject": subject,
                "current_mastery": current_mastery,
                "target_mastery": target_mastery
            }

            st.success("Student registration submitted!")

if "student_preview" in st.session_state:

    student = st.session_state["student_preview"]

    st.divider()
    st.subheader("📋 Student Academic Profile")

    col1, col2, col3 = st.columns(3)

    col1.metric("Student", student["name"])
    col2.metric("Student ID", student["id"])
    col3.metric("Subject", student["subject"])

    col4, col5 = st.columns(2)

    col4.metric(
        "Current Mastery",
        f"{student['current_mastery']}%"
    )

    col5.metric(
        "Target Mastery",
        f"{student['target_mastery']}%"
    )

    st.info(
        "Academic information is currently stored in the "
        "Streamlit session. Permanent database storage "
        "will be implemented in a later mission."
    )

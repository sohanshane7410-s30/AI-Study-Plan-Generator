
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

st.write(
    "Register a student to begin building their personalized learning plan."
)

with st.form("student_registration"):

    student_name = st.text_input(
        "Student Name",
        placeholder="Enter student name"
    )

    student_id = st.text_input(
        "Student ID",
        placeholder="Enter a unique student ID"
    )

    submitted = st.form_submit_button(
        "Register Student",
        use_container_width=True
    )

    if submitted:

        if not student_name.strip() or not student_id.strip():

            st.error("Please enter both student name and student ID.")

        else:

            st.session_state["student_preview"] = {
                "name": student_name.strip(),
                "id": student_id.strip()
            }

            st.success("Student registration form submitted!")

if "student_preview" in st.session_state:

    student = st.session_state["student_preview"]

    st.subheader("Student Profile Preview")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Student Name", student["name"])

    with col2:
        st.metric("Student ID", student["id"])

    st.info(
        "This is a temporary session preview. "
        "Permanent database storage will be added in a later task."
    )

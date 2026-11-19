
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

with st.form("student_registration"):

    student_name = st.text_input("Student Name")
    student_id = st.text_input("Student ID")

    subject = st.selectbox(
        "Academic Subject",
        ["Mathematics", "Science", "English", "Computer Science"]
    )

    st.subheader("📊 Academic Performance")

    current_mastery = st.number_input(
        "Current Mastery (%)",
        min_value=0,
        max_value=100,
        value=42
    )

    target_mastery = st.number_input(
        "Target Mastery (%)",
        min_value=0,
        max_value=100,
        value=80
    )

    st.subheader("🧠 Learning Strengths and Weaknesses")

    weak_topics_input = st.text_input(
        "Weak Topics",
        placeholder="Fractions, Decimals"
    )

    strong_topics_input = st.text_input(
        "Strong Topics",
        placeholder="Percentages, Basic arithmetic"
    )

    st.subheader("⏰ Study Availability")

    daily_study_minutes = st.number_input(
        "Daily Available Study Time (minutes)",
        min_value=15,
        max_value=240,
        value=120,
        step=15
    )

    st.subheader("📅 Preferred Study Days")

    available_days = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ]

    study_days = st.multiselect(
        "Select the days you can study",
        available_days,
        default=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    )

    submitted = st.form_submit_button(
        "Register Student",
        use_container_width=True
    )

    if submitted:

        weak_topics = [
            topic.strip()
            for topic in weak_topics_input.split(",")
            if topic.strip()
        ]

        strong_topics = [
            topic.strip()
            for topic in strong_topics_input.split(",")
            if topic.strip()
        ]

        overlap = (
            {topic.lower() for topic in weak_topics}
            & {topic.lower() for topic in strong_topics}
        )

        if not student_name.strip() or not student_id.strip():
            st.error("Please enter student name and ID.")

        elif not weak_topics or not strong_topics:
            st.error("Please enter weak and strong topics.")

        elif overlap:
            st.error(
                "A topic cannot be both weak and strong: "
                + ", ".join(sorted(overlap))
            )

        elif target_mastery <= current_mastery:
            st.error("Target mastery must be greater than current mastery.")

        elif not study_days:
            st.error("Please select at least one study day.")

        else:

            st.session_state["student_preview"] = {
                "name": student_name.strip(),
                "id": student_id.strip(),
                "subject": subject,
                "current_mastery": current_mastery,
                "target_mastery": target_mastery,
                "weak_topics": weak_topics,
                "strong_topics": strong_topics,
                "daily_study_minutes": daily_study_minutes,
                "study_days": study_days
            }

            st.success("Student profile submitted successfully!")

if "student_preview" in st.session_state:

    student = st.session_state["student_preview"]

    st.divider()
    st.header("📋 Student Academic Profile")

    col1, col2, col3 = st.columns(3)

    col1.metric("Student", student["name"])
    col2.metric("Student ID", student["id"])
    col3.metric("Subject", student["subject"])

    col4, col5 = st.columns(2)

    col4.metric("Current Mastery", f"{student['current_mastery']}%")
    col5.metric("Target Mastery", f"{student['target_mastery']}%")

    st.subheader("🔴 Weak Topics")

    for topic in student["weak_topics"]:
        st.write(f"🔴 {topic}")

    st.subheader("🟢 Strong Topics")

    for topic in student["strong_topics"]:
        st.write(f"🟢 {topic}")

    st.subheader("⏰ Daily Study Availability")

    minutes = student["daily_study_minutes"]

    st.metric(
        "Study Time",
        f"{minutes} minutes",
        f"{minutes / 60:g} hours per day"
    )

    st.subheader("📅 Weekly Study Availability")

    st.write(f"Available study days: {len(student['study_days'])}")

    for day in student["study_days"]:
        st.write(f"✅ {day}")

    st.info(
        "Student information is temporarily stored in the "
        "Streamlit session. Permanent database storage "
        "will be implemented in a later mission."
    )

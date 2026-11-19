
import streamlit as st

st.set_page_config(
    page_title="AI Study Plan Generator",
    page_icon="📚",
    layout="wide"
)

# Initialize session storage
if "students" not in st.session_state:
    st.session_state["students"] = []


def parse_topics(raw_text):
    """Clean topics and remove duplicates."""
    topics = []
    seen = set()

    for item in raw_text.split(","):
        topic = item.strip()

        if topic and topic.casefold() not in seen:
            topics.append(topic)
            seen.add(topic.casefold())

    return topics


# Application header
st.title("📚 AI Study Plan Generator")
st.caption("Personalized Learning Starts Here")

st.divider()

st.header("👩‍🎓 Student Registration")

st.write(
    "Register students and create their personalized academic profiles."
)

# Registration form
with st.form("student_registration"):

    student_name = st.text_input(
        "Student Name",
        placeholder="Enter student name"
    )

    student_id = st.text_input(
        "Student ID",
        placeholder="Enter a unique ID"
    )

    subject = st.selectbox(
        "Academic Subject",
        [
            "Mathematics",
            "Science",
            "English",
            "Computer Science"
        ]
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
        "Preferred Study Days",
        available_days,
        default=[
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday"
        ]
    )

    submitted = st.form_submit_button(
        "Register Student",
        use_container_width=True
    )

    if submitted:

        name = student_name.strip()
        clean_id = student_id.strip().upper()

        weak_topics = parse_topics(weak_topics_input)
        strong_topics = parse_topics(strong_topics_input)

        overlap = (
            {topic.casefold() for topic in weak_topics}
            & {topic.casefold() for topic in strong_topics}
        )

        duplicate_id = any(
            student["id"].casefold() == clean_id.casefold()
            for student in st.session_state["students"]
        )

        if not name or not clean_id:
            st.error("Student name and ID are required.")

        elif duplicate_id:
            st.error("This student ID is already registered.")

        elif not weak_topics or not strong_topics:
            st.error(
                "Please enter at least one weak and one strong topic."
            )

        elif overlap:
            st.error(
                "A topic cannot be both weak and strong: "
                + ", ".join(sorted(overlap))
            )

        elif target_mastery < current_mastery:
            st.error(
                "Target mastery cannot be lower than current mastery."
            )

        elif not study_days:
            st.error("Please select at least one study day.")

        else:

            mastery_gap = max(
                target_mastery - current_mastery,
                0
            )

            weekly_minutes = (
                daily_study_minutes * len(study_days)
            )

            student = {
                "name": name,
                "id": clean_id,
                "subject": subject,
                "current_mastery": current_mastery,
                "target_mastery": target_mastery,
                "mastery_gap": mastery_gap,
                "weak_topics": weak_topics,
                "strong_topics": strong_topics,
                "daily_study_minutes": daily_study_minutes,
                "study_days": study_days,
                "weekly_minutes": weekly_minutes
            }

            st.session_state["students"].append(student)

            st.success(
                f"{name} registered successfully!"
            )

# Display registered students
st.divider()

st.header("📋 Registered Students")

students = st.session_state["students"]

if students:

    st.metric(
        "Total Registered Students",
        len(students)
    )

    student_table = []

    for student in students:

        student_table.append({
            "Name": student["name"],
            "Student ID": student["id"],
            "Subject": student["subject"],
            "Mastery": f"{student['current_mastery']}%",
            "Target": f"{student['target_mastery']}%",
            "Gap": f"{student['mastery_gap']}%",
            "Weekly Hours": round(
                student["weekly_minutes"] / 60, 2
            )
        })

    st.dataframe(
        student_table,
        use_container_width=True,
        hide_index=True
    )

    # Individual academic profiles
    st.divider()
    st.header("🔍 Individual Student Profiles")

    for student in students:

        with st.expander(
            f"{student['name']} — {student['id']}"
        ):

            st.write(f"**Subject:** {student['subject']}")

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Current Mastery",
                f"{student['current_mastery']}%"
            )

            col2.metric(
                "Target Mastery",
                f"{student['target_mastery']}%"
            )

            col3.metric(
                "Mastery Gap",
                f"{student['mastery_gap']}%"
            )

            st.subheader("🔴 Weak Topics")

            for topic in student["weak_topics"]:
                st.write(f"🔴 {topic}")

            st.subheader("🟢 Strong Topics")

            for topic in student["strong_topics"]:
                st.write(f"🟢 {topic}")

            st.subheader("📅 Study Availability")

            for day in student["study_days"]:
                st.write(f"✅ {day}")

            st.metric(
                "Weekly Study Capacity",
                f"{student['weekly_minutes'] / 60:g} hours"
            )

            if student["mastery_gap"] == 0:
                st.success("Target mastery already achieved!")
            else:
                st.info(
                    f"{student['mastery_gap']} percentage "
                    "points remaining to target mastery."
                )

else:

    st.info("No students registered yet.")

st.divider()

st.caption(
    "AI Study Plan Generator | Student Registration Module"
)

st.warning(
    "Student records currently exist only in Streamlit session "
    "memory. Permanent storage and duplicate protection across "
    "sessions will be implemented using Supabase."
)

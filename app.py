
import streamlit as st

st.set_page_config(
    page_title="AI Study Plan Generator",
    page_icon="📚",
    layout="wide"
)

# Initialize student records
if "students" not in st.session_state:
    st.session_state["students"] = []


# Topic processing
def parse_topics(raw_text):
    topics = []
    seen = set()

    for item in raw_text.split(","):
        topic = item.strip()

        if topic and topic.casefold() not in seen:
            topics.append(topic)
            seen.add(topic.casefold())

    return topics


# Priority classification engine
def classify_priority(current, target):

    if current >= target:
        return "TARGET ACHIEVED"

    elif current < 40:
        return "URGENT"

    elif current < 60:
        return "HIGH"

    else:
        return "MODERATE"


# Application heading
st.title("📚 AI Study Plan Generator")
st.caption("Personalized Learning Starts Here")

st.divider()


# ==================================
# STUDENT REGISTRATION
# ==================================

st.header("👩‍🎓 Student Registration")

with st.form("student_registration"):

    student_name = st.text_input("Student Name")
    student_id = st.text_input("Student ID")

    subject = st.selectbox(
        "Academic Subject",
        ["Mathematics", "Science", "English", "Computer Science"]
    )

    st.subheader("Academic Performance")

    current_mastery = st.number_input(
        "Current Mastery (%)",
        0, 100, 42
    )

    target_mastery = st.number_input(
        "Target Mastery (%)",
        0, 100, 80
    )

    st.subheader("Learning Strengths and Weaknesses")

    weak_input = st.text_input(
        "Weak Topics",
        "Fractions, Decimals"
    )

    strong_input = st.text_input(
        "Strong Topics",
        "Percentages, Basic arithmetic"
    )

    st.subheader("Study Availability")

    daily_minutes = st.number_input(
        "Daily Study Time (minutes)",
        15, 240, 120, step=15
    )

    available_days = [
        "Monday", "Tuesday", "Wednesday",
        "Thursday", "Friday", "Saturday", "Sunday"
    ]

    study_days = st.multiselect(
        "Preferred Study Days",
        available_days,
        default=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    )

    submitted = st.form_submit_button(
        "Register Student",
        use_container_width=True
    )

    if submitted:

        name = student_name.strip()
        clean_id = student_id.strip().upper()

        weak_topics = parse_topics(weak_input)
        strong_topics = parse_topics(strong_input)

        overlap = (
            {t.casefold() for t in weak_topics}
            & {t.casefold() for t in strong_topics}
        )

        existing_ids = [
            s["id"].casefold()
            for s in st.session_state["students"]
        ]

        if not name or not clean_id:
            st.error("Enter student name and ID.")

        elif clean_id.casefold() in existing_ids:
            st.error("Student ID already exists.")

        elif not weak_topics or not strong_topics:
            st.error("Enter at least one weak and one strong topic.")

        elif overlap:
            st.error("A topic cannot be both weak and strong.")

        elif target_mastery < current_mastery:
            st.error("Target cannot be lower than current mastery.")

        elif not study_days:
            st.error("Select at least one study day.")

        else:

            student = {
                "name": name,
                "id": clean_id,
                "subject": subject,
                "current_mastery": current_mastery,
                "target_mastery": target_mastery,
                "mastery_gap": max(
                    target_mastery - current_mastery, 0
                ),
                "priority": classify_priority(
                    current_mastery, target_mastery
                ),
                "weak_topics": weak_topics,
                "strong_topics": strong_topics,
                "daily_minutes": daily_minutes,
                "study_days": study_days,
                "weekly_minutes": daily_minutes * len(study_days)
            }

            st.session_state["students"].append(student)

            st.success(f"{name} registered successfully!")


# ==================================
# ACADEMIC PERFORMANCE DASHBOARD
# ==================================

st.divider()
st.header("📊 Academic Performance Dashboard")

students = st.session_state["students"]

if students:

    total_students = len(students)

    average_mastery = sum(
        s["current_mastery"] for s in students
    ) / total_students

    urgent_count = sum(
        s["priority"] == "URGENT" for s in students
    )

    high_count = sum(
        s["priority"] == "HIGH" for s in students
    )

    moderate_count = sum(
        s["priority"] == "MODERATE" for s in students
    )

    achieved_count = sum(
        s["priority"] == "TARGET ACHIEVED" for s in students
    )

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Students", total_students)

    col2.metric(
        "Average Mastery",
        f"{average_mastery:.1f}%"
    )

    col3.metric("Urgent Students", urgent_count)

    col4, col5, col6 = st.columns(3)

    col4.metric("High Priority", high_count)
    col5.metric("Moderate Priority", moderate_count)
    col6.metric("Target Achieved", achieved_count)

    # Student priority table
    st.subheader("🎯 Student Priority Analysis")

    priority_data = []

    for s in students:

        priority_data.append({
            "Student": s["name"],
            "Subject": s["subject"],
            "Mastery": f"{s['current_mastery']}%",
            "Target": f"{s['target_mastery']}%",
            "Gap": f"{s['mastery_gap']}%",
            "Priority": s["priority"]
        })

    st.dataframe(
        priority_data,
        use_container_width=True,
        hide_index=True
    )

    # Visual priority distribution
    st.subheader("📈 Priority Distribution")

    priority_counts = {
        "Urgent": urgent_count,
        "High": high_count,
        "Moderate": moderate_count,
        "Target Achieved": achieved_count
    }

    st.bar_chart(priority_counts)

    # Individual student analysis
    st.subheader("🔍 Individual Student Analysis")

    for s in students:

        with st.expander(
            f"{s['name']} — {s['priority']}"
        ):

            st.write(f"Subject: {s['subject']}")

            st.metric(
                "Mastery Gap",
                f"{s['mastery_gap']} percentage points"
            )

            st.write(
                f"Current mastery: {s['current_mastery']}%"
            )

            st.write(
                f"Target mastery: {s['target_mastery']}%"
            )

            st.write(
                f"Support Priority: {s['priority']}"
            )

            st.write("Weak Topics:", ", ".join(s["weak_topics"]))

else:

    st.info(
        "No student records available. Register students "
        "to generate academic performance insights."
    )

st.divider()

st.caption(
    "AI Study Plan Generator | Academic Performance Analysis"
)

st.warning(
    "Priority classifications are rule-based screening indicators. "
    "Student records are currently held in session memory. "
    "Supabase persistence will be added in a later mission."
)

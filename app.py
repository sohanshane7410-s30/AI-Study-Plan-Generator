
import streamlit as st
import pandas as pd      


# ==========================================
# 1. APPLICATION CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="AI Study Plan Generator",
    page_icon="📚",
    layout="wide"
)


# ==========================================
# 2. SESSION STATE INITIALIZATION
# ==========================================

if "students" not in st.session_state:
    st.session_state["students"] = []

if not isinstance(st.session_state["students"], list):
    st.session_state["students"] = []


# ==========================================
# 3. HELPER FUNCTIONS
# ==========================================

def safe_int(value, default=0):
    """Safely convert a value into an integer."""

    try:
        return int(float(value))
    except (TypeError, ValueError, OverflowError):
        return default


def parse_topics(raw_text):
    """Clean topics and remove duplicate entries."""

    if not isinstance(raw_text, str):
        return []

    topics = []
    seen = set()

    for item in raw_text.split(","):

        topic = item.strip()

        if topic and topic.casefold() not in seen:
            topics.append(topic)
            seen.add(topic.casefold())

    return topics


def normalize_topics(value):
    """Support topic records from older application versions."""

    if isinstance(value, str):
        return parse_topics(value)

    if isinstance(value, (list, tuple, set)):
        return parse_topics(",".join(str(x) for x in value))

    return []


# ==========================================
# 4. PRIORITY CLASSIFICATION ENGINE
# ==========================================

def classify_priority(current, target):

    if current >= target:
        return "TARGET ACHIEVED"

    elif current < 40:
        return "URGENT"

    elif current < 60:
        return "HIGH"

    else:
        return "MODERATE"


# ==========================================
# 5. OLD STUDENT RECORD MIGRATION
# ==========================================

def migrate_student_records(records):
    """
    Upgrade older student records so that every record
    has all fields required by the current application.

    This prevents KeyErrors when the data structure changes.
    """

    upgraded_records = []

    for old_record in records:

        if not isinstance(old_record, dict):
            continue

        student = dict(old_record)

        # Identity
        student["name"] = str(
            student.get(
                "name",
                student.get("student_name", "Unknown")
            )
        )

        student["id"] = str(
            student.get(
                "id",
                student.get("student_id", "")
            )
        ).strip().upper()

        # Subject
        student["subject"] = str(
            student.get("subject") or "Not specified"
        )

        # Academic performance
        current = safe_int(
            student.get("current_mastery", 0)
        )

        target = safe_int(
            student.get("target_mastery", 80),
            80
        )

        current = max(0, min(current, 100))
        target = max(0, min(target, 100))

        student["current_mastery"] = current
        student["target_mastery"] = target

        # Always recalculate derived values.
        student["mastery_gap"] = max(
            target - current,
            0
        )

        student["priority"] = classify_priority(
            current,
            target
        )

        # Learning strengths and weaknesses
        student["weak_topics"] = normalize_topics(
            student.get("weak_topics", [])
        )

        student["strong_topics"] = normalize_topics(
            student.get("strong_topics", [])
        )

        # Study availability
        daily_minutes = safe_int(
            student.get(
                "daily_minutes",
                student.get("daily_study_minutes", 0)
            )
        )

        student["daily_minutes"] = max(
            0,
            daily_minutes
        )

        valid_days = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday"
        ]

        raw_days = student.get("study_days", [])

        if not isinstance(raw_days, list):
            raw_days = []

        student["study_days"] = [
            day for day in valid_days
            if day in raw_days
        ]

        # Always recalculate weekly capacity.
        student["weekly_minutes"] = (
            student["daily_minutes"]
            * len(student["study_days"])
        )

        upgraded_records.append(student)

    return upgraded_records


# Upgrade all existing session records.
st.session_state["students"] = migrate_student_records(
    st.session_state["students"]
)


# ==========================================
# 6. APPLICATION HEADER
# ==========================================

st.title("📚 AI Study Plan Generator")

st.caption(
    "An intelligent platform for personalized and adaptive learning."
)

st.divider()


# ==========================================
# 7. STUDENT REGISTRATION
# ==========================================

st.header("👩‍🎓 Student Registration")

st.write(
    "Register students and create their personalized academic profiles."
)

with st.form("student_registration"):

    col1, col2 = st.columns(2)

    with col1:

        student_name = st.text_input(
            "Student Name",
            placeholder="Enter student name"
        )

    with col2:

        student_id = st.text_input(
            "Student ID",
            placeholder="Enter unique student ID"
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

    col1, col2 = st.columns(2)

    with col1:

        current_mastery = st.number_input(
            "Current Mastery (%)",
            min_value=0,
            max_value=100,
            value=42,
            step=1
        )

    with col2:

        target_mastery = st.number_input(
            "Target Mastery (%)",
            min_value=0,
            max_value=100,
            value=80,
            step=1
        )

    st.subheader("🧠 Learning Strengths and Weaknesses")

    weak_input = st.text_input(
        "Weak Topics",
        placeholder="Fractions, Decimals"
    )

    strong_input = st.text_input(
        "Strong Topics",
        placeholder="Percentages, Basic arithmetic"
    )

    st.subheader("⏰ Study Availability")

    daily_minutes = st.number_input(
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

        weak_topics = parse_topics(weak_input)
        strong_topics = parse_topics(strong_input)

        # Check for overlapping topics.
        overlap = (
            {topic.casefold() for topic in weak_topics}
            &
            {topic.casefold() for topic in strong_topics}
        )

        # Check duplicate student IDs.
        existing_ids = {
            student["id"].casefold()
            for student in st.session_state["students"]
        }

        # Validate submitted information.
        if not name or not clean_id:

            st.error(
                "Please enter both student name and student ID."
            )

        elif clean_id.casefold() in existing_ids:

            st.error(
                "This student ID is already registered."
            )

        elif not weak_topics or not strong_topics:

            st.error(
                "Please enter at least one weak topic "
                "and one strong topic."
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

            st.error(
                "Please select at least one study day."
            )

        else:

            # Calculate academic metrics.
            mastery_gap = max(
                target_mastery - current_mastery,
                0
            )

            priority = classify_priority(
                current_mastery,
                target_mastery
            )

            weekly_minutes = (
                daily_minutes * len(study_days)
            )

            # Create complete student record.
            student = {

                "name": name,

                "id": clean_id,

                "subject": subject,

                "current_mastery": current_mastery,

                "target_mastery": target_mastery,

                "mastery_gap": mastery_gap,

                "priority": priority,

                "weak_topics": weak_topics,

                "strong_topics": strong_topics,

                "daily_minutes": daily_minutes,

                "study_days": study_days,

                "weekly_minutes": weekly_minutes

            }

            st.session_state["students"].append(student)

            st.success(
                f"{name} registered successfully!"
            )


# ==========================================
# 8. ACADEMIC PERFORMANCE DASHBOARD
# ==========================================

st.divider()

st.header("📊 Academic Performance Dashboard")

students = st.session_state["students"]

if students:

    total_students = len(students)

    average_mastery = sum(
        student["current_mastery"]
        for student in students
    ) / total_students

    # Count student priorities.
    urgent_count = sum(
        student["priority"] == "URGENT"
        for student in students
    )

    high_count = sum(
        student["priority"] == "HIGH"
        for student in students
    )

    moderate_count = sum(
        student["priority"] == "MODERATE"
        for student in students
    )

    achieved_count = sum(
        student["priority"] == "TARGET ACHIEVED"
        for student in students
    )

    # KPI cards.
    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Students",
        total_students
    )

    col2.metric(
        "Average Mastery",
        f"{average_mastery:.1f}%"
    )

    col3.metric(
        "Urgent Students",
        urgent_count
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "High Priority",
        high_count
    )

    col2.metric(
        "Moderate Priority",
        moderate_count
    )

    col3.metric(
        "Target Achieved",
        achieved_count
    )

    # ======================================
    # 9. STUDENT PRIORITY ANALYSIS
    # ======================================

    st.divider()

    st.subheader("🎯 Student Priority Analysis")

    priority_data = []

    for student in students:

        priority_data.append({

            "Student": student["name"],

            "Student ID": student["id"],

            "Subject": student["subject"],

            "Current Mastery": student["current_mastery"],

            "Target Mastery": student["target_mastery"],

            "Mastery Gap": student["mastery_gap"],

            "Priority": student["priority"]

        })

    priority_df = pd.DataFrame(priority_data)

    st.dataframe(
        priority_df,
        use_container_width=True,
        hide_index=True
    )

    # ======================================
    # 10. PRIORITY DISTRIBUTION
    # ======================================

    st.divider()

    st.subheader("📈 Priority Distribution")

    priority_df_chart = pd.DataFrame({

        "Priority": [
            "URGENT",
            "HIGH",
            "MODERATE",
            "TARGET ACHIEVED"
        ],

        "Students": [
            urgent_count,
            high_count,
            moderate_count,
            achieved_count
        ]

    })

    st.bar_chart(
        priority_df_chart.set_index("Priority")
    )

    # ======================================
    # 11. INDIVIDUAL STUDENT ANALYSIS
    # ======================================

    st.divider()

    st.subheader("🔍 Individual Student Analysis")

    for student in students:

        with st.expander(
            f"{student['name']} — {student['priority']}"
        ):

            st.write(
                f"**Student ID:** {student['id']}"
            )

            st.write(
                f"**Subject:** {student['subject']}"
            )

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
                f"{student['mastery_gap']} points"
            )

            st.progress(
                student["current_mastery"] / 100
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

            col1, col2 = st.columns(2)

            col1.metric(
                "Daily Study Time",
                f"{student['daily_minutes']} minutes"
            )

            col2.metric(
                "Weekly Study Time",
                f"{student['weekly_minutes'] / 60:g} hours"
            )

            if student["priority"] == "URGENT":

                st.error(
                    "Urgent academic support recommended."
                )

            elif student["priority"] == "HIGH":

                st.warning(
                    "Targeted learning support recommended."
                )

            elif student["priority"] == "MODERATE":

                st.info(
                    "Monitor progress and address remaining gaps."
                )

            else:

                st.success(
                    "The student's target mastery has been achieved."
                )

else:

    st.info(
        "No student records available. "
        "Register students to generate academic insights."
    )


# ==========================================
# 12. APPLICATION FOOTER
# ==========================================

st.divider()

st.caption(
    "AI Study Plan Generator | Academic Performance Intelligence"
)

st.warning(
    "Priority classifications are rule-based screening indicators, "
    "not complete measures of student learning needs. "
    "Student records currently exist in Streamlit session memory. "
    "Permanent cloud database storage will be implemented "
    "using Supabase."
)

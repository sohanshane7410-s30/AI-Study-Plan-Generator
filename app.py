
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
# 2. SESSION STATE
# ==========================================

if "students" not in st.session_state:
    st.session_state["students"] = []


# ==========================================
# 3. HELPER FUNCTIONS
# ==========================================

def safe_int(value, default=0):
    try:
        return int(float(value))
    except (TypeError, ValueError, OverflowError):
        return default


def parse_topics(raw_text):

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

    if isinstance(value, str):
        return parse_topics(value)

    if isinstance(value, (list, tuple, set)):
        return parse_topics(
            ", ".join(str(x) for x in value)
        )

    return []


# ==========================================
# 4. PRIORITY CLASSIFICATION
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
# 5. LEARNING GAP CLASSIFICATION
# ==========================================

def classify_gap(gap):

    if gap == 0:
        return "TARGET ACHIEVED"

    elif gap >= 30:
        return "LARGE GAP"

    elif gap >= 15:
        return "MODERATE GAP"

    else:
        return "SMALL GAP"


# ==========================================
# 6. STUDENT RISK DETECTION ENGINE
# ==========================================

def detect_learning_risk(student):

    mastery = student["current_mastery"]
    gap = student["mastery_gap"]
    weak_topics = student["weak_topics"]

    # Initial transparent screening rules.

    if mastery < 40 or gap >= 35:

        risk = "HIGH"
        explanation = (
            "Low current mastery or a substantial "
            "remaining mastery gap."
        )

    elif mastery < 60 or gap >= 20:

        risk = "MODERATE"
        explanation = (
            "The student may benefit from targeted "
            "practice and closer progress monitoring."
        )

    else:

        risk = "LOW"
        explanation = (
            "Current mastery and remaining gap "
            "indicate a lower immediate screening concern."
        )

    # Record topic-related evidence.
    if weak_topics:

        evidence = (
            f"{len(weak_topics)} identified weak topic(s)."
        )

    else:

        evidence = "No weak topics recorded."

    return {
        "risk": risk,
        "explanation": explanation,
        "evidence": evidence
    }


# ==========================================
# 7. OLD RECORD MIGRATION
# ==========================================

def migrate_student_records(records):

    upgraded_records = []

    valid_days = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ]

    for old_record in records:

        if not isinstance(old_record, dict):
            continue

        student = dict(old_record)

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

        student["subject"] = str(
            student.get("subject") or "Not specified"
        )

        current = max(
            0,
            min(
                safe_int(student.get("current_mastery")),
                100
            )
        )

        target = max(
            0,
            min(
                safe_int(student.get("target_mastery"), 80),
                100
            )
        )

        student["current_mastery"] = current
        student["target_mastery"] = target

        student["mastery_gap"] = max(
            target - current,
            0
        )

        student["priority"] = classify_priority(
            current,
            target
        )

        student["weak_topics"] = normalize_topics(
            student.get("weak_topics", [])
        )

        student["strong_topics"] = normalize_topics(
            student.get("strong_topics", [])
        )

        daily_minutes = max(
            0,
            safe_int(
                student.get(
                    "daily_minutes",
                    student.get("daily_study_minutes", 0)
                )
            )
        )

        student["daily_minutes"] = daily_minutes

        raw_days = student.get("study_days", [])

        if not isinstance(raw_days, list):
            raw_days = []

        student["study_days"] = [
            day for day in valid_days
            if day in raw_days
        ]

        student["weekly_minutes"] = (
            daily_minutes * len(student["study_days"])
        )

        upgraded_records.append(student)

    return upgraded_records


st.session_state["students"] = migrate_student_records(
    st.session_state["students"]
)


# ==========================================
# 8. APPLICATION HEADER
# ==========================================

st.title("📚 AI Study Plan Generator")

st.caption(
    "An intelligent platform for personalized and adaptive learning."
)

st.divider()


# ==========================================
# 9. STUDENT REGISTRATION
# ==========================================

st.header("👩‍🎓 Student Registration")

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
            placeholder="Enter unique ID"
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
            0,
            100,
            42
        )

    with col2:

        target_mastery = st.number_input(
            "Target Mastery (%)",
            0,
            100,
            80
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
        "Daily Study Time (minutes)",
        15,
        240,
        120,
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

        overlap = (
            {x.casefold() for x in weak_topics}
            &
            {x.casefold() for x in strong_topics}
        )

        existing_ids = {
            s["id"].casefold()
            for s in st.session_state["students"]
        }

        if not name or not clean_id:

            st.error("Student name and ID are required.")

        elif clean_id.casefold() in existing_ids:

            st.error("This student ID already exists.")

        elif not weak_topics or not strong_topics:

            st.error(
                "Enter at least one weak topic "
                "and one strong topic."
            )

        elif overlap:

            st.error(
                "A topic cannot be both weak and strong."
            )

        elif not study_days:

            st.error("Select at least one study day.")

        else:

            gap = max(
                target_mastery - current_mastery,
                0
            )

            student = {

                "name": name,
                "id": clean_id,
                "subject": subject,
                "current_mastery": current_mastery,
                "target_mastery": target_mastery,
                "mastery_gap": gap,

                "priority": classify_priority(
                    current_mastery,
                    target_mastery
                ),

                "weak_topics": weak_topics,
                "strong_topics": strong_topics,

                "daily_minutes": daily_minutes,
                "study_days": study_days,

                "weekly_minutes": (
                    daily_minutes * len(study_days)
                )

            }

            st.session_state["students"].append(student)

            st.success(
                f"{name} registered successfully!"
            )


# ==========================================
# 10. ACADEMIC PERFORMANCE DASHBOARD
# ==========================================

students = st.session_state["students"]

st.divider()

st.header("📊 Academic Performance Dashboard")

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
        s["priority"] == "TARGET ACHIEVED"
        for s in students
    )

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Students", total_students)

    col2.metric(
        "Average Mastery",
        f"{average_mastery:.1f}%"
    )

    col3.metric("Urgent Students", urgent_count)

    col1, col2, col3 = st.columns(3)

    col1.metric("High Priority", high_count)
    col2.metric("Moderate Priority", moderate_count)
    col3.metric("Target Achieved", achieved_count)

    # Priority table
    st.subheader("🎯 Student Priority Analysis")

    priority_data = []

    for s in students:

        priority_data.append({
            "Student": s["name"],
            "ID": s["id"],
            "Subject": s["subject"],
            "Mastery": s["current_mastery"],
            "Target": s["target_mastery"],
            "Gap": s["mastery_gap"],
            "Priority": s["priority"]
        })

    priority_df = pd.DataFrame(priority_data)

    st.dataframe(
        priority_df,
        use_container_width=True,
        hide_index=True
    )

    st.subheader("📈 Priority Distribution")

    priority_chart = pd.DataFrame({
        "Students": [
            urgent_count,
            high_count,
            moderate_count,
            achieved_count
        ]
    }, index=[
        "Urgent",
        "High",
        "Moderate",
        "Target Achieved"
    ])

    st.bar_chart(priority_chart)


    # ======================================
    # 11. LEARNING GAP ANALYSIS
    # ======================================

    st.divider()

    st.header("🧠 Learning Gap Analysis")

    gap_analysis = []

    for student in students:

        current = student["current_mastery"]
        target = student["target_mastery"]

        gap = max(target - current, 0)

        if target == 0:
            target_progress = 100
        else:
            target_progress = min(
                current / target * 100,
                100
            )

        gap_analysis.append({

            "Student": student["name"],

            "Current Mastery": current,

            "Target Mastery": target,

            "Mastery Gap": gap,

            "Target Progress (%)": round(
                target_progress,
                1
            ),

            "Gap Classification": classify_gap(gap)

        })

    gap_df = pd.DataFrame(gap_analysis)

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Average Gap",
        f"{gap_df['Mastery Gap'].mean():.1f} points"
    )

    col2.metric(
        "Largest Gap",
        f"{gap_df['Mastery Gap'].max()} points"
    )

    col3.metric(
        "Large Gaps",
        int(
            (gap_df["Gap Classification"] == "LARGE GAP").sum()
        )
    )

    st.subheader("Individual Learning Gap Report")

    st.dataframe(
        gap_df.sort_values(
            "Mastery Gap",
            ascending=False
        ),
        use_container_width=True,
        hide_index=True
    )

    st.subheader("Mastery Comparison")

    mastery_chart = gap_df.set_index("Student")[
        ["Current Mastery", "Target Mastery"]
    ]

    st.bar_chart(mastery_chart)


    # ======================================
    # 12. STUDENT LEARNING RISK DETECTION
    # ======================================

    st.divider()

    st.header("🚨 Student Learning Risk Detection")

    risk_analysis = []

    for student in students:

        result = detect_learning_risk(student)

        risk_analysis.append({

            "Student": student["name"],

            "Current Mastery": student["current_mastery"],

            "Mastery Gap": student["mastery_gap"],

            "Risk Level": result["risk"],

            "Explanation": result["explanation"],

            "Evidence": result["evidence"]

        })

    risk_df = pd.DataFrame(risk_analysis)

    high_risk_count = sum(
        result["Risk Level"] == "HIGH"
        for result in risk_analysis
    )

    moderate_risk_count = sum(
        result["Risk Level"] == "MODERATE"
        for result in risk_analysis
    )

    low_risk_count = sum(
        result["Risk Level"] == "LOW"
        for result in risk_analysis
    )

    col1, col2, col3 = st.columns(3)

    col1.metric("High Risk", high_risk_count)

    col2.metric("Moderate Risk", moderate_risk_count)

    col3.metric("Low Risk", low_risk_count)

    st.subheader("Student Risk Report")

    st.dataframe(
        risk_df,
        use_container_width=True,
        hide_index=True
    )

    st.subheader("Risk Distribution")

    risk_chart = pd.DataFrame({
        "Students": [
            high_risk_count,
            moderate_risk_count,
            low_risk_count
        ]
    }, index=[
        "High Risk",
        "Moderate Risk",
        "Low Risk"
    ])

    st.bar_chart(risk_chart)

    st.subheader("Risk Investigation")

    for result in risk_analysis:

        with st.expander(
            f"{result['Student']} — {result['Risk Level']} RISK"
        ):

            st.write(
                "**Reason:**",
                result["Explanation"]
            )

            st.write(
                "**Supporting information:**",
                result["Evidence"]
            )

            st.write(
                f"**Mastery gap:** {result['Mastery Gap']} points"
            )

            st.info(
                "This is an initial rules-based screening result. "
                "Assessment history, topic-level accuracy, "
                "learning trends and student context are needed "
                "for a more complete risk assessment."
            )


    # ======================================
    # 13. INDIVIDUAL STUDENT PROFILES
    # ======================================

    st.divider()

    st.header("🔍 Individual Student Profiles")

    for student in students:

        with st.expander(
            f"{student['name']} — {student['id']}"
        ):

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

            st.write("**Subject:**", student["subject"])

            st.write(
                "**Priority:**",
                student["priority"]
            )

            st.write("**Weak Topics:**")

            for topic in student["weak_topics"]:
                st.write(f"🔴 {topic}")

            st.write("**Strong Topics:**")

            for topic in student["strong_topics"]:
                st.write(f"🟢 {topic}")

            st.write("**Study Days:**")

            st.write(", ".join(student["study_days"]))

            st.metric(
                "Weekly Study Capacity",
                f"{student['weekly_minutes'] / 60:g} hours"
            )

else:

    st.info(
        "No students registered yet. "
        "Register students to generate academic insights."
    )


# ==========================================
# 14. FOOTER
# ==========================================

st.divider()

st.caption(
    "AI Study Plan Generator | Academic Intelligence Platform"
)

st.warning(
    "Student information is held in temporary Streamlit "
    "session memory. Supabase database integration will "
    "be implemented in a later mission."
)

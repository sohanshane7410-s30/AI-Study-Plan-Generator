
import streamlit as st
import pandas as pd
from datetime import date


# =========================================================
# 1. APPLICATION CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Learning Intelligence Studio",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# 2. PREMIUM DESIGN SYSTEM
# =========================================================

st.markdown("""
<style>

.stApp {
    background: #F5F6FC;
    color: #19213C;
}

.block-container {
    max-width: 1500px;
    padding-top: 1.8rem;
    padding-bottom: 3rem;
}

[data-testid="stSidebar"] {
    background: #111A35;
    border-right: 1px solid #29345A;
}

[data-testid="stSidebar"] * {
    color: #E9EDFF;
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    color: #AEB9DB;
}

h1 {
    color: #1A2240 !important;
    font-weight: 800 !important;
    letter-spacing: -1.5px;
}

h2 {
    color: #263252 !important;
    font-weight: 750 !important;
}

h3 {
    color: #384568 !important;
    font-weight: 700 !important;
}

.learning-hero {
    background: linear-gradient(
        115deg,
        #111A35 0%,
        #292C68 55%,
        #6653D6 100%
    );
    padding: 38px;
    border-radius: 22px;
    margin-bottom: 28px;
    box-shadow: 0 14px 35px rgba(30, 35, 92, 0.15);
}

.learning-hero .eyebrow {
    color: #BEB4FF;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 2px;
    text-transform: uppercase;
}

.learning-hero h1 {
    color: white !important;
    font-size: 36px !important;
    margin-top: 12px;
    margin-bottom: 10px;
}

.learning-hero p {
    color: #D8DDF5;
    font-size: 15px;
    max-width: 750px;
}

.learning-hero .hero-status {
    color: #82E4C4;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1px;
}

[data-testid="stMetric"] {
    background: #FFFFFF;
    padding: 20px;
    border: 1px solid #E8EAF3;
    border-radius: 17px;
    box-shadow: 0 5px 18px rgba(24, 34, 70, 0.045);
}

[data-testid="stMetricLabel"] {
    color: #75809B !important;
    font-weight: 600;
}

[data-testid="stMetricValue"] {
    color: #6250D5 !important;
    font-weight: 800;
}

[data-testid="stForm"] {
    background: white;
    padding: 24px;
    border-radius: 18px;
    border: 1px solid #E5E8F1;
    box-shadow: 0 5px 18px rgba(24, 34, 70, 0.04);
}

.stButton > button,
.stFormSubmitButton > button,
.stDownloadButton > button {
    background: linear-gradient(110deg, #6654D6, #8069E8);
    color: white;
    border: none;
    border-radius: 11px;
    min-height: 42px;
    font-weight: 700;
    transition: 0.2s ease;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover,
.stDownloadButton > button:hover {
    background: #5040B9;
    color: white;
    border: none;
    transform: translateY(-1px);
}

.stTextInput input,
.stNumberInput input,
.stTextArea textarea {
    background: white;
    border-radius: 10px;
    border: 1px solid #DCE1EF;
}

[data-testid="stSelectbox"] [data-baseweb="select"] {
    border-radius: 10px;
}

[data-testid="stExpander"] {
    background: white;
    border: 1px solid #E5E8F1;
    border-radius: 13px;
    margin-bottom: 10px;
}

[data-testid="stDataFrame"] {
    border: 1px solid #E5E8F1;
    border-radius: 12px;
}

[data-testid="stAlert"] {
    border-radius: 12px;
}

hr {
    border-color: #E7E9F1 !important;
}

.stProgress > div > div > div {
    background: linear-gradient(90deg, #6553D9, #4CC8A5);
}

.sidebar-brand {
    padding: 18px 12px 24px 12px;
    border-bottom: 1px solid #303B5E;
    margin-bottom: 15px;
}

.sidebar-brand .logo {
    font-size: 28px;
}

.sidebar-brand .name {
    color: white;
    font-size: 18px;
    font-weight: 800;
}

.sidebar-brand .sub {
    color: #AAB6DC;
    font-size: 11px;
    letter-spacing: 1.3px;
}

.section-label {
    color: #7665D9;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1.5px;
    margin-bottom: 7px;
}

.info-card {
    background: white;
    border: 1px solid #E6E9F2;
    border-radius: 16px;
    padding: 21px;
    margin-bottom: 12px;
}

.info-card .card-label {
    color: #76809A;
    font-size: 12px;
    font-weight: 700;
}

.info-card .card-value {
    color: #242F52;
    font-size: 26px;
    font-weight: 800;
}

.info-card .card-description {
    color: #8290AA;
    font-size: 12px;
}

.small-footer {
    color: #8992A8;
    font-size: 11px;
    text-align: center;
    padding: 20px;
}

footer {
    visibility: hidden;
}

#MainMenu {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# 3. SESSION STATE
# =========================================================

if "students" not in st.session_state:
    st.session_state.students = []

if "plans" not in st.session_state:
    st.session_state.plans = {}

if "navigation" not in st.session_state:
    st.session_state.navigation = "Dashboard"


# =========================================================
# 4. HELPER FUNCTIONS
# =========================================================

def safe_int(value, default=0):

    try:
        return int(float(value))

    except (TypeError, ValueError, OverflowError):
        return default


def parse_topics(raw_text):

    topics = []
    seen = set()

    for item in raw_text.split(","):

        topic = item.strip()

        if topic and topic.casefold() not in seen:

            topics.append(topic)
            seen.add(topic.casefold())

    return topics


def parse_topic_scores(raw_text):

    scores = {}
    errors = []
    seen = set()

    for item in raw_text.split(","):

        item = item.strip()

        if not item:
            continue

        if ":" not in item:

            errors.append(
                f"Invalid topic format: {item}"
            )

            continue

        topic, raw_score = item.split(":", 1)

        topic = topic.strip()

        if not topic:

            errors.append("Topic name cannot be empty.")
            continue

        try:
            score = float(raw_score.strip())

        except ValueError:

            errors.append(
                f"Invalid score for {topic}."
            )

            continue

        if not 0 <= score <= 100:

            errors.append(
                f"{topic} score must be between 0 and 100."
            )

            continue

        if topic.casefold() in seen:

            errors.append(
                f"Duplicate topic score: {topic}."
            )

            continue

        scores[topic] = round(score, 1)
        seen.add(topic.casefold())

    return scores, errors


def parse_history(raw_text):

    history = []
    errors = []

    for item in raw_text.split(","):

        item = item.strip()

        if not item:
            continue

        try:
            score = float(item)

        except ValueError:

            errors.append(
                f"Invalid assessment score: {item}"
            )

            continue

        if not 0 <= score <= 100:

            errors.append(
                f"Assessment score {score} must be between 0 and 100."
            )

            continue

        history.append(round(score, 1))

    return history, errors


# =========================================================
# 5. ACADEMIC INTELLIGENCE FUNCTIONS
# =========================================================

def classify_priority(current, target):

    if current >= target:
        return "TARGET ACHIEVED"

    if current < 40:
        return "URGENT"

    if current < 60:
        return "HIGH"

    return "MODERATE"


def classify_gap(gap):

    if gap == 0:
        return "TARGET ACHIEVED"

    if gap >= 30:
        return "LARGE GAP"

    if gap >= 15:
        return "MODERATE GAP"

    return "SMALL GAP"


def classify_topic_score(score):

    if score < 60:
        return "NEEDS SUPPORT"

    if score < 80:
        return "DEVELOPING"

    return "STRONG"


def detect_learning_risk(student):

    mastery = student["current_mastery"]
    gap = student["mastery_gap"]

    if mastery < 40 or gap >= 35:

        return {
            "risk": "HIGH",
            "reason": "Low mastery or substantial mastery gap."
        }

    if mastery < 60 or gap >= 20:

        return {
            "risk": "MODERATE",
            "reason": "Targeted learning support may be beneficial."
        }

    return {
        "risk": "LOW",
        "reason": "Lower immediate screening concern."
    }


def detect_learning_trend(history):

    if len(history) < 2:

        return {
            "trend": "INSUFFICIENT DATA",
            "change": None,
            "reason": "At least two assessments are required."
        }

    change = round(history[-1] - history[0], 1)

    if change >= 5:

        return {
            "trend": "IMPROVING",
            "change": change,
            "reason": f"Performance increased by {change} points."
        }

    if change <= -5:

        return {
            "trend": "DECLINING",
            "change": change,
            "reason": f"Performance decreased by {abs(change)} points."
        }

    return {
        "trend": "STABLE",
        "change": change,
        "reason": "Net change is less than 5 points."
    }


def calculate_intervention_priority(student):

    current = student["current_mastery"]
    target = student["target_mastery"]

    gap = student["mastery_gap"]

    if current >= target:

        return {
            "score": 0,
            "priority": "P4 - MONITOR",
            "gap_points": 0,
            "mastery_points": 0,
            "trend_points": 0,
            "topic_points": 0,
            "recommendation": "Target achieved. Consider enrichment."
        }

    gap_points = min(gap, 40)

    if current < 40:
        mastery_points = 20

    elif current < 60:
        mastery_points = 15

    elif current < 80:
        mastery_points = 8

    else:
        mastery_points = 0

    trend = detect_learning_trend(
        student["assessment_history"]
    )

    if trend["trend"] == "DECLINING":
        trend_points = 20

    elif trend["trend"] == "STABLE":
        trend_points = 10

    elif trend["trend"] == "INSUFFICIENT DATA":
        trend_points = 8

    else:
        trend_points = 0

    support_count = sum(
        classify_topic_score(score) == "NEEDS SUPPORT"
        for score in student["topic_scores"].values()
    )

    topic_points = min(support_count * 5, 15)

    total = (
        gap_points
        + mastery_points
        + trend_points
        + topic_points
    )

    if total >= 65:

        priority = "P1 - URGENT"

        recommendation = (
            "Prompt teacher investigation and individualized support."
        )

    elif total >= 45:

        priority = "P2 - HIGH"

        recommendation = (
            "Schedule targeted topic practice and reassessment."
        )

    elif total >= 25:

        priority = "P3 - SCHEDULED"

        recommendation = (
            "Schedule focused learning support and monitor progress."
        )

    else:

        priority = "P4 - MONITOR"

        recommendation = (
            "Continue routine monitoring and practice."
        )

    return {
        "score": total,
        "priority": priority,
        "gap_points": gap_points,
        "mastery_points": mastery_points,
        "trend_points": trend_points,
        "topic_points": topic_points,
        "recommendation": recommendation
    }


def classify_student_segment(student):

    risk = detect_learning_risk(student)
    trend = detect_learning_trend(
        student["assessment_history"]
    )

    current = student["current_mastery"]
    target = student["target_mastery"]

    support_topics = sum(
        classify_topic_score(score) == "NEEDS SUPPORT"
        for score in student["topic_scores"].values()
    )

    if current >= target:

        return {
            "segment": "ENRICHMENT",
            "reason": "Target achieved."
        }

    if risk["risk"] == "HIGH":

        return {
            "segment": "INTENSIVE SUPPORT",
            "reason": "Substantial mastery gap or low mastery."
        }

    if (
        risk["risk"] == "MODERATE"
        or trend["trend"] == "DECLINING"
        or support_topics >= 2
    ):

        return {
            "segment": "TARGETED SUPPORT",
            "reason": "Multiple learning indicators need investigation."
        }

    return {
        "segment": "PROGRESS MONITORING",
        "reason": "Continue routine progress monitoring."
    }


# =========================================================
# 6. DATA MIGRATION
# =========================================================

def migrate_students(records):

    upgraded = []

    valid_days = [
        "Monday", "Tuesday", "Wednesday",
        "Thursday", "Friday", "Saturday", "Sunday"
    ]

    for old in records:

        if not isinstance(old, dict):
            continue

        student = dict(old)

        student["name"] = str(
            student.get("name", "Unknown")
        )

        student["id"] = str(
            student.get(
                "id",
                student.get("student_id", "")
            )
        ).strip().upper()

        student["subject"] = str(
            student.get("subject", "Mathematics")
        )

        current = max(
            0,
            min(safe_int(student.get("current_mastery")), 100)
        )

        target = max(
            0,
            min(safe_int(student.get("target_mastery"), 80), 100)
        )

        student["current_mastery"] = current
        student["target_mastery"] = target

        student["mastery_gap"] = max(
            target - current, 0
        )

        student["priority"] = classify_priority(
            current, target
        )

        for field in ["weak_topics", "strong_topics"]:

            value = student.get(field, [])

            if isinstance(value, str):
                value = parse_topics(value)

            if not isinstance(value, list):
                value = []

            student[field] = value

        old_scores = student.get("topic_scores", {})

        if not isinstance(old_scores, dict):
            old_scores = {}

        valid_scores = {}

        for topic, score in old_scores.items():

            try:
                score = float(score)

                if 0 <= score <= 100:
                    valid_scores[str(topic)] = score

            except (TypeError, ValueError):
                continue

        student["topic_scores"] = valid_scores

        history = student.get("assessment_history", [])

        if not isinstance(history, list):
            history = []

        clean_history = []

        for score in history:

            try:
                score = float(score)

                if 0 <= score <= 100:
                    clean_history.append(score)

            except (TypeError, ValueError):
                continue

        if not clean_history:
            clean_history = [current]

        student["assessment_history"] = clean_history

        student["assessment_records"] = student.get(
            "assessment_records", []
        )

        if not isinstance(student["assessment_records"], list):
            student["assessment_records"] = []

        student["daily_minutes"] = max(
            0,
            safe_int(
                student.get(
                    "daily_minutes",
                    student.get("daily_study_minutes", 120)
                ),
                120
            )
        )

        old_days = student.get("study_days", [])

        if not isinstance(old_days, list):
            old_days = []

        student["study_days"] = [
            day for day in valid_days
            if day in old_days
        ]

        if not student["study_days"]:
            student["study_days"] = [
                "Monday", "Tuesday", "Wednesday",
                "Thursday", "Friday"
            ]

        student["weekly_minutes"] = (
            student["daily_minutes"]
            * len(student["study_days"])
        )

        upgraded.append(student)

    return upgraded


st.session_state.students = migrate_students(
    st.session_state.students
)


# =========================================================
# 7. REPORT GENERATION
# =========================================================

def build_student_report(student):

    risk = detect_learning_risk(student)

    trend = detect_learning_trend(
        student["assessment_history"]
    )

    segment = classify_student_segment(student)

    intervention = calculate_intervention_priority(student)

    current = student["current_mastery"]
    target = student["target_mastery"]

    target_progress = (
        min(current / target * 100, 100)
        if target > 0 else 100
    )

    recommendations = []

    if current >= target:

        recommendations.append(
            "Maintain mastery with periodic reassessment and enrichment."
        )

    else:

        weak_topics = sorted(
            student["topic_scores"].items(),
            key=lambda item: item[1]
        )

        for topic, score in weak_topics:

            if score < 60:

                recommendations.append(
                    f"Provide focused practice in {topic} ({score}%)."
                )

        if trend["trend"] == "DECLINING":

            recommendations.append(
                "Investigate causes of declining performance."
            )

        elif trend["trend"] == "IMPROVING":

            recommendations.append(
                "Reinforce learning strategies associated with improvement."
            )

        recommendations.append(
            intervention["recommendation"]
        )

    if not recommendations:

        recommendations.append(
            "Collect additional diagnostic evidence."
        )

    lines = [

        "LEARNING INTELLIGENCE STUDIO",
        "STUDENT ACADEMIC PERFORMANCE REPORT",
        "=" * 55,

        "",

        "STUDENT INFORMATION",
        f"Name: {student['name']}",
        f"Student ID: {student['id']}",
        f"Subject: {student['subject']}",

        "",

        "ACADEMIC PERFORMANCE",
        f"Current Mastery: {current}%",
        f"Target Mastery: {target}%",
        f"Mastery Gap: {student['mastery_gap']} points",
        f"Progress Toward Target: {target_progress:.1f}%",

        "",

        "LEARNING RISK",
        f"Risk Level: {risk['risk']}",
        f"Reason: {risk['reason']}",

        "",

        "TOPIC PERFORMANCE"

    ]

    for topic, score in student["topic_scores"].items():

        lines.append(
            f"{topic}: {score}% - {classify_topic_score(score)}"
        )

    lines.extend([

        "",
        "LEARNING TREND",
        f"Trend: {trend['trend']}",
        f"Explanation: {trend['reason']}",

        "",
        "STUDENT SEGMENTATION",
        f"Segment: {segment['segment']}",
        f"Reason: {segment['reason']}",

        "",
        "INTERVENTION PRIORITIZATION",
        f"Score: {intervention['score']} / 95",
        f"Priority: {intervention['priority']}",

        f"Gap Points: {intervention['gap_points']}/40",
        f"Mastery Points: {intervention['mastery_points']}/20",
        f"Trend Points: {intervention['trend_points']}/20",
        f"Topic Points: {intervention['topic_points']}/15",

        "",
        "RECOMMENDED ACTIONS"

    ])

    for i, item in enumerate(recommendations, 1):
        lines.append(f"{i}. {item}")

    lines.extend([

        "",
        "STUDY AVAILABILITY",
        f"Daily minutes: {student['daily_minutes']}",
        f"Available days: {', '.join(student['study_days'])}",
        f"Weekly hours: {student['weekly_minutes'] / 60:g}",

        "",
        "LIMITATIONS",
        "This is a rule-based academic report.",
        "Thresholds are initial project screening rules.",
        "Assessment history and topic data may be incomplete.",
        "Teacher judgment is required before intervention.",

        "",
        "=" * 55,
        "END OF REPORT"

    ])

    return "\n".join(lines)


# =========================================================
# 8. STUDY PLAN GENERATOR
# =========================================================

def generate_study_plan(student):

    daily_minutes = student["daily_minutes"]

    topic_scores = student["topic_scores"]

    candidates = []

    for topic in student["weak_topics"]:

        score = topic_scores.get(topic, 50)

        if score < 80:
            candidates.append((topic, score))

    # Also include low-scoring topics even if not declared weak.
    known_names = {
        topic.casefold()
        for topic, score in candidates
    }

    for topic, score in topic_scores.items():

        if (
            score < 80
            and topic.casefold() not in known_names
        ):

            candidates.append((topic, score))

    candidates.sort(key=lambda item: item[1])

    if not candidates:
        candidates = [
            ("Mixed practice and enrichment", 80)
        ]

    focus_minutes = int(daily_minutes * 0.4)
    practice_minutes = int(daily_minutes * 0.4)
    assessment_minutes = (
        daily_minutes - focus_minutes - practice_minutes
    )

    schedule = []

    for index, day in enumerate(student["study_days"]):

        topic, score = candidates[index % len(candidates)]

        schedule.append({

            "Day": day,
            "Focus Topic": topic,
            "Current Topic Score": score,
            "Concept Review": focus_minutes,
            "Guided Practice": practice_minutes,
            "Quick Assessment": assessment_minutes,
            "Total Minutes": daily_minutes

        })

    return schedule


# =========================================================
# 9. REUSABLE VISUAL COMPONENTS
# =========================================================

def render_hero(eyebrow, title, subtitle):

    st.markdown(f"""
    <div class="learning-hero">

        <div class="eyebrow">{eyebrow}</div>

        <h1>{title}</h1>

        <p>{subtitle}</p>

        <div class="hero-status">
            ● LEARNING INTELLIGENCE STUDIO
        </div>

    </div>
    """, unsafe_allow_html=True)


def render_section(label, heading):

    st.markdown(
        f'<div class="section-label">{label}</div>',
        unsafe_allow_html=True
    )

    st.subheader(heading)


# =========================================================
# 10. SIDEBAR NAVIGATION
# =========================================================

with st.sidebar:

    st.markdown("""
    <div class="sidebar-brand">

        <div class="logo">🎓</div>

        <div class="name">Learning Studio</div>

        <div class="sub">INTELLIGENCE PLATFORM</div>

    </div>
    """, unsafe_allow_html=True)

    st.caption("WORKSPACE")

    page = st.radio(
        "Navigation",
        [
            "Dashboard",
            "Students",
            "AI Insights",
            "Study Planner",
            "Progress Tracker",
            "Reports"
        ],
        key="navigation",
        label_visibility="collapsed"
    )

    st.divider()

    st.caption("PLATFORM STATUS")

    st.success("Application running")

    st.caption(
        f"{len(st.session_state.students)} students in this session"
    )

    st.divider()

    st.caption("VERSION 1.0")

    st.caption("Built with Streamlit and Python")


students = st.session_state.students


# =========================================================
# 11. DASHBOARD PAGE
# =========================================================

if page == "Dashboard":

    render_hero(
        "YOUR LEARNING INTELLIGENCE PLATFORM",
        "Understand. Improve. Master.",
        "Discover learning gaps, investigate student performance, "
        "and build personalized learning journeys."
    )

    render_section(
        "OVERVIEW",
        "Academic Command Center"
    )

    if students:

        total = len(students)

        average = sum(
            s["current_mastery"] for s in students
        ) / total

        high_risk = sum(
            detect_learning_risk(s)["risk"] == "HIGH"
            for s in students
        )

        achieved = sum(
            s["current_mastery"] >= s["target_mastery"]
            for s in students
        )

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Students Tracked", total)
        c2.metric("Average Mastery", f"{average:.1f}%")
        c3.metric("High Screening Risk", high_risk)
        c4.metric("Targets Achieved", achieved)

        st.divider()

        left, right = st.columns([1.5, 1])

        with left:

            render_section(
                "PERFORMANCE",
                "Student Mastery Overview"
            )

            mastery_df = pd.DataFrame([
                {
                    "Student": s["name"],
                    "Current Mastery": s["current_mastery"],
                    "Target Mastery": s["target_mastery"]
                }
                for s in students
            ])

            mastery_df = mastery_df.set_index("Student")

            st.bar_chart(mastery_df)

        with right:

            render_section(
                "PRIORITIES",
                "Learning Support Distribution"
            )

            priority_counts = {

                "Urgent": sum(
                    s["priority"] == "URGENT"
                    for s in students
                ),

                "High": sum(
                    s["priority"] == "HIGH"
                    for s in students
                ),

                "Moderate": sum(
                    s["priority"] == "MODERATE"
                    for s in students
                ),

                "Achieved": sum(
                    s["priority"] == "TARGET ACHIEVED"
                    for s in students
                )

            }

            st.bar_chart(
                pd.DataFrame({
                    "Students": list(priority_counts.values())
                }, index=list(priority_counts.keys()))
            )

        st.divider()

        render_section(
            "ATTENTION REQUIRED",
            "Intervention Queue"
        )

        queue = []

        for s in students:

            result = calculate_intervention_priority(s)

            queue.append({

                "Student": s["name"],
                "Mastery": s["current_mastery"],
                "Gap": s["mastery_gap"],
                "Intervention Score": result["score"],
                "Priority": result["priority"]

            })

        queue_df = pd.DataFrame(queue).sort_values(
            "Intervention Score",
            ascending=False
        )

        st.dataframe(
            queue_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No student records yet. Visit the Students page "
            "to register your first student."
        )

        if st.button("Go to Student Registration"):
            st.session_state.navigation = "Students"
            st.rerun()


# =========================================================
# 12. STUDENTS PAGE
# =========================================================

elif page == "Students":

    render_hero(
        "STUDENT MANAGEMENT",
        "Meet your learners.",
        "Register students, understand their academic profiles, "
        "and explore their individual learning needs."
    )

    render_section(
        "STUDENT DATABASE",
        "Register a New Student"
    )

    with st.form("new_student_form"):

        c1, c2 = st.columns(2)

        with c1:

            name = st.text_input(
                "Student Name",
                placeholder="Sophia"
            )

        with c2:

            student_id = st.text_input(
                "Student ID",
                placeholder="STU101"
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

        st.markdown("#### Academic Mastery")

        c1, c2 = st.columns(2)

        with c1:

            current = st.number_input(
                "Current Mastery (%)",
                0, 100, 42
            )

        with c2:

            target = st.number_input(
                "Target Mastery (%)",
                0, 100, 80
            )

        st.markdown("#### Learning Profile")

        weak_input = st.text_input(
            "Weak Topics",
            placeholder="Fractions, Decimals"
        )

        strong_input = st.text_input(
            "Strong Topics",
            placeholder="Percentages, Basic arithmetic"
        )

        topic_input = st.text_area(
            "Topic Assessment Scores",
            placeholder=(
                "Fractions: 35, Decimals: 45, "
                "Percentages: 85, Basic arithmetic: 90"
            )
        )

        history_input = st.text_input(
            "Assessment History (oldest to newest)",
            placeholder="30, 36, 42",
            help="Optional. If entered, the latest score must match current mastery."
        )

        st.markdown("#### Study Availability")

        daily = st.number_input(
            "Daily Study Minutes",
            15, 240, 120, step=15
        )

        days = st.multiselect(
            "Study Days",
            [
                "Monday", "Tuesday", "Wednesday",
                "Thursday", "Friday", "Saturday", "Sunday"
            ],
            default=[
                "Monday", "Tuesday", "Wednesday",
                "Thursday", "Friday"
            ]
        )

        submitted = st.form_submit_button(
            "＋ Register Student",
            use_container_width=True
        )

        if submitted:

            clean_name = name.strip()
            clean_id = student_id.strip().upper()

            weak = parse_topics(weak_input)
            strong = parse_topics(strong_input)

            topic_scores, score_errors = parse_topic_scores(
                topic_input
            )

            history, history_errors = parse_history(
                history_input
            )

            overlap = (
                {x.casefold() for x in weak}
                &
                {x.casefold() for x in strong}
            )

            existing_ids = {
                s["id"].casefold()
                for s in students
            }

            if not clean_name or not clean_id:

                st.error("Student name and ID are required.")

            elif clean_id.casefold() in existing_ids:

                st.error("This student ID is already registered.")

            elif target < current:

                st.error(
                    "Target mastery cannot be lower than current mastery."
                )

            elif overlap:

                st.error(
                    "A topic cannot be both weak and strong."
                )

            elif score_errors:

                for error in score_errors:
                    st.error(error)

            elif history_errors:

                for error in history_errors:
                    st.error(error)

            elif history and abs(history[-1] - current) > 0.01:

                st.error(
                    "The latest assessment score must match current mastery."
                )

            elif not days:

                st.error("Please select at least one study day.")

            else:

                if not history:
                    history = [float(current)]

                new_student = {

                    "name": clean_name,
                    "id": clean_id,
                    "subject": subject,

                    "current_mastery": current,
                    "target_mastery": target,

                    "mastery_gap": max(target - current, 0),

                    "priority": classify_priority(current, target),

                    "weak_topics": weak,
                    "strong_topics": strong,

                    "topic_scores": topic_scores,

                    "assessment_history": history,
                    "assessment_records": [],

                    "daily_minutes": daily,
                    "study_days": days,

                    "weekly_minutes": daily * len(days)

                }

                st.session_state.students.append(
                    new_student
                )

                st.success(
                    f"{clean_name} registered successfully!"
                )

    st.divider()

    render_section(
        "LEARNER DIRECTORY",
        "Registered Students"
    )

    if students:

        st.metric(
            "Total Registered Students",
            len(students)
        )

        for s in students:

            with st.expander(
                f"🎓 {s['name']} — {s['id']}"
            ):

                c1, c2, c3 = st.columns(3)

                c1.metric(
                    "Current Mastery",
                    f"{s['current_mastery']}%"
                )

                c2.metric(
                    "Target Mastery",
                    f"{s['target_mastery']}%"
                )

                c3.metric(
                    "Mastery Gap",
                    f"{s['mastery_gap']} points"
                )

                st.progress(
                    min(
                        s["current_mastery"] / 100,
                        1.0
                    )
                )

                st.write("**Subject:**", s["subject"])

                st.write(
                    "**Weak Topics:**",
                    ", ".join(s["weak_topics"]) or "Not recorded"
                )

                st.write(
                    "**Strong Topics:**",
                    ", ".join(s["strong_topics"]) or "Not recorded"
                )

                st.write(
                    "**Study Availability:**",
                    ", ".join(s["study_days"])
                )

                st.write(
                    "**Weekly Capacity:**",
                    f"{s['weekly_minutes'] / 60:g} hours"
                )

    else:

        st.info(
            "Your student directory is empty. "
            "Register your first learner above."
        )


# =========================================================
# 13. AI INSIGHTS PAGE
# =========================================================

elif page == "AI Insights":

    render_hero(
        "ACADEMIC INTELLIGENCE",
        "See beyond the scores.",
        "Discover learning gaps, identify concerning trends, "
        "and understand which students need investigation."
    )

    render_section(
        "LEARNING ANALYTICS",
        "Student Intelligence Report"
    )

    if students:

        insight_rows = []

        for s in students:

            risk = detect_learning_risk(s)
            trend = detect_learning_trend(
                s["assessment_history"]
            )
            segment = classify_student_segment(s)
            intervention = calculate_intervention_priority(s)

            insight_rows.append({

                "Student": s["name"],
                "Mastery": s["current_mastery"],
                "Gap": s["mastery_gap"],
                "Risk": risk["risk"],
                "Trend": trend["trend"],
                "Segment": segment["segment"],
                "Intervention Score": intervention["score"],
                "Priority": intervention["priority"]

            })

        insights_df = pd.DataFrame(insight_rows)

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "High Risk",
            sum(x["Risk"] == "HIGH" for x in insight_rows)
        )

        c2.metric(
            "Declining",
            sum(x["Trend"] == "DECLINING" for x in insight_rows)
        )

        c3.metric(
            "Intensive Support",
            sum(
                x["Segment"] == "INTENSIVE SUPPORT"
                for x in insight_rows
            )
        )

        st.subheader("Student Intelligence Matrix")

        st.dataframe(
            insights_df.sort_values(
                "Intervention Score",
                ascending=False
            ),
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        render_section(
            "TOPIC INTELLIGENCE",
            "Topics Requiring Attention"
        )

        topic_rows = []

        for s in students:

            for topic, score in s["topic_scores"].items():

                topic_rows.append({

                    "Student": s["name"],
                    "Topic": topic,
                    "Score": score,
                    "Status": classify_topic_score(score)

                })

        if topic_rows:

            topic_df = pd.DataFrame(topic_rows)

            st.dataframe(
                topic_df.sort_values(
                    "Score",
                    ascending=True
                ),
                use_container_width=True,
                hide_index=True
            )

            st.bar_chart(
                topic_df.set_index(
                    ["Student", "Topic"]
                )[["Score"]]
            )

        else:

            st.info("No topic assessment scores available.")

        st.info(
            "These are transparent, rule-based insights. "
            "They are not validated predictive models. "
            "A teacher should review the evidence before "
            "deciding on an intervention."
        )

    else:

        st.info(
            "Register students to unlock learning intelligence."
        )


# =========================================================
# 14. STUDY PLANNER PAGE
# =========================================================

elif page == "Study Planner":

    render_hero(
        "PERSONALIZED LEARNING",
        "Every minute has a purpose.",
        "Create a practical weekly learning schedule around "
        "each student's topics, availability and assessment needs."
    )

    render_section(
        "STUDY PLANNING",
        "Personalized Weekly Study Planner"
    )

    if students:

        selected_id = st.selectbox(
            "Choose a Student",
            [s["id"] for s in students],
            format_func=lambda sid: next(
                f"{s['name']} ({s['id']})"
                for s in students
                if s["id"] == sid
            )
        )

        student = next(
            s for s in students
            if s["id"] == selected_id
        )

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Daily Available Time",
            f"{student['daily_minutes']} min"
        )

        c2.metric(
            "Available Days",
            len(student["study_days"])
        )

        c3.metric(
            "Weekly Capacity",
            f"{student['weekly_minutes'] / 60:g} hrs"
        )

        st.write(
            "**Current weak topics:**",
            ", ".join(student["weak_topics"]) or "No weak topics recorded"
        )

        st.write(
            "**Current mastery gap:**",
            f"{student['mastery_gap']} percentage points"
        )

        if st.button(
            "✦ Generate Personalized Study Plan",
            use_container_width=True
        ):

            plan = generate_study_plan(student)

            st.session_state.plans[selected_id] = plan

            st.success(
                "Personalized weekly study plan generated!"
            )

        if selected_id in st.session_state.plans:

            plan = st.session_state.plans[selected_id]

            st.divider()

            render_section(
                "YOUR WEEKLY JOURNEY",
                f"{student['name']}'s Study Schedule"
            )

            plan_df = pd.DataFrame(plan)

            st.dataframe(
                plan_df,
                use_container_width=True,
                hide_index=True
            )

            st.subheader("Daily Learning Sessions")

            for day_plan in plan:

                with st.expander(day_plan["Day"]):

                    st.write(
                        f"**Focus Topic:** {day_plan['Focus Topic']}"
                    )

                    st.write(
                        f"Current topic score: "
                        f"{day_plan['Current Topic Score']}%"
                    )

                    st.write(
                        f"📖 Concept review: "
                        f"{day_plan['Concept Review']} minutes"
                    )

                    st.write(
                        f"✏️ Guided practice: "
                        f"{day_plan['Guided Practice']} minutes"
                    )

                    st.write(
                        f"🧠 Assessment: "
                        f"{day_plan['Quick Assessment']} minutes"
                    )

                    st.metric(
                        "Daily Study Time",
                        f"{day_plan['Total Minutes']} minutes"
                    )

            plan_text = plan_df.to_csv(index=False)

            st.download_button(
                "📥 Download Weekly Study Plan",
                plan_text,
                file_name=f"Study_Plan_{selected_id}.csv",
                mime="text/csv",
                use_container_width=True
            )

            st.caption(
                "This is a rule-based study-plan prototype. "
                "It allocates available time to recorded learning "
                "needs; it is not an LLM-generated plan."
            )

    else:

        st.info(
            "Register a student before generating a study plan."
        )


# =========================================================
# 15. PROGRESS TRACKER PAGE
# =========================================================

elif page == "Progress Tracker":

    render_hero(
        "CONTINUOUS IMPROVEMENT",
        "Progress is the real achievement.",
        "Record new assessments and understand how student "
        "performance changes over time."
    )

    render_section(
        "ASSESSMENT MANAGEMENT",
        "Record a New Assessment"
    )

    if students:

        selected_id = st.selectbox(
            "Select Student",
            [s["id"] for s in students],
            format_func=lambda sid: next(
                f"{s['name']} ({s['id']})"
                for s in students
                if s["id"] == sid
            )
        )

        student = next(
            s for s in students
            if s["id"] == selected_id
        )

        st.metric(
            "Current Mastery",
            f"{student['current_mastery']}%"
        )

        with st.form("assessment_update_form"):

            new_score = st.number_input(
                "New Overall Mastery Score (%)",
                0, 100,
                int(student["current_mastery"])
            )

            assessment_date = st.date_input(
                "Assessment Date",
                value=date.today()
            )

            topic_options = [
                "Overall assessment only"
            ] + list(student["topic_scores"].keys())

            selected_topic = st.selectbox(
                "Topic to Update (Optional)",
                topic_options
            )

            new_topic_score = st.number_input(
                "New Topic Score (%)",
                0, 100, 50
            )

            notes = st.text_input(
                "Assessment Notes",
                placeholder="Short assessment observation"
            )

            update = st.form_submit_button(
                "Save Assessment",
                use_container_width=True
            )

            if update:

                student["assessment_history"].append(
                    float(new_score)
                )

                student["current_mastery"] = new_score

                student["mastery_gap"] = max(
                    student["target_mastery"] - new_score,
                    0
                )

                student["priority"] = classify_priority(
                    new_score,
                    student["target_mastery"]
                )

                if selected_topic != "Overall assessment only":

                    student["topic_scores"][
                        selected_topic
                    ] = float(new_topic_score)

                student["assessment_records"].append({

                    "date": assessment_date.isoformat(),
                    "overall_score": float(new_score),
                    "topic": (
                        selected_topic
                        if selected_topic != "Overall assessment only"
                        else ""
                    ),
                    "topic_score": (
                        float(new_topic_score)
                        if selected_topic != "Overall assessment only"
                        else None
                    ),
                    "notes": notes

                })

                st.success(
                    "Assessment saved to the current session!"
                )

        st.divider()

        render_section(
            "LEARNING JOURNEY",
            f"{student['name']}'s Progress History"
        )

        history = student["assessment_history"]

        history_df = pd.DataFrame({
            "Mastery (%)": history
        })

        history_df.index = [
            f"Assessment {i + 1}"
            for i in range(len(history))
        ]

        st.line_chart(history_df)

        trend = detect_learning_trend(history)

        c1, c2 = st.columns(2)

        c1.metric(
            "Current Mastery",
            f"{student['current_mastery']}%"
        )

        c2.metric(
            "Learning Trend",
            trend["trend"],
            (
                f"{trend['change']:+g} points"
                if trend["change"] is not None
                else None
            )
        )

        if student["assessment_records"]:

            st.subheader("Assessment Records")

            st.dataframe(
                pd.DataFrame(
                    student["assessment_records"]
                ),
                use_container_width=True,
                hide_index=True
            )

    else:

        st.info(
            "Register a student before recording assessments."
        )


# =========================================================
# 16. REPORTS PAGE
# =========================================================

elif page == "Reports":

    render_hero(
        "ACADEMIC REPORTING",
        "Turn data into decisions.",
        "Generate individual performance reports, cohort "
        "summaries and downloadable academic datasets."
    )

    render_section(
        "REPORT CENTER",
        "Academic Performance Reports"
    )

    if students:

        selected_id = st.selectbox(
            "Select a Student for Individual Report",
            [s["id"] for s in students],
            format_func=lambda sid: next(
                f"{s['name']} ({s['id']})"
                for s in students
                if s["id"] == sid
            )
        )

        student = next(
            s for s in students
            if s["id"] == selected_id
        )

        report = build_student_report(student)

        st.subheader("Individual Academic Report")

        st.text_area(
            "Report Preview",
            report,
            height=420
        )

        st.download_button(
            "📥 Download Student Report",
            report,
            file_name=f"Academic_Report_{selected_id}.txt",
            mime="text/plain",
            use_container_width=True
        )

        st.divider()

        render_section(
            "COHORT INTELLIGENCE",
            "Class Performance Dataset"
        )

        cohort_rows = []

        for s in students:

            risk = detect_learning_risk(s)
            trend = detect_learning_trend(
                s["assessment_history"]
            )
            segment = classify_student_segment(s)
            intervention = calculate_intervention_priority(s)

            cohort_rows.append({

                "Student": s["name"],
                "ID": s["id"],
                "Subject": s["subject"],
                "Mastery": s["current_mastery"],
                "Target": s["target_mastery"],
                "Gap": s["mastery_gap"],
                "Priority": s["priority"],
                "Risk": risk["risk"],
                "Trend": trend["trend"],
                "Segment": segment["segment"],
                "Intervention Score": intervention["score"]

            })

        cohort_df = pd.DataFrame(cohort_rows)

        average = cohort_df["Mastery"].mean()

        c1, c2, c3 = st.columns(3)

        c1.metric("Students", len(students))
        c2.metric("Average Mastery", f"{average:.1f}%")
        c3.metric(
            "Average Mastery Gap",
            f"{cohort_df['Gap'].mean():.1f} points"
        )

        st.dataframe(
            cohort_df,
            use_container_width=True,
            hide_index=True
        )

        csv_data = cohort_df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            "📊 Download Academic Dataset (CSV)",
            csv_data,
            file_name="Academic_Performance_Data.csv",
            mime="text/csv",
            use_container_width=True
        )

    else:

        st.info(
            "Register students to generate academic reports."
        )


# =========================================================
# 17. APPLICATION FOOTER
# =========================================================

st.divider()

st.markdown("""
<div class="small-footer">

    LEARNING INTELLIGENCE STUDIO

    <br>

    Personalized learning powered by academic data.

    <br><br>

    Built with Python · Streamlit · Pandas

</div>
""", unsafe_allow_html=True)

st.caption(
    "Academic risk, segmentation and intervention results use "
    "initial rule-based screening thresholds. The study planner "
    "is a rule-based prototype, not a connected LLM. Teacher "
    "review is required before instructional decisions."
)

st.info(
    "Cloud storage note: Student records and generated plans "
    "currently use temporary Streamlit session memory. They "
    "may disappear after a session ends or the app restarts. "
    "Permanent Supabase storage and multi-user access are "
    "planned for the database integration mission."
)

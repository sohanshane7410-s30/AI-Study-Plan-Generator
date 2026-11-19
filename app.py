
import streamlit as st
import pandas as pd
import html


# =====================================================
# 1. APPLICATION CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Learning Intelligence Studio",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =====================================================
# 2. PREMIUM DESIGN SYSTEM
# =====================================================

st.markdown("""
<style>

.stApp {
    background: #F5F6FC;
    color: #18213B;
}

.block-container {
    max-width: 1500px;
    padding: 2rem 2.2rem 3rem;
}

[data-testid="stSidebar"] {
    background: #111A35;
    border-right: 1px solid #293454;
}

[data-testid="stSidebar"] * {
    color: #EDF0FC;
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    color: #C4CBE2;
}

[data-testid="stSidebar"] hr {
    border-color: #35405E !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label {
    background: #192441;
    padding: 10px 13px;
    margin-bottom: 5px;
    border-radius: 10px;
    border: 1px solid #263252;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
    background: #29365A;
}

h1 {
    color: #18213B !important;
    font-weight: 800 !important;
    letter-spacing: -1.4px;
}

h2 {
    color: #202B4D !important;
    font-weight: 750 !important;
}

h3 {
    color: #34416A !important;
    font-weight: 700 !important;
}

[data-testid="stMetric"] {
    background: #FFFFFF;
    padding: 19px;
    border-radius: 16px;
    border: 1px solid #E6E8F1;
    box-shadow: 0 4px 17px rgba(31, 42, 80, .045);
}

[data-testid="stMetricLabel"] {
    color: #77819A !important;
    font-weight: 600;
}

[data-testid="stMetricValue"] {
    color: #594BC5 !important;
    font-weight: 800;
}

.stButton > button,
.stFormSubmitButton > button,
.stDownloadButton > button {
    background: linear-gradient(110deg, #6250D3, #8368E8);
    color: white;
    border: none;
    border-radius: 11px;
    padding: .65rem 1.1rem;
    font-weight: 700;
    transition: .2s ease;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover,
.stDownloadButton > button:hover {
    background: #4F40B7;
    color: white;
    border: none;
    transform: translateY(-1px);
}

.stTextInput input,
.stNumberInput input,
.stTextArea textarea {
    background: white;
    border: 1px solid #DDE1EF;
    border-radius: 10px;
    color: #18213B;
}

[data-baseweb="select"] {
    border-radius: 10px;
}

[data-testid="stForm"] {
    background: #FFFFFF;
    padding: 24px;
    border-radius: 17px;
    border: 1px solid #E7E9F2;
    box-shadow: 0 4px 18px rgba(31, 42, 80, .04);
}

[data-testid="stExpander"] {
    background: white;
    border: 1px solid #E6E8F1;
    border-radius: 13px;
}

[data-testid="stDataFrame"] {
    border-radius: 12px;
    border: 1px solid #E6E8F1;
    overflow: hidden;
}

[data-testid="stAlert"] {
    border-radius: 12px;
}

.stProgress > div > div > div {
    background: linear-gradient(90deg, #6653DB, #48C9A5);
}

hr {
    border-color: #E4E7F0 !important;
}

.hero {
    background: linear-gradient(
        115deg,
        #111A35 0%,
        #282C68 58%,
        #6352C8 100%
    );
    padding: 35px;
    border-radius: 21px;
    margin-bottom: 24px;
    box-shadow: 0 12px 30px rgba(45, 42, 105, .15);
}

.hero-eyebrow {
    color: #B9ABFF;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 2px;
}

.hero h1 {
    color: #FFFFFF !important;
    font-size: 35px !important;
    margin: 12px 0 !important;
    letter-spacing: -1.4px;
}

.hero p {
    color: #D7DEF6;
    font-size: 15px;
    max-width: 720px;
}

.hero-status {
    color: #7BE0BE;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1.5px;
    margin-top: 15px;
}

.section-label {
    color: #7166CB;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1.5px;
    text-transform: uppercase;
}

.info-card {
    background: white;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #E7E9F2;
    margin-bottom: 12px;
}

.info-card h4 {
    color: #243153;
    margin-bottom: 7px;
}

.info-card p {
    color: #73809A;
    font-size: 13px;
}

.muted-text {
    color: #7B849D;
    font-size: 13px;
}

footer {
    visibility: hidden;
}

#MainMenu {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# 3. SESSION STATE
# =====================================================

if "students" not in st.session_state:
    st.session_state["students"] = []

if not isinstance(st.session_state["students"], list):
    st.session_state["students"] = []


# =====================================================
# 4. HELPER FUNCTIONS
# =====================================================

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
        return parse_topics(", ".join(str(x) for x in value))

    return []


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
                f"Invalid format: {item}. Use Topic: Score."
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
            errors.append(f"Invalid score for {topic}.")
            continue

        if not 0 <= score <= 100:
            errors.append(
                f"{topic} score must be between 0 and 100."
            )
            continue

        if topic.casefold() in seen:
            errors.append(f"Duplicate topic score: {topic}.")
            continue

        scores[topic] = round(score, 1)
        seen.add(topic.casefold())

    return scores, errors


def parse_assessment_history(raw_text):

    history = []
    errors = []

    for item in raw_text.split(","):

        item = item.strip()

        if not item:
            continue

        try:
            score = float(item)

        except ValueError:
            errors.append(f"Invalid assessment score: {item}")
            continue

        if not 0 <= score <= 100:
            errors.append(
                f"Assessment score {score} must be between 0 and 100."
            )
            continue

        history.append(round(score, 1))

    return history, errors


# =====================================================
# 5. ACADEMIC INTELLIGENCE ENGINES
# =====================================================

def classify_priority(current, target):

    if current >= target:
        return "TARGET ACHIEVED"

    elif current < 40:
        return "URGENT"

    elif current < 60:
        return "HIGH"

    return "MODERATE"


def classify_gap(gap):

    if gap == 0:
        return "TARGET ACHIEVED"

    elif gap >= 30:
        return "LARGE GAP"

    elif gap >= 15:
        return "MODERATE GAP"

    return "SMALL GAP"


def classify_topic_score(score):

    if score < 60:
        return "NEEDS SUPPORT"

    elif score < 80:
        return "DEVELOPING"

    return "STRONG"


def detect_learning_risk(student):

    mastery = student["current_mastery"]
    gap = student["mastery_gap"]

    if mastery < 40 or gap >= 35:

        return {
            "risk": "HIGH",
            "explanation": (
                "Low current mastery or a substantial remaining gap."
            )
        }

    elif mastery < 60 or gap >= 20:

        return {
            "risk": "MODERATE",
            "explanation": (
                "Targeted practice and closer monitoring may be useful."
            )
        }

    return {
        "risk": "LOW",
        "explanation": (
            "Lower immediate concern based on available mastery data."
        )
    }


def detect_learning_trend(history):

    if len(history) < 2:

        return {
            "trend": "INSUFFICIENT DATA",
            "change": None,
            "explanation": (
                "At least two assessment scores are required."
            )
        }

    change = round(history[-1] - history[0], 1)

    if change >= 5:
        trend = "IMPROVING"
        explanation = (
            f"Performance increased by {change} percentage points."
        )

    elif change <= -5:
        trend = "DECLINING"
        explanation = (
            f"Performance decreased by {abs(change)} points."
        )

    else:
        trend = "STABLE"
        explanation = (
            "Net performance change is less than 5 points."
        )

    return {
        "trend": trend,
        "change": change,
        "explanation": explanation
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

        segment = "ENRICHMENT"

        explanation = (
            "Target achieved. Consider advanced learning activities."
        )

    elif risk["risk"] == "HIGH":

        segment = "INTENSIVE SUPPORT"

        explanation = (
            "Substantial learning gap or low mastery requires investigation."
        )

    elif (
        risk["risk"] == "MODERATE"
        or trend["trend"] == "DECLINING"
        or support_topics >= 2
    ):

        segment = "TARGETED SUPPORT"

        explanation = (
            "Targeted practice may help address risk, declining trends "
            "or multiple weak topics."
        )

    else:

        segment = "PROGRESS MONITORING"

        explanation = (
            "Continue routine assessments and progress monitoring."
        )

    return {
        "segment": segment,
        "risk": risk["risk"],
        "trend": trend["trend"],
        "support_topics": support_topics,
        "explanation": explanation
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
            "recommendation": (
                "Target achieved. Consider enrichment and reassessment."
            )
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

    support_topics = sum(
        classify_topic_score(score) == "NEEDS SUPPORT"
        for score in student["topic_scores"].values()
    )

    topic_points = min(
        support_topics * 5,
        15
    )

    total = (
        gap_points
        + mastery_points
        + trend_points
        + topic_points
    )

    if total >= 65:

        priority = "P1 - URGENT"

        recommendation = (
            "Prompt teacher investigation, foundational concept review "
            "and individualized instructional support."
        )

    elif total >= 45:

        priority = "P2 - HIGH"

        recommendation = (
            "Schedule targeted practice, investigate weak topics "
            "and reassess learning."
        )

    elif total >= 25:

        priority = "P3 - SCHEDULED"

        recommendation = (
            "Schedule focused support and monitor the next assessment."
        )

    else:

        priority = "P4 - MONITOR"

        recommendation = (
            "Continue routine monitoring and provide additional practice."
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


# =====================================================
# 6. BACKWARD-COMPATIBLE RECORD MIGRATION
# =====================================================

def migrate_records(records):

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
            student.get("name", student.get("student_name", "Unknown"))
        )

        student["id"] = str(
            student.get("id", student.get("student_id", ""))
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

            student[field] = normalize_topics(
                student.get(field, [])
            )

        old_scores = student.get("topic_scores", {})

        if not isinstance(old_scores, dict):
            old_scores = {}

        valid_scores = {}

        for topic, score in old_scores.items():

            try:
                value = float(score)

                if 0 <= value <= 100:
                    valid_scores[str(topic)] = value

            except (TypeError, ValueError):
                continue

        student["topic_scores"] = valid_scores

        raw_history = student.get("assessment_history", [])

        if not isinstance(raw_history, list):
            raw_history = []

        valid_history = []

        for score in raw_history:

            try:
                value = float(score)

                if 0 <= value <= 100:
                    valid_history.append(value)

            except (TypeError, ValueError):
                continue

        student["assessment_history"] = valid_history

        student["daily_minutes"] = max(
            0,
            safe_int(
                student.get(
                    "daily_minutes",
                    student.get("daily_study_minutes", 0)
                )
            )
        )

        raw_days = student.get("study_days", [])

        if not isinstance(raw_days, list):
            raw_days = []

        student["study_days"] = [
            day for day in valid_days
            if day in raw_days
        ]

        student["weekly_minutes"] = (
            student["daily_minutes"] * len(student["study_days"])
        )

        upgraded.append(student)

    return upgraded


st.session_state["students"] = migrate_records(
    st.session_state["students"]
)


# =====================================================
# 7. REPORT GENERATION
# =====================================================

def build_student_report(student):

    risk = detect_learning_risk(student)

    trend = detect_learning_trend(
        student["assessment_history"]
    )

    segment = classify_student_segment(student)

    intervention = calculate_intervention_priority(student)

    current = student["current_mastery"]
    target = student["target_mastery"]

    progress = (
        min(current / target * 100, 100)
        if target > 0 else 100
    )

    topics = sorted(
        student["topic_scores"].items(),
        key=lambda item: item[1]
    )

    recommendations = []

    needs_support = [
        topic for topic, score in topics if score < 60
    ]

    developing = [
        topic for topic, score in topics if 60 <= score < 80
    ]

    if current >= target:

        recommendations.append(
            "Maintain mastery through periodic reassessment "
            "and enrichment activities."
        )

    else:

        if needs_support:
            recommendations.append(
                "Prioritize additional practice in: "
                + ", ".join(needs_support)
            )

        if trend["trend"] == "DECLINING":
            recommendations.append(
                "Investigate reasons for declining assessment performance."
            )

        elif trend["trend"] == "IMPROVING":
            recommendations.append(
                "Identify successful teaching strategies and reinforce them."
            )

        if risk["risk"] == "HIGH":
            recommendations.append(
                "Arrange prompt teacher review and check foundational understanding."
            )

        if developing:
            recommendations.append(
                "Continue practice in: " + ", ".join(developing)
            )

    if not recommendations:
        recommendations.append(
            "Collect additional assessment evidence before intervention."
        )

    lines = [
        "LEARNING INTELLIGENCE STUDIO",
        "STUDENT ACADEMIC PERFORMANCE REPORT",
        "=" * 55,
        "",
        "1. STUDENT INFORMATION",
        f"Name: {student['name']}",
        f"Student ID: {student['id']}",
        f"Subject: {student['subject']}",
        "",
        "2. ACADEMIC PERFORMANCE",
        f"Current Mastery: {current}%",
        f"Target Mastery: {target}%",
        f"Mastery Gap: {student['mastery_gap']} percentage points",
        f"Progress Toward Target: {progress:.1f}%",
        "",
        "3. PRIORITY AND RISK",
        f"Priority: {student['priority']}",
        f"Risk: {risk['risk']}",
        risk["explanation"],
        "",
        "4. TOPIC PERFORMANCE"
    ]

    for topic, score in topics:

        lines.append(
            f"{topic}: {score}% - {classify_topic_score(score)}"
        )

    lines.extend([
        "",
        "5. LEARNING TREND",
        f"Trend: {trend['trend']}",
        f"Net Change: {trend['change']}",
        trend["explanation"],
        "",
        "6. STUDENT SEGMENTATION",
        f"Segment: {segment['segment']}",
        segment["explanation"],
        "",
        "7. INTERVENTION PRIORITIZATION",
        f"Score: {intervention['score']} / 95",
        f"Priority: {intervention['priority']}",
        f"Gap Points: {intervention['gap_points']} / 40",
        f"Mastery Points: {intervention['mastery_points']} / 20",
        f"Trend Points: {intervention['trend_points']} / 20",
        f"Topic Points: {intervention['topic_points']} / 15",
        f"Suggested Action: {intervention['recommendation']}",
        "",
        "8. STUDY AVAILABILITY",
        f"Daily Minutes: {student['daily_minutes']}",
        f"Available Days: {', '.join(student['study_days'])}",
        f"Weekly Minutes: {student['weekly_minutes']}",
        f"Weekly Hours: {student['weekly_minutes'] / 60:g}",
        "",
        "9. RECOMMENDATIONS"
    ])

    for i, recommendation in enumerate(recommendations, 1):
        lines.append(f"{i}. {recommendation}")

    lines.extend([
        "",
        "10. DATA LIMITATIONS",
        "This report uses transparent Python rules.",
        "Thresholds are initial project screening criteria.",
        "Historical trends are based on supplied assessment scores.",
        "Teacher review is necessary before instructional decisions.",
        "",
        "End of Report"
    ])

    return "\n".join(lines)


def build_cohort_report(students):

    total = len(students)

    average = sum(
        s["current_mastery"] for s in students
    ) / total

    average_gap = sum(
        s["mastery_gap"] for s in students
    ) / total

    lines = [
        "LEARNING INTELLIGENCE STUDIO",
        "COHORT ACADEMIC PERFORMANCE SUMMARY",
        "=" * 55,
        "",
        f"Total Students: {total}",
        f"Average Mastery: {average:.1f}%",
        f"Average Mastery Gap: {average_gap:.1f} points",
        "",
        "PRIORITY DISTRIBUTION"
    ]

    for priority in [
        "URGENT", "HIGH", "MODERATE", "TARGET ACHIEVED"
    ]:

        count = sum(
            s["priority"] == priority for s in students
        )

        lines.append(f"{priority}: {count}")

    lines.extend(["", "LEARNING RISK DISTRIBUTION"])

    for risk_name in ["HIGH", "MODERATE", "LOW"]:

        count = sum(
            detect_learning_risk(s)["risk"] == risk_name
            for s in students
        )

        lines.append(f"{risk_name}: {count}")

    lines.extend(["", "LEARNING TREND DISTRIBUTION"])

    for trend_name in [
        "IMPROVING", "DECLINING", "STABLE", "INSUFFICIENT DATA"
    ]:

        count = sum(
            detect_learning_trend(
                s["assessment_history"]
            )["trend"] == trend_name
            for s in students
        )

        lines.append(f"{trend_name}: {count}")

    ranked = sorted(
        students,
        key=lambda s: calculate_intervention_priority(s)["score"],
        reverse=True
    )

    lines.extend(["", "TOP INTERVENTION SCORES"])

    for index, student in enumerate(ranked[:5], 1):

        result = calculate_intervention_priority(student)

        lines.append(
            f"{index}. {student['name']} - "
            f"{result['score']}/95 - {result['priority']}"
        )

    lines.extend([
        "",
        "Cohort recommendations:",
        "Investigate students with high screening risk.",
        "Review declining assessment trends.",
        "Prioritize topics with low assessment scores.",
        "Monitor improving students.",
        "Provide enrichment for students achieving their targets.",
        "",
        "Reports use initial project rules and require teacher review."
    ])

    return "\n".join(lines)


# =====================================================
# 8. GLOBAL NAVIGATION AND BRANDING
# =====================================================

students = st.session_state["students"]

with st.sidebar:

    st.markdown("""
    <div style="padding:12px 3px 23px;">
        <div style="font-size:32px;">✦</div>
        <div style="font-size:18px;font-weight:850;color:#FFFFFF;">
            LEARNING STUDIO
        </div>
        <div style="font-size:10px;letter-spacing:2px;color:#AFA5F4;">
            INTELLIGENCE PLATFORM
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("**WORKSPACE**")

    page = st.radio(
        "Main Navigation",
        [
            "Overview",
            "Students",
            "Learning Insights",
            "Intervention Center",
            "Study Planner",
            "Progress Tracking",
            "Reports"
        ],
        label_visibility="collapsed"
    )

    st.divider()

    st.markdown("**LIVE WORKSPACE STATUS**")

    st.metric(
        "Students tracked",
        len(st.session_state["students"])
    )

    st.caption("Cloud-hosted application")

    st.divider()

    st.caption("LEARNING INTELLIGENCE STUDIO")
    st.caption("Version 2.0 | Portfolio Build")


# =====================================================
# 9. COMMON HERO
# =====================================================

def show_hero(eyebrow, title, description):

    st.markdown(
        f"""
        <div class="hero">
            <div class="hero-eyebrow">{html.escape(eyebrow)}</div>
            <h1>{html.escape(title)}</h1>
            <p>{html.escape(description)}</p>
            <div class="hero-status">
                ● LEARNING INTELLIGENCE WORKSPACE
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def show_empty_state(title, description):

    st.markdown(
        f"""
        <div class="info-card">
            <h4>{html.escape(title)}</h4>
            <p>{html.escape(description)}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


def get_topic_rows(records):

    rows = []

    for student in records:

        weak = {
            topic.casefold()
            for topic in student["weak_topics"]
        }

        strong = {
            topic.casefold()
            for topic in student["strong_topics"]
        }

        for topic, score in student["topic_scores"].items():

            if topic.casefold() in weak:
                declared = "Declared Weak"
            elif topic.casefold() in strong:
                declared = "Declared Strong"
            else:
                declared = "Unspecified"

            status = classify_topic_score(score)

            review = ""

            if declared == "Declared Weak" and status == "STRONG":
                review = "Review weak label"

            elif declared == "Declared Strong" and status == "NEEDS SUPPORT":
                review = "Review strong label"

            rows.append({
                "Student": student["name"],
                "ID": student["id"],
                "Subject": student["subject"],
                "Topic": topic,
                "Score (%)": score,
                "Declared Category": declared,
                "Performance": status,
                "Review": review
            })

    return rows


# =====================================================
# 10. OVERVIEW PAGE
# =====================================================

if page == "Overview":

    show_hero(
        "YOUR ACADEMIC COMMAND CENTER",
        "Understand. Improve. Master.",
        "See the whole learning picture. Identify gaps, monitor trends "
        "and understand where instructional support may be needed."
    )

    st.markdown(
        '<div class="section-label">WORKSPACE OVERVIEW</div>',
        unsafe_allow_html=True
    )

    total = len(students)

    if total:

        average = sum(
            s["current_mastery"] for s in students
        ) / total

        at_target = sum(
            s["current_mastery"] >= s["target_mastery"]
            for s in students
        )

        high_risk = sum(
            detect_learning_risk(s)["risk"] == "HIGH"
            for s in students
        )

        declining = sum(
            detect_learning_trend(
                s["assessment_history"]
            )["trend"] == "DECLINING"
            for s in students
        )

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Students Tracked", total)

        c2.metric("Average Mastery", f"{average:.1f}%")

        c3.metric("High Screening Risk", high_risk)

        c4.metric("Targets Achieved", at_target)

        st.divider()

        left, right = st.columns([1.35, 1])

        with left:

            st.subheader("Academic Mastery Overview")

            mastery_df = pd.DataFrame([
                {
                    "Student": s["name"],
                    "Current Mastery": s["current_mastery"],
                    "Target Mastery": s["target_mastery"]
                }
                for s in students
            ]).set_index("Student")

            st.bar_chart(mastery_df)

        with right:

            st.subheader("Learning Trend Distribution")

            trend_counts = {
                name: sum(
                    detect_learning_trend(
                        s["assessment_history"]
                    )["trend"] == name
                    for s in students
                )
                for name in [
                    "IMPROVING",
                    "DECLINING",
                    "STABLE",
                    "INSUFFICIENT DATA"
                ]
            }

            st.bar_chart(
                pd.DataFrame({
                    "Students": list(trend_counts.values())
                }, index=list(trend_counts.keys()))
            )

        st.divider()

        st.subheader("Priority Overview")

        priority_counts = {
            name: sum(s["priority"] == name for s in students)
            for name in [
                "URGENT",
                "HIGH",
                "MODERATE",
                "TARGET ACHIEVED"
            ]
        }

        st.bar_chart(
            pd.DataFrame({
                "Students": list(priority_counts.values())
            }, index=list(priority_counts.keys()))
        )

        st.subheader("Recently Registered Student Profiles")

        recent = students[-5:][::-1]

        for student in recent:

            with st.expander(
                f"{student['name']} · {student['subject']} · {student['id']}"
            ):

                col1, col2, col3 = st.columns(3)

                col1.metric(
                    "Mastery",
                    f"{student['current_mastery']}%"
                )

                col2.metric(
                    "Target",
                    f"{student['target_mastery']}%"
                )

                col3.metric(
                    "Mastery Gap",
                    f"{student['mastery_gap']} points"
                )

    else:

        c1, c2, c3 = st.columns(3)

        c1.metric("Students Tracked", 0)
        c2.metric("Academic Insights", 0)
        c3.metric("Reports Generated", 0)

        show_empty_state(
            "Your learning workspace is ready.",
            "Visit Students to register your first student and "
            "start generating academic insights."
        )

    st.divider()

    st.subheader("Workspace Modules")

    module_cols = st.columns(3)

    modules = [
        ("🧠", "Learning Insights", "Understand academic performance."),
        ("🎯", "Intervention Center", "Prioritize support actions."),
        ("📄", "Reports", "Generate downloadable reports.")
    ]

    for column, module in zip(module_cols, modules):

        with column:

            show_empty_state(
                module[0] + " " + module[1],
                module[2]
            )


# =====================================================
# 11. STUDENTS PAGE
# =====================================================

elif page == "Students":

    show_hero(
        "STUDENT MANAGEMENT",
        "Every learner has a story.",
        "Build student profiles, record academic evidence and "
        "understand the individual learning journey."
    )

    st.header("Register a New Student")

    with st.form("student_registration"):

        col1, col2 = st.columns(2)

        with col1:

            student_name = st.text_input(
                "Student Name",
                placeholder="e.g. Sophia"
            )

        with col2:

            student_id = st.text_input(
                "Student ID",
                placeholder="e.g. STU101"
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

        st.subheader("Academic Performance")

        col1, col2 = st.columns(2)

        with col1:

            current_mastery = st.number_input(
                "Current Mastery (%)",
                min_value=0,
                max_value=100,
                value=42
            )

        with col2:

            target_mastery = st.number_input(
                "Target Mastery (%)",
                min_value=0,
                max_value=100,
                value=80
            )

        st.subheader("Learning Strengths and Weaknesses")

        col1, col2 = st.columns(2)

        with col1:

            weak_input = st.text_input(
                "Weak Topics",
                placeholder="Fractions, Decimals"
            )

        with col2:

            strong_input = st.text_input(
                "Strong Topics",
                placeholder="Percentages, Basic arithmetic"
            )

        st.subheader("Topic-Level Assessment Scores")

        topic_scores_input = st.text_area(
            "Enter topic scores",
            placeholder=(
                "Fractions: 35, Decimals: 45, "
                "Percentages: 85, Basic arithmetic: 90"
            )
        )

        st.subheader("Assessment History")

        history_input = st.text_input(
            "Scores from oldest to newest",
            placeholder="30, 36, 42",
            help="The most recent score must match current mastery."
        )

        st.subheader("Study Availability")

        daily_minutes = st.number_input(
            "Daily Study Time (minutes)",
            min_value=15,
            max_value=240,
            value=120,
            step=15
        )

        study_days = st.multiselect(
            "Preferred Study Days",
            [
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
                "Sunday"
            ],
            default=[
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday"
            ]
        )

        submitted = st.form_submit_button(
            "✦ Register Student",
            use_container_width=True
        )

        if submitted:

            name = student_name.strip()
            clean_id = student_id.strip().upper()

            weak_topics = parse_topics(weak_input)
            strong_topics = parse_topics(strong_input)

            topic_scores, score_errors = parse_topic_scores(
                topic_scores_input
            )

            history, history_errors = parse_assessment_history(
                history_input
            )

            overlap = (
                {x.casefold() for x in weak_topics}
                &
                {x.casefold() for x in strong_topics}
            )

            existing_ids = {
                s["id"].casefold() for s in students
            }

            topic_lookup = {
                topic.casefold()
                for topic in topic_scores
            }

            missing_scores = [
                topic
                for topic in weak_topics + strong_topics
                if topic.casefold() not in topic_lookup
            ]

            if not name or not clean_id:

                st.error("Student name and ID are required.")

            elif clean_id.casefold() in existing_ids:

                st.error("This student ID already exists.")

            elif overlap:

                st.error(
                    "A topic cannot be both weak and strong."
                )

            elif missing_scores:

                st.error(
                    "Add assessment scores for: "
                    + ", ".join(missing_scores)
                )

            elif score_errors:

                for error in score_errors:
                    st.error(error)

            elif history_errors:

                for error in history_errors:
                    st.error(error)

            elif history and abs(
                history[-1] - current_mastery
            ) > 0.01:

                st.error(
                    "The latest assessment must match current mastery."
                )

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
                        target_mastery - current_mastery,
                        0
                    ),

                    "priority": classify_priority(
                        current_mastery,
                        target_mastery
                    ),

                    "weak_topics": weak_topics,
                    "strong_topics": strong_topics,

                    "topic_scores": topic_scores,
                    "assessment_history": history,

                    "daily_minutes": daily_minutes,
                    "study_days": study_days,

                    "weekly_minutes": (
                        daily_minutes * len(study_days)
                    )

                }

                st.session_state["students"].append(student)

                st.success(
                    f"{name} successfully added to the learning workspace!"
                )

    st.divider()

    st.subheader("Registered Students")

    if students:

        student_table = []

        for s in students:

            student_table.append({

                "Student": s["name"],
                "ID": s["id"],
                "Subject": s["subject"],
                "Mastery": s["current_mastery"],
                "Target": s["target_mastery"],
                "Gap": s["mastery_gap"],
                "Priority": s["priority"]

            })

        st.dataframe(
            pd.DataFrame(student_table),
            use_container_width=True,
            hide_index=True
        )

        st.subheader("Individual Profiles")

        for s in students:

            with st.expander(
                f"{s['name']} · {s['id']}"
            ):

                col1, col2, col3 = st.columns(3)

                col1.metric(
                    "Current Mastery",
                    f"{s['current_mastery']}%"
                )

                col2.metric(
                    "Target Mastery",
                    f"{s['target_mastery']}%"
                )

                col3.metric(
                    "Mastery Gap",
                    f"{s['mastery_gap']} points"
                )

                st.write("**Weak Topics**")

                for topic in s["weak_topics"]:
                    st.write("🔴", topic)

                st.write("**Strong Topics**")

                for topic in s["strong_topics"]:
                    st.write("🟢", topic)

                st.write("**Assessment History**")
                st.write(s["assessment_history"])

                st.write(
                    f"**Weekly Study Capacity:** "
                    f"{s['weekly_minutes'] / 60:g} hours"
                )

    else:

        show_empty_state(
            "No students registered yet.",
            "Use the registration form above to create your first student profile."
        )


# =====================================================
# 12. LEARNING INSIGHTS PAGE
# =====================================================

elif page == "Learning Insights":

    show_hero(
        "ACADEMIC INTELLIGENCE",
        "See beyond the scores.",
        "Investigate mastery gaps, weak topics, assessment trends, "
        "learning risk and student segments."
    )

    if not students:

        show_empty_state(
            "No academic data available.",
            "Register students to unlock the intelligence dashboards."
        )

    else:

        st.header("Learning Gap Analysis")

        gap_rows = []

        for s in students:

            target_progress = (
                min(s["current_mastery"] / s["target_mastery"] * 100, 100)
                if s["target_mastery"] > 0 else 100
            )

            gap_rows.append({

                "Student": s["name"],
                "Mastery": s["current_mastery"],
                "Target": s["target_mastery"],
                "Gap": s["mastery_gap"],
                "Target Progress (%)": round(target_progress, 1),
                "Classification": classify_gap(s["mastery_gap"])

            })

        gap_df = pd.DataFrame(gap_rows)

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Average Gap",
            f"{gap_df['Gap'].mean():.1f} points"
        )

        c2.metric(
            "Largest Gap",
            f"{gap_df['Gap'].max()} points"
        )

        c3.metric(
            "Large Gaps",
            int((gap_df["Classification"] == "LARGE GAP").sum())
        )

        st.dataframe(
            gap_df.sort_values("Gap", ascending=False),
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        st.header("Learning Risk Analysis")

        risk_rows = []

        for s in students:

            risk = detect_learning_risk(s)

            risk_rows.append({

                "Student": s["name"],
                "Mastery": s["current_mastery"],
                "Gap": s["mastery_gap"],
                "Risk": risk["risk"],
                "Reason": risk["explanation"]

            })

        risk_df = pd.DataFrame(risk_rows)

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "High Risk",
            sum(x["Risk"] == "HIGH" for x in risk_rows)
        )

        c2.metric(
            "Moderate Risk",
            sum(x["Risk"] == "MODERATE" for x in risk_rows)
        )

        c3.metric(
            "Low Risk",
            sum(x["Risk"] == "LOW" for x in risk_rows)
        )

        st.dataframe(
            risk_df,
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        st.header("Topic-Level Performance")

        topic_rows = get_topic_rows(students)

        if topic_rows:

            topic_df = pd.DataFrame(topic_rows)

            c1, c2 = st.columns(2)

            c1.metric(
                "Average Topic Score",
                f"{topic_df['Score (%)'].mean():.1f}%"
            )

            c2.metric(
                "Topics Needing Support",
                int(
                    (topic_df["Performance"] == "NEEDS SUPPORT").sum()
                )
            )

            st.dataframe(
                topic_df.sort_values("Score (%)"),
                use_container_width=True,
                hide_index=True
            )

            chart_df = topic_df.copy()

            chart_df["Topic Label"] = (
                chart_df["Student"]
                + " - "
                + chart_df["Topic"]
            )

            st.bar_chart(
                chart_df.set_index("Topic Label")[["Score (%)"]]
            )

            review_df = topic_df[
                topic_df["Review"] != ""
            ]

            if not review_df.empty:

                st.subheader("Classification Review")

                st.dataframe(
                    review_df,
                    use_container_width=True,
                    hide_index=True
                )

        else:

            st.info("No topic assessment data available.")

        st.divider()

        st.header("Learning Trend Analysis")

        trend_rows = []

        for s in students:

            result = detect_learning_trend(
                s["assessment_history"]
            )

            trend_rows.append({

                "Student": s["name"],
                "Assessment Count": len(s["assessment_history"]),
                "Net Change": result["change"],
                "Trend": result["trend"],
                "Explanation": result["explanation"]

            })

        st.dataframe(
            pd.DataFrame(trend_rows),
            use_container_width=True,
            hide_index=True
        )

        trend_counts = {
            name: sum(
                row["Trend"] == name for row in trend_rows
            )
            for name in [
                "IMPROVING",
                "DECLINING",
                "STABLE",
                "INSUFFICIENT DATA"
            ]
        }

        st.bar_chart(
            pd.DataFrame({
                "Students": list(trend_counts.values())
            }, index=list(trend_counts.keys()))
        )

        for s in students:

            with st.expander(
                f"{s['name']} — Assessment History"
            ):

                if len(s["assessment_history"]) >= 2:

                    chart = pd.DataFrame({
                        "Mastery (%)": s["assessment_history"]
                    })

                    chart.index = [
                        f"Assessment {i + 1}"
                        for i in range(len(s["assessment_history"]))
                    ]

                    st.line_chart(chart)

                else:

                    st.info("Insufficient assessment history.")

        st.divider()

        st.header("Student Segmentation")

        segment_rows = []

        for s in students:

            result = classify_student_segment(s)

            segment_rows.append({

                "Student": s["name"],
                "Risk": result["risk"],
                "Trend": result["trend"],
                "Support Topics": result["support_topics"],
                "Segment": result["segment"],
                "Explanation": result["explanation"]

            })

        segment_df = pd.DataFrame(segment_rows)

        st.dataframe(
            segment_df,
            use_container_width=True,
            hide_index=True
        )

        segment_counts = {
            name: sum(
                row["Segment"] == name
                for row in segment_rows
            )
            for name in [
                "INTENSIVE SUPPORT",
                "TARGETED SUPPORT",
                "PROGRESS MONITORING",
                "ENRICHMENT"
            ]
        }

        st.bar_chart(
            pd.DataFrame({
                "Students": list(segment_counts.values())
            }, index=list(segment_counts.keys()))
        )

        st.info(
            "These are initial rule-based analytical indicators. "
            "They are not validated educational predictions."
        )


# =====================================================
# 13. INTERVENTION CENTER
# =====================================================

elif page == "Intervention Center":

    show_hero(
        "INTERVENTION COMMAND CENTER",
        "Know where to focus.",
        "Rank potential interventions using mastery gaps, "
        "historical trends and topic-level performance."
    )

    if students:

        intervention_rows = []

        for s in students:

            result = calculate_intervention_priority(s)

            intervention_rows.append({

                "Student": s["name"],
                "Student ID": s["id"],
                "Mastery": s["current_mastery"],
                "Gap": s["mastery_gap"],
                "Score": result["score"],
                "Priority": result["priority"],
                "Recommendation": result["recommendation"]

            })

        intervention_df = pd.DataFrame(
            intervention_rows
        ).sort_values(
            "Score",
            ascending=False
        ).reset_index(drop=True)

        intervention_df.insert(
            0, "Rank", range(1, len(intervention_df) + 1)
        )

        counts = {
            priority: sum(
                row["Priority"] == priority
                for row in intervention_rows
            )
            for priority in [
                "P1 - URGENT",
                "P2 - HIGH",
                "P3 - SCHEDULED",
                "P4 - MONITOR"
            ]
        }

        cols = st.columns(4)

        for col, (name, count) in zip(cols, counts.items()):

            with col:
                st.metric(name, count)

        st.divider()

        st.subheader("Ranked Intervention Queue")

        st.dataframe(
            intervention_df[
                [
                    "Rank",
                    "Student",
                    "Student ID",
                    "Score",
                    "Priority",
                    "Mastery"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

        chart = intervention_df[
            ["Student", "Score"]
        ].set_index("Student")

        st.subheader("Intervention Score Comparison")
        st.bar_chart(chart)

        st.divider()

        st.subheader("Decision Explanations")

        for s in students:

            result = calculate_intervention_priority(s)

            with st.expander(
                f"{s['name']} · {result['priority']}"
            ):

                col1, col2 = st.columns(2)

                col1.metric(
                    "Intervention Score",
                    f"{result['score']} / 95"
                )

                col2.metric(
                    "Mastery Gap",
                    f"{s['mastery_gap']} points"
                )

                st.write("**Score breakdown**")

                st.write(
                    f"Mastery gap: {result['gap_points']} / 40"
                )

                st.write(
                    f"Current mastery: {result['mastery_points']} / 20"
                )

                st.write(
                    f"Learning trend: {result['trend_points']} / 20"
                )

                st.write(
                    f"Weak topics: {result['topic_points']} / 15"
                )

                st.divider()

                st.write("**Recommended next action**")

                st.info(result["recommendation"])

        st.warning(
            "The intervention score is a project-specific screening "
            "heuristic, not a validated student outcome prediction. "
            "Teachers should examine underlying evidence before acting."
        )

    else:

        show_empty_state(
            "Intervention queue is empty.",
            "Register students to generate intervention priorities."
        )


# =====================================================
# 14. STUDY PLANNER PAGE
# =====================================================

elif page == "Study Planner":

    show_hero(
        "PERSONALIZED LEARNING",
        "Every student deserves a plan.",
        "The next development milestone is turning academic evidence "
        "into individualized study schedules."
    )

    st.info(
        "The personalized study-plan generation engine is scheduled "
        "for Mission 4. This module is not yet implemented."
    )

    st.subheader("Planned capabilities")

    planned = [
        ("01", "Weak Topic Prioritization",
         "Identify which learning areas should receive attention first."),
        ("02", "Intelligent Time Allocation",
         "Distribute available study minutes across learning activities."),
        ("03", "Daily Learning Objectives",
         "Create measurable daily learning goals."),
        ("04", "Practice Assignments",
         "Generate targeted practice based on academic gaps."),
        ("05", "Weekly Learning Calendar",
         "Build schedules that respect student availability.")
    ]

    for number, name, description in planned:

        show_empty_state(
            f"{number}  ·  {name}",
            description
        )

    if students:

        st.subheader("Available Student Profiles")

        st.dataframe(
            pd.DataFrame([
                {
                    "Student": s["name"],
                    "Mastery": s["current_mastery"],
                    "Target": s["target_mastery"],
                    "Weekly Capacity": s["weekly_minutes"]
                }
                for s in students
            ]),
            use_container_width=True,
            hide_index=True
        )


# =====================================================
# 15. PROGRESS TRACKING PAGE
# =====================================================

elif page == "Progress Tracking":

    show_hero(
        "STUDENT GROWTH",
        "Progress is a journey.",
        "Monitor assessment history and identify changes "
        "in academic performance over time."
    )

    st.info(
        "Daily assignment completion, reassessment submission "
        "and persistent progress history are scheduled for Mission 6."
    )

    if students:

        selected_id = st.selectbox(
            "Select student",
            [s["id"] for s in students],
            format_func=lambda sid: next(
                f"{s['name']} ({s['id']})"
                for s in students if s["id"] == sid
            )
        )

        selected = next(
            s for s in students if s["id"] == selected_id
        )

        st.subheader(
            f"{selected['name']}'s Learning Journey"
        )

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Current Mastery",
            f"{selected['current_mastery']}%"
        )

        col2.metric(
            "Target Mastery",
            f"{selected['target_mastery']}%"
        )

        col3.metric(
            "Remaining Gap",
            f"{selected['mastery_gap']} points"
        )

        history = selected["assessment_history"]

        if history:

            history_df = pd.DataFrame({
                "Mastery (%)": history
            })

            history_df.index = [
                f"Assessment {i + 1}"
                for i in range(len(history))
            ]

            st.line_chart(history_df)

            result = detect_learning_trend(history)

            st.write("**Learning Trend:**", result["trend"])

            st.info(result["explanation"])

        else:

            st.warning(
                "No historical assessment scores have been recorded."
            )

    else:

        show_empty_state(
            "No progress records available.",
            "Register students to inspect their assessment data."
        )


# =====================================================
# 16. REPORTS PAGE
# =====================================================

elif page == "Reports":

    show_hero(
        "ACADEMIC REPORTING",
        "Turn data into decisions.",
        "Generate individual performance reports, cohort summaries "
        "and downloadable academic datasets."
    )

    if students:

        st.subheader("Individual Academic Report")

        selected_id = st.selectbox(
            "Choose student",
            [s["id"] for s in students],
            format_func=lambda sid: next(
                f"{s['name']} ({s['id']})"
                for s in students if s["id"] == sid
            )
        )

        selected_student = next(
            s for s in students if s["id"] == selected_id
        )

        individual_report = build_student_report(
            selected_student
        )

        st.success(
            f"Report generated for {selected_student['name']}."
        )

        with st.expander("Preview Full Student Report", expanded=True):

            st.text(individual_report)

        st.download_button(
            "📥 Download Student Report",
            data=individual_report,
            file_name=f"Academic_Report_{selected_id}.txt",
            mime="text/plain",
            use_container_width=True
        )

        st.divider()

        st.subheader("Cohort Executive Report")

        cohort_report = build_cohort_report(students)

        with st.expander("Preview Cohort Report"):

            st.text(cohort_report)

        st.download_button(
            "📥 Download Cohort Report",
            data=cohort_report,
            file_name="Cohort_Academic_Report.txt",
            mime="text/plain",
            use_container_width=True
        )

        st.divider()

        st.subheader("Academic Performance Dataset")

        export_rows = []

        for s in students:

            risk = detect_learning_risk(s)
            trend = detect_learning_trend(
                s["assessment_history"]
            )
            segment = classify_student_segment(s)
            intervention = calculate_intervention_priority(s)

            export_rows.append({

                "Student": s["name"],
                "Student ID": s["id"],
                "Subject": s["subject"],
                "Current Mastery": s["current_mastery"],
                "Target Mastery": s["target_mastery"],
                "Mastery Gap": s["mastery_gap"],
                "Priority": s["priority"],
                "Risk": risk["risk"],
                "Learning Trend": trend["trend"],
                "Segment": segment["segment"],
                "Intervention Score": intervention["score"],
                "Intervention Priority": intervention["priority"],
                "Daily Study Minutes": s["daily_minutes"],
                "Weekly Study Minutes": s["weekly_minutes"]

            })

        export_df = pd.DataFrame(export_rows)

        st.dataframe(
            export_df,
            use_container_width=True,
            hide_index=True
        )

        csv_data = export_df.to_csv(
            index=False
        ).encode("utf-8-sig")

        st.download_button(
            "📊 Download Academic Dataset (CSV)",
            data=csv_data,
            file_name="Academic_Performance_Data.csv",
            mime="text/csv",
            use_container_width=True
        )

    else:

        show_empty_state(
            "No reports available yet.",
            "Register students to generate individual and cohort reports."
        )


# =====================================================
# 17. GLOBAL FOOTER
# =====================================================

st.divider()

st.markdown(
    """
    <div style="text-align:center;padding:15px 0 5px;">
        <div style="font-weight:800;color:#554BC0;">
            ✦ LEARNING INTELLIGENCE STUDIO
        </div>
        <div style="font-size:11px;color:#8991A8;">
            Personalized Learning · Academic Intelligence · Student Growth
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.caption(
    "Current academic analytics use transparent Python rules. "
    "These are initial project screening criteria, not validated "
    "educational predictions. LLM integration, study-plan generation "
    "and persistent Supabase storage are future development milestones."
)

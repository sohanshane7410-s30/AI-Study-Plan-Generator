
import streamlit as st
import pandas as pd
import html


# =========================================================
# 1. APPLICATION CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Learning Intelligence Studio",
    page_icon="📚",
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
}

.stTextInput input,
.stNumberInput input,
.stTextArea textarea {
    background: white;
    border: 1px solid #DDE1EF;
    border-radius: 10px;
    color: #18213B;
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

.section-label {
    color: #7166CB;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1.5px;
}

.profile-hero {
    background: linear-gradient(120deg, #171F42, #5245A5);
    padding: 26px;
    border-radius: 19px;
    margin: 12px 0 20px;
    color: white;
}

.profile-hero h2 {
    color: white !important;
    font-size: 29px;
    margin: 10px 0;
}

.focus-chip {
    background: #FFF0F0;
    border: 1px solid #F5D8D8;
    color: #9E3535;
    padding: 11px 14px;
    margin: 7px 0;
    border-radius: 10px;
    font-weight: 600;
}

.strength-chip {
    background: #EAF8F2;
    border: 1px solid #D3EDDF;
    color: #24775A;
    padding: 11px 14px;
    margin: 7px 0;
    border-radius: 10px;
    font-weight: 600;
}

.calendar-day {
    border-radius: 14px;
    padding: 12px 5px;
    text-align: center;
    min-height: 145px;
}

.calendar-study {
    background: linear-gradient(180deg, #EDEAFF, #FFFFFF);
    border: 1px solid #D9D1FF;
}

.calendar-rest {
    background: #F0F1F6;
    border: 1px solid #E4E6ED;
}

footer, #MainMenu {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# 3. SESSION STATE
# =========================================================

if "students" not in st.session_state:
    st.session_state["students"] = []

if not isinstance(st.session_state["students"], list):
    st.session_state["students"] = []


# =========================================================
# 4. DATA PROCESSING FUNCTIONS
# =========================================================

def safe_int(value, default=0):
    try:
        return int(float(value))
    except (TypeError, ValueError, OverflowError):
        return default


def parse_topics(raw_text):

    topics = []
    seen = set()

    if not isinstance(raw_text, str):
        return topics

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
                f"{topic} must have a score between 0 and 100."
            )
            continue

        if topic.casefold() in seen:
            errors.append(f"Duplicate topic: {topic}.")
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


# =========================================================
# 5. ACADEMIC INTELLIGENCE ENGINES
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
            "explanation": (
                "Low current mastery or a substantial remaining gap."
            )
        }

    if mastery < 60 or gap >= 20:

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

        return {
            "trend": "IMPROVING",
            "change": change,
            "explanation": (
                f"Performance increased by {change} percentage points."
            )
        }

    if change <= -5:

        return {
            "trend": "DECLINING",
            "change": change,
            "explanation": (
                f"Performance decreased by {abs(change)} percentage points."
            )
        }

    return {
        "trend": "STABLE",
        "change": change,
        "explanation": (
            "Net performance change is less than 5 percentage points."
        )
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
            "Targeted practice may address risk, declining trends "
            "or multiple weak topics."
        )

    else:

        segment = "PROGRESS MONITORING"

        explanation = (
            "Continue routine assessments and monitor progress."
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

    topic_points = min(support_topics * 5, 15)

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


# =========================================================
# 6. BACKWARD-COMPATIBLE DATA MIGRATION
# =========================================================

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

        student["mastery_gap"] = max(target - current, 0)

        student["priority"] = classify_priority(current, target)

        student["weak_topics"] = normalize_topics(
            student.get("weak_topics", [])
        )

        student["strong_topics"] = normalize_topics(
            student.get("strong_topics", [])
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

students = st.session_state["students"]


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
            "Maintain mastery through reassessment and enrichment."
        )

    else:

        if needs_support:
            recommendations.append(
                "Prioritize practice in: " + ", ".join(needs_support)
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
        "3. LEARNING PRIORITY",
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
        "8. WEEKLY STUDY AVAILABILITY",
        f"Daily Minutes: {student['daily_minutes']}",
        f"Available Days: {', '.join(student['study_days'])}",
        f"Weekly Minutes: {student['weekly_minutes']}",
        f"Weekly Hours: {student['weekly_minutes'] / 60:g}",
        "",
        "9. RECOMMENDED ACTIONS"

    ])

    for number, item in enumerate(recommendations, 1):
        lines.append(f"{number}. {item}")

    lines.extend([

        "",
        "10. DATA LIMITATIONS",
        "This report uses transparent Python rules.",
        "Thresholds are initial project screening criteria.",
        "Trends use the supplied assessment history.",
        "Teacher review is required before instructional decisions.",
        "",
        "END OF REPORT"

    ])

    return "\n".join(lines)


def build_cohort_report(records):

    total = len(records)

    average = sum(
        s["current_mastery"] for s in records
    ) / total

    average_gap = sum(
        s["mastery_gap"] for s in records
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

    for name in ["URGENT", "HIGH", "MODERATE", "TARGET ACHIEVED"]:

        count = sum(
            s["priority"] == name for s in records
        )

        lines.append(f"{name}: {count}")

    lines.extend(["", "LEARNING RISK DISTRIBUTION"])

    for name in ["HIGH", "MODERATE", "LOW"]:

        count = sum(
            detect_learning_risk(s)["risk"] == name
            for s in records
        )

        lines.append(f"{name}: {count}")

    lines.extend(["", "LEARNING TREND DISTRIBUTION"])

    for name in [
        "IMPROVING", "DECLINING", "STABLE", "INSUFFICIENT DATA"
    ]:

        count = sum(
            detect_learning_trend(
                s["assessment_history"]
            )["trend"] == name
            for s in records
        )

        lines.append(f"{name}: {count}")

    ranked = sorted(
        records,
        key=lambda s: calculate_intervention_priority(s)["score"],
        reverse=True
    )

    lines.extend(["", "HIGHEST INTERVENTION SCORES"])

    for index, student in enumerate(ranked[:5], 1):

        result = calculate_intervention_priority(student)

        lines.append(
            f"{index}. {student['name']} - "
            f"{result['score']}/95 - {result['priority']}"
        )

    lines.extend([

        "",
        "COHORT RECOMMENDATIONS",
        "Investigate students with high screening risk.",
        "Review declining assessment trends.",
        "Prioritize topics with low assessment scores.",
        "Monitor improving students.",
        "Provide enrichment to students achieving their targets.",
        "",
        "Analysis uses initial project rules and requires teacher review."

    ])

    return "\n".join(lines)


# =========================================================
# 8. DISPLAY HELPERS
# =========================================================

def show_hero(eyebrow, title, description):

    st.markdown(
        f"""
        <div class="hero">
            <div class="hero-eyebrow">
                {html.escape(eyebrow)}
            </div>
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


# =========================================================
# 9. SIDEBAR NAVIGATION
# =========================================================

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

    st.markdown("**WORKSPACE STATUS**")

    st.metric(
        "Students Tracked",
        len(st.session_state["students"])
    )

    st.caption("Cloud-hosted application")

    st.divider()

    st.caption("LEARNING INTELLIGENCE STUDIO")
    st.caption("Portfolio Edition")


# =========================================================
# 10. OVERVIEW PAGE
# =========================================================

if page == "Overview":

    show_hero(
        "YOUR ACADEMIC COMMAND CENTER",
        "Understand. Improve. Master.",
        "Discover learning gaps, understand student performance, "
        "and turn academic data into personalized learning journeys."
    )

    st.markdown(
        '<div class="section-label">WORKSPACE OVERVIEW</div>',
        unsafe_allow_html=True
    )

    if students:

        total = len(students)

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

            trend_names = [
                "IMPROVING",
                "DECLINING",
                "STABLE",
                "INSUFFICIENT DATA"
            ]

            trend_counts = {
                name: sum(
                    detect_learning_trend(
                        s["assessment_history"]
                    )["trend"] == name
                    for s in students
                )
                for name in trend_names
            }

            st.bar_chart(
                pd.DataFrame(
                    {"Students": list(trend_counts.values())},
                    index=trend_names
                )
            )

        st.divider()

        st.subheader("Priority Overview")

        priority_names = [
            "URGENT",
            "HIGH",
            "MODERATE",
            "TARGET ACHIEVED"
        ]

        priority_counts = {
            name: sum(s["priority"] == name for s in students)
            for name in priority_names
        }

        st.bar_chart(
            pd.DataFrame(
                {"Students": list(priority_counts.values())},
                index=priority_names
            )
        )

        st.subheader("Recent Student Profiles")

        for student in students[-5:][::-1]:

            with st.expander(
                f"{student['name']} · {student['subject']} · {student['id']}"
            ):

                c1, c2, c3 = st.columns(3)

                c1.metric(
                    "Mastery",
                    f"{student['current_mastery']}%"
                )

                c2.metric(
                    "Target",
                    f"{student['target_mastery']}%"
                )

                c3.metric(
                    "Gap",
                    f"{student['mastery_gap']} points"
                )

    else:

        c1, c2, c3 = st.columns(3)

        c1.metric("Students Tracked", 0)
        c2.metric("Learning Insights", 0)
        c3.metric("Reports Generated", 0)

        show_empty_state(
            "Your learning workspace is ready.",
            "Visit Students to register your first student and "
            "start generating academic insights."
        )

    st.divider()

    st.subheader("Your Workspace")

    columns = st.columns(3)

    modules = [
        ("🧠 Learning Insights", "Understand academic performance."),
        ("🎯 Intervention Center", "Prioritize student support."),
        ("📄 Reports", "Generate downloadable reports.")
    ]

    for column, module in zip(columns, modules):

        with column:
            show_empty_state(module[0], module[1])


# =========================================================
# 11. STUDENTS PAGE
# =========================================================

elif page == "Students":

    show_hero(
        "STUDENT MANAGEMENT",
        "Every learner has a story.",
        "Create student profiles, record academic evidence, "
        "and explore each individual learning journey."
    )

    st.header("Register a New Student")

    with st.form("student_registration"):

        c1, c2 = st.columns(2)

        with c1:
            student_name = st.text_input(
                "Student Name",
                placeholder="e.g. Sophia"
            )

        with c2:
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

        c1, c2 = st.columns(2)

        with c1:
            current_mastery = st.number_input(
                "Current Mastery (%)",
                0, 100, 42
            )

        with c2:
            target_mastery = st.number_input(
                "Target Mastery (%)",
                0, 100, 80
            )

        st.subheader("Learning Strengths and Weaknesses")

        c1, c2 = st.columns(2)

        with c1:
            weak_input = st.text_input(
                "Weak Topics",
                placeholder="Fractions, Decimals"
            )

        with c2:
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

        st.subheader("Historical Assessment Scores")

        history_input = st.text_input(
            "Scores from oldest to newest",
            placeholder="30, 36, 42"
        )

        st.subheader("Study Availability")

        daily_minutes = st.number_input(
            "Daily Study Time (minutes)",
            15, 240, 120,
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
                topic.casefold() for topic in topic_scores
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

            elif not weak_topics or not strong_topics:

                st.error("Enter at least one weak and one strong topic.")

            elif overlap:

                st.error("A topic cannot be both weak and strong.")

            elif score_errors:

                for error in score_errors:
                    st.error(error)

            elif history_errors:

                for error in history_errors:
                    st.error(error)

            elif missing_scores:

                st.error(
                    "Add assessment scores for: "
                    + ", ".join(missing_scores)
                )

            elif len(history) < 2:

                st.error("Enter at least two assessment scores.")

            elif abs(history[-1] - current_mastery) > 0.01:

                st.error(
                    "The latest assessment score must match current mastery."
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

        table = []

        for s in students:

            table.append({

                "Student": s["name"],
                "ID": s["id"],
                "Subject": s["subject"],
                "Mastery": s["current_mastery"],
                "Target": s["target_mastery"],
                "Gap": s["mastery_gap"],
                "Priority": s["priority"]

            })

        st.dataframe(
            pd.DataFrame(table),
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        st.header("✨ Interactive Student Spotlight")

        selected_id = st.selectbox(
            "Choose a student to explore",
            [s["id"] for s in students],
            format_func=lambda sid: next(
                f"{s['name']} · {s['id']}"
                for s in students if s["id"] == sid
            ),
            key="student_spotlight_selector"
        )

        selected = next(
            s for s in students
            if s["id"] == selected_id
        )

        risk = detect_learning_risk(selected)

        trend = detect_learning_trend(
            selected["assessment_history"]
        )

        segment = classify_student_segment(selected)

        intervention = calculate_intervention_priority(selected)

        st.markdown(
            f"""
            <div class="profile-hero">
                <div style="
                    color:#BDB3FF;
                    font-size:11px;
                    font-weight:800;
                    letter-spacing:2px;
                ">LEARNER PROFILE</div>

                <h2>{html.escape(selected['name'])}</h2>

                <div style="color:#D6DBF5;font-size:13px;">
                    {html.escape(selected['id'])}
                    &nbsp; · &nbsp;
                    {html.escape(selected['subject'])}
                </div>

                <div style="
                    color:#83E1C1;
                    font-size:12px;
                    margin-top:15px;
                    font-weight:700;
                ">
                    ✦ PERSONALIZED LEARNING PROFILE
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Mastery",
            f"{selected['current_mastery']}%"
        )

        c2.metric(
            "Target",
            f"{selected['target_mastery']}%"
        )

        c3.metric(
            "Remaining Gap",
            f"{selected['mastery_gap']} points"
        )

        c4.metric(
            "Intervention Score",
            f"{intervention['score']}/95"
        )

        st.subheader("Mastery Journey")

        st.progress(
            selected["current_mastery"] / 100
        )

        st.caption(
            f"Current mastery: {selected['current_mastery']}% "
            f"· Target: {selected['target_mastery']}%"
        )

        c1, c2, c3 = st.columns(3)

        with c1:
            st.markdown("**Learning Risk**")
            st.write(risk["risk"])
            st.caption(risk["explanation"])

        with c2:
            st.markdown("**Learning Trend**")
            st.write(trend["trend"])
            st.caption(trend["explanation"])

        with c3:
            st.markdown("**Learning Segment**")
            st.write(segment["segment"])
            st.caption(segment["explanation"])

        left, right = st.columns(2)

        with left:

            st.subheader("🔴 Focus Areas")

            for topic in selected["weak_topics"]:

                st.markdown(
                    f'<div class="focus-chip">'
                    f'● {html.escape(topic)}</div>',
                    unsafe_allow_html=True
                )

        with right:

            st.subheader("🟢 Existing Strengths")

            for topic in selected["strong_topics"]:

                st.markdown(
                    f'<div class="strength-chip">'
                    f'● {html.escape(topic)}</div>',
                    unsafe_allow_html=True
                )

        st.subheader("Topic Assessment Scores")

        topic_data = pd.DataFrame([
            {
                "Topic": topic,
                "Score": score,
                "Performance": classify_topic_score(score)
            }
            for topic, score in selected["topic_scores"].items()
        ])

        st.dataframe(
            topic_data,
            use_container_width=True,
            hide_index=True
        )

        if len(selected["assessment_history"]) >= 2:

            st.subheader("Assessment History")

            history_df = pd.DataFrame({
                "Mastery (%)": selected["assessment_history"]
            })

            history_df.index = [
                f"Assessment {i+1}"
                for i in range(len(selected["assessment_history"]))
            ]

            st.line_chart(history_df)

    else:

        show_empty_state(
            "No students registered yet.",
            "Use the registration form above to create the first student profile."
        )


# =========================================================
# 12. LEARNING INSIGHTS PAGE
# =========================================================

elif page == "Learning Insights":

    show_hero(
        "ACADEMIC INTELLIGENCE",
        "See beyond the scores.",
        "Investigate mastery gaps, learning risks, weak topics, "
        "assessment trends and student segments."
    )

    if not students:

        show_empty_state(
            "No academic data available.",
            "Register students to unlock the learning intelligence dashboards."
        )

    else:

        st.header("Learning Gap Analysis")

        gap_rows = []

        for s in students:

            progress = (
                min(s["current_mastery"] / s["target_mastery"] * 100, 100)
                if s["target_mastery"] > 0 else 100
            )

            gap_rows.append({

                "Student": s["name"],
                "Mastery": s["current_mastery"],
                "Target": s["target_mastery"],
                "Gap": s["mastery_gap"],
                "Target Progress (%)": round(progress, 1),
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
            int(
                (gap_df["Classification"] == "LARGE GAP").sum()
            )
        )

        st.dataframe(
            gap_df.sort_values("Gap", ascending=False),
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        st.header("Learning Risk Analysis")

        risk_rows = [
            {
                "Student": s["name"],
                "Mastery": s["current_mastery"],
                "Gap": s["mastery_gap"],
                "Risk": detect_learning_risk(s)["risk"],
                "Reason": detect_learning_risk(s)["explanation"]
            }
            for s in students
        ]

        risk_df = pd.DataFrame(risk_rows)

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "High Risk",
            sum(r["Risk"] == "HIGH" for r in risk_rows)
        )

        c2.metric(
            "Moderate Risk",
            sum(r["Risk"] == "MODERATE" for r in risk_rows)
        )

        c3.metric(
            "Low Risk",
            sum(r["Risk"] == "LOW" for r in risk_rows)
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

            chart_data = topic_df.copy()

            chart_data["Topic Label"] = (
                chart_data["Student"] + " - " + chart_data["Topic"]
            )

            st.bar_chart(
                chart_data.set_index("Topic Label")[["Score (%)"]]
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

            st.info("No topic assessment information available.")

        st.divider()

        st.header("Learning Trend Analysis")

        trend_rows = []

        for s in students:

            result = detect_learning_trend(
                s["assessment_history"]
            )

            trend_rows.append({

                "Student": s["name"],
                "Assessments": len(s["assessment_history"]),
                "Net Change": result["change"],
                "Trend": result["trend"],
                "Explanation": result["explanation"]

            })

        trend_df = pd.DataFrame(trend_rows)

        st.dataframe(
            trend_df,
            use_container_width=True,
            hide_index=True
        )

        trend_counts = {
            name: sum(r["Trend"] == name for r in trend_rows)
            for name in [
                "IMPROVING",
                "DECLINING",
                "STABLE",
                "INSUFFICIENT DATA"
            ]
        }

        st.bar_chart(
            pd.DataFrame(
                {"Students": list(trend_counts.values())},
                index=list(trend_counts.keys())
            )
        )

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

        segment_names = [
            "INTENSIVE SUPPORT",
            "TARGETED SUPPORT",
            "PROGRESS MONITORING",
            "ENRICHMENT"
        ]

        segment_counts = {
            name: sum(
                r["Segment"] == name
                for r in segment_rows
            )
            for name in segment_names
        }

        st.bar_chart(
            pd.DataFrame(
                {"Students": list(segment_counts.values())},
                index=segment_names
            )
        )

        st.info(
            "These are initial rule-based analytical indicators, "
            "not validated educational predictions."
        )


# =========================================================
# 13. INTERVENTION CENTER
# =========================================================

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

        priorities = [
            "P1 - URGENT",
            "P2 - HIGH",
            "P3 - SCHEDULED",
            "P4 - MONITOR"
        ]

        columns = st.columns(4)

        for column, priority in zip(columns, priorities):

            with column:

                column.metric(
                    priority,
                    sum(
                        r["Priority"] == priority
                        for r in intervention_rows
                    )
                )

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
                    "Gap"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

        st.subheader("Intervention Score Comparison")

        st.bar_chart(
            intervention_df.set_index("Student")[["Score"]]
        )

        st.divider()

        st.subheader("Decision Explanations")

        for s in students:

            result = calculate_intervention_priority(s)

            with st.expander(
                f"{s['name']} · {result['priority']}"
            ):

                c1, c2 = st.columns(2)

                c1.metric(
                    "Intervention Score",
                    f"{result['score']} / 95"
                )

                c2.metric(
                    "Mastery Gap",
                    f"{s['mastery_gap']} points"
                )

                st.write("**Score Breakdown**")

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

                st.write("**Recommended Next Action**")

                st.info(result["recommendation"])

        st.warning(
            "Intervention scores are initial project-specific screening "
            "heuristics. They are not validated predictive scores."
        )

    else:

        show_empty_state(
            "Intervention queue is empty.",
            "Register students to generate intervention priorities."
        )


# =========================================================
# 14. STUDY PLANNER — WEEKLY CALENDAR
# =========================================================

elif page == "Study Planner":

    show_hero(
        "PERSONALIZED LEARNING",
        "Design the learning week.",
        "Explore each student's study availability and visualize "
        "weekly learning capacity."
    )

    if students:

        selected_id = st.selectbox(
            "Select Student",
            [s["id"] for s in students],
            format_func=lambda sid: next(
                f"{s['name']} ({s['id']})"
                for s in students if s["id"] == sid
            ),
            key="weekly_calendar_student"
        )

        selected = next(
            s for s in students if s["id"] == selected_id
        )

        st.divider()

        st.subheader(
            f"📅 {selected['name']}'s Weekly Learning Calendar"
        )

        st.caption(
            f"{selected['subject']} · {selected['id']}"
        )

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Daily Availability",
            f"{selected['daily_minutes']} min"
        )

        c2.metric(
            "Available Days",
            len(selected["study_days"])
        )

        c3.metric(
            "Weekly Capacity",
            f"{selected['weekly_minutes'] / 60:g} hours"
        )

        st.divider()

        st.subheader("Your Learning Week")

        days = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday"
        ]

        columns = st.columns(7)

        for day, column in zip(days, columns):

            available = day in selected["study_days"]

            with column:

                if available:

                    class_name = "calendar-day calendar-study"

                    status = "✦"
                    label = "STUDY"
                    minutes = f"{selected['daily_minutes']} min"

                else:

                    class_name = "calendar-day calendar-rest"

                    status = "☁"
                    label = "REST DAY"
                    minutes = "Unavailable"

                st.markdown(
                    f"""
                    <div class="{class_name}">
                        <div style="
                            color:#685AB8;
                            font-size:11px;
                            font-weight:800;
                        ">{day[:3].upper()}</div>

                        <div style="
                            font-size:27px;
                            margin:15px 0;
                        ">{status}</div>

                        <div style="
                            color:#5548B5;
                            font-size:11px;
                            font-weight:800;
                        ">{label}</div>

                        <div style="
                            color:#8790A5;
                            font-size:11px;
                            margin-top:9px;
                        ">{minutes}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        st.divider()

        st.subheader("Weekly Capacity Breakdown")

        capacity = pd.DataFrame({
            "Study Minutes": [
                selected["daily_minutes"]
                if day in selected["study_days"]
                else 0
                for day in days
            ]
        }, index=days)

        st.bar_chart(capacity)

        st.divider()

        left, right = st.columns(2)

        with left:

            st.subheader("🔴 Focus Areas")

            for topic in selected["weak_topics"]:
                st.write(f"🔴 {topic}")

        with right:

            st.subheader("🟢 Existing Strengths")

            for topic in selected["strong_topics"]:
                st.write(f"🟢 {topic}")

        st.success(
            f"{selected['name']} has "
            f"{selected['weekly_minutes']} available study minutes "
            "per week."
        )

        st.info(
            "This calendar shows available study time, not generated "
            "or completed assignments. Personalized objectives, "
            "time allocation and practice scheduling will be built "
            "in Mission 4."
        )

    else:

        show_empty_state(
            "Your calendar is waiting.",
            "Register a student to create a weekly availability calendar."
        )


# =========================================================
# 15. PROGRESS TRACKING
# =========================================================

elif page == "Progress Tracking":

    show_hero(
        "STUDENT GROWTH",
        "Progress is a journey.",
        "Explore assessment history and understand changes "
        "in academic performance."
    )

    if students:

        selected_id = st.selectbox(
            "Select Student",
            [s["id"] for s in students],
            format_func=lambda sid: next(
                f"{s['name']} ({s['id']})"
                for s in students if s["id"] == sid
            ),
            key="progress_student"
        )

        selected = next(
            s for s in students if s["id"] == selected_id
        )

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Current Mastery",
            f"{selected['current_mastery']}%"
        )

        c2.metric(
            "Target Mastery",
            f"{selected['target_mastery']}%"
        )

        c3.metric(
            "Remaining Gap",
            f"{selected['mastery_gap']} points"
        )

        st.divider()

        st.subheader("Assessment History")

        history = selected["assessment_history"]

        if len(history) >= 2:

            history_df = pd.DataFrame({
                "Mastery (%)": history
            })

            history_df.index = [
                f"Assessment {i+1}"
                for i in range(len(history))
            ]

            st.line_chart(history_df)

        else:

            st.info("More assessment records are needed.")

        result = detect_learning_trend(history)

        st.subheader("Learning Trend")

        st.write(result["trend"])

        st.info(result["explanation"])

        st.divider()

        st.subheader("Topic Performance")

        for topic, score in selected["topic_scores"].items():

            st.write(
                f"**{topic}** — {score}% "
                f"({classify_topic_score(score)})"
            )

            st.progress(score / 100)

        st.info(
            "Historical assessment visualization is available. "
            "Daily task completion, assessment entry and persistent "
            "progress tracking will be developed in Mission 6."
        )

    else:

        show_empty_state(
            "No progress records yet.",
            "Register students to explore their assessment histories."
        )


# =========================================================
# 16. REPORT GENERATION
# =========================================================

elif page == "Reports":

    show_hero(
        "ACADEMIC REPORTING",
        "Turn data into decisions.",
        "Generate individual academic reports, cohort summaries "
        "and downloadable performance datasets."
    )

    if students:

        st.subheader("Individual Academic Report")

        selected_id = st.selectbox(
            "Choose Student",
            [s["id"] for s in students],
            format_func=lambda sid: next(
                f"{s['name']} ({s['id']})"
                for s in students if s["id"] == sid
            ),
            key="report_student"
        )

        selected = next(
            s for s in students if s["id"] == selected_id
        )

        individual_report = build_student_report(selected)

        st.success(
            f"Report generated for {selected['name']}."
        )

        with st.expander("Preview Student Report", expanded=True):

            st.text(individual_report)

        st.download_button(
            "📥 Download Student Report",
            data=individual_report,
            file_name=f"Academic_Report_{selected_id}.txt",
            mime="text/plain",
            use_container_width=True
        )

        st.divider()

        st.subheader("Cohort Executive Summary")

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


# =========================================================
# 17. GLOBAL FOOTER
# =========================================================

st.divider()

st.markdown(
    """
    <div style="
        text-align:center;
        padding:15px 0 5px;
    ">
        <div style="
            font-weight:800;
            color:#554BC0;
        ">
            ✦ LEARNING INTELLIGENCE STUDIO
        </div>

        <div style="
            font-size:11px;
            color:#8991A8;
        ">
            Personalized Learning · Academic Intelligence · Student Growth
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.caption(
    "Academic analytics use transparent Python rules. "
    "These are initial project screening criteria, not validated "
    "educational predictions. LLM integration, actual personalized "
    "study-plan generation and persistent Supabase storage remain "
    "future development milestones."
)


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
# 2. DESIGN SYSTEM
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
    background: white;
    padding: 19px;
    border-radius: 16px;
    border: 1px solid #E6E8F1;
    box-shadow: 0 4px 17px rgba(31,42,80,.045);
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
    background: linear-gradient(110deg,#6250D3,#8368E8);
    color: white;
    border: none;
    border-radius: 11px;
    padding: .65rem 1.1rem;
    font-weight: 700;
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
    background: white;
    padding: 24px;
    border-radius: 17px;
    border: 1px solid #E7E9F2;
    box-shadow: 0 4px 18px rgba(31,42,80,.04);
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
    background: linear-gradient(90deg,#6653DB,#48C9A5);
}

.hero {
    background: linear-gradient(
        115deg,#111A35 0%,#282C68 58%,#6352C8 100%
    );
    padding: 35px;
    border-radius: 21px;
    margin-bottom: 24px;
    box-shadow: 0 12px 30px rgba(45,42,105,.15);
}

.hero-eyebrow {
    color: #B9ABFF;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 2px;
}

.hero h1 {
    color: white !important;
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

.profile-hero {
    background: linear-gradient(120deg,#171F42,#5245A5);
    padding: 26px;
    border-radius: 19px;
    margin: 12px 0 20px;
}

.profile-hero h2 {
    color: white !important;
}

.focus-chip {
    background: #FFF0F0;
    color: #9E3535;
    padding: 11px 14px;
    margin: 7px 0;
    border-radius: 10px;
    font-weight: 600;
}

.strength-chip {
    background: #EAF8F2;
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
    background: linear-gradient(180deg,#EDEAFF,#FFFFFF);
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


# =====================================================
# 3. SESSION STATE
# =====================================================

if "students" not in st.session_state:
    st.session_state["students"] = []

if "study_plans" not in st.session_state:
    st.session_state["study_plans"] = {}

if not isinstance(st.session_state["students"], list):
    st.session_state["students"] = []

if not isinstance(st.session_state["study_plans"], dict):
    st.session_state["study_plans"] = {}


# =====================================================
# 4. DATA PROCESSING
# =====================================================

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
                f"{topic} must have a score from 0 to 100."
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
                f"Assessment score {score} must be from 0 to 100."
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
                "Low mastery or a substantial remaining mastery gap."
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
                f"Performance decreased by {abs(change)} points."
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
        explanation = "Target achieved. Consider enrichment activities."

    elif risk["risk"] == "HIGH":

        segment = "INTENSIVE SUPPORT"
        explanation = "Substantial gap or low mastery requires investigation."

    elif (
        risk["risk"] == "MODERATE"
        or trend["trend"] == "DECLINING"
        or support_topics >= 2
    ):

        segment = "TARGETED SUPPORT"
        explanation = "Targeted practice may address identified needs."

    else:

        segment = "PROGRESS MONITORING"
        explanation = "Continue routine assessments and progress monitoring."

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
            "Prompt teacher investigation and individualized support."
        )

    elif total >= 45:

        priority = "P2 - HIGH"
        recommendation = (
            "Schedule targeted practice and reassess learning."
        )

    elif total >= 25:

        priority = "P3 - SCHEDULED"
        recommendation = (
            "Schedule focused practice and monitor progress."
        )

    else:

        priority = "P4 - MONITOR"
        recommendation = (
            "Continue routine monitoring and additional practice."
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
# 6. MISSION 4 — STUDY PLAN GENERATION ENGINE
# =====================================================

def generate_study_plan(student):
    """
    Generates a foundational weekly learning plan.

    Topics with the lowest recorded assessment scores
    are scheduled first and rotated across available days.

    Each daily session is divided into:
    20% concept review
    60% guided practice
    20% knowledge check
    """

    days = student["study_days"]
    daily_minutes = student["daily_minutes"]

    if not days:
        raise ValueError("Student has no available study days.")

    if daily_minutes < 15:
        raise ValueError("Daily study availability is too low.")

    if not student["weak_topics"]:
        raise ValueError("No weak topics have been recorded.")

    score_lookup = {
        topic.casefold(): score
        for topic, score in student["topic_scores"].items()
    }

    # Sort weak topics by lowest assessment score.
    ordered_topics = sorted(
        student["weak_topics"],
        key=lambda topic: score_lookup.get(
            topic.casefold(), 50
        )
    )

    # Divide daily time into three learning blocks.
    review_minutes = max(
        1, round(daily_minutes * 0.20)
    )

    check_minutes = max(
        1, round(daily_minutes * 0.20)
    )

    practice_minutes = (
        daily_minutes
        - review_minutes
        - check_minutes
    )

    sessions = []

    for index, day in enumerate(days):

        topic = ordered_topics[
            index % len(ordered_topics)
        ]

        score = score_lookup.get(
            topic.casefold(), 50
        )

        if score < 40:

            objective = (
                f"Rebuild foundational understanding of {topic}, "
                "review key concepts and explain the solution method."
            )

        elif score < 60:

            objective = (
                f"Strengthen {topic} through worked examples "
                "and structured problem solving."
            )

        elif score < 80:

            objective = (
                f"Improve accuracy in {topic} and solve mixed "
                "problems with less support."
            )

        else:

            objective = (
                f"Maintain understanding of {topic} through "
                "challenging practice and retrieval."
            )

        session = {

            "day": day,

            "topic": topic,

            "topic_score": score,

            "objective": objective,

            "review_minutes": review_minutes,

            "practice_minutes": practice_minutes,

            "check_minutes": check_minutes,

            "total_minutes": daily_minutes,

            "activities": [

                {
                    "name": "Concept Review",
                    "minutes": review_minutes,
                    "instruction": (
                        f"Review the important ideas and worked "
                        f"examples in {topic}."
                    )
                },

                {
                    "name": "Guided Practice",
                    "minutes": practice_minutes,
                    "instruction": (
                        f"Complete structured practice exercises "
                        f"for {topic} and show your working."
                    )
                },

                {
                    "name": "Knowledge Check",
                    "minutes": check_minutes,
                    "instruction": (
                        f"Complete a short knowledge check on {topic} "
                        "and explain one answer."
                    )
                }

            ]

        }

        sessions.append(session)

    total_weekly_minutes = sum(
        session["total_minutes"]
        for session in sessions
    )

    return {

        "student_id": student["id"],

        "student_name": student["name"],

        "subject": student["subject"],

        "current_mastery": student["current_mastery"],

        "target_mastery": student["target_mastery"],

        "mastery_gap": student["mastery_gap"],

        "daily_minutes": daily_minutes,

        "study_days": days.copy(),

        "sessions": sessions,

        "weekly_minutes": total_weekly_minutes,

        "weekly_hours": total_weekly_minutes / 60

    }


def build_study_plan_text(plan):

    lines = [

        "LEARNING INTELLIGENCE STUDIO",
        "PERSONALIZED WEEKLY STUDY PLAN",
        "=" * 55,
        "",
        f"Student: {plan['student_name']}",
        f"Student ID: {plan['student_id']}",
        f"Subject: {plan['subject']}",
        f"Current Mastery: {plan['current_mastery']}%",
        f"Target Mastery: {plan['target_mastery']}%",
        f"Mastery Gap: {plan['mastery_gap']} points",
        "",
        f"Weekly Capacity: {plan['weekly_minutes']} minutes",
        f"Weekly Hours: {plan['weekly_hours']:g}",
        "",
        "WEEKLY LEARNING SCHEDULE",
        "=" * 55

    ]

    for session in plan["sessions"]:

        lines.extend([

            "",
            session["day"].upper(),
            f"Focus Topic: {session['topic']}",
            f"Topic Assessment Score: {session['topic_score']}%",
            f"Daily Objective: {session['objective']}",
            f"Total Study Time: {session['total_minutes']} minutes",
            ""

        ])

        for activity in session["activities"]:

            lines.append(
                f"{activity['name']} - "
                f"{activity['minutes']} minutes"
            )

            lines.append(
                activity["instruction"]
            )

    lines.extend([

        "",
        "=" * 55,
        "PLAN NOTES",
        "This is a foundational rule-based study plan.",
        "Activities and time allocations are initial project rules.",
        "The plan should be reviewed by a teacher or learning coach.",
        "Actual assignment generation and LLM integration are upcoming.",
        "",
        "END OF STUDY PLAN"

    ])

    return "\n".join(lines)


# =====================================================
# 7. BACKWARD-COMPATIBLE DATA MIGRATION
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

        student["mastery_gap"] = max(
            target - current, 0
        )

        student["priority"] = classify_priority(
            current, target
        )

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
            student["daily_minutes"]
            * len(student["study_days"])
        )

        upgraded.append(student)

    return upgraded


st.session_state["students"] = migrate_records(
    st.session_state["students"]
)

students = st.session_state["students"]


# =====================================================
# 8. REPORT GENERATION
# =====================================================

def build_student_report(student):

    risk = detect_learning_risk(student)

    trend = detect_learning_trend(
        student["assessment_history"]
    )

    segment = classify_student_segment(student)

    intervention = calculate_intervention_priority(student)

    lines = [

        "LEARNING INTELLIGENCE STUDIO",
        "STUDENT ACADEMIC PERFORMANCE REPORT",
        "=" * 55,
        "",
        f"Student: {student['name']}",
        f"Student ID: {student['id']}",
        f"Subject: {student['subject']}",
        "",
        f"Current Mastery: {student['current_mastery']}%",
        f"Target Mastery: {student['target_mastery']}%",
        f"Mastery Gap: {student['mastery_gap']} points",
        "",
        f"Priority: {student['priority']}",
        f"Learning Risk: {risk['risk']}",
        f"Learning Trend: {trend['trend']}",
        f"Learning Segment: {segment['segment']}",
        "",
        "TOPIC PERFORMANCE"

    ]

    for topic, score in student["topic_scores"].items():

        lines.append(
            f"{topic}: {score}% - {classify_topic_score(score)}"
        )

    lines.extend([

        "",
        "INTERVENTION ANALYSIS",
        f"Intervention Score: {intervention['score']}/95",
        f"Intervention Priority: {intervention['priority']}",
        f"Recommended Action: {intervention['recommendation']}",
        "",
        "STUDY AVAILABILITY",
        f"Daily Minutes: {student['daily_minutes']}",
        f"Available Days: {', '.join(student['study_days'])}",
        f"Weekly Hours: {student['weekly_minutes']/60:g}",
        "",
        "DATA LIMITATIONS",
        "This report uses initial project screening rules.",
        "Teacher review is required before instructional decisions."

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
        f"Students: {total}",
        f"Average Mastery: {average:.1f}%",
        f"Average Mastery Gap: {average_gap:.1f} points",
        "",
        "INTERVENTION RANKING"

    ]

    ranked = sorted(
        records,
        key=lambda s: calculate_intervention_priority(s)["score"],
        reverse=True
    )

    for index, student in enumerate(ranked, 1):

        result = calculate_intervention_priority(student)

        lines.append(
            f"{index}. {student['name']} - "
            f"{result['score']}/95 - {result['priority']}"
        )

    lines.extend([
        "",
        "Teacher review is required before instructional decisions."
    ])

    return "\n".join(lines)


# =====================================================
# 9. DISPLAY HELPERS
# =====================================================

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


# =====================================================
# 10. SIDEBAR NAVIGATION
# =====================================================

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
        len(students)
    )

    st.metric(
        "Plans Generated",
        len(st.session_state["study_plans"])
    )

    st.caption("Cloud-hosted application")

    st.divider()

    st.caption("LEARNING INTELLIGENCE STUDIO")
    st.caption("Portfolio Edition")


# =====================================================
# 11. OVERVIEW PAGE
# =====================================================

if page == "Overview":

    show_hero(
        "YOUR ACADEMIC COMMAND CENTER",
        "Understand. Improve. Master.",
        "Discover learning gaps, understand student performance "
        "and turn academic data into personalized learning journeys."
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

        plans_count = len(st.session_state["study_plans"])

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Students Tracked", total)
        c2.metric("Average Mastery", f"{average:.1f}%")
        c3.metric("High Screening Risk", high_risk)
        c4.metric("Study Plans", plans_count)

        st.divider()

        left, right = st.columns([1.35, 1])

        with left:

            st.subheader("Academic Mastery Overview")

            chart = pd.DataFrame([
                {
                    "Student": s["name"],
                    "Current Mastery": s["current_mastery"],
                    "Target Mastery": s["target_mastery"]
                }
                for s in students
            ]).set_index("Student")

            st.bar_chart(chart)

        with right:

            st.subheader("Learning Trends")

            trend_names = [
                "IMPROVING",
                "DECLINING",
                "STABLE",
                "INSUFFICIENT DATA"
            ]

            counts = {
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
                    {"Students": list(counts.values())},
                    index=trend_names
                )
            )

        st.divider()

        st.subheader("Student Priority Overview")

        priorities = [
            "URGENT",
            "HIGH",
            "MODERATE",
            "TARGET ACHIEVED"
        ]

        priority_counts = {
            name: sum(s["priority"] == name for s in students)
            for name in priorities
        }

        st.bar_chart(
            pd.DataFrame(
                {"Students": list(priority_counts.values())},
                index=priorities
            )
        )

    else:

        c1, c2, c3 = st.columns(3)

        c1.metric("Students Tracked", 0)
        c2.metric("Plans Generated", 0)
        c3.metric("Academic Insights", 0)

        show_empty_state(
            "Your learning workspace is ready.",
            "Visit Students to register your first learner."
        )


# =====================================================
# 12. STUDENTS PAGE
# =====================================================

elif page == "Students":

    show_hero(
        "STUDENT MANAGEMENT",
        "Every learner has a story.",
        "Create student profiles and record academic evidence."
    )

    st.header("Register a New Student")

    with st.form("student_registration"):

        c1, c2 = st.columns(2)

        with c1:
            student_name = st.text_input("Student Name")

        with c2:
            student_id = st.text_input("Student ID")

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
                "Fractions, Decimals"
            )

        with c2:
            strong_input = st.text_input(
                "Strong Topics",
                "Percentages, Basic arithmetic"
            )

        st.subheader("Topic Assessment Scores")

        topic_input = st.text_area(
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

            weak = parse_topics(weak_input)
            strong = parse_topics(strong_input)

            topic_scores, score_errors = parse_topic_scores(
                topic_input
            )

            history, history_errors = parse_assessment_history(
                history_input
            )

            overlap = (
                {x.casefold() for x in weak}
                & {x.casefold() for x in strong}
            )

            existing_ids = {
                s["id"].casefold() for s in students
            }

            topic_lookup = {
                topic.casefold() for topic in topic_scores
            }

            missing = [
                topic for topic in weak + strong
                if topic.casefold() not in topic_lookup
            ]

            if not name or not clean_id:

                st.error("Student name and ID are required.")

            elif clean_id.casefold() in existing_ids:

                st.error("Student ID already exists.")

            elif not weak or not strong:

                st.error("Enter at least one weak and one strong topic.")

            elif overlap:

                st.error("A topic cannot be both weak and strong.")

            elif target_mastery < current_mastery:

                st.error("Target cannot be lower than current mastery.")

            elif score_errors:

                for error in score_errors:
                    st.error(error)

            elif history_errors:

                for error in history_errors:
                    st.error(error)

            elif missing:

                st.error(
                    "Add assessment scores for: " + ", ".join(missing)
                )

            elif len(history) < 2:

                st.error("Enter at least two assessment scores.")

            elif abs(history[-1] - current_mastery) > 0.01:

                st.error(
                    "Latest assessment must match current mastery."
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

                    "weak_topics": weak,
                    "strong_topics": strong,

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
                    f"{name} registered successfully!"
                )

    if students:

        st.divider()

        st.header("Registered Students")

        st.dataframe(
            pd.DataFrame([
                {
                    "Name": s["name"],
                    "ID": s["id"],
                    "Subject": s["subject"],
                    "Mastery": s["current_mastery"],
                    "Target": s["target_mastery"],
                    "Gap": s["mastery_gap"],
                    "Priority": s["priority"]
                }
                for s in students
            ]),
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        st.header("✨ Interactive Student Spotlight")

        selected_id = st.selectbox(
            "Choose a student",
            [s["id"] for s in students],
            format_func=lambda sid: next(
                f"{s['name']} · {s['id']}"
                for s in students if s["id"] == sid
            )
        )

        selected = next(
            s for s in students if s["id"] == selected_id
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
                <div style="color:#BDB3FF;font-size:11px;
                font-weight:800;letter-spacing:2px;">
                    LEARNER PROFILE
                </div>
                <h2>{html.escape(selected['name'])}</h2>
                <div style="color:#D6DBF5;">
                    {html.escape(selected['id'])}
                    · {html.escape(selected['subject'])}
                </div>
                <div style="color:#83E1C1;font-size:12px;
                margin-top:15px;font-weight:700;">
                    ✦ PERSONALIZED LEARNING PROFILE
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Mastery", f"{selected['current_mastery']}%")
        c2.metric("Target", f"{selected['target_mastery']}%")
        c3.metric("Gap", f"{selected['mastery_gap']} points")
        c4.metric("Intervention", f"{intervention['score']}/95")

        c1, c2, c3 = st.columns(3)

        c1.metric("Risk", risk["risk"])
        c2.metric("Trend", trend["trend"])
        c3.metric("Segment", segment["segment"])

        left, right = st.columns(2)

        with left:

            st.subheader("🔴 Focus Areas")

            for topic in selected["weak_topics"]:

                st.markdown(
                    f'<div class="focus-chip">'
                    f'{html.escape(topic)}</div>',
                    unsafe_allow_html=True
                )

        with right:

            st.subheader("🟢 Existing Strengths")

            for topic in selected["strong_topics"]:

                st.markdown(
                    f'<div class="strength-chip">'
                    f'{html.escape(topic)}</div>',
                    unsafe_allow_html=True
                )

        st.progress(selected["current_mastery"] / 100)

        st.caption(
            f"Weekly available capacity: "
            f"{selected['weekly_minutes'] / 60:g} hours"
        )

        if len(selected["assessment_history"]) >= 2:

            st.line_chart(
                pd.DataFrame({
                    "Mastery (%)": selected["assessment_history"]
                })
            )


# =====================================================
# 13. LEARNING INSIGHTS PAGE
# =====================================================

elif page == "Learning Insights":

    show_hero(
        "ACADEMIC INTELLIGENCE",
        "See beyond the scores.",
        "Investigate mastery gaps, weak topics, trends and student risk."
    )

    if not students:

        show_empty_state(
            "No academic data available.",
            "Register students to unlock learning insights."
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
                "Target Progress": round(progress, 1),
                "Classification": classify_gap(s["mastery_gap"])
            })

        gap_df = pd.DataFrame(gap_rows)

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Average Gap",
            f"{gap_df['Gap'].mean():.1f}"
        )

        c2.metric(
            "Largest Gap",
            f"{gap_df['Gap'].max()}"
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

        st.header("Risk Detection")

        risk_rows = []

        for s in students:

            result = detect_learning_risk(s)

            risk_rows.append({
                "Student": s["name"],
                "Mastery": s["current_mastery"],
                "Gap": s["mastery_gap"],
                "Risk": result["risk"],
                "Reason": result["explanation"]
            })

        risk_df = pd.DataFrame(risk_rows)

        st.dataframe(
            risk_df,
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        st.header("Topic-Level Performance")

        topic_rows = []

        for s in students:

            for topic, score in s["topic_scores"].items():

                topic_rows.append({
                    "Student": s["name"],
                    "Topic": topic,
                    "Score": score,
                    "Performance": classify_topic_score(score)
                })

        if topic_rows:

            topic_df = pd.DataFrame(topic_rows)

            st.metric(
                "Average Topic Score",
                f"{topic_df['Score'].mean():.1f}%"
            )

            st.dataframe(
                topic_df.sort_values("Score"),
                use_container_width=True,
                hide_index=True
            )

            chart_df = topic_df.copy()

            chart_df["Topic Label"] = (
                chart_df["Student"] + " - " + chart_df["Topic"]
            )

            st.bar_chart(
                chart_df.set_index("Topic Label")[["Score"]]
            )

        st.divider()

        st.header("Learning Trend Analysis")

        trend_rows = []

        for s in students:

            result = detect_learning_trend(
                s["assessment_history"]
            )

            trend_rows.append({
                "Student": s["name"],
                "Trend": result["trend"],
                "Net Change": result["change"],
                "Explanation": result["explanation"]
            })

        st.dataframe(
            pd.DataFrame(trend_rows),
            use_container_width=True,
            hide_index=True
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
                "Segment": result["segment"],
                "Explanation": result["explanation"]
            })

        st.dataframe(
            pd.DataFrame(segment_rows),
            use_container_width=True,
            hide_index=True
        )

        st.info(
            "Analytical labels use initial project screening rules "
            "and are not validated educational predictions."
        )


# =====================================================
# 14. INTERVENTION CENTER
# =====================================================

elif page == "Intervention Center":

    show_hero(
        "INTERVENTION COMMAND CENTER",
        "Know where to focus.",
        "Prioritize potential student interventions using academic evidence."
    )

    if students:

        rows = []

        for s in students:

            result = calculate_intervention_priority(s)

            rows.append({
                "Student": s["name"],
                "ID": s["id"],
                "Mastery": s["current_mastery"],
                "Gap": s["mastery_gap"],
                "Score": result["score"],
                "Priority": result["priority"]
            })

        df = pd.DataFrame(rows).sort_values(
            "Score",
            ascending=False
        ).reset_index(drop=True)

        df.insert(0, "Rank", range(1, len(df) + 1))

        st.subheader("Ranked Intervention Queue")

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        st.bar_chart(
            df.set_index("Student")[["Score"]]
        )

        st.subheader("Decision Explanations")

        for s in students:

            result = calculate_intervention_priority(s)

            with st.expander(
                f"{s['name']} · {result['priority']}"
            ):

                st.metric(
                    "Intervention Score",
                    f"{result['score']} / 95"
                )

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

                st.info(result["recommendation"])

    else:

        show_empty_state(
            "Intervention queue is empty.",
            "Register students to generate intervention priorities."
        )


# =====================================================
# 15. MISSION 4 — STUDY PLANNER
# =====================================================

elif page == "Study Planner":

    show_hero(
        "PERSONALIZED LEARNING",
        "Design the learning week.",
        "Transform student performance data into structured "
        "weekly learning schedules."
    )

    if not students:

        show_empty_state(
            "Your study planner is waiting.",
            "Register a student before generating a personalized plan."
        )

    else:

        st.header("Create a Personalized Study Plan")

        selected_id = st.selectbox(
            "Choose a student",
            [s["id"] for s in students],
            format_func=lambda sid: next(
                f"{s['name']} · {s['id']}"
                for s in students if s["id"] == sid
            ),
            key="planner_student"
        )

        selected = next(
            s for s in students if s["id"] == selected_id
        )

        # Student planning context.

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Current Mastery",
            f"{selected['current_mastery']}%"
        )

        c2.metric(
            "Target Mastery",
            f"{selected['target_mastery']}%"
        )

        c3.metric(
            "Mastery Gap",
            f"{selected['mastery_gap']} points"
        )

        c4.metric(
            "Weekly Capacity",
            f"{selected['weekly_minutes'] / 60:g} hours"
        )

        st.divider()

        st.subheader("Topics Requiring Attention")

        topic_lookup = {
            topic.casefold(): score
            for topic, score in selected["topic_scores"].items()
        }

        weak_topics_sorted = sorted(
            selected["weak_topics"],
            key=lambda topic: topic_lookup.get(
                topic.casefold(), 50
            )
        )

        for topic in weak_topics_sorted:

            score = topic_lookup.get(topic.casefold(), 50)

            c1, c2 = st.columns([3, 1])

            c1.write(f"🔴 **{topic}**")

            c2.write(f"{score}%")

        st.divider()

        st.subheader("Weekly Availability")

        st.write(
            f"**Available days:** "
            f"{', '.join(selected['study_days'])}"
        )

        st.write(
            f"**Daily available time:** "
            f"{selected['daily_minutes']} minutes"
        )

        st.write(
            f"**Total weekly capacity:** "
            f"{selected['weekly_minutes']} minutes"
        )

        st.divider()

        st.subheader("Generate Personalized Plan")

        st.caption(
            "The generator prioritizes recorded weak topics, "
            "rotates focus across available days and creates "
            "three timed learning activities for each session."
        )

        if st.button(
            "✦ Generate Weekly Study Plan",
            use_container_width=True,
            key="generate_plan_button"
        ):

            try:

                plan = generate_study_plan(selected)

                st.session_state["study_plans"][
                    selected_id
                ] = plan

                st.success(
                    f"Weekly study plan generated for {selected['name']}!"
                )

            except ValueError as error:

                st.error(str(error))

        plan = st.session_state["study_plans"].get(
            selected_id
        )

        if plan:

            st.divider()

            st.header(
                f"📅 {plan['student_name']}'s Weekly Study Plan"
            )

            c1, c2, c3 = st.columns(3)

            c1.metric(
                "Study Days",
                len(plan["study_days"])
            )

            c2.metric(
                "Weekly Minutes",
                f"{plan['weekly_minutes']} min"
            )

            c3.metric(
                "Weekly Hours",
                f"{plan['weekly_hours']:g} hrs"
            )

            st.divider()

            st.subheader("Weekly Plan Overview")

            overview_rows = []

            for session in plan["sessions"]:

                overview_rows.append({

                    "Day": session["day"],

                    "Focus Topic": session["topic"],

                    "Topic Score": session["topic_score"],

                    "Review": session["review_minutes"],

                    "Practice": session["practice_minutes"],

                    "Knowledge Check": session["check_minutes"],

                    "Total Minutes": session["total_minutes"]

                })

            overview_df = pd.DataFrame(overview_rows)

            st.dataframe(
                overview_df,
                use_container_width=True,
                hide_index=True
            )

            st.divider()

            st.subheader("Daily Learning Sessions")

            for session in plan["sessions"]:

                with st.expander(
                    f"{session['day']} · "
                    f"{session['topic']} · "
                    f"{session['total_minutes']} minutes"
                ):

                    st.markdown(
                        f"**Daily Objective:** "
                        f"{session['objective']}"
                    )

                    st.progress(
                        session["topic_score"] / 100
                    )

                    st.caption(
                        f"Current topic assessment: "
                        f"{session['topic_score']}%"
                    )

                    for activity in session["activities"]:

                        st.markdown(
                            f"**{activity['name']}** · "
                            f"{activity['minutes']} minutes"
                        )

                        st.write(activity["instruction"])

                        st.divider()

            st.subheader("Weekly Time Distribution")

            time_data = pd.DataFrame({

                "Minutes": [
                    plan["daily_minutes"]
                    for session in plan["sessions"]
                ]

            }, index=[
                session["day"]
                for session in plan["sessions"]
            ])

            st.bar_chart(time_data)

            st.divider()

            st.subheader("Download Your Study Plan")

            text_plan = build_study_plan_text(plan)

            st.download_button(
                "📥 Download Weekly Study Plan",
                data=text_plan,
                file_name=(
                    f"Study_Plan_{selected_id}.txt"
                ),
                mime="text/plain",
                use_container_width=True
            )

            csv_plan = pd.DataFrame(
                overview_rows
            ).to_csv(
                index=False
            ).encode("utf-8-sig")

            st.download_button(
                "📊 Download Schedule as CSV",
                data=csv_plan,
                file_name=(
                    f"Weekly_Schedule_{selected_id}.csv"
                ),
                mime="text/csv",
                use_container_width=True
            )

            st.warning(
                "This is a first-version, rule-based study plan. "
                "Generated activities are instructional suggestions, "
                "not individualized question sets. Actual assignments, "
                "adaptive time allocation and LLM-generated teaching "
                "content are future development tasks."
            )

        else:

            st.info(
                "No study plan has been generated for this student yet. "
                "Click Generate Weekly Study Plan to begin."
            )


# =====================================================
# 16. PROGRESS TRACKING
# =====================================================

elif page == "Progress Tracking":

    show_hero(
        "STUDENT GROWTH",
        "Progress is a journey.",
        "Explore assessment histories and academic performance changes."
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

        history = selected["assessment_history"]

        if len(history) >= 2:

            st.subheader("Assessment History")

            history_df = pd.DataFrame({
                "Mastery (%)": history
            })

            history_df.index = [
                f"Assessment {i+1}"
                for i in range(len(history))
            ]

            st.line_chart(history_df)

            trend = detect_learning_trend(history)

            st.write("**Learning Trend:**", trend["trend"])

            st.info(trend["explanation"])

        else:

            st.info("Additional assessment data is needed.")

        st.subheader("Available Study Capacity")

        st.metric(
            "Weekly Study Capacity",
            f"{selected['weekly_minutes'] / 60:g} hours"
        )

        st.info(
            "Daily assignment completion and persistent progress "
            "tracking will be developed in Mission 6."
        )

    else:

        show_empty_state(
            "No progress records available.",
            "Register a student to view assessment history."
        )


# =====================================================
# 17. REPORTS
# =====================================================

elif page == "Reports":

    show_hero(
        "ACADEMIC REPORTING",
        "Turn data into decisions.",
        "Generate student performance reports and downloadable datasets."
    )

    if students:

        selected_id = st.selectbox(
            "Choose a student",
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

        report = build_student_report(selected)

        st.subheader("Individual Academic Report")

        with st.expander("Preview Student Report", expanded=True):

            st.text(report)

        st.download_button(
            "📥 Download Student Report",
            data=report,
            file_name=f"Academic_Report_{selected_id}.txt",
            mime="text/plain",
            use_container_width=True
        )

        st.divider()

        st.subheader("Cohort Executive Summary")

        cohort = build_cohort_report(students)

        with st.expander("Preview Cohort Report"):

            st.text(cohort)

        st.download_button(
            "📥 Download Cohort Report",
            data=cohort,
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
                "Trend": trend["trend"],
                "Segment": segment["segment"],
                "Intervention Score": intervention["score"],
                "Intervention Priority": intervention["priority"],
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
            "📊 Download Academic Dataset",
            data=csv_data,
            file_name="Academic_Performance_Data.csv",
            mime="text/csv",
            use_container_width=True
        )

    else:

        show_empty_state(
            "No reports available.",
            "Register students to generate individual and cohort reports."
        )


# =====================================================
# 18. GLOBAL FOOTER
# =====================================================

st.divider()

st.markdown("""
<div style="text-align:center;padding:15px 0 5px;">
    <div style="font-weight:800;color:#554BC0;">
        ✦ LEARNING INTELLIGENCE STUDIO
    </div>
    <div style="font-size:11px;color:#8991A8;">
        Personalized Learning · Academic Intelligence · Student Growth
    </div>
</div>
""", unsafe_allow_html=True)

st.caption(
    "Study plans use initial rule-based scheduling logic. "
    "Student information and generated plans currently use "
    "temporary Streamlit session storage. Supabase persistence "
    "and LLM integration are planned future milestones."
)


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
        115deg,#111A35,#282C68 58%,#6352C8
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
}

.strength-chip {
    background: #EAF8F2;
    color: #24775A;
    padding: 11px 14px;
    margin: 7px 0;
    border-radius: 10px;
}

.allocation-card {
    background: white;
    border: 1px solid #E6E8F1;
    padding: 15px;
    border-radius: 13px;
    margin-bottom: 9px;
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

if "study_plans" not in st.session_state:
    st.session_state["study_plans"] = {}

if not isinstance(st.session_state["students"], list):
    st.session_state["students"] = []

if not isinstance(st.session_state["study_plans"], dict):
    st.session_state["study_plans"] = {}

# Upgrade old generated study plan formats.
if any(
    not isinstance(plan, dict) or plan.get("version") != 2
    for plan in st.session_state["study_plans"].values()
):
    st.session_state["study_plans"] = {}


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
# 5. EXACT MINUTE ALLOCATION FUNCTION
# =========================================================

def allocate_minutes(total_minutes, weights):
    """
    Distribute whole minutes proportionally.

    Largest-remainder rounding ensures that the sum
    of allocated minutes equals the original total.

    Example:
    120 minutes with weights [45, 35]
    produces [68, 52].
    """

    total_minutes = int(total_minutes)

    if total_minutes < 0:
        raise ValueError("Total minutes cannot be negative.")

    if not weights:
        return []

    clean_weights = [
        max(0.0, float(weight))
        for weight in weights
    ]

    total_weight = sum(clean_weights)

    if total_weight <= 0:
        clean_weights = [1.0] * len(weights)
        total_weight = len(weights)

    exact_allocations = [
        total_minutes * weight / total_weight
        for weight in clean_weights
    ]

    allocations = [
        int(value)
        for value in exact_allocations
    ]

    remainder = total_minutes - sum(allocations)

    ranking = sorted(
        range(len(weights)),
        key=lambda index: (
            exact_allocations[index] - allocations[index],
            -index
        ),
        reverse=True
    )

    for index in ranking[:remainder]:
        allocations[index] += 1

    assert sum(allocations) == total_minutes

    return allocations


# =========================================================
# 6. SPLIT TOPIC TIME INTO LEARNING ACTIVITIES
# =========================================================

def split_activity_minutes(topic_minutes):

    if topic_minutes <= 0:
        return []

    # Review: 20%, Practice: 60%, Check: 20%.
    allocation = allocate_minutes(
        topic_minutes,
        [20, 60, 20]
    )

    activities = [
        {
            "name": "Concept Review",
            "minutes": allocation[0],
            "instruction": (
                "Review important concepts, definitions and "
                "worked examples."
            )
        },
        {
            "name": "Guided Practice",
            "minutes": allocation[1],
            "instruction": (
                "Solve structured problems, show working and "
                "practice the topic independently."
            )
        },
        {
            "name": "Knowledge Check",
            "minutes": allocation[2],
            "instruction": (
                "Complete a short retrieval check and explain "
                "the reasoning behind an answer."
            )
        }
    ]

    return [
        activity for activity in activities
        if activity["minutes"] > 0
    ]


# =========================================================
# 7. ACADEMIC INTELLIGENCE ENGINES
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
            "Targeted practice may address learning needs."
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


# =========================================================
# 8. MISSION 4 — INTELLIGENT STUDY TIME ALLOCATION
# =========================================================

TOPIC_BENCHMARK = 80


def calculate_topic_weights(student):
    """
    Calculate how much time each weak topic should receive.

    Higher topic gaps receive higher weights.

    Example:
    Fractions 35% -> weight 45
    Decimals 45% -> weight 35
    """

    scores = {
        topic.casefold(): score
        for topic, score in student["topic_scores"].items()
    }

    topics = student["weak_topics"]

    if not topics:
        raise ValueError("No weak topics recorded.")

    weights = []

    for topic in topics:

        score = scores.get(
            topic.casefold(),
            50
        )

        topic_gap = max(
            TOPIC_BENCHMARK - score,
            1
        )

        weights.append(topic_gap)

    return weights


def generate_study_plan(student):
    """
    Generate an individualized weekly schedule.

    The plan:
    1. Prioritizes the weakest topics.
    2. Calculates proportional topic weights.
    3. Allocates available minutes exactly.
    4. Splits topic time into learning activities.
    5. Repeats the allocation on each selected study day.
    """

    days = student["study_days"]
    daily_minutes = student["daily_minutes"]

    if not days:
        raise ValueError("Student has no available study days.")

    if daily_minutes < 15:
        raise ValueError("Daily study time is insufficient.")

    topics = student["weak_topics"]

    if not topics:
        raise ValueError("No weak topics recorded.")

    topic_scores = {
        topic.casefold(): score
        for topic, score in student["topic_scores"].items()
    }

    # Calculate proportional topic weights.
    weights = calculate_topic_weights(student)

    # Allocate the entire daily study budget.
    daily_allocations = allocate_minutes(
        daily_minutes,
        weights
    )

    # Calculate each topic's weekly allocation.
    weekly_topic_minutes = {
        topic: minutes * len(days)
        for topic, minutes in zip(topics, daily_allocations)
    }

    sessions = []

    for day in days:

        topic_allocations = []

        for topic, weight, minutes in zip(
            topics,
            weights,
            daily_allocations
        ):

            score = topic_scores.get(
                topic.casefold(),
                50
            )

            if score < 40:

                objective = (
                    f"Rebuild foundational understanding of {topic}. "
                    "Review concepts and explain worked examples."
                )

            elif score < 60:

                objective = (
                    f"Strengthen {topic} using worked examples "
                    "and structured problem solving."
                )

            else:

                objective = (
                    f"Improve accuracy in {topic} through "
                    "mixed problem solving and retrieval practice."
                )

            activities = split_activity_minutes(minutes)

            topic_allocations.append({

                "topic": topic,

                "score": score,

                "weight": weight,

                "minutes": minutes,

                "objective": objective,

                "activities": activities

            })

        day_total = sum(
            item["minutes"]
            for item in topic_allocations
        )

        # Quality check: each day must use exactly its budget.
        assert day_total == daily_minutes

        sessions.append({

            "day": day,

            "topic_allocations": topic_allocations,

            "total_minutes": day_total

        })

    weekly_total = sum(
        session["total_minutes"]
        for session in sessions
    )

    assert weekly_total == daily_minutes * len(days)

    return {

        "version": 2,

        "student_id": student["id"],

        "student_name": student["name"],

        "subject": student["subject"],

        "current_mastery": student["current_mastery"],

        "target_mastery": student["target_mastery"],

        "mastery_gap": student["mastery_gap"],

        "daily_minutes": daily_minutes,

        "study_days": days.copy(),

        "sessions": sessions,

        "daily_topic_minutes": dict(
            zip(topics, daily_allocations)
        ),

        "weekly_topic_minutes": weekly_topic_minutes,

        "topic_weights": dict(zip(topics, weights)),

        "weekly_minutes": weekly_total,

        "weekly_hours": weekly_total / 60,

        "allocation_method": (
            "Proportional allocation based on the topic gap "
            "from the 80% topic proficiency benchmark."
        )

    }


# =========================================================
# 9. STUDY PLAN TEXT EXPORT
# =========================================================

def build_study_plan_text(plan):

    lines = [

        "LEARNING INTELLIGENCE STUDIO",
        "PERSONALIZED WEEKLY STUDY PLAN",
        "=" * 60,

        "",

        f"Student: {plan['student_name']}",
        f"Student ID: {plan['student_id']}",
        f"Subject: {plan['subject']}",

        f"Current Mastery: {plan['current_mastery']}%",
        f"Target Mastery: {plan['target_mastery']}%",
        f"Mastery Gap: {plan['mastery_gap']} points",

        "",

        f"Daily Capacity: {plan['daily_minutes']} minutes",
        f"Weekly Capacity: {plan['weekly_minutes']} minutes",
        f"Weekly Hours: {plan['weekly_hours']:g}",

        "",
        "TIME ALLOCATION METHOD",
        plan["allocation_method"],

        "",
        "WEEKLY TOPIC ALLOCATION",
        "=" * 60

    ]

    for topic, minutes in plan["weekly_topic_minutes"].items():

        lines.append(
            f"{topic}: {minutes} minutes per week"
        )

    for session in plan["sessions"]:

        lines.extend([

            "",
            "=" * 60,
            session["day"].upper(),
            f"Total Study Time: {session['total_minutes']} minutes",
            "=" * 60

        ])

        for item in session["topic_allocations"]:

            lines.extend([

                "",
                f"TOPIC: {item['topic']}",

                f"Assessment Score: {item['score']}%",

                f"Topic Weight: {item['weight']}",

                f"Allocated Minutes: {item['minutes']}",

                f"Learning Objective: {item['objective']}",

                "ACTIVITIES:"

            ])

            for activity in item["activities"]:

                lines.append(
                    f"{activity['name']}: {activity['minutes']} minutes"
                )

                lines.append(
                    activity["instruction"]
                )

    lines.extend([

        "",
        "=" * 60,
        "PLAN NOTES",
        "Time allocation uses transparent Python decision rules.",
        "The topic benchmark is an initial project setting of 80%.",
        "Minute totals are rounded using the largest-remainder method.",
        "The generated activities are instructional suggestions.",
        "Teacher review is required before applying the schedule.",
        "",
        "END OF STUDY PLAN"

    ])

    return "\n".join(lines)


# =========================================================
# 10. MIGRATE OLD STUDENT RECORDS
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


# =========================================================
# 11. REPORT FUNCTIONS
# =========================================================

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
        f"Score: {intervention['score']}/95",
        f"Priority: {intervention['priority']}",
        f"Recommendation: {intervention['recommendation']}",

        "",
        "WEEKLY STUDY AVAILABILITY",
        f"Daily Minutes: {student['daily_minutes']}",
        f"Available Days: {', '.join(student['study_days'])}",
        f"Weekly Hours: {student['weekly_minutes'] / 60:g}",

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

    ranked = sorted(
        records,
        key=lambda s: calculate_intervention_priority(s)["score"],
        reverse=True
    )

    lines = [

        "LEARNING INTELLIGENCE STUDIO",
        "COHORT PERFORMANCE SUMMARY",
        "=" * 55,

        "",
        f"Total Students: {total}",
        f"Average Mastery: {average:.1f}%",
        f"Average Mastery Gap: {average_gap:.1f} points",

        "",
        "INTERVENTION RANKING"

    ]

    for index, student in enumerate(ranked[:5], 1):

        result = calculate_intervention_priority(student)

        lines.append(
            f"{index}. {student['name']} - "
            f"{result['score']}/95 - {result['priority']}"
        )

    return "\n".join(lines)


# =========================================================
# 12. DISPLAY HELPERS
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


# =========================================================
# 13. SIDEBAR NAVIGATION
# =========================================================

with st.sidebar:

    st.markdown("""
    <div style="padding:12px 3px 23px;">
        <div style="font-size:32px;">✦</div>

        <div style="
            font-size:18px;
            font-weight:850;
            color:#FFFFFF;
        ">
            LEARNING STUDIO
        </div>

        <div style="
            font-size:10px;
            letter-spacing:2px;
            color:#AFA5F4;
        ">
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

    st.metric("Students Tracked", len(students))

    st.metric(
        "Study Plans Generated",
        len(st.session_state["study_plans"])
    )

    st.caption("Cloud-hosted application")

    st.divider()

    st.caption("LEARNING INTELLIGENCE STUDIO")
    st.caption("Portfolio Edition")


# =========================================================
# 14. OVERVIEW PAGE
# =========================================================

if page == "Overview":

    show_hero(
        "YOUR ACADEMIC COMMAND CENTER",
        "Understand. Improve. Master.",
        "Discover learning gaps, monitor performance and "
        "turn academic data into personalized learning journeys."
    )

    if students:

        average = sum(
            s["current_mastery"] for s in students
        ) / len(students)

        high_risk = sum(
            detect_learning_risk(s)["risk"] == "HIGH"
            for s in students
        )

        achieved = sum(
            s["current_mastery"] >= s["target_mastery"]
            for s in students
        )

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Students Tracked", len(students))
        c2.metric("Average Mastery", f"{average:.1f}%")
        c3.metric("High Screening Risk", high_risk)
        c4.metric("Study Plans", len(st.session_state["study_plans"]))

        st.divider()

        left, right = st.columns([1.3, 1])

        with left:

            st.subheader("Academic Mastery")

            mastery_df = pd.DataFrame([
                {
                    "Student": s["name"],
                    "Current": s["current_mastery"],
                    "Target": s["target_mastery"]
                }
                for s in students
            ]).set_index("Student")

            st.bar_chart(mastery_df)

        with right:

            st.subheader("Learning Trends")

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

        st.subheader("Recent Learners")

        for student in students[-5:][::-1]:

            with st.expander(
                f"{student['name']} · {student['id']}"
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
        c2.metric("Plans Generated", 0)
        c3.metric("Learning Insights", 0)

        show_empty_state(
            "Your learning workspace is ready.",
            "Open Students to register your first learner."
        )


# =========================================================
# 15. STUDENTS PAGE
# =========================================================

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
            name = st.text_input("Student Name")

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
            current = st.number_input(
                "Current Mastery (%)",
                0, 100, 42
            )

        with c2:
            target = st.number_input(
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
            "Topic: Score",
            "Fractions: 35, Decimals: 45, Percentages: 85, Basic arithmetic: 90"
        )

        st.subheader("Historical Assessments")

        history_input = st.text_input(
            "Scores from oldest to newest",
            "30, 36, 42"
        )

        st.subheader("Study Availability")

        daily = st.number_input(
            "Daily Study Minutes",
            15, 240, 120, step=15
        )

        days = st.multiselect(
            "Available Study Days",
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

            clean_name = name.strip()
            clean_id = student_id.strip().upper()

            weak = parse_topics(weak_input)
            strong = parse_topics(strong_input)

            scores, score_errors = parse_topic_scores(topic_input)

            history, history_errors = parse_assessment_history(
                history_input
            )

            overlap = (
                {x.casefold() for x in weak}
                & {x.casefold() for x in strong}
            )

            existing = {
                s["id"].casefold() for s in students
            }

            score_lookup = {
                topic.casefold() for topic in scores
            }

            missing = [
                topic for topic in weak + strong
                if topic.casefold() not in score_lookup
            ]

            if not clean_name or not clean_id:

                st.error("Enter student name and ID.")

            elif clean_id.casefold() in existing:

                st.error("Student ID already exists.")

            elif not weak or not strong:

                st.error("Enter weak and strong topics.")

            elif overlap:

                st.error("A topic cannot be both weak and strong.")

            elif score_errors:

                for error in score_errors:
                    st.error(error)

            elif missing:

                st.error(
                    "Enter scores for: " + ", ".join(missing)
                )

            elif history_errors:

                for error in history_errors:
                    st.error(error)

            elif len(history) < 2:

                st.error("Enter at least two assessment scores.")

            elif abs(history[-1] - current) > 0.01:

                st.error(
                    "Latest assessment score must match current mastery."
                )

            elif not days:

                st.error("Select at least one study day.")

            else:

                student = {

                    "name": clean_name,
                    "id": clean_id,
                    "subject": subject,

                    "current_mastery": current,
                    "target_mastery": target,

                    "mastery_gap": max(target - current, 0),

                    "priority": classify_priority(current, target),

                    "weak_topics": weak,
                    "strong_topics": strong,

                    "topic_scores": scores,
                    "assessment_history": history,

                    "daily_minutes": daily,
                    "study_days": days,

                    "weekly_minutes": daily * len(days)

                }

                st.session_state["students"].append(student)

                st.success(
                    f"{clean_name} registered successfully!"
                )

    if students:

        st.divider()

        st.subheader("Registered Students")

        table = pd.DataFrame([
            {
                "Student": s["name"],
                "ID": s["id"],
                "Subject": s["subject"],
                "Mastery": s["current_mastery"],
                "Target": s["target_mastery"],
                "Gap": s["mastery_gap"],
                "Priority": s["priority"]
            }
            for s in students
        ])

        st.dataframe(
            table,
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        st.header("✨ Interactive Student Spotlight")

        selected_id = st.selectbox(
            "Choose Student",
            [s["id"] for s in students],
            format_func=lambda sid: next(
                f"{s['name']} · {s['id']}"
                for s in students if s["id"] == sid
            )
        )

        selected = next(
            s for s in students if s["id"] == selected_id
        )

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

                <div style="color:#D6DBF5;">
                    {html.escape(selected['id'])}
                    · {html.escape(selected['subject'])}
                </div>

                <div style="
                    color:#83E1C1;
                    margin-top:15px;
                    font-size:12px;
                    font-weight:700;
                ">✦ PERSONALIZED LEARNING PROFILE</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Mastery", f"{selected['current_mastery']}%")
        c2.metric("Target", f"{selected['target_mastery']}%")
        c3.metric("Gap", f"{selected['mastery_gap']} points")

        c4.metric(
            "Intervention",
            f"{calculate_intervention_priority(selected)['score']}/95"
        )

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


# =========================================================
# 16. LEARNING INSIGHTS PAGE
# =========================================================

elif page == "Learning Insights":

    show_hero(
        "ACADEMIC INTELLIGENCE",
        "See beyond the scores.",
        "Understand mastery gaps, topic performance, trends and risk."
    )

    if not students:

        show_empty_state(
            "No academic information available.",
            "Register students to activate learning insights."
        )

    else:

        st.header("Learning Gap Analysis")

        gap_data = []

        for s in students:

            progress = (
                min(
                    s["current_mastery"] / s["target_mastery"] * 100,
                    100
                )
                if s["target_mastery"] > 0 else 100
            )

            gap_data.append({

                "Student": s["name"],
                "Current Mastery": s["current_mastery"],
                "Target": s["target_mastery"],
                "Gap": s["mastery_gap"],
                "Target Progress (%)": round(progress, 1),
                "Classification": classify_gap(s["mastery_gap"])

            })

        gap_df = pd.DataFrame(gap_data)

        c1, c2, c3 = st.columns(3)

        c1.metric("Average Gap", f"{gap_df['Gap'].mean():.1f} points")
        c2.metric("Largest Gap", f"{gap_df['Gap'].max()} points")
        c3.metric(
            "Large Gaps",
            int((gap_df["Classification"] == "LARGE GAP").sum())
        )

        st.dataframe(
            gap_df,
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        st.header("Topic-Level Analysis")

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

            st.dataframe(
                topic_df.sort_values("Score"),
                use_container_width=True,
                hide_index=True
            )

            chart = topic_df.copy()

            chart["Topic Label"] = (
                chart["Student"] + " - " + chart["Topic"]
            )

            st.bar_chart(
                chart.set_index("Topic Label")[["Score"]]
            )

        st.divider()

        st.header("Learning Risk and Trends")

        for s in students:

            with st.expander(f"{s['name']} · {s['id']}"):

                risk = detect_learning_risk(s)

                trend = detect_learning_trend(
                    s["assessment_history"]
                )

                segment = classify_student_segment(s)

                c1, c2, c3 = st.columns(3)

                c1.metric("Risk", risk["risk"])
                c2.metric("Trend", trend["trend"])
                c3.metric("Segment", segment["segment"])

                st.write(risk["explanation"])
                st.write(trend["explanation"])
                st.write(segment["explanation"])


# =========================================================
# 17. INTERVENTION CENTER
# =========================================================

elif page == "Intervention Center":

    show_hero(
        "INTERVENTION COMMAND CENTER",
        "Know where to focus.",
        "Rank potential interventions using academic evidence."
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
                    f"Gap: {result['gap_points']} / 40"
                )

                st.write(
                    f"Mastery: {result['mastery_points']} / 20"
                )

                st.write(
                    f"Trend: {result['trend_points']} / 20"
                )

                st.write(
                    f"Topics: {result['topic_points']} / 15"
                )

                st.info(result["recommendation"])

    else:

        show_empty_state(
            "No intervention records.",
            "Register students to create the intervention queue."
        )


# =========================================================
# 18. STUDY PLANNER — INTELLIGENT TIME ALLOCATION
# =========================================================

elif page == "Study Planner":

    show_hero(
        "PERSONALIZED LEARNING",
        "Every minute has a purpose.",
        "Allocate study time according to topic-level learning gaps."
    )

    st.markdown(
        """
        <div class="info-card">
            <h4>✦ Intelligent Allocation Engine</h4>
            <p>
                The engine compares each weak topic against an
                initial 80% proficiency benchmark. Topics with
                larger gaps receive a larger share of available time.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if not students:

        show_empty_state(
            "Your study planner is waiting.",
            "Register a student to create a personalized weekly plan."
        )

    else:

        selected_id = st.selectbox(
            "Choose a Student",
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
            "Daily Capacity",
            f"{selected['daily_minutes']} min"
        )

        c4.metric(
            "Weekly Capacity",
            f"{selected['weekly_minutes']} min"
        )

        st.divider()

        st.subheader("1. Topic Gap and Weight Analysis")

        weights = calculate_topic_weights(selected)

        weight_rows = []

        for topic, weight in zip(
            selected["weak_topics"],
            weights
        ):

            score_lookup = {
                t.casefold(): score
                for t, score in selected["topic_scores"].items()
            }

            score = score_lookup.get(
                topic.casefold(),
                50
            )

            weight_rows.append({

                "Weak Topic": topic,
                "Assessment Score (%)": score,
                "Benchmark Gap": max(TOPIC_BENCHMARK - score, 1),
                "Allocation Weight": weight

            })

        weight_df = pd.DataFrame(weight_rows)

        st.dataframe(
            weight_df,
            use_container_width=True,
            hide_index=True
        )

        st.caption(
            "Higher allocation weight means a larger share "
            "of the available study time."
        )

        st.divider()

        st.subheader("2. Daily Intelligent Time Allocation")

        daily_allocations = allocate_minutes(
            selected["daily_minutes"],
            weights
        )

        daily_topic_df = pd.DataFrame({

            "Topic": selected["weak_topics"],

            "Allocation Weight": weights,

            "Daily Minutes": daily_allocations,

            "Weekly Minutes": [
                minutes * len(selected["study_days"])
                for minutes in daily_allocations
            ]

        })

        st.dataframe(
            daily_topic_df,
            use_container_width=True,
            hide_index=True
        )

        st.bar_chart(
            daily_topic_df.set_index("Topic")[["Daily Minutes"]]
        )

        st.success(
            f"All {sum(daily_allocations)} daily minutes "
            f"have been allocated across {len(selected['weak_topics'])} topics."
        )

        st.divider()

        st.subheader("3. Generate Personalized Weekly Plan")

        if st.button(
            "✦ Generate Intelligent Study Plan",
            use_container_width=True
        ):

            try:

                plan = generate_study_plan(selected)

                st.session_state["study_plans"][selected_id] = plan

                st.success(
                    f"Intelligent study plan generated for "
                    f"{selected['name']}!"
                )

            except (ValueError, AssertionError) as error:

                st.error(str(error))

        plan = st.session_state["study_plans"].get(selected_id)

        if plan and plan.get("version") != 2:

            st.session_state["study_plans"].pop(
                selected_id,
                None
            )

            plan = None

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
                plan["weekly_minutes"]
            )

            c3.metric(
                "Weekly Hours",
                f"{plan['weekly_hours']:g}"
            )

            st.divider()

            st.subheader("Weekly Topic Allocation")

            weekly_rows = []

            for topic, minutes in plan["weekly_topic_minutes"].items():

                weekly_rows.append({

                    "Topic": topic,

                    "Daily Minutes": plan["daily_topic_minutes"][topic],

                    "Weekly Minutes": minutes,

                    "Allocation Weight": plan["topic_weights"][topic]

                })

            weekly_df = pd.DataFrame(weekly_rows)

            st.dataframe(
                weekly_df,
                use_container_width=True,
                hide_index=True
            )

            st.bar_chart(
                weekly_df.set_index("Topic")[["Weekly Minutes"]]
            )

            st.divider()

            st.subheader("Daily Learning Schedule")

            for session in plan["sessions"]:

                with st.expander(
                    f"{session['day']} · "
                    f"{session['total_minutes']} minutes",
                    expanded=True
                ):

                    for item in session["topic_allocations"]:

                        st.markdown(
                            f"""
                            <div class="allocation-card">
                                <strong>
                                    {html.escape(item['topic'])}
                                </strong>
                                <div style="
                                    color:#6D7390;
                                    font-size:12px;
                                    margin-top:5px;
                                ">
                                    Assessment: {item['score']}%
                                    · Allocation Weight: {item['weight']}
                                    · Study Time: {item['minutes']} minutes
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                        st.progress(
                            item["minutes"] / plan["daily_minutes"]
                        )

                        st.write(
                            f"**Learning Objective:** {item['objective']}"
                        )

                        for activity in item["activities"]:

                            st.markdown(
                                f"**{activity['name']}** "
                                f"· {activity['minutes']} minutes"
                            )

                            st.caption(activity["instruction"])

                        st.divider()

                    assert session["total_minutes"] == plan["daily_minutes"]

            st.success(
                f"Verified: every study day uses exactly "
                f"{plan['daily_minutes']} minutes. "
                f"Weekly total: {plan['weekly_minutes']} minutes."
            )

            st.divider()

            st.subheader("Download Your Personalized Plan")

            text_plan = build_study_plan_text(plan)

            st.download_button(
                "📥 Download Weekly Study Plan",
                data=text_plan,
                file_name=f"Study_Plan_{selected_id}.txt",
                mime="text/plain",
                use_container_width=True
            )

            csv_rows = []

            for session in plan["sessions"]:

                for item in session["topic_allocations"]:

                    activity_names = []

                    for activity in item["activities"]:

                        activity_names.append(
                            f"{activity['name']}: "
                            f"{activity['minutes']} min"
                        )

                    csv_rows.append({

                        "Day": session["day"],
                        "Topic": item["topic"],
                        "Assessment Score": item["score"],
                        "Allocation Weight": item["weight"],
                        "Topic Minutes": item["minutes"],
                        "Activities": " | ".join(activity_names)

                    })

            csv_plan = pd.DataFrame(csv_rows).to_csv(
                index=False
            ).encode("utf-8-sig")

            st.download_button(
                "📊 Download Detailed Schedule (CSV)",
                data=csv_plan,
                file_name=f"Detailed_Study_Plan_{selected_id}.csv",
                mime="text/csv",
                use_container_width=True
            )

            st.info(
                "This version uses rule-based proportional scheduling. "
                "The 80% topic benchmark is a configurable project "
                "assumption, not a validated educational standard. "
                "LLM-generated content and adaptive rescheduling "
                "will be developed in later tasks."
            )

        else:

            st.info(
                "No study plan has been generated for this student. "
                "Click Generate Intelligent Study Plan."
            )


# =========================================================
# 19. PROGRESS TRACKING
# =========================================================

elif page == "Progress Tracking":

    show_hero(
        "STUDENT GROWTH",
        "Progress is a journey.",
        "Explore assessment histories and understand performance changes."
    )

    if students:

        selected_id = st.selectbox(
            "Choose Student",
            [s["id"] for s in students],
            format_func=lambda sid: next(
                f"{s['name']} · {s['id']}"
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

            history_df = pd.DataFrame({
                "Mastery (%)": history
            })

            history_df.index = [
                f"Assessment {i+1}"
                for i in range(len(history))
            ]

            st.line_chart(history_df)

        trend = detect_learning_trend(history)

        st.subheader("Learning Trend")

        st.write(trend["trend"])

        st.info(trend["explanation"])

        if selected_id in st.session_state["study_plans"]:

            st.divider()

            st.subheader("Generated Study Plan")

            st.success("A study plan exists for this student.")

            st.write(
                st.session_state["study_plans"][selected_id][
                    "weekly_minutes"
                ],
                "weekly study minutes allocated."
            )

        else:

            st.info("No study plan has been generated yet.")

    else:

        show_empty_state(
            "No progress records available.",
            "Register students to inspect assessment history."
        )


# =========================================================
# 20. REPORTS
# =========================================================

elif page == "Reports":

    show_hero(
        "ACADEMIC REPORTING",
        "Turn data into decisions.",
        "Generate student performance reports and downloadable datasets."
    )

    if students:

        selected_id = st.selectbox(
            "Select Student",
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

        with st.expander("Preview Report", expanded=True):

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

        st.subheader("Academic Dataset")

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
                "ID": s["id"],
                "Subject": s["subject"],
                "Current Mastery": s["current_mastery"],
                "Target Mastery": s["target_mastery"],
                "Mastery Gap": s["mastery_gap"],
                "Priority": s["priority"],
                "Risk": risk["risk"],
                "Trend": trend["trend"],
                "Segment": segment["segment"],
                "Intervention Score": intervention["score"]

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


# =========================================================
# 21. GLOBAL FOOTER
# =========================================================

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
    "Intelligent time allocation uses transparent proportional "
    "Python rules. Student and study-plan data remain temporary "
    "in Streamlit session memory. Supabase persistence and "
    "LLM-generated learning content are future milestones."
)

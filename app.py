
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
# 6. TOPIC PERFORMANCE CLASSIFICATION
# ==========================================

def classify_topic_score(score):

    if score < 60:
        return "NEEDS SUPPORT"

    elif score < 80:
        return "DEVELOPING"

    else:
        return "STRONG"


# ==========================================
# 7. LEARNING RISK DETECTION
# ==========================================

def detect_learning_risk(student):

    mastery = student["current_mastery"]
    gap = student["mastery_gap"]

    if mastery < 40 or gap >= 35:

        return {
            "risk": "HIGH",
            "explanation": (
                "Low current mastery or a substantial "
                "remaining mastery gap."
            )
        }

    elif mastery < 60 or gap >= 20:

        return {
            "risk": "MODERATE",
            "explanation": (
                "Targeted practice and closer monitoring "
                "may be beneficial."
            )
        }

    return {
        "risk": "LOW",
        "explanation": (
            "Lower immediate concern based on current "
            "mastery and mastery gap."
        )
    }


# ==========================================
# 8. LEARNING TREND DETECTION
# ==========================================

def detect_learning_trend(history):

    if len(history) < 2:

        return {
            "trend": "INSUFFICIENT DATA",
            "change": None,
            "explanation": (
                "At least two assessment scores are needed."
            )
        }

    change = round(
        history[-1] - history[0], 1
    )

    if change >= 5:

        trend = "IMPROVING"
        explanation = (
            f"Performance increased by {change} percentage points."
        )

    elif change <= -5:

        trend = "DECLINING"
        explanation = (
            f"Performance decreased by {abs(change)} percentage points."
        )

    else:

        trend = "STABLE"
        explanation = (
            "Net performance change is less than 5 percentage points."
        )

    return {
        "trend": trend,
        "change": change,
        "explanation": explanation
    }


# ==========================================
# 9. STUDENT SEGMENTATION
# ==========================================

def classify_student_segment(student):

    risk_result = detect_learning_risk(student)

    trend_result = detect_learning_trend(
        student["assessment_history"]
    )

    current = student["current_mastery"]
    target = student["target_mastery"]

    support_topics = sum(
        classify_topic_score(score) == "NEEDS SUPPORT"
        for score in student["topic_scores"].values()
    )

    risk = risk_result["risk"]
    trend = trend_result["trend"]

    if current >= target:

        segment = "ENRICHMENT"

        explanation = (
            "Target achieved. Consider advanced learning activities."
        )

    elif risk == "HIGH":

        segment = "INTENSIVE SUPPORT"

        explanation = (
            "Substantial learning gap or low current mastery."
        )

    elif (
        risk == "MODERATE"
        or trend == "DECLINING"
        or support_topics >= 2
    ):

        segment = "TARGETED SUPPORT"

        explanation = (
            "Targeted practice may be useful based on "
            "risk, learning trends or topic-level performance."
        )

    else:

        segment = "PROGRESS MONITORING"

        explanation = (
            "Continue routine monitoring and regular assessments."
        )

    return {
        "segment": segment,
        "risk": risk,
        "trend": trend,
        "support_topics": support_topics,
        "explanation": explanation
    }


# ==========================================
# 10. INTERVENTION PRIORITIZATION ENGINE
# ==========================================

def calculate_intervention_priority(student):

    current = student["current_mastery"]
    target = student["target_mastery"]
    gap = student["mastery_gap"]

    history = student["assessment_history"]
    topic_scores = student["topic_scores"]

    # Students who achieved their target.
    if current >= target:

        return {
            "score": 0,
            "priority": "P4 - MONITOR",
            "gap_points": 0,
            "mastery_points": 0,
            "trend_points": 0,
            "topic_points": 0,
            "support_topics": 0,
            "recommendation": (
                "Target achieved. Consider enrichment activities "
                "and periodic reassessment."
            )
        }

    # Factor 1: Mastery gap (maximum 40 points).
    gap_points = min(gap, 40)

    # Factor 2: Current mastery (maximum 20 points).
    if current < 40:
        mastery_points = 20

    elif current < 60:
        mastery_points = 15

    elif current < 80:
        mastery_points = 8

    else:
        mastery_points = 0

    # Factor 3: Learning trend (maximum 20 points).
    trend_result = detect_learning_trend(history)

    if trend_result["trend"] == "DECLINING":
        trend_points = 20

    elif trend_result["trend"] == "STABLE":
        trend_points = 10

    elif trend_result["trend"] == "INSUFFICIENT DATA":
        trend_points = 8

    else:
        trend_points = 0

    # Factor 4: Topic-level weaknesses (maximum 15 points).
    support_topics = sum(
        classify_topic_score(score) == "NEEDS SUPPORT"
        for score in topic_scores.values()
    )

    topic_points = min(
        support_topics * 5,
        15
    )

    # Calculate final score.
    total_score = (
        gap_points
        + mastery_points
        + trend_points
        + topic_points
    )

    # Assign intervention priority.
    if total_score >= 65:

        priority = "P1 - URGENT"

        recommendation = (
            "Arrange prompt teacher investigation, review "
            "foundational concepts and design an individualized "
            "intervention."
        )

    elif total_score >= 45:

        priority = "P2 - HIGH"

        recommendation = (
            "Schedule targeted practice, investigate weak topics "
            "and reassess learning progress."
        )

    elif total_score >= 25:

        priority = "P3 - SCHEDULED"

        recommendation = (
            "Schedule focused learning support and monitor "
            "the next assessment."
        )

    else:

        priority = "P4 - MONITOR"

        recommendation = (
            "Continue regular progress monitoring and "
            "provide additional practice when needed."
        )

    return {

        "score": total_score,

        "priority": priority,

        "gap_points": gap_points,

        "mastery_points": mastery_points,

        "trend_points": trend_points,

        "topic_points": topic_points,

        "support_topics": support_topics,

        "recommendation": recommendation

    }


# ==========================================
# 11. OLD RECORD MIGRATION
# ==========================================

def migrate_records(records):

    upgraded = []

    valid_days = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ]

    for old in records:

        if not isinstance(old, dict):
            continue

        student = dict(old)

        student["name"] = str(
            student.get("name", "Unknown")
        )

        student["id"] = str(
            student.get("id", "")
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
                number = float(score)

                if 0 <= number <= 100:
                    valid_scores[str(topic)] = number

            except (TypeError, ValueError):
                continue

        student["topic_scores"] = valid_scores

        raw_history = student.get(
            "assessment_history", []
        )

        if not isinstance(raw_history, list):
            raw_history = []

        valid_history = []

        for score in raw_history:

            try:
                number = float(score)

                if 0 <= number <= 100:
                    valid_history.append(number)

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


# ==========================================
# 12. APPLICATION HEADER
# ==========================================

st.title("📚 AI Study Plan Generator")

st.caption(
    "An intelligent platform for personalized and adaptive learning."
)

st.divider()


# ==========================================
# 13. STUDENT REGISTRATION
# ==========================================

st.header("👩‍🎓 Student Registration")

with st.form("student_registration"):

    col1, col2 = st.columns(2)

    with col1:
        student_name = st.text_input("Student Name")

    with col2:
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

    st.subheader("📊 Academic Performance")

    col1, col2 = st.columns(2)

    with col1:
        current_mastery = st.number_input(
            "Current Mastery (%)",
            0, 100, 42
        )

    with col2:
        target_mastery = st.number_input(
            "Target Mastery (%)",
            0, 100, 80
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

    st.subheader("📝 Topic Assessment Scores")

    topic_scores_input = st.text_area(
        "Topic scores",
        placeholder=(
            "Fractions: 35, Decimals: 45, "
            "Percentages: 85, Basic arithmetic: 90"
        )
    )

    st.subheader("📈 Historical Assessment Scores")

    history_input = st.text_input(
        "Scores from oldest to newest",
        placeholder="30, 36, 42"
    )

    st.subheader("⏰ Study Availability")

    daily_minutes = st.number_input(
        "Daily Study Time (minutes)",
        15, 240, 120, step=15
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
            s["id"].casefold()
            for s in st.session_state["students"]
        }

        score_lookup = {
            topic.casefold() for topic in topic_scores
        }

        missing_scores = [
            topic for topic in weak_topics + strong_topics
            if topic.casefold() not in score_lookup
        ]

        if not name or not clean_id:

            st.error("Student name and ID are required.")

        elif clean_id.casefold() in existing_ids:

            st.error("Student ID already exists.")

        elif not weak_topics or not strong_topics:

            st.error("Enter weak and strong topics.")

        elif overlap:

            st.error("A topic cannot be both weak and strong.")

        elif target_mastery < current_mastery:

            st.error(
                "Target mastery cannot be lower than current mastery."
            )

        elif score_errors:

            for error in score_errors:
                st.error(error)

        elif history_errors:

            for error in history_errors:
                st.error(error)

        elif missing_scores:

            st.error(
                "Missing topic scores for: "
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


# ==========================================
# 14. ACADEMIC PERFORMANCE DASHBOARD
# ==========================================

students = st.session_state["students"]

st.divider()

st.header("📊 Academic Performance Dashboard")

if students:

    total = len(students)

    average = sum(
        s["current_mastery"] for s in students
    ) / total

    urgent = sum(
        s["priority"] == "URGENT" for s in students
    )

    high = sum(
        s["priority"] == "HIGH" for s in students
    )

    moderate = sum(
        s["priority"] == "MODERATE" for s in students
    )

    achieved = sum(
        s["priority"] == "TARGET ACHIEVED"
        for s in students
    )

    c1, c2, c3 = st.columns(3)

    c1.metric("Total Students", total)
    c2.metric("Average Mastery", f"{average:.1f}%")
    c3.metric("Urgent Students", urgent)

    c1, c2, c3 = st.columns(3)

    c1.metric("High Priority", high)
    c2.metric("Moderate Priority", moderate)
    c3.metric("Target Achieved", achieved)

    st.subheader("Student Priority Analysis")

    priority_data = [
        {
            "Student": s["name"],
            "ID": s["id"],
            "Mastery": s["current_mastery"],
            "Target": s["target_mastery"],
            "Gap": s["mastery_gap"],
            "Priority": s["priority"]
        }
        for s in students
    ]

    st.dataframe(
        pd.DataFrame(priority_data),
        use_container_width=True,
        hide_index=True
    )


    # ======================================
    # 15. LEARNING GAP ANALYSIS
    # ======================================

    st.divider()
    st.header("🧠 Learning Gap Analysis")

    gap_data = []

    for s in students:

        current = s["current_mastery"]
        target = s["target_mastery"]

        progress = (
            min(current / target * 100, 100)
            if target > 0 else 100
        )

        gap_data.append({

            "Student": s["name"],
            "Current Mastery": current,
            "Target Mastery": target,
            "Mastery Gap": s["mastery_gap"],
            "Target Progress (%)": round(progress, 1),
            "Gap Classification": classify_gap(
                s["mastery_gap"]
            )

        })

    gap_df = pd.DataFrame(gap_data)

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Average Gap",
        f"{gap_df['Mastery Gap'].mean():.1f} points"
    )

    c2.metric(
        "Largest Gap",
        f"{gap_df['Mastery Gap'].max()} points"
    )

    c3.metric(
        "Large Gaps",
        int(
            (gap_df["Gap Classification"] == "LARGE GAP").sum()
        )
    )

    st.dataframe(
        gap_df.sort_values(
            "Mastery Gap",
            ascending=False
        ),
        use_container_width=True,
        hide_index=True
    )


    # ======================================
    # 16. LEARNING RISK DETECTION
    # ======================================

    st.divider()
    st.header("🚨 Student Learning Risk Detection")

    risk_data = []

    for s in students:

        result = detect_learning_risk(s)

        risk_data.append({

            "Student": s["name"],
            "Mastery": s["current_mastery"],
            "Gap": s["mastery_gap"],
            "Risk": result["risk"],
            "Explanation": result["explanation"]

        })

    risk_df = pd.DataFrame(risk_data)

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "High Risk",
        int((risk_df["Risk"] == "HIGH").sum())
    )

    c2.metric(
        "Moderate Risk",
        int((risk_df["Risk"] == "MODERATE").sum())
    )

    c3.metric(
        "Low Risk",
        int((risk_df["Risk"] == "LOW").sum())
    )

    st.dataframe(
        risk_df,
        use_container_width=True,
        hide_index=True
    )


    # ======================================
    # 17. TOPIC-LEVEL PERFORMANCE ANALYSIS
    # ======================================

    st.divider()
    st.header("📚 Topic-Level Performance Analysis")

    topic_rows = []

    for s in students:

        weak_lookup = {
            topic.casefold() for topic in s["weak_topics"]
        }

        strong_lookup = {
            topic.casefold() for topic in s["strong_topics"]
        }

        for topic, score in s["topic_scores"].items():

            if topic.casefold() in weak_lookup:
                category = "Declared Weak"

            elif topic.casefold() in strong_lookup:
                category = "Declared Strong"

            else:
                category = "Unspecified"

            status = classify_topic_score(score)

            review_flag = ""

            if category == "Declared Weak" and status == "STRONG":
                review_flag = "Review weak topic label"

            elif category == "Declared Strong" and status == "NEEDS SUPPORT":
                review_flag = "Review strong topic label"

            topic_rows.append({

                "Student": s["name"],
                "Topic": topic,
                "Score (%)": score,
                "Declared Category": category,
                "Performance Status": status,
                "Review Flag": review_flag

            })

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
                (topic_df["Performance Status"] == "NEEDS SUPPORT").sum()
            )
        )

        st.dataframe(
            topic_df.sort_values(
                "Score (%)",
                ascending=True
            ),
            use_container_width=True,
            hide_index=True
        )

        review_df = topic_df[
            topic_df["Review Flag"] != ""
        ]

        if not review_df.empty:

            st.subheader("Topic Classification Review")

            st.dataframe(
                review_df,
                use_container_width=True,
                hide_index=True
            )


    # ======================================
    # 18. LEARNING TREND ANALYSIS
    # ======================================

    st.divider()
    st.header("📈 Student Learning Trend Detection")

    trend_rows = []

    for s in students:

        result = detect_learning_trend(
            s["assessment_history"]
        )

        trend_rows.append({

            "Student": s["name"],
            "Assessment Count": len(s["assessment_history"]),
            "Net Change": (
                result["change"]
                if result["change"] is not None
                else "N/A"
            ),
            "Learning Trend": result["trend"],
            "Explanation": result["explanation"]

        })

    trend_df = pd.DataFrame(trend_rows)

    for trend in [
        "IMPROVING",
        "DECLINING",
        "STABLE",
        "INSUFFICIENT DATA"
    ]:

        count = sum(
            row["Learning Trend"] == trend
            for row in trend_rows
        )

        st.write(f"**{trend}:** {count} students")

    st.dataframe(
        trend_df,
        use_container_width=True,
        hide_index=True
    )

    for s in students:

        with st.expander(
            f"{s['name']} — Assessment History"
        ):

            if len(s["assessment_history"]) >= 2:

                history_df = pd.DataFrame({
                    "Mastery (%)": s["assessment_history"]
                })

                history_df.index = [
                    f"Assessment {i + 1}"
                    for i in range(len(s["assessment_history"]))
                ]

                st.line_chart(history_df)

            else:

                st.info("Insufficient assessment history.")


    # ======================================
    # 19. STUDENT SEGMENTATION
    # ======================================

    st.divider()
    st.header("👥 Student Segmentation Engine")

    segment_rows = []

    for s in students:

        result = classify_student_segment(s)

        segment_rows.append({

            "Student": s["name"],
            "ID": s["id"],
            "Risk": result["risk"],
            "Trend": result["trend"],
            "Segment": result["segment"],
            "Reason": result["explanation"]

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
            row["Segment"] == name
            for row in segment_rows
        )
        for name in segment_names
    }

    segment_chart = pd.DataFrame({

        "Students": list(segment_counts.values())

    }, index=segment_names)

    st.bar_chart(segment_chart)


    # ======================================
    # 20. INTERVENTION PRIORITIZATION
    # ======================================

    st.divider()

    st.header("🎯 Intervention Prioritization Engine")

    st.write(
        "Students are ranked by a transparent screening score "
        "built from mastery gaps, current mastery, learning "
        "trends and weak topic performance."
    )

    intervention_rows = []

    for s in students:

        result = calculate_intervention_priority(s)

        intervention_rows.append({

            "Student": s["name"],
            "Student ID": s["id"],
            "Mastery": s["current_mastery"],
            "Mastery Gap": s["mastery_gap"],
            "Gap Points": result["gap_points"],
            "Mastery Points": result["mastery_points"],
            "Trend Points": result["trend_points"],
            "Topic Points": result["topic_points"],
            "Intervention Score": result["score"],
            "Priority": result["priority"],
            "Recommendation": result["recommendation"]

        })

    intervention_df = pd.DataFrame(intervention_rows)

    intervention_df = intervention_df.sort_values(
        by=["Intervention Score", "Student"],
        ascending=[False, True]
    ).reset_index(drop=True)

    intervention_df.insert(
        0,
        "Rank",
        range(1, len(intervention_df) + 1)
    )

    p1_count = sum(
        row["Priority"] == "P1 - URGENT"
        for row in intervention_rows
    )

    p2_count = sum(
        row["Priority"] == "P2 - HIGH"
        for row in intervention_rows
    )

    p3_count = sum(
        row["Priority"] == "P3 - SCHEDULED"
        for row in intervention_rows
    )

    p4_count = sum(
        row["Priority"] == "P4 - MONITOR"
        for row in intervention_rows
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("P1 Urgent", p1_count)
    c2.metric("P2 High", p2_count)
    c3.metric("P3 Scheduled", p3_count)
    c4.metric("P4 Monitor", p4_count)

    st.subheader("Ranked Intervention Queue")

    st.dataframe(
        intervention_df[
            [
                "Rank",
                "Student",
                "Student ID",
                "Intervention Score",
                "Priority",
                "Mastery Gap"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

    st.subheader("📊 Intervention Score Comparison")

    score_chart = intervention_df[
        ["Student", "Intervention Score"]
    ].set_index("Student")

    st.bar_chart(score_chart)

    st.subheader("🔎 Intervention Decision Explanations")

    for s in students:

        result = calculate_intervention_priority(s)

        with st.expander(
            f"{s['name']} — {result['priority']} "
            f"— Score {result['score']}"
        ):

            c1, c2 = st.columns(2)

            c1.metric(
                "Final Intervention Score",
                f"{result['score']} / 95"
            )

            c2.metric(
                "Mastery Gap",
                f"{s['mastery_gap']} points"
            )

            st.write("**Score Breakdown**")

            st.write(
                f"Mastery gap: "
                f"{result['gap_points']} / 40"
            )

            st.write(
                f"Current mastery: "
                f"{result['mastery_points']} / 20"
            )

            st.write(
                f"Learning trend: "
                f"{result['trend_points']} / 20"
            )

            st.write(
                f"Topic weaknesses: "
                f"{result['topic_points']} / 15"
            )

            st.divider()

            st.write("**Recommended next action**")

            st.info(result["recommendation"])


    # ======================================
    # 21. INDIVIDUAL STUDENT PROFILES
    # ======================================

    st.divider()
    st.header("🔍 Individual Student Profiles")

    for s in students:

        with st.expander(
            f"{s['name']} — {s['id']}"
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

            st.write("**Subject:**", s["subject"])

            st.write("**Priority:**", s["priority"])

            st.write("**Weak Topics:**")

            for topic in s["weak_topics"]:
                st.write(f"🔴 {topic}")

            st.write("**Strong Topics:**")

            for topic in s["strong_topics"]:
                st.write(f"🟢 {topic}")

            st.write("**Assessment History:**", s["assessment_history"])

            result = calculate_intervention_priority(s)

            st.metric(
                "Intervention Score",
                f"{result['score']} / 95"
            )

            st.write(
                "**Intervention Priority:**",
                result["priority"]
            )

            st.write(
                "**Weekly Study Capacity:**",
                f"{s['weekly_minutes'] / 60:g} hours"
            )

else:

    st.info(
        "No student records available. "
        "Register students to generate academic insights."
    )


# ==========================================
# 22. APPLICATION FOOTER
# ==========================================

st.divider()

st.caption(
    "AI Study Plan Generator | Academic Intelligence Platform"
)

st.warning(
    "The intervention score is an initial heuristic screening "
    "system, not a validated predictive model or an automatic "
    "instructional decision. Teachers should investigate the "
    "underlying evidence before assigning interventions. "
    "Student records currently use temporary Streamlit session "
    "memory. Supabase persistence will be implemented later."
)

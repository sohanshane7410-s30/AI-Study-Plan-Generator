
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
    """
    Format:
    Fractions: 35, Decimals: 45
    """

    scores = {}
    errors = []

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
            errors.append(
                f"Invalid score for {topic}."
            )
            continue

        if not 0 <= score <= 100:
            errors.append(
                f"{topic} must have a score between 0 and 100."
            )
            continue

        normalized = topic.casefold()

        if normalized in {
            name.casefold() for name in scores
        }:
            errors.append(
                f"Duplicate topic score: {topic}."
            )
            continue

        scores[topic] = round(score, 1)

    return scores, errors


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
# 5. GAP CLASSIFICATION
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
# 7. RISK DETECTION
# ==========================================

def detect_learning_risk(student):

    mastery = student["current_mastery"]
    gap = student["mastery_gap"]

    if mastery < 40 or gap >= 35:

        risk = "HIGH"

        explanation = (
            "Low current mastery or a substantial "
            "remaining mastery gap."
        )

    elif mastery < 60 or gap >= 20:

        risk = "MODERATE"

        explanation = (
            "Targeted practice and closer monitoring "
            "may be beneficial."
        )

    else:

        risk = "LOW"

        explanation = (
            "Lower immediate concern based on the "
            "current mastery and mastery gap."
        )

    return {
        "risk": risk,
        "explanation": explanation
    }


# ==========================================
# 8. OLD RECORD MIGRATION
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

        student["weak_topics"] = (
            student.get("weak_topics", [])
        )

        student["strong_topics"] = (
            student.get("strong_topics", [])
        )

        if isinstance(student["weak_topics"], str):
            student["weak_topics"] = parse_topics(
                student["weak_topics"]
            )

        if isinstance(student["strong_topics"], str):
            student["strong_topics"] = parse_topics(
                student["strong_topics"]
            )

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
# 9. APPLICATION HEADER
# ==========================================

st.title("📚 AI Study Plan Generator")

st.caption(
    "An intelligent platform for personalized and adaptive learning."
)

st.divider()


# ==========================================
# 10. STUDENT REGISTRATION
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

    st.subheader("📝 Topic-Level Assessment Scores")

    topic_scores_input = st.text_area(
        "Enter topic scores",
        placeholder=(
            "Fractions: 35, Decimals: 45, "
            "Percentages: 85, Basic arithmetic: 90"
        ),
        help=(
            "Enter every weak and strong topic with "
            "its assessment score out of 100."
        )
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
            topic.casefold(): score
            for topic, score in topic_scores.items()
        }

        all_topics = weak_topics + strong_topics

        missing_scores = [
            topic for topic in all_topics
            if topic.casefold() not in score_lookup
        ]

        if not name or not clean_id:
            st.error("Student name and ID are required.")

        elif clean_id.casefold() in existing_ids:
            st.error("Student ID already exists.")

        elif not weak_topics or not strong_topics:
            st.error(
                "Enter at least one weak and one strong topic."
            )

        elif overlap:
            st.error(
                "A topic cannot be both weak and strong."
            )

        elif target_mastery < current_mastery:
            st.error(
                "Target mastery cannot be lower than current mastery."
            )

        elif score_errors:
            for error in score_errors:
                st.error(error)

        elif missing_scores:
            st.error(
                "Missing assessment scores for: "
                + ", ".join(missing_scores)
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
# 11. ACADEMIC PERFORMANCE DASHBOARD
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

    st.subheader("🎯 Student Priority Analysis")

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
    # 12. LEARNING GAP ANALYSIS
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
    # 13. LEARNING RISK DETECTION
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
    # 14. TOPIC-LEVEL PERFORMANCE ANALYSIS
    # ======================================

    st.divider()

    st.header("📚 Topic-Level Performance Analysis")

    topic_rows = []

    for s in students:

        weak_lookup = {
            topic.casefold()
            for topic in s["weak_topics"]
        }

        strong_lookup = {
            topic.casefold()
            for topic in s["strong_topics"]
        }

        for topic, score in s["topic_scores"].items():

            status = classify_topic_score(score)

            if topic.casefold() in weak_lookup:
                declared_category = "Declared Weak"
            elif topic.casefold() in strong_lookup:
                declared_category = "Declared Strong"
            else:
                declared_category = "Unspecified"

            discrepancy = ""

            if (
                declared_category == "Declared Weak"
                and status == "STRONG"
            ):
                discrepancy = "Review: weak label, high score"

            elif (
                declared_category == "Declared Strong"
                and status == "NEEDS SUPPORT"
            ):
                discrepancy = "Review: strong label, low score"

            topic_rows.append({

                "Student": s["name"],
                "Subject": s["subject"],
                "Topic": topic,
                "Assessment Score (%)": score,
                "Declared Category": declared_category,
                "Performance Status": status,
                "Review Flag": discrepancy

            })

    if topic_rows:

        topic_df = pd.DataFrame(topic_rows)

        average_topic_score = topic_df[
            "Assessment Score (%)"
        ].mean()

        support_count = int(
            (
                topic_df["Performance Status"]
                == "NEEDS SUPPORT"
            ).sum()
        )

        developing_count = int(
            (
                topic_df["Performance Status"]
                == "DEVELOPING"
            ).sum()
        )

        strong_count = int(
            (
                topic_df["Performance Status"]
                == "STRONG"
            ).sum()
        )

        c1, c2 = st.columns(2)

        c1.metric(
            "Average Topic Score",
            f"{average_topic_score:.1f}%"
        )

        c2.metric(
            "Topics Requiring Support",
            support_count
        )

        c1, c2, c3 = st.columns(3)

        c1.metric("Needs Support", support_count)
        c2.metric("Developing", developing_count)
        c3.metric("Strong Topics", strong_count)

        st.subheader("Individual Topic Performance Report")

        st.dataframe(
            topic_df.sort_values(
                "Assessment Score (%)",
                ascending=True
            ),
            use_container_width=True,
            hide_index=True
        )

        st.subheader("📈 Topic Score Comparison")

        topic_chart = topic_df.copy()

        topic_chart["Topic Label"] = (
            topic_chart["Student"]
            + " - "
            + topic_chart["Topic"]
        )

        chart_data = topic_chart.set_index(
            "Topic Label"
        )[["Assessment Score (%)"]]

        st.bar_chart(chart_data)

        # Display inconsistencies for further investigation.
        flagged = topic_df[
            topic_df["Review Flag"] != ""
        ]

        if not flagged.empty:

            st.subheader("🔎 Classification Review")

            st.warning(
                "Some teacher-reported topic labels do not "
                "match the supplied assessment scores."
            )

            st.dataframe(
                flagged[
                    [
                        "Student",
                        "Topic",
                        "Assessment Score (%)",
                        "Declared Category",
                        "Review Flag"
                    ]
                ],
                use_container_width=True,
                hide_index=True
            )

        st.subheader("💡 Topic-Level Insights")

        lowest_topics = topic_df.nsmallest(
            min(3, len(topic_df)),
            "Assessment Score (%)"
        )

        for _, row in lowest_topics.iterrows():

            st.write(
                f"🔴 {row['Student']} — {row['Topic']}: "
                f"{row['Assessment Score (%)']}%"
            )

    else:

        st.info(
            "No topic assessment scores are available yet. "
            "Register students with topic-level assessment scores."
        )

    # ======================================
    # 15. INDIVIDUAL STUDENT PROFILES
    # ======================================

    st.divider()

    st.header("🔍 Individual Student Profiles")

    for s in students:

        with st.expander(
            f"{s['name']} — {s['id']}"
        ):

            st.write("Subject:", s["subject"])

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

            st.write("**Weak Topics:**")

            for topic in s["weak_topics"]:
                st.write(f"🔴 {topic}")

            st.write("**Strong Topics:**")

            for topic in s["strong_topics"]:
                st.write(f"🟢 {topic}")

            st.write("**Topic Assessment Scores:**")

            for topic, score in s["topic_scores"].items():

                st.write(
                    f"{topic}: {score}% — "
                    f"{classify_topic_score(score)}"
                )

            st.metric(
                "Weekly Study Capacity",
                f"{s['weekly_minutes'] / 60:g} hours"
            )

else:

    st.info(
        "No student records available. Register students "
        "to generate academic insights."
    )


# ==========================================
# 16. FOOTER
# ==========================================

st.divider()

st.caption(
    "AI Study Plan Generator | Academic Intelligence Platform"
)

st.warning(
    "Topic performance categories use initial project "
    "thresholds: below 60% needs support, 60–79% developing, "
    "and 80% or above strong. These are screening bands, "
    "not validated educational standards. Student data currently "
    "uses temporary session storage. Supabase persistence "
    "will be implemented in a later mission."
)

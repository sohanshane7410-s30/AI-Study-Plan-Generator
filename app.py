
import uuid
from datetime import datetime

import pandas as pd
import streamlit as st


# =========================================================
# 1. APPLICATION CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Study Plan Generator",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# 2. DESIGN SYSTEM
# =========================================================

st.markdown("""
<style>
.stApp {
    background: #F5F6FC;
    color: #18213B;
}
.block-container {
    max-width: 1450px;
    padding: 2rem 2.2rem 3rem;
}
[data-testid="stSidebar"] {
    background: #111A35;
}
[data-testid="stSidebar"] * {
    color: #EDF0FC;
}
h1 {
    color: #18213B;
    font-weight: 800;
}
h2 {
    color: #202B4D;
    font-weight: 750;
}
[data-testid="stMetric"] {
    background: white;
    padding: 18px;
    border-radius: 15px;
    border: 1px solid #E6E8F1;
}
.stButton > button {
    background: #6250D3;
    color: white;
    border-radius: 10px;
    border: none;
    font-weight: 700;
}
.stButton > button:hover {
    background: #4F40B7;
    color: white;
}
[data-testid="stForm"] {
    background: white;
    padding: 22px;
    border-radius: 15px;
    border: 1px solid #E6E8F1;
}
.hero {
    background: linear-gradient(115deg,#111A35,#282C68,#6352C8);
    padding: 32px;
    border-radius: 20px;
    margin-bottom: 24px;
}
.hero h1 {
    color: white !important;
    font-size: 34px;
}
.hero p {
    color: #D7DEF6;
    font-size: 15px;
}
footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)


# =========================================================
# 3. SESSION STORAGE
# =========================================================

if "students" not in st.session_state:
    st.session_state.students = []

if "plans" not in st.session_state:
    st.session_state.plans = {}

if "selected_student" not in st.session_state:
    st.session_state.selected_student = None


# =========================================================
# 4. STUDENT ANALYSIS ENGINE
# =========================================================

def classify_priority(score, target):

    gap = max(0, target - score)

    if score < 40:
        priority = "URGENT"
    elif score < 60:
        priority = "HIGH"
    elif score < target:
        priority = "MODERATE"
    else:
        priority = "TARGET ACHIEVED"

    return priority, gap


def analyze_student(student):

    results = []

    for subject, score in student["subjects"].items():

        priority, gap = classify_priority(
            score,
            student["target"]
        )

        results.append({
            "Subject": subject,
            "Mastery": score,
            "Target": student["target"],
            "Gap": gap,
            "Priority": priority
        })

    return pd.DataFrame(results)


# =========================================================
# 5. STUDY PLAN GENERATION ENGINE
# =========================================================

def generate_study_plan(student):

    subjects = student["subjects"]
    target = student["target"]
    daily_minutes = student["daily_minutes"]

    weak_subjects = []

    for subject, score in subjects.items():

        if score < target:
            weak_subjects.append({
                "subject": subject,
                "score": score,
                "gap": target - score
            })

    if not weak_subjects:
        return []

    # Prioritize subjects according to their mastery gaps.
    weak_subjects.sort(
        key=lambda x: x["gap"],
        reverse=True
    )

    # Give every weak subject at least five minutes.
    base_minutes = 5
    remaining = daily_minutes - (
        base_minutes * len(weak_subjects)
    )

    total_gap = sum(
        item["gap"] for item in weak_subjects
    )

    allocations = []

    for item in weak_subjects:

        exact = remaining * item["gap"] / total_gap

        allocations.append({
            "subject": item["subject"],
            "score": item["score"],
            "gap": item["gap"],
            "minutes": base_minutes + int(exact),
            "fraction": exact - int(exact)
        })

    # Distribute remaining minutes caused by rounding.
    leftover = daily_minutes - sum(
        item["minutes"] for item in allocations
    )

    allocations.sort(
        key=lambda x: x["fraction"],
        reverse=True
    )

    for i in range(leftover):
        allocations[i]["minutes"] += 1

    tasks = []

    for item in allocations:

        score = item["score"]
        subject = item["subject"]

        if score < 40:
            activity = "Foundation lesson and worked examples"
            objective = (
                "Understand fundamental concepts "
                "and solve basic questions."
            )

        elif score < 60:
            activity = "Concept review and guided practice"
            objective = (
                "Strengthen understanding and solve "
                "guided practice questions."
            )

        elif score < target:
            activity = "Independent practice and retrieval quiz"
            objective = (
                "Improve accuracy through independent "
                "practice and self-testing."
            )

        else:
            activity = "Advanced challenge questions"
            objective = "Extend learning through advanced problems."

        tasks.append({
            "id": str(uuid.uuid4())[:8],
            "subject": subject,
            "activity": activity,
            "objective": objective,
            "minutes": item["minutes"],
            "completed": False
        })

    return tasks


# =========================================================
# 6. HELPER FUNCTIONS
# =========================================================

def get_student(student_id):

    for student in st.session_state.students:

        if student["id"] == student_id:
            return student

    return None


def get_average(student):

    scores = list(student["subjects"].values())

    if not scores:
        return 0

    return sum(scores) / len(scores)


def get_completed_tasks(student_id):

    tasks = st.session_state.plans.get(student_id, [])

    return sum(
        1 for task in tasks if task["completed"]
    )


def get_progress(student_id):

    tasks = st.session_state.plans.get(student_id, [])

    if not tasks:
        return 0

    completed = get_completed_tasks(student_id)

    return completed / len(tasks)


def regenerate_plan(student):

    st.session_state.plans[student["id"]] = (
        generate_study_plan(student)
    )


# =========================================================
# 7. SIDEBAR NAVIGATION
# =========================================================

with st.sidebar:

    st.markdown("# 📚 Learning Studio")

    st.caption("AI-POWERED STUDENT INTELLIGENCE")

    st.divider()

    page = st.radio(
        "NAVIGATION",
        [
            "Dashboard",
            "Add Student",
            "Student Analysis",
            "Study Plans",
            "Progress Tracker",
            "Reports"
        ]
    )

    st.divider()

    st.caption(
        "AI STUDY PLAN GENERATOR"
    )

    st.caption(
        "Personalized learning. "
        "Measurable progress."
    )


# =========================================================
# 8. HERO SECTION
# =========================================================

st.markdown("""
<div class="hero">
    <h1>AI Study Plan Generator</h1>
    <p>
        Transform student performance data into
        personalized learning strategies, daily study
        schedules, and measurable academic progress.
    </p>
    <p>
        PERFORMANCE INTELLIGENCE • ADAPTIVE LEARNING
        • PERSONALIZED STUDY PLANS
    </p>
</div>
""", unsafe_allow_html=True)


# =========================================================
# 9. DASHBOARD
# =========================================================

if page == "Dashboard":

    st.title("📊 Performance Dashboard")

    students = st.session_state.students

    if not students:

        st.info(
            "No students available yet. "
            "Start by adding your first student."
        )

        if st.button("Add Your First Student"):

            st.session_state.selected_student = None
            st.rerun()

    else:

        total_students = len(students)

        average = sum(
            get_average(s) for s in students
        ) / total_students

        total_subjects = sum(
            len(s["subjects"]) for s in students
        )

        at_risk = sum(
            1
            for s in students
            if any(score < 60 for score in s["subjects"].values())
        )

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Total Students", total_students)
        col2.metric("Average Mastery", f"{average:.1f}%")
        col3.metric("Subjects Tracked", total_subjects)
        col4.metric("Students Requiring Support", at_risk)

        st.divider()

        st.subheader("Student Performance Overview")

        rows = []

        for student in students:

            rows.append({
                "Student": student["name"],
                "Grade": student["grade"],
                "Average Mastery": round(
                    get_average(student), 1
                ),
                "Target": student["target"],
                "Study Progress": round(
                    get_progress(student["id"]) * 100, 1
                )
            })

        df = pd.DataFrame(rows)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        st.subheader("Average Mastery by Student")

        chart_df = df.set_index("Student")[
            ["Average Mastery"]
        ]

        st.bar_chart(chart_df)

        st.subheader("Students Requiring Attention")

        for student in students:

            analysis = analyze_student(student)

            urgent = analysis[
                analysis["Priority"].isin(
                    ["URGENT", "HIGH"]
                )
            ]

            if not urgent.empty:

                with st.expander(
                    f"⚠️ {student['name']} — "
                    f"{len(urgent)} subjects need attention"
                ):

                    st.dataframe(
                        urgent,
                        use_container_width=True,
                        hide_index=True
                    )


# =========================================================
# 10. ADD STUDENT
# =========================================================

elif page == "Add Student":

    st.title("👨‍🎓 Student Registration")

    st.write(
        "Create a student profile and enter current "
        "subject mastery scores."
    )

    with st.form("student_registration"):

        name = st.text_input(
            "Student Name",
            placeholder="Enter student name"
        )

        grade = st.text_input(
            "Grade / Class",
            placeholder="Example: Grade 7"
        )

        target = st.slider(
            "Target Mastery (%)",
            50, 100, 80
        )

        daily_minutes = st.slider(
            "Available Daily Study Time (minutes)",
            30, 360, 120, step=15
        )

        subjects_text = st.text_area(
            "Subject Mastery Scores",
            value=(
                "Mathematics: 45\n"
                "Science: 65\n"
                "English: 75"
            ),
            height=150,
            help=(
                "Enter one subject per line. "
                "Format: Subject: Score"
            )
        )

        submitted = st.form_submit_button(
            "Create Student & Generate Study Plan"
        )

    if submitted:

        if not name.strip() or not grade.strip():

            st.error(
                "Please enter the student name and grade."
            )

        else:

            subjects = {}

            try:

                for line in subjects_text.splitlines():

                    if not line.strip():
                        continue

                    if ":" not in line:
                        raise ValueError(
                            "Use the format Subject: Score"
                        )

                    subject, score = line.rsplit(":", 1)

                    subject = subject.strip()
                    score = float(score.strip())

                    if not subject:
                        raise ValueError(
                            "Subject name cannot be empty."
                        )

                    if not 0 <= score <= 100:
                        raise ValueError(
                            "Mastery scores must be between 0 and 100."
                        )

                    if subject in subjects:
                        raise ValueError(
                            "Duplicate subject: " + subject
                        )

                    subjects[subject] = score

                if not subjects:
                    raise ValueError(
                        "Enter at least one subject."
                    )

                if len(subjects) > 8:
                    raise ValueError(
                        "Enter no more than 8 subjects."
                    )

                student = {
                    "id": str(uuid.uuid4())[:8],
                    "name": name.strip(),
                    "grade": grade.strip(),
                    "target": target,
                    "daily_minutes": daily_minutes,
                    "subjects": subjects,
                    "created_at": datetime.now().strftime(
                        "%Y-%m-%d %H:%M"
                    )
                }

                st.session_state.students.append(student)

                regenerate_plan(student)

                st.session_state.selected_student = student["id"]

                st.success(
                    "Student created and personalized study plan generated!"
                )

                st.balloons()

            except ValueError as exc:

                st.error(str(exc))


# =========================================================
# 11. STUDENT ANALYSIS
# =========================================================

elif page == "Student Analysis":

    st.title("🔍 Student Performance Analysis")

    students = st.session_state.students

    if not students:

        st.info("Add a student to begin analysis.")

    else:

        selected = st.selectbox(
            "Select Student",
            students,
            format_func=lambda x: x["name"],
            key="analysis_student"
        )

        analysis = analyze_student(selected)

        average = get_average(selected)

        st.subheader(
            f"Academic Profile: {selected['name']}"
        )

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Average Mastery",
            f"{average:.1f}%"
        )

        col2.metric(
            "Target Mastery",
            f"{selected['target']}%"
        )

        col3.metric(
            "Daily Study Time",
            f"{selected['daily_minutes']} min"
        )

        st.divider()

        st.subheader("Subject-wise Analysis")

        st.dataframe(
            analysis,
            use_container_width=True,
            hide_index=True
        )

        st.subheader("Mastery Comparison")

        chart = analysis.set_index("Subject")[
            ["Mastery", "Target"]
        ]

        st.bar_chart(chart)

        st.subheader("Learning Strengths")

        strengths = analysis[
            analysis["Mastery"] >= selected["target"]
        ]

        if strengths.empty:

            st.info(
                "No subjects have reached the target yet."
            )

        else:

            for _, row in strengths.iterrows():

                st.success(
                    f"{row['Subject']}: "
                    f"{row['Mastery']}% mastery"
                )

        st.subheader("Priority Areas")

        weak = analysis[
            analysis["Mastery"] < selected["target"]
        ].sort_values("Gap", ascending=False)

        if weak.empty:

            st.success(
                "All subjects have achieved the target!"
            )

        else:

            for _, row in weak.iterrows():

                st.warning(
                    f"{row['Subject']} — "
                    f"{row['Mastery']}% mastery | "
                    f"{row['Gap']}% gap | "
                    f"{row['Priority']} priority"
                )


# =========================================================
# 12. PERSONALIZED STUDY PLANS
# =========================================================

elif page == "Study Plans":

    st.title("🧠 Personalized Study Plans")

    students = st.session_state.students

    if not students:

        st.info("Register a student first.")

    else:

        student = st.selectbox(
            "Select Student",
            students,
            format_func=lambda x: x["name"],
            key="plan_student"
        )

        tasks = st.session_state.plans.get(
            student["id"], []
        )

        st.subheader(
            f"Daily Learning Plan — {student['name']}"
        )

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Daily Study Time",
            f"{student['daily_minutes']} min"
        )

        col2.metric(
            "Learning Activities",
            len(tasks)
        )

        col3.metric(
            "Completed",
            get_completed_tasks(student["id"])
        )

        st.divider()

        if not tasks:

            st.success(
                "All subjects have achieved the target mastery!"
            )

        else:

            for i, task in enumerate(tasks):

                with st.container(border=True):

                    st.markdown(
                        f"### {i + 1}. {task['subject']}"
                    )

                    st.write(
                        f"**Activity:** {task['activity']}"
                    )

                    st.write(
                        f"**Objective:** {task['objective']}"
                    )

                    st.write(
                        f"**Time allocation:** "
                        f"{task['minutes']} minutes"
                    )

                    st.write(
                        "Status: "
                        + (
                            "✅ Completed"
                            if task["completed"]
                            else "⏳ Pending"
                        )
                    )

        st.divider()

        if st.button(
            "🔄 Regenerate Study Plan",
            key="regenerate_plan"
        ):

            regenerate_plan(student)

            st.success("Study plan regenerated!")

            st.rerun()


# =========================================================
# 13. PROGRESS TRACKER
# =========================================================

elif page == "Progress Tracker":

    st.title("📈 Learning Progress Tracker")

    students = st.session_state.students

    if not students:

        st.info("Add a student to track progress.")

    else:

        student = st.selectbox(
            "Select Student",
            students,
            format_func=lambda x: x["name"],
            key="progress_student"
        )

        tasks = st.session_state.plans.get(
            student["id"], []
        )

        if not tasks:

            st.success(
                "No pending study activities. "
                "All subjects have achieved the target."
            )

        else:

            completed = get_completed_tasks(student["id"])

            progress = get_progress(student["id"])

            st.subheader("Daily Plan Completion")

            st.progress(progress)

            st.write(
                f"{completed} of {len(tasks)} activities completed "
                f"({progress * 100:.1f}%)"
            )

            st.divider()

            st.subheader("Mark Learning Activities Complete")

            for task in tasks:

                checked = st.checkbox(
                    (
                        f"{task['subject']} — "
                        f"{task['activity']} "
                        f"({task['minutes']} min)"
                    ),
                    value=task["completed"],
                    key=(
                        f"task_{student['id']}_{task['id']}"
                    )
                )

                task["completed"] = checked

            completed = get_completed_tasks(student["id"])

            st.progress(get_progress(student["id"]))

            st.write(
                f"Updated completion: {completed}/{len(tasks)}"
            )

        st.divider()

        st.subheader("Update Academic Mastery")

        st.write(
            "Enter new mastery scores after reassessment. "
            "The application will recalculate priorities "
            "and generate an updated study plan."
        )

        with st.form("mastery_update_form"):

            subject = st.selectbox(
                "Subject",
                list(student["subjects"].keys())
            )

            new_score = st.slider(
                "New Mastery Score (%)",
                0, 100,
                int(student["subjects"][subject])
            )

            update = st.form_submit_button(
                "Update Mastery & Adapt Study Plan"
            )

        if update:

            old_score = student["subjects"][subject]

            student["subjects"][subject] = new_score

            regenerate_plan(student)

            st.success(
                f"{subject} updated from {old_score}% "
                f"to {new_score}%."
            )

            st.info(
                "The learning priorities and daily study plan "
                "have been recalculated."
            )

            st.rerun()


# =========================================================
# 14. REPORTS
# =========================================================

elif page == "Reports":

    st.title("📑 Academic Performance Reports")

    students = st.session_state.students

    if not students:

        st.info("Add students to generate reports.")

    else:

        student = st.selectbox(
            "Select Student",
            students,
            format_func=lambda x: x["name"],
            key="report_student"
        )

        analysis = analyze_student(student)

        tasks = st.session_state.plans.get(
            student["id"], []
        )

        completed = get_completed_tasks(student["id"])

        st.subheader("Student Academic Report")

        st.write(f"**Student:** {student['name']}")
        st.write(f"**Grade:** {student['grade']}")
        st.write(f"**Target:** {student['target']}%")
        st.write(
            f"**Average mastery:** {get_average(student):.1f}%"
        )

        st.write(
            f"**Study plan completion:** "
            f"{get_progress(student['id']) * 100:.1f}%"
        )

        st.divider()

        st.subheader("Performance Breakdown")

        st.dataframe(
            analysis,
            use_container_width=True,
            hide_index=True
        )

        st.subheader("Recommended Learning Priorities")

        for _, row in analysis.iterrows():

            if row["Mastery"] < student["target"]:

                st.warning(
                    f"{row['Subject']}: Focus on closing "
                    f"the {row['Gap']}% mastery gap."
                )

            else:

                st.success(
                    f"{row['Subject']}: Target achieved."
                )

        st.divider()

        report = analysis.copy()

        report.insert(0, "Student", student["name"])
        report["Study Plan Completion (%)"] = round(
            get_progress(student["id"]) * 100, 1
        )

        st.download_button(
            "⬇️ Download Academic Report (CSV)",
            data=report.to_csv(index=False).encode("utf-8"),
            file_name=(
                f"{student['name'].replace(' ', '_')}_report.csv"
            ),
            mime="text/csv"
        )

        if tasks:

            task_report = pd.DataFrame(tasks)

            st.download_button(
                "⬇️ Download Daily Study Plan (CSV)",
                data=task_report.to_csv(
                    index=False
                ).encode("utf-8"),
                file_name=(
                    f"{student['name'].replace(' ', '_')}_study_plan.csv"
                ),
                mime="text/csv"
            )


# =========================================================
# 15. FOOTER
# =========================================================

st.divider()

st.caption(
    "AI Study Plan Generator | Learning Intelligence Studio | "
    "Personalized Learning & Academic Performance Analytics"
)

st.caption(
    "Prototype version: Student data is stored in "
    "Streamlit session state and is not permanently persisted."
)

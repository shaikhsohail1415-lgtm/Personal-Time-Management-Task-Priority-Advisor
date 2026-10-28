import os
import streamlit as st
import pandas as pd
from dotenv import load_dotenv

from models.task import Task, TaskAnalysis
from utils.time_utils import calculate_urgency, calculate_time_pressure
from utils.validation import validate_task
from fuzzy.inference import MamdaniFuzzySystem
from ai.extractor import extract_tasks
from ai.explainer import explain_results
from ui.components import render_task_card, render_fuzzy_analysis
from ui.charts import priority_chart, membership_chart

load_dotenv()

st.set_page_config(page_title="Personal Time Management & Task Priority Advisor",
                   page_icon="⏱️", layout="wide")

st.title("⏱️ Personal Time Management & Task Priority Advisor")
st.caption("AI-powered task prioritization using LangChain and Mamdani Fuzzy Logic")

with st.sidebar:
    st.header("Settings")
    available_hours = st.number_input("Available Time Today (hours)", min_value=0.25, max_value=24.0,
                                       value=5.0, step=0.25)
    st.markdown("---")
    st.markdown("**AI mode:** LangChain + structured LLM extraction")
    st.markdown("**Decision engine:** Mamdani Fuzzy Inference System")
    st.info("Manual mode works without an LLM/API key.")

fuzzy = MamdaniFuzzySystem()
tasks = []

tab_nl, tab_manual = st.tabs(["🧠 Natural Language", "📝 Manual Task Entry"])

with tab_nl:
    text = st.text_area(
        "Describe your tasks naturally",
        placeholder="I have a DBMS assignment due tomorrow. It is very important and will take 3 hours. I also have a presentation next week that will take 2 hours.",
        height=180,
    )
    if st.button("Analyze Tasks", type="primary", key="analyze_nl"):
        if not text.strip():
            st.warning("Please describe at least one task.")
        elif not os.getenv("OPENAI_API_KEY"):
            st.error("OPENAI_API_KEY is not configured. Use Manual Task Entry or add your API key to .env / Streamlit secrets.")
        else:
            with st.spinner("LangChain is extracting structured tasks..."):
                try:
                    tasks = extract_tasks(text)
                    st.session_state["tasks"] = tasks
                    st.success(f"Extracted {len(tasks)} task(s).")
                except Exception as e:
                    st.error(f"AI extraction failed: {e}")

with tab_manual:
    with st.form("manual_form"):
        name = st.text_input("Task Name")
        description = st.text_area("Description")
        c1, c2, c3 = st.columns(3)
        with c1:
            deadline = st.date_input("Deadline")
            estimated_hours = st.number_input("Estimated Hours", min_value=0.1, max_value=100.0, value=2.0, step=0.5)
        with c2:
            importance = st.slider("Importance", 0, 100, 70)
            difficulty = st.slider("Difficulty", 0, 100, 50)
        with c3:
            category = st.selectbox("Category", ["Academic", "Work", "Personal", "Health", "Other"])
        submitted = st.form_submit_button("Calculate Priority", type="primary")
        if submitted:
            if not name.strip():
                st.warning("Task name is required.")
            else:
                task = Task(name=name.strip(), description=description, deadline=deadline,
                            estimated_hours=estimated_hours, importance=importance,
                            difficulty=difficulty, category=category)
                st.session_state["tasks"] = [task]
                st.success("Task added.")

tasks = st.session_state.get("tasks", [])

if tasks:
    analyses = []
    for task in tasks:
        try:
            validate_task(task)
            urgency = calculate_urgency(task.deadline)
            pressure = calculate_time_pressure(task.estimated_hours, available_hours)
            result = fuzzy.infer(urgency, task.importance, pressure, task.difficulty)
            analysis = TaskAnalysis(
                task=task, urgency=urgency, time_pressure=pressure,
                priority_score=result["score"], priority_level=result["level"],
                membership_values=result["memberships"],
                activated_rules=result["rules"],
                aggregated_output=result["aggregated"],
            )
            analyses.append(analysis)
        except Exception as e:
            st.error(f"Could not analyze '{task.name}': {e}")

    if analyses:
        analyses.sort(key=lambda x: x.priority_score, reverse=True)
        st.session_state["analyses"] = analyses

        best = analyses[0]
        st.subheader("🎯 Recommended Next Task")
        st.success(f"**{best.task.name}** — {best.priority_score:.1f}/100 ({best.priority_level})")

        cols = st.columns(4)
        cols[0].metric("Priority", f"{best.priority_score:.1f}")
        cols[1].metric("Urgency", f"{best.urgency:.1f}")
        cols[2].metric("Time Pressure", f"{best.time_pressure:.1f}")
        cols[3].metric("Importance", f"{best.task.importance:.1f}")

        st.subheader("📋 Task Priority")
        rows = []
        for i, a in enumerate(analyses, 1):
            rows.append({
                "Rank": i, "Task": a.task.name, "Priority Score": round(a.priority_score, 1),
                "Level": a.priority_level, "Urgency": round(a.urgency, 1),
                "Importance": a.task.importance, "Time Pressure": round(a.time_pressure, 1),
                "Duration (h)": a.task.estimated_hours,
                "Deadline": str(a.task.deadline) if a.task.deadline else "No deadline"
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
        st.plotly_chart(priority_chart(rows), use_container_width=True)

        for a in analyses:
            render_task_card(a)
            with st.expander(f"View Fuzzy Logic Analysis — {a.task.name}"):
                render_fuzzy_analysis(a)
                st.plotly_chart(membership_chart(a.membership_values), use_container_width=True)

        if os.getenv("OPENAI_API_KEY"):
            with st.expander("🤖 AI Explanation", expanded=True):
                with st.spinner("Generating explanation..."):
                    try:
                        st.write(explain_results(analyses, available_hours))
                    except Exception as e:
                        st.warning(f"Explanation unavailable: {e}")
        else:
            st.info("Add OPENAI_API_KEY to enable LangChain-generated explanations.")

        st.subheader("🗓️ Simple Time Allocation")
        remaining = available_hours
        for a in analyses:
            if remaining <= 0:
                break
            allocated = min(a.task.estimated_hours, remaining)
            st.write(f"**{a.task.name}** — allocate about **{allocated:.1f} hour(s)**")
            remaining -= allocated
        if remaining > 0:
            st.write(f"Remaining flexible time: **{remaining:.1f} hour(s)**")
else:
    st.info("Enter tasks using Natural Language or Manual Task Entry to begin.")

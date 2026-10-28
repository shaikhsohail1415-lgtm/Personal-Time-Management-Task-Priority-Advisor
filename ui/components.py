import streamlit as st

def render_task_card(a):
    st.markdown(f"### {a.task.name}")
    st.caption(f"{a.task.category} • {a.task.estimated_hours:.1f} hours • deadline: {a.task.deadline or 'None'}")
    st.write(f"**Priority:** {a.priority_score:.1f}/100 — **{a.priority_level}**")

def render_fuzzy_analysis(a):
    st.write("**Membership degrees**")
    for variable, values in a.membership_values.items():
        st.write(f"**{variable.replace('_',' ').title()}** — " +
                 " | ".join(f"{k}: {v:.3f}" for k,v in values.items()))
    st.write("**Activated rules**")
    if not a.activated_rules:
        st.write("No rules fired above zero.")
    else:
        for r in a.activated_rules:
            st.write(f"Rule {r['rule']} — strength {r['strength']:.3f} — {r['description']}")

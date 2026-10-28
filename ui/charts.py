import pandas as pd
import plotly.express as px
import numpy as np
from fuzzy.membership import INPUT_SETS

def priority_chart(rows):
    df = pd.DataFrame(rows)
    return px.bar(df, x="Task", y="Priority Score", color="Level", title="Task Priority Scores",
                  range_y=[0,100])

def membership_chart(memberships):
    # Visualize the membership degree observed for each input variable.
    rows = []
    for var, sets in memberships.items():
        for name, value in sets.items():
            rows.append({"Variable": var.replace("_"," ").title(), "Set": name, "Membership": value})
    df = pd.DataFrame(rows)
    return px.bar(df, x="Set", y="Membership", color="Set", facet_col="Variable",
                  title="Observed Fuzzy Membership Degrees", range_y=[0,1])

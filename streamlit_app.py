import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Technology Radar Chart", layout="wide")

st.title("🌈 Technology Radar Chart Generator")
st.markdown("""
An interactive, colorful **Technology Radar** inspired by ThoughtWorks.  
Each ring represents an adoption stage — **Adopt**, **Trial**, **Assess**, and **Hold** — and  
each quadrant represents a technology category.
""")

# --- Setup ---
categories = ["AI", "Cloud", "Dev Tools", "Platforms", "Languages", "Other"]
stages = ["Adopt", "Trial", "Assess", "Hold"]
stage_colors = {
    "Adopt": "rgba(102, 187, 106, 0.4)",   # Green
    "Trial": "rgba(255, 235, 59, 0.4)",    # Yellow
    "Assess": "rgba(33, 150, 243, 0.4)",   # Blue
    "Hold": "rgba(239, 83, 80, 0.4)"       # Red
}
stage_to_radius = {"Adopt": 1, "Trial": 2, "Assess": 3, "Hold": 4}

# --- Sidebar Inputs ---
st.sidebar.header("⚙️ Add Technologies")
num_techs = st.sidebar.number_input("Number of technologies", min_value=1, max_value=30, value=6)

technologies = []
for i in range(num_techs):
    with st.sidebar.expander(f"Technology {i+1}", expanded=(i == 0)):
        name = st.text_input(f"Name of Technology {i+1}", key=f"name_{i}")
        category = st.selectbox(f"Category for {i+1}", categories, key=f"cat_{i}")
        stage = st.selectbox(f"Adoption Stage for {i+1}", stages, key=f"stage_{i}")
        if name:
            technologies.append({"name": name, "category": category, "stage": stage})

if not technologies:
    st.info("👈 Add some technologies in the sidebar to generate your radar chart.")
    st.stop()

# --- Assign each category a distinct angular zone (for even spacing) ---
angle_per_category = 360 / len(categories)
category_angles = {cat: i * angle_per_category + angle_per_category / 2 for i, cat in enumerate(categories)}

# --- Create the Figure ---
fig = go.Figure()

# Add colored background rings (bigger to smaller)
for stage, radius in reversed(stage_to_radius.items()):
    fig.add_trace(go.Scatterpolar(
        r=[radius, radius, 0],
        theta=[0, 360, 0],
        mode='lines',
        fill='toself',
        fillcolor=stage_colors[stage],
        line_color='rgba(255,255,255,0)',
        name=f"{stage} Zone",
        hoverinfo='skip',
        showlegend=False
    ))

# Add technology points
for category in categories:
    items = [t for t in technologies if t["category"] == category]
    if items:
        fig.add_trace(go.Scatterpolar(
            r=[stage_to_radius[t["stage"]] for t in items],
            theta=[category_angles[category]] * len(items),
            mode='markers+text',
            text=[t["name"] for t in items],
            textposition='top center',
            name=category,
            marker=dict(size=12, line=dict(width=1, color='white'))
        ))

# --- Layout ---
fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            tickvals=[1, 2, 3, 4],
            ticktext=stages,
            range=[0.5, 4.5],
            showgrid=False
        ),
        angularaxis=dict(
            tickvals=[v for v in category_angles.values()],
            ticktext=categories,
            rotation=90,
            direction="clockwise"
        )
    ),
    showlegend=True,
    template="plotly_white",
    height=750,
    title="Technology Radar",
)

st.plotly_chart(fig, use_container_width=True)

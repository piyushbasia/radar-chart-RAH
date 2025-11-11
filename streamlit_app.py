import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Technology Radar Chart", layout="wide")

st.title("🧭 Technology Radar Chart Generator")
st.markdown("""
Create a colorful, interactive **Technology Radar** inspired by ThoughtWorks Radar.  
Each ring shows an adoption stage: **Adopt → Trial → Assess → Hold**.
""")

# --- Setup ---
categories = ["AI", "Cloud", "Dev Tools", "Platforms", "Languages", "Other"]
stages = ["Adopt", "Trial", "Assess", "Hold"]
stage_colors = {
    "Adopt": "rgba(102, 187, 106, 0.3)",     # Green
    "Trial": "rgba(255, 235, 59, 0.3)",      # Yellow
    "Assess": "rgba(33, 150, 243, 0.3)",     # Blue
    "Hold": "rgba(239, 83, 80, 0.3)"         # Red
}

stage_to_radius = {"Adopt": 1, "Trial": 2, "Assess": 3, "Hold": 4}

# --- User Inputs ---
st.sidebar.header("⚙️ Add Technologies")
num_techs = st.sidebar.number_input("Number of technologies", min_value=1, max_value=20, value=5)

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

# --- Plotly Figure ---
fig = go.Figure()

# Add colorful background rings
for stage, radius in reversed(stage_to_radius.items()):
    fig.add_trace(go.Scatterpolar(
        r=[radius, radius],
        theta=[0, 360],
        mode='lines',
        fill='toself',
        fillcolor=stage_colors[stage],
        line_color='rgba(255,255,255,0)',
        name=f"{stage} (Zone)",
        hoverinfo='skip'
    ))

# Add technology points
for category in categories:
    items = [t for t in technologies if t["category"] == category]
    if items:
        fig.add_trace(go.Scatterpolar(
            r=[stage_to_radius[t["stage"]] for t in items],
            theta=[category] * len(items),
            mode='markers+text',
            text=[t["name"] for t in items],
            textposition='top center',
            name=category,
            marker=dict(size=12, line=dict(width=1, color='white'))
        ))

# Layout styling
fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            tickvals=[1, 2, 3, 4],
            ticktext=stages,
            range=[0.5, 4.5],
            showline=False,
            showgrid=False
        ),
        angularaxis=dict(
            tickvals=[i for i, c in enumerate(categories)],
            ticktext=categories,
            rotation=90,
            direction="clockwise"
        )
    ),
    showlegend=True,
    template="plotly_white",
    height=700,
    title="🌈 Technology Radar"
)

st.plotly_chart(fig, use_container_width=True)

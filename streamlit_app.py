import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Technology Radar Generator", layout="wide")

st.title("🧭 Technology Radar Chart Generator")
st.markdown("""
This app lets you create a **Technology Radar** based on your team's technology stack.
Add technologies, select their category and adoption stage, and visualize them instantly.
""")

# Define radar categories and adoption stages
categories = ["AI", "Cloud", "Dev Tools", "Platforms", "Languages", "Other"]
stages = ["Adopt", "Trial", "Assess", "Hold"]

# User input section
st.sidebar.header("Add Technologies")
num_techs = st.sidebar.number_input("Number of technologies", min_value=1, max_value=20, value=5)

technologies = []
for i in range(num_techs):
    with st.sidebar.expander(f"Technology {i+1}", expanded=(i == 0)):
        name = st.text_input(f"Name of Technology {i+1}", key=f"name_{i}")
        category = st.selectbox(f"Category for {i+1}", categories, key=f"cat_{i}")
        stage = st.selectbox(f"Adoption Stage for {i+1}", stages, key=f"stage_{i}")
        if name:
            technologies.append({"name": name, "category": category, "stage": stage})

if technologies:
    st.subheader("📊 Generated Technology Radar")

    # Mapping stages to radar radius
    stage_to_radius = {"Adopt": 1, "Trial": 2, "Assess": 3, "Hold": 4}

    # Convert data to plotly radar format
    radar_points = {
        "AI": [],
        "Cloud": [],
        "Dev Tools": [],
        "Platforms": [],
        "Languages": [],
        "Other": [],
    }

    for tech in technologies:
        radar_points[tech["category"]].append({
            "name": tech["name"],
            "radius": stage_to_radius[tech["stage"]]
        })

    # Plotly figure
    fig = go.Figure()

    for category, items in radar_points.items():
        if items:
            fig.add_trace(go.Scatterpolar(
                r=[i["radius"] for i in items],
                theta=[category]*len(items),
                mode='markers+text',
                text=[i["name"] for i in items],
                textposition='top center',
                name=category,
                marker=dict(size=10, line=dict(width=1, color='white'))
            ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                tickvals=[1, 2, 3, 4],
                ticktext=stages[::-1],
                range=[0.5, 4.5]
            ),
            angularaxis=dict(
                tickvals=[i for i, c in enumerate(categories)],
                ticktext=categories
            )
        ),
        showlegend=True,
        template="plotly_white",
        height=700
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("👈 Add some technologies in the sidebar to generate your radar chart.")

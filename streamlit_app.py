import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import patches

st.title("Radar Chart")

# Optional: make placements reproducible while testing
np.random.seed(42)

# --- Chart Configuration ---
quadrant_labels = ["GenAI", "Dev tool", "Platforms", "Tools"]
status_rings = {
    "Approved": {"radius": 2, "color": "#4CAF50"},
    "Testing": {"radius": 3, "color": "#FFC107"},
    "Innovation": {"radius": 4, "color": "#2196F3"},
    "Not Approved": {"radius": 5, "color": "#FF0000"},
}

ai_tools = {
    "ChatGPT-4": ("GenAI", "Approved"),
    "Copilot": ("Dev tool", "Approved"),
    "TensorFlow": ("Platforms", "Approved"),
    "Midjourney": ("GenAI", "Testing"),
    "GitHub Actions": ("Tools", "Approved"),
    "LangChain": ("Dev tool", "Testing"),
    "Hugging Face": ("Platforms", "Innovation"),
    "Zapier": ("Tools", "Not Approved"),
    "DALL-E 3": ("GenAI", "Innovation"),
    "Jira": ("Tools", "Testing"),
}

# --- Chart Generation ---
fig, ax = plt.subplots(figsize=(12, 12))
ax.set_aspect('equal')

# Draw rings as annuli using Wedge (width = outer - inner)
prev_radius = 0.0
for status, props in status_rings.items():
    outer = props['radius']
    width = outer - prev_radius
    # full circle wedge with width draws an annulus
    ann = patches.Wedge(center=(0, 0),
                        r=outer,
                        theta1=0,
                        theta2=360,
                        width=width,
                        facecolor=props['color'],
                        alpha=0.25,
                        edgecolor='black',
                        linewidth=1.0,
                        zorder=1)
    ax.add_patch(ann)

    # label the band (placed at mid-radius)
    ax.text(0,
            (outer + prev_radius) / 2,
            status,
            ha='center',
            va='center',
            fontsize=12,
            weight='bold',
            zorder=3)
    prev_radius = outer

# Draw quadrant crosshair
ax.axhline(0, color='black', lw=1, zorder=4)
ax.axvline(0, color='black', lw=1, zorder=4)

# Add quadrant labels
max_radius = max(r['radius'] for r in status_rings.values())
label_offset = max_radius + 0.6
ax.text(label_offset / np.sqrt(2), label_offset / np.sqrt(2), quadrant_labels[0], ha='center', va='center', fontsize=14, weight='bold', zorder=5)
ax.text(-label_offset / np.sqrt(2), label_offset / np.sqrt(2), quadrant_labels[1], ha='center', va='center', fontsize=14, weight='bold', zorder=5)
ax.text(-label_offset / np.sqrt(2), -label_offset / np.sqrt(2), quadrant_labels[2], ha='center', va='center', fontsize=14, weight='bold', zorder=5)
ax.text(label_offset / np.sqrt(2), -label_offset / np.sqrt(2), quadrant_labels[3], ha='center', va='center', fontsize=14, weight='bold', zorder=5)

# Precompute status radii list to find inner radius for each status easily
status_order = list(status_rings.keys())
status_radius_map = {s: status_rings[s]['radius'] for s in status_order}
status_inner_map = {}
prev = 0.0
for s in status_order:
    status_inner_map[s] = prev
    prev = status_radius_map[s]

# Plot the AI tools inside correct annulus and quadrant
for tool, (quadrant, status) in ai_tools.items():
    if quadrant not in quadrant_labels or status not in status_rings:
        # skip invalid entries
        continue

    quadrant_index = quadrant_labels.index(quadrant)
    inner_r = status_inner_map[status]
    outer_r = status_radius_map[status]

    # radial position within the band's bounds (leave a margin of 0.25)
    radial_pos = np.random.uniform(inner_r + 0.25, outer_r - 0.25)

    # angular span for quadrant: e.g., quadrant 0 => 0..90 degrees
    angle_min = quadrant_index * 90
    angle_max = (quadrant_index + 1) * 90
    angle_deg = np.random.uniform(angle_min + 8, angle_max - 8)
    angle_rad = np.deg2rad(angle_deg)

    x = radial_pos * np.cos(angle_rad)
    y = radial_pos * np.sin(angle_rad)

    ax.text(x, y, tool,
            ha='center', va='center',
            fontsize=9,
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="black", lw=0.5),
            zorder=6)

# Final touches
ax.set_xlim(-max_radius - 1, max_radius + 1)
ax.set_ylim(-max_radius - 1, max_radius + 1)
ax.set_title("AI Tools Landscape", fontsize=20, weight='bold', pad=20)
ax.axis('off')

st.pyplot(plt)

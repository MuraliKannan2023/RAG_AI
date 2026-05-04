import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

fig, ax = plt.subplots(1, 1, figsize=(20, 14))
fig.patch.set_facecolor('#0a0a1a')
ax.set_facecolor('#0a0a1a')
ax.set_xlim(0, 20)
ax.set_ylim(0, 14)
ax.axis('off')

# --- Color Palette ---
COLORS = {
    'title': '#ffffff',
    'subtitle': '#8892b0',
    'user': '#64ffda',
    'streamlit': '#ff6b6b',
    'pdf': '#ffd93d',
    'chunker': '#6c5ce7',
    'embedder': '#00b894',
    'vectordb': '#0984e3',
    'llm': '#e17055',
    'response': '#74b9ff',
    'arrow': '#4a5568',
    'box_edge': '#2d3748',
    'glow': '#1a1a2e',
}

def draw_rounded_box(ax, x, y, w, h, color, label, sublabel="", icon=""):
    """Draw a modern rounded box with gradient-like effect."""
    # Shadow
    shadow = FancyBboxPatch((x + 0.05, y - 0.05), w, h,
                             boxstyle="round,pad=0.15", linewidth=0,
                             facecolor='#000000', alpha=0.3, zorder=1)
    ax.add_patch(shadow)
    # Main box
    box = FancyBboxPatch((x, y), w, h,
                          boxstyle="round,pad=0.15", linewidth=2,
                          edgecolor=color, facecolor=color + '18', zorder=2)
    ax.add_patch(box)
    # Top accent line
    accent = FancyBboxPatch((x, y + h - 0.08), w, 0.08,
                             boxstyle="round,pad=0.02", linewidth=0,
                             facecolor=color, alpha=0.7, zorder=3)
    ax.add_patch(accent)
    # Icon + Label
    full_label = f"{icon} {label}" if icon else label
    ax.text(x + w / 2, y + h / 2 + (0.15 if sublabel else 0), full_label,
            ha='center', va='center', fontsize=13, fontweight='bold',
            color=color, zorder=4, fontfamily='sans-serif')
    if sublabel:
        ax.text(x + w / 2, y + h / 2 - 0.25, sublabel,
                ha='center', va='center', fontsize=9,
                color='#8892b0', zorder=4, fontfamily='sans-serif')

def draw_arrow(ax, x1, y1, x2, y2, color='#4a5568', label="", curved=False):
    """Draw a styled arrow between components."""
    style = "arc3,rad=0.2" if curved else "arc3,rad=0.0"
    arrow = FancyArrowPatch((x1, y1), (x2, y2),
                             arrowstyle='->', mutation_scale=18,
                             linewidth=2, color=color, alpha=0.8,
                             connectionstyle=style, zorder=5)
    ax.add_patch(arrow)
    if label:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        ax.text(mx, my + 0.25, label, ha='center', va='center',
                fontsize=8, color='#a0aec0', fontstyle='italic', zorder=6,
                bbox=dict(boxstyle='round,pad=0.2', facecolor='#0a0a1a', 
                         edgecolor='none', alpha=0.8))

# === TITLE ===
ax.text(10, 13.3, "RAG AI — Document Assistant", ha='center', va='center',
        fontsize=26, fontweight='bold', color=COLORS['title'],
        fontfamily='sans-serif', zorder=10)
ax.text(10, 12.8, "Retrieval-Augmented Generation Architecture",
        ha='center', va='center', fontsize=13, color=COLORS['subtitle'],
        fontfamily='sans-serif', zorder=10)

# Decorative line under title
ax.plot([3, 17], [12.5, 12.5], color='#64ffda', linewidth=1.5, alpha=0.4, zorder=10)

# === PHASE LABELS ===
# Ingestion phase
ax.text(5.5, 11.8, ">>  INGESTION PIPELINE", ha='center', va='center',
        fontsize=11, fontweight='bold', color='#ffd93d', alpha=0.8,
        fontfamily='sans-serif', zorder=10)

# Query phase  
ax.text(14.5, 11.8, ">>  QUERY PIPELINE", ha='center', va='center',
        fontsize=11, fontweight='bold', color='#74b9ff', alpha=0.8,
        fontfamily='sans-serif', zorder=10)

# Divider line
ax.plot([10.3, 10.3], [2, 11.5], color='#2d3748', linewidth=1.5, 
        linestyle='--', alpha=0.5, zorder=1)

# ============================
# LEFT SIDE: INGESTION PIPELINE
# ============================

# 1. User Upload
draw_rounded_box(ax, 0.5, 9.5, 3.2, 1.5, COLORS['user'], "User Upload", "PDF Document", "[U]")

# 2. Streamlit UI
draw_rounded_box(ax, 5, 9.5, 3.2, 1.5, COLORS['streamlit'], "Streamlit UI", "Web Interface", "[S]")

# 3. PDF Reader
draw_rounded_box(ax, 0.5, 6.5, 3.2, 1.5, COLORS['pdf'], "PDF Reader", "pypdf Library", "[P]")

# 4. Text Chunker
draw_rounded_box(ax, 5, 6.5, 3.2, 1.5, COLORS['chunker'], "Text Chunker", "900 chars / 150 overlap", "[C]")

# 5. Embedder (Ingestion)
draw_rounded_box(ax, 0.5, 3.5, 3.2, 1.5, COLORS['embedder'], "Gemini Embedder", "768-dim vectors", "[E]")

# 6. Pinecone (center-bottom, shared)
draw_rounded_box(ax, 5, 3.5, 3.2, 1.5, COLORS['vectordb'], "Pinecone", "Vector Database", "[DB]")

# Arrows - Ingestion
draw_arrow(ax, 3.7, 10.25, 5.0, 10.25, '#64ffda', "Upload PDF")
draw_arrow(ax, 2.1, 9.5, 2.1, 8.0, '#ff6b6b', "Extract")
draw_arrow(ax, 3.7, 7.25, 5.0, 7.25, '#ffd93d', "Pages")
draw_arrow(ax, 6.6, 6.5, 6.6, 5.0, '#6c5ce7', "")
draw_arrow(ax, 5.0, 4.25, 3.7, 4.25, '#0984e3', "Vectors")
draw_arrow(ax, 2.1, 6.5, 2.1, 5.0, '#ffd93d', "Text")

# Label for chunks->embed
draw_arrow(ax, 6.6, 6.5, 2.1, 5.0, '#6c5ce7', "Chunks", curved=True)

# ============================
# RIGHT SIDE: QUERY PIPELINE
# ============================

# 7. User Query
draw_rounded_box(ax, 11.5, 9.5, 3.2, 1.5, COLORS['user'], "User Query", "Natural Language", "[Q]")

# 8. Query Embedder
draw_rounded_box(ax, 15.5, 9.5, 3.2, 1.5, COLORS['embedder'], "Gemini Embedder", "Query -> Vector", "[E]")

# 9. Pinecone Search
draw_rounded_box(ax, 11.5, 6.5, 3.2, 1.5, COLORS['vectordb'], "Pinecone Search", "Top-K Similarity", "[S]")

# 10. Context Builder
draw_rounded_box(ax, 15.5, 6.5, 3.2, 1.5, COLORS['response'], "Context Builder", "Matched Chunks", "[CB]")

# 11. Groq LLM
draw_rounded_box(ax, 11.5, 3.5, 3.2, 1.5, COLORS['llm'], "Groq LLM", "Llama 3.3 70B", "[LLM]")

# 12. Response
draw_rounded_box(ax, 15.5, 3.5, 3.2, 1.5, COLORS['streamlit'], "AI Response", "Streamlit Chat UI", "[R]")

# Arrows - Query
draw_arrow(ax, 14.7, 10.25, 15.5, 10.25, '#64ffda', "Embed Query")
draw_arrow(ax, 17.1, 9.5, 17.1, 8.0, '#00b894', "")
draw_arrow(ax, 15.5, 7.25, 14.7, 7.25, '#0984e3', "Results")
draw_arrow(ax, 13.1, 9.5, 13.1, 8.0, '#64ffda', "")
draw_arrow(ax, 17.1, 6.5, 17.1, 5.0, '#74b9ff', "Context")
draw_arrow(ax, 15.5, 4.25, 14.7, 4.25, '#e17055', "Answer")
draw_arrow(ax, 13.1, 6.5, 13.1, 5.0, '#0984e3', "Matched")

# Cross arrow: Embed -> Search
draw_arrow(ax, 17.1, 8.0, 14.7, 7.25, '#00b894', "Query Vector", curved=True)

# ============================
# BOTTOM: TECH STACK BAR
# ============================
tech_bar = FancyBboxPatch((1, 0.5), 18, 1.8, boxstyle="round,pad=0.2",
                           linewidth=1.5, edgecolor='#2d3748',
                           facecolor='#111827', zorder=2)
ax.add_patch(tech_bar)

ax.text(10, 2.0, "TECH STACK", ha='center', va='center',
        fontsize=11, fontweight='bold', color='#e2e8f0', zorder=10)

techs = [
    ("Streamlit", COLORS['streamlit'], 3),
    ("pypdf", COLORS['pdf'], 6),
    ("Gemini Embeddings", COLORS['embedder'], 9),
    ("Pinecone", COLORS['vectordb'], 12),
    ("Groq API", COLORS['llm'], 15),
    ("Llama 3.3", COLORS['llm'], 18),
]

for name, color, x_pos in techs:
    pill = FancyBboxPatch((x_pos - 1.2, 0.8), 2.4, 0.7,
                           boxstyle="round,pad=0.15", linewidth=1.5,
                           edgecolor=color, facecolor=color + '22', zorder=3)
    ax.add_patch(pill)
    ax.text(x_pos, 1.15, name, ha='center', va='center',
            fontsize=9, fontweight='bold', color=color, zorder=4)

# Save
plt.tight_layout()
plt.savefig(r"c:\Users\muralidharan.k\RAG AI\RAG_AI_Architecture.jpg",
            dpi=200, bbox_inches='tight', facecolor='#0a0a1a',
            edgecolor='none', format='jpg')
plt.close()
print("Architecture diagram saved as RAG_AI_Architecture.jpg")

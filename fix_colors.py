content = open('app.py', encoding='utf-8').read()

replacements = [
    # Primary brand blue → golden yellow
    ("#1D4ED8", "#B45309"),
    ("#2563EB", "#D97706"),
    ("#1e3a5f", "#78350F"),
    ("#0f2942", "#451A03"),
    ("#0369a1", "#B45309"),
    ("#0284c7", "#D97706"),
    ("#075985", "#92400E"),
    ("#1e40af", "#92400E"),

    # Teal accent → keep as secondary (warm green-gold)
    ("#0D9488", "#CA8A04"),
    ("#99f6e4", "#FEF08A"),

    # Light blue backgrounds → light yellow
    ("#bfdbfe", "#FEF9C3"),
    ("#dbeafe", "#FEF9C3"),
    ("#eff6ff", "#FFFBEB"),
    ("#e0f2fe", "#FEF9C3"),
    ("#f0f9ff", "#FFFBEB"),
    ("#f0fdf4", "#FEFCE8"),
    ("#e0f7fa", "#FEF9C3"),

    # Blue text colors
    ("#7dd3fc", "#FCD34D"),
    ("#bae6fd", "#FDE68A"),
    ("#94a3b8", "#A16207"),

    # Gradient backgrounds
    ("linear-gradient(135deg,#1e3a5f 0%,#1D4ED8 60%,#0D9488 100%)",
     "linear-gradient(135deg,#78350F 0%,#B45309 60%,#D97706 100%)"),
    ("linear-gradient(135deg, #1e3a5f 0%, #1D4ED8 60%, #0D9488 100%)",
     "linear-gradient(135deg, #78350F 0%, #B45309 60%, #D97706 100%)"),
    ("linear-gradient(90deg,#1e3a5f 0%,#1D4ED8 100%)",
     "linear-gradient(90deg,#78350F 0%,#B45309 100%)"),
    ("linear-gradient(90deg, #1e3a5f 0%, #0369a1 100%)",
     "linear-gradient(90deg, #78350F 0%, #B45309 100%)"),
    ("linear-gradient(180deg,#1e3a5f 0%,#0f2942 100%)",
     "linear-gradient(180deg,#78350F 0%,#451A03 100%)"),
    ("linear-gradient(180deg, #1e3a5f 0%, #0f2942 100%)",
     "linear-gradient(180deg, #78350F 0%, #451A03 100%)"),
    ("linear-gradient(90deg,#1D4ED8,#2563EB)",
     "linear-gradient(90deg,#B45309,#D97706)"),
    ("linear-gradient(90deg, #0369a1 0%, #0284c7 100%)",
     "linear-gradient(90deg, #B45309 0%, #D97706 100%)"),
    ("linear-gradient(90deg, #075985 0%, #0369a1 100%)",
     "linear-gradient(90deg, #92400E 0%, #B45309 100%)"),
    ("linear-gradient(135deg, #0369a1 0%, #0284c7 100%)",
     "linear-gradient(135deg, #B45309 0%, #D97706 100%)"),
    ("linear-gradient(135deg,#1D4ED8,#2563EB)",
     "linear-gradient(135deg,#B45309,#D97706)"),

    # Plotly color scales
    ('[[0,"#bfdbfe"],[1,C_BLUE]]',  '[[0,"#FEF9C3"],[1,C_AMBER]]'),
    ('[[0,"#99f6e4"],[1,C_TEAL]]',  '[[0,"#FEF9C3"],[1,C_GOLD]]'),
    ('[[0,"#dbeafe"],[0.5,C_BLUE],[1,"#1e3a5f"]]',
     '[[0,"#FEF9C3"],[0.5,C_AMBER],[1,"#78350F"]]'),

    # Python color constants
    ('C_BLUE   = "#1D4ED8"', 'C_AMBER  = "#D97706"'),
    ('C_TEAL   = "#0D9488"', 'C_GOLD   = "#CA8A04"'),
    ('C_AMBER  = "#D97706"', 'C_BROWN  = "#92400E"'),
    ('C_SLATE  = "#334155"', 'C_SLATE  = "#44403C"'),
    ('PALETTE  = [C_BLUE, C_TEAL, C_AMBER, "#7C3AED", "#059669", "#DC2626", "#0891B2"]',
     'PALETTE  = [C_AMBER, C_GOLD, C_BROWN, "#D97706", "#B45309", "#78350F", "#CA8A04"]'),

    # Border colors
    ("border: 2px solid #1D4ED8", "border: 2px solid #D97706"),
    ("border: 2px solid #0369a1", "border: 2px solid #D97706"),
    ("border-left: 4px solid #1D4ED8", "border-left: 4px solid #D97706"),
    ("border-top: 4px solid #1D4ED8", "border-top: 4px solid #D97706"),
    ("border-top-color: #1D4ED8", "border-top-color: #D97706"),
    ("border-top-color:#0D9488", "border-top-color:#CA8A04"),
    ("border: 1px solid #bfdbfe", "border: 1px solid #FDE68A"),
    ("border-color: #334155", "border-color: #78350F"),

    # KPI card accent colors
    (".kpi-card.teal   { border-top-color:#0D9488; }",
     ".kpi-card.teal   { border-top-color:#CA8A04; }"),
    (".kpi-card.amber  { border-top-color:#D97706; }",
     ".kpi-card.amber  { border-top-color:#B45309; }"),
    (".kpi-card.purple { border-top-color:#7C3AED; }",
     ".kpi-card.purple { border-top-color:#92400E; }"),
    (".kpi-card.green  { border-top-color:#059669; }",
     ".kpi-card.green  { border-top-color:#78350F; }"),

    # Metric card gradients
    ("background:linear-gradient(135deg,#065f46,#059669)",
     "background:linear-gradient(135deg,#78350F,#B45309)"),
    ("background:linear-gradient(135deg,#7c3aed,#8b5cf6)",
     "background:linear-gradient(135deg,#92400E,#D97706)"),
    ("background:linear-gradient(135deg,#b45309,#d97706)",
     "background:linear-gradient(135deg,#451A03,#78350F)"),

    # App background
    ("background: #F8FAFC", "background: #FFFBEB"),
    ("background:#F8FAFC",  "background:#FFFBEB"),

    # Supplier bar color
    ("marker_color=C_TEAL", "marker_color=C_GOLD"),

    # Text colors
    ("color:#1D4ED8", "color:#B45309"),
    ("color: #1D4ED8", "color: #B45309"),
    ("color:#1e3a5f", "color:#78350F"),
    ("color: #1e3a5f", "color: #78350F"),
    ("color:#0369a1", "color:#B45309"),
    ("color: #0369a1", "color: #B45309"),
    ("color:#7dd3fc", "color:#FCD34D"),
    ("color:#94a3b8", "color:#A16207"),
    ("color:#64748b", "color:#92400E"),
    ("color: #64748b", "color: #92400E"),
    ("color:#334155", "color:#44403C"),
    ("color: #334155", "color: #44403C"),
    ("font_color=C_SLATE", "font_color=C_SLATE"),
]

for old, new in replacements:
    content = content.replace(old, new)

open('app.py', 'w', encoding='utf-8').write(content)
print("Done - colors updated to yellow/amber theme")

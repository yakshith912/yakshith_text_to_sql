c = open("app.py", encoding="utf-8").read()

# ── 1. Full CSS replacement ───────────────────────────────────────────────────
OLD = 'background:linear-gradient(135deg,#060818 0%,#0B0F2A 50%,#0D1117 100%)!important;'
NEW = 'background:linear-gradient(135deg,#0A0A0A 0%,#0F1923 40%,#071A12 100%)!important;'
c = c.replace(OLD, NEW)

# Sidebar bg
c = c.replace(
    'background:linear-gradient(180deg,#060818 0%,#0B0F2A 100%)!important;',
    'background:linear-gradient(180deg,#0A0A0A 0%,#0F1923 100%)!important;'
)

# Sidebar border
c = c.replace(
    'border-right:1px solid rgba(0,212,255,0.12)!important;',
    'border-right:1px solid rgba(16,185,129,0.15)!important;'
)

# Sidebar hover
c = c.replace(
    'background:rgba(0,212,255,0.1)!important;color:#00D4FF!important;transform:none!important;',
    'background:rgba(16,185,129,0.1)!important;color:#10B981!important;transform:none!important;'
)

# Collapsed control
c = c.replace('color:#00D4FF!important;}', 'color:#10B981!important;}', 1)

# Input border/focus
c = c.replace(
    'background:rgba(0,212,255,0.04)!important;\n    border:1.5px solid rgba(0,212,255,0.15)!important;\n    border-radius:12px!important;color:#F1F5F9!important;\n    font-size:1rem!important;padding:0.75rem 1rem!important;\n}\n.stTextInput>div>div>input:focus,.stTextArea>div>div>textarea:focus{\n    border-color:#00D4FF!important;box-shadow:0 0 0 3px rgba(0,212,255,0.12)!important;',
    'background:rgba(16,185,129,0.04)!important;\n    border:1.5px solid rgba(16,185,129,0.15)!important;\n    border-radius:12px!important;color:#F1F5F9!important;\n    font-size:1rem!important;padding:0.75rem 1rem!important;\n}\n.stTextInput>div>div>input:focus,.stTextArea>div>div>textarea:focus{\n    border-color:#10B981!important;box-shadow:0 0 0 3px rgba(16,185,129,0.12)!important;'
)

# Buttons
c = c.replace(
    'background:linear-gradient(135deg,#00D4FF,#7C3AED)!important;\n    color:#FFFFFF!important;border:none!important;border-radius:10px!important;\n    font-weight:700!important;font-size:0.9rem!important;padding:0.6rem 1.4rem!important;\n    transition:all 0.2s ease!important;box-shadow:0 4px 15px rgba(0,212,255,0.2)!important;\n}\n.stButton>button:hover{\n    transform:translateY(-2px)!important;box-shadow:0 8px 25px rgba(0,212,255,0.35)!important;',
    'background:linear-gradient(135deg,#10B981,#059669)!important;\n    color:#FFFFFF!important;border:none!important;border-radius:10px!important;\n    font-weight:700!important;font-size:0.9rem!important;padding:0.6rem 1.4rem!important;\n    transition:all 0.2s ease!important;box-shadow:0 4px 15px rgba(16,185,129,0.25)!important;\n}\n.stButton>button:hover{\n    transform:translateY(-2px)!important;box-shadow:0 8px 25px rgba(16,185,129,0.4)!important;'
)

# Selectbox
c = c.replace(
    'background:rgba(0,212,255,0.04)!important;\n    border:1.5px solid rgba(0,212,255,0.15)!important;\n    border-radius:10px!important;color:#F1F5F9!important;',
    'background:rgba(16,185,129,0.04)!important;\n    border:1.5px solid rgba(16,185,129,0.15)!important;\n    border-radius:10px!important;color:#F1F5F9!important;'
)

# Tabs
c = c.replace(
    'background:rgba(0,212,255,0.04)!important;border-radius:12px!important;\n    padding:4px!important;gap:4px!important;border:1px solid rgba(0,212,255,0.1)!important;',
    'background:rgba(16,185,129,0.04)!important;border-radius:12px!important;\n    padding:4px!important;gap:4px!important;border:1px solid rgba(16,185,129,0.1)!important;'
)
c = c.replace(
    '.stTabs [aria-selected="true"]{background:rgba(0,212,255,0.15)!important;color:#00D4FF!important;}',
    '.stTabs [aria-selected="true"]{background:rgba(16,185,129,0.15)!important;color:#10B981!important;}'
)

# Dataframe
c = c.replace(
    'border:1px solid rgba(0,212,255,0.1)!important;}',
    'border:1px solid rgba(16,185,129,0.1)!important;}'
)

# Scrollbar
c = c.replace('background:#1E3A5F;border-radius:3px;}', 'background:#134E3A;border-radius:3px;}')
c = c.replace('::-webkit-scrollbar-thumb:hover{background:#00D4FF;}', '::-webkit-scrollbar-thumb:hover{background:#10B981;}')

# Cards
c = c.replace(
    '.glass-card{\n    background:rgba(0,212,255,0.03);\n    border:1px solid rgba(0,212,255,0.1);',
    '.glass-card{\n    background:rgba(16,185,129,0.03);\n    border:1px solid rgba(16,185,129,0.1);'
)
c = c.replace(
    '.glass-card:hover{\n    border-color:rgba(0,212,255,0.3);\n    box-shadow:0 8px 32px rgba(0,212,255,0.08);transform:translateY(-2px);\n}',
    '.glass-card:hover{\n    border-color:rgba(16,185,129,0.3);\n    box-shadow:0 8px 32px rgba(16,185,129,0.08);transform:translateY(-2px);\n}'
)

# KPI tile
c = c.replace(
    '.kpi-tile{\n    background:rgba(0,212,255,0.03);border:1px solid rgba(0,212,255,0.1);',
    '.kpi-tile{\n    background:rgba(16,185,129,0.03);border:1px solid rgba(16,185,129,0.1);'
)
c = c.replace(
    '.kpi-tile:hover{border-color:rgba(0,212,255,0.3);box-shadow:0 4px 20px rgba(0,212,255,0.1);}',
    '.kpi-tile:hover{border-color:rgba(16,185,129,0.3);box-shadow:0 4px 20px rgba(16,185,129,0.1);}'
)
c = c.replace('.kpi-tile-val{font-size:1.8rem;font-weight:800;color:#00D4FF!important;}',
              '.kpi-tile-val{font-size:1.8rem;font-weight:800;color:#10B981!important;}')

# Feature cards
c = c.replace(
    '.feature-card{\n    background:rgba(0,212,255,0.02);border:1px solid rgba(0,212,255,0.08);',
    '.feature-card{\n    background:rgba(16,185,129,0.02);border:1px solid rgba(16,185,129,0.08);'
)
c = c.replace(
    '.feature-card:hover{\n    background:rgba(0,212,255,0.05);border-color:rgba(0,212,255,0.25);\n    transform:translateY(-4px);box-shadow:0 12px 40px rgba(0,212,255,0.1);\n}',
    '.feature-card:hover{\n    background:rgba(16,185,129,0.05);border-color:rgba(16,185,129,0.25);\n    transform:translateY(-4px);box-shadow:0 12px 40px rgba(16,185,129,0.1);\n}'
)
c = c.replace(
    '.feature-icon{\n    width:48px;height:48px;background:rgba(0,212,255,0.1);\n    border:1px solid rgba(0,212,255,0.2);',
    '.feature-icon{\n    width:48px;height:48px;background:rgba(16,185,129,0.1);\n    border:1px solid rgba(16,185,129,0.2);'
)

# History items
c = c.replace(
    '.history-item{\n    background:rgba(0,212,255,0.02);border:1px solid rgba(0,212,255,0.08);',
    '.history-item{\n    background:rgba(16,185,129,0.02);border:1px solid rgba(16,185,129,0.08);'
)
c = c.replace(
    '.history-item:hover{border-color:rgba(0,212,255,0.25);background:rgba(0,212,255,0.04);}',
    '.history-item:hover{border-color:rgba(16,185,129,0.25);background:rgba(16,185,129,0.04);}'
)

# Animations
c = c.replace(
    '@keyframes glow{0%,100%{box-shadow:0 0 10px rgba(0,212,255,0.3);}50%{box-shadow:0 0 25px rgba(0,212,255,0.6);}}',
    '@keyframes glow{0%,100%{box-shadow:0 0 10px rgba(16,185,129,0.3);}50%{box-shadow:0 0 25px rgba(16,185,129,0.6);}}'
)
c = c.replace('hr{border-color:rgba(0,212,255,0.08)!important;}',
              'hr{border-color:rgba(16,185,129,0.08)!important;}')

# ── 2. Sidebar logo ───────────────────────────────────────────────────────────
c = c.replace(
    'background:linear-gradient(135deg,#00D4FF,#7C3AED);',
    'background:linear-gradient(135deg,#10B981,#059669);'
)

# ── 3. Hero title gradient ────────────────────────────────────────────────────
c = c.replace(
    'background:linear-gradient(135deg,#FFFFFF 0%,#00D4FF 50%,#7C3AED 100%);',
    'background:linear-gradient(135deg,#FFFFFF 0%,#10B981 50%,#F59E0B 100%);'
)
c = c.replace(
    'background:linear-gradient(90deg,#FFFFFF 0%,#00D4FF 60%,#7C3AED 100%);',
    'background:linear-gradient(90deg,#FFFFFF 0%,#10B981 60%,#F59E0B 100%);'
)

# ── 4. Robot SVG glow ─────────────────────────────────────────────────────────
c = c.replace(
    'filter:drop-shadow(0 0 18px rgba(0,212,255,0.6))',
    'filter:drop-shadow(0 0 18px rgba(16,185,129,0.7))'
)
c = c.replace(
    'filter:drop-shadow(0 0 16px rgba(0,212,255,0.6))',
    'filter:drop-shadow(0 0 16px rgba(16,185,129,0.7))'
)
c = c.replace(
    'filter:drop-shadow(0 0 10px rgba(0,212,255,0.5))',
    'filter:drop-shadow(0 0 10px rgba(16,185,129,0.6))'
)

# ── 5. Robot card border ──────────────────────────────────────────────────────
c = c.replace(
    'rgba(0,212,255,0.08) 0%,rgba(124,58,237,0.05)',
    'rgba(16,185,129,0.08) 0%,rgba(245,158,11,0.05)'
)
c = c.replace(
    'border:1px solid rgba(0,212,255,0.2);\n            border-radius:24px;',
    'border:1px solid rgba(16,185,129,0.2);\n            border-radius:24px;'
)
c = c.replace(
    'background:rgba(0,212,255,0.05);border:1px solid rgba(0,212,255,0.2);',
    'background:rgba(16,185,129,0.05);border:1px solid rgba(16,185,129,0.2);'
)

# ── 6. Hero section border ────────────────────────────────────────────────────
c = c.replace(
    'border:1px solid rgba(0,212,255,0.15);border-radius:20px;',
    'border:1px solid rgba(16,185,129,0.15);border-radius:20px;'
)
c = c.replace(
    'background:radial-gradient(circle,rgba(0,212,255,0.06) 0%,transparent 70%)',
    'background:radial-gradient(circle,rgba(16,185,129,0.06) 0%,transparent 70%)'
)

# ── 7. Badges ─────────────────────────────────────────────────────────────────
c = c.replace(
    'background:rgba(0,212,255,0.1);border:1px solid rgba(0,212,255,0.3);color:#00D4FF',
    'background:rgba(16,185,129,0.1);border:1px solid rgba(16,185,129,0.3);color:#10B981'
)
c = c.replace(
    'background:rgba(0,212,255,0.1);border:1px solid rgba(0,212,255,0.3);\n                    color:#00D4FF',
    'background:rgba(16,185,129,0.1);border:1px solid rgba(16,185,129,0.3);\n                    color:#10B981'
)

# ── 8. Query input pulse dot ──────────────────────────────────────────────────
c = c.replace(
    'width:8px;height:8px;background:#00D4FF;border-radius:50%;box-shadow:0 0 6px #00D4FF',
    'width:8px;height:8px;background:#10B981;border-radius:50%;box-shadow:0 0 6px #10B981'
)

# ── 9. Dashboard colors ───────────────────────────────────────────────────────
c = c.replace(
    'C1="#00D4FF"; C2="#7C3AED"; C3="#10B981"; C4="#F97316"; C5="#EC4899"',
    'C1="#10B981"; C2="#F59E0B"; C3="#8B5CF6"; C4="#EF4444"; C5="#0EA5E9"'
)
c = c.replace(
    'PAL=[C1,C2,C3,C4,C5,"#FBB724","#EF4444"]',
    'PAL=[C1,C2,C3,C4,C5,"#06B6D4","#EC4899"]'
)

# ── 10. Dashboard header ──────────────────────────────────────────────────────
c = c.replace(
    'border:1px solid rgba(0,212,255,0.2);border-radius:16px;\n        padding:1.5rem 2rem;margin-bottom:1.2rem',
    'border:1px solid rgba(16,185,129,0.2);border-radius:16px;\n        padding:1.5rem 2rem;margin-bottom:1.2rem'
)
c = c.replace(
    'color:#00D4FF;\n                    text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.4rem;',
    'color:#10B981;\n                    text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.4rem;'
)

# ── 11. Section labels ────────────────────────────────────────────────────────
c = c.replace('border-left:3px solid #00D4FF;', 'border-left:3px solid #10B981;')

# ── 12. Insight banner ────────────────────────────────────────────────────────
c = c.replace(
    'rgba(0,212,255,0.08),rgba(124,58,237,0.05)',
    'rgba(16,185,129,0.08),rgba(245,158,11,0.05)'
)
c = c.replace(
    'border:1px solid rgba(0,212,255,0.2)',
    'border:1px solid rgba(16,185,129,0.2)'
)
c = c.replace(
    '<span style="color:#00D4FF;font-weight:700;">&#10022; Key Insights',
    '<span style="color:#10B981;font-weight:700;">&#10022; Key Insights'
)

# ── 13. Hero background ───────────────────────────────────────────────────────
c = c.replace(
    'background:linear-gradient(135deg,#060818 0%,#0B0F2A 50%,#0D1B3E 100%);',
    'background:linear-gradient(135deg,#071A12 0%,#0A1F14 50%,#0F1A0A 100%);'
)

open("app.py", "w", encoding="utf-8").write(c)
print("Theme updated: Emerald Green + Amber Gold + Deep Forest")

content = open("app.py", encoding="utf-8").read()

# ── Replace entire CSS block ──────────────────────────────────────────────────
old_css_start = "st.markdown(\"\"\"\n<style>"
old_css_end   = "</style>\n\"\"\", unsafe_allow_html=True)"

start = content.index(old_css_start)
end   = content.index(old_css_end) + len(old_css_end)

new_css = '''st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

*,*::before,*::after{box-sizing:border-box;}

/* ── Base ── */
html,body,[data-testid="stAppViewContainer"]{
    font-family:'Inter',sans-serif!important;
    background:linear-gradient(135deg,#060818 0%,#0B0F2A 50%,#0D1117 100%)!important;
    color:#E2E8F0!important;
}
[data-testid="stAppViewContainer"]>.main{padding:0!important;}
.block-container{padding:0.5rem 2rem 2rem!important;max-width:100%!important;}

/* ── Hide Streamlit header ── */
[data-testid="stHeader"],header.stAppHeader,.stAppHeader{display:none!important;height:0!important;}
[data-testid="stToolbar"],.stAppToolbar,.stDeployButton,[data-testid="stMainMenu"],.stMainMenu{display:none!important;}
[data-testid="collapsedControl"]{display:flex!important;visibility:visible!important;color:#00D4FF!important;}

/* ── Sidebar ── */
[data-testid="stSidebar"]{
    background:linear-gradient(180deg,#060818 0%,#0B0F2A 100%)!important;
    border-right:1px solid rgba(0,212,255,0.12)!important;
    min-width:240px!important;display:block!important;visibility:visible!important;opacity:1!important;
}
[data-testid="stSidebarContent"]{background:transparent!important;padding:0!important;}
[data-testid="stSidebar"] *{color:#94A3B8!important;}
[data-testid="stSidebar"] .stButton>button{
    background:transparent!important;border:none!important;color:#94A3B8!important;
    text-align:left!important;padding:0.55rem 1rem!important;border-radius:10px!important;
    font-size:0.88rem!important;font-weight:500!important;width:100%!important;
    transition:all 0.2s!important;box-shadow:none!important;
}
[data-testid="stSidebar"] .stButton>button:hover{
    background:rgba(0,212,255,0.1)!important;color:#00D4FF!important;transform:none!important;
}

/* ── Text ── */
[data-testid="stAppViewContainer"] p,
[data-testid="stAppViewContainer"] label,
[data-testid="stAppViewContainer"] li,
[data-testid="stAppViewContainer"] h1,
[data-testid="stAppViewContainer"] h2,
[data-testid="stAppViewContainer"] h3,
[data-testid="stAppViewContainer"] h4{color:#E2E8F0!important;}
[data-testid="stAppViewContainer"] span[style]{color:unset;-webkit-text-fill-color:unset;}
[data-testid="stAppViewContainer"] .stMarkdown p,
[data-testid="stAppViewContainer"] .element-container p{color:#E2E8F0!important;}

/* ── Inputs ── */
.stTextInput>div>div>input,.stTextArea>div>div>textarea{
    background:rgba(0,212,255,0.04)!important;
    border:1.5px solid rgba(0,212,255,0.15)!important;
    border-radius:12px!important;color:#F1F5F9!important;
    font-size:1rem!important;padding:0.75rem 1rem!important;
}
.stTextInput>div>div>input:focus,.stTextArea>div>div>textarea:focus{
    border-color:#00D4FF!important;box-shadow:0 0 0 3px rgba(0,212,255,0.12)!important;
}
.stTextInput>div>div>input::placeholder,.stTextArea>div>div>textarea::placeholder{color:#334155!important;}

/* ── Buttons ── */
.stButton>button{
    background:linear-gradient(135deg,#00D4FF,#7C3AED)!important;
    color:#FFFFFF!important;border:none!important;border-radius:10px!important;
    font-weight:700!important;font-size:0.9rem!important;padding:0.6rem 1.4rem!important;
    transition:all 0.2s ease!important;box-shadow:0 4px 15px rgba(0,212,255,0.2)!important;
}
.stButton>button:hover{
    transform:translateY(-2px)!important;box-shadow:0 8px 25px rgba(0,212,255,0.35)!important;
}

/* ── Selectbox ── */
.stSelectbox>div>div{
    background:rgba(0,212,255,0.04)!important;
    border:1.5px solid rgba(0,212,255,0.15)!important;
    border-radius:10px!important;color:#F1F5F9!important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"]{
    background:rgba(0,212,255,0.04)!important;border-radius:12px!important;
    padding:4px!important;gap:4px!important;border:1px solid rgba(0,212,255,0.1)!important;
}
.stTabs [data-baseweb="tab"]{border-radius:8px!important;color:#64748B!important;font-weight:600!important;}
.stTabs [aria-selected="true"]{background:rgba(0,212,255,0.15)!important;color:#00D4FF!important;}

/* ── Dataframe ── */
[data-testid="stDataFrame"]{border-radius:12px!important;overflow:hidden!important;
    border:1px solid rgba(0,212,255,0.1)!important;}

/* ── Scrollbar ── */
::-webkit-scrollbar{width:6px;height:6px;}
::-webkit-scrollbar-track{background:#060818;}
::-webkit-scrollbar-thumb{background:#1E3A5F;border-radius:3px;}
::-webkit-scrollbar-thumb:hover{background:#00D4FF;}

/* ── Cards ── */
.glass-card{
    background:rgba(0,212,255,0.03);
    border:1px solid rgba(0,212,255,0.1);
    border-radius:16px;padding:1.5rem;
    backdrop-filter:blur(10px);transition:all 0.3s ease;
}
.glass-card:hover{
    border-color:rgba(0,212,255,0.3);
    box-shadow:0 8px 32px rgba(0,212,255,0.08);transform:translateY(-2px);
}
.kpi-tile{
    background:rgba(0,212,255,0.03);border:1px solid rgba(0,212,255,0.1);
    border-radius:14px;padding:1.2rem 1rem;text-align:center;transition:all 0.2s;
}
.kpi-tile:hover{border-color:rgba(0,212,255,0.3);box-shadow:0 4px 20px rgba(0,212,255,0.1);}
.kpi-tile-val{font-size:1.8rem;font-weight:800;color:#00D4FF!important;}
.kpi-tile-lbl{font-size:0.72rem;color:#475569!important;text-transform:uppercase;
    letter-spacing:0.08em;margin-top:4px;font-weight:600;}
.feature-card{
    background:rgba(0,212,255,0.02);border:1px solid rgba(0,212,255,0.08);
    border-radius:16px;padding:1.5rem;height:100%;transition:all 0.3s ease;
}
.feature-card:hover{
    background:rgba(0,212,255,0.05);border-color:rgba(0,212,255,0.25);
    transform:translateY(-4px);box-shadow:0 12px 40px rgba(0,212,255,0.1);
}
.feature-icon{
    width:48px;height:48px;background:rgba(0,212,255,0.1);
    border:1px solid rgba(0,212,255,0.2);border-radius:12px;
    font-size:1.4rem;margin-bottom:1rem;display:flex;align-items:center;justify-content:center;
}
.feature-title{font-size:1rem;font-weight:700;color:#F1F5F9!important;margin-bottom:0.4rem;}
.feature-desc{font-size:0.83rem;color:#64748B!important;line-height:1.6;}
.history-item{
    background:rgba(0,212,255,0.02);border:1px solid rgba(0,212,255,0.08);
    border-radius:12px;padding:1rem 1.2rem;margin-bottom:0.6rem;transition:all 0.2s;
}
.history-item:hover{border-color:rgba(0,212,255,0.25);background:rgba(0,212,255,0.04);}
.toast-success{
    background:rgba(16,185,129,0.1);border:1px solid rgba(16,185,129,0.3);
    border-radius:10px;padding:0.7rem 1rem;color:#10B981!important;
    font-size:0.85rem;font-weight:600;margin-bottom:0.8rem;
}
.toast-error{
    background:rgba(239,68,68,0.1);border:1px solid rgba(239,68,68,0.3);
    border-radius:10px;padding:0.7rem 1rem;color:#EF4444!important;
    font-size:0.85rem;font-weight:600;margin-bottom:0.8rem;
}
.section-label{
    font-size:0.68rem;font-weight:700;color:#1E3A5F!important;
    text-transform:uppercase;letter-spacing:0.1em;padding:0 1rem;margin:1rem 0 0.4rem;
}
.status-dot-green{display:inline-block;width:8px;height:8px;background:#10B981;border-radius:50%;margin-right:6px;}
.status-dot-red{display:inline-block;width:8px;height:8px;background:#EF4444;border-radius:50%;margin-right:6px;}
@keyframes float{0%,100%{transform:translateY(0px);}50%{transform:translateY(-12px);}}
@keyframes pulse-dot{0%,100%{opacity:1;}50%{opacity:0.4;}}
@keyframes glow{0%,100%{box-shadow:0 0 10px rgba(0,212,255,0.3);}50%{box-shadow:0 0 25px rgba(0,212,255,0.6);}}
hr{border-color:rgba(0,212,255,0.08)!important;}
</style>
""", unsafe_allow_html=True)'''

content = content[:start] + new_css + content[end:]

# ── Update color palette in dashboard ────────────────────────────────────────
content = content.replace(
    'C1="#FBB724"; C2="#10B981"; C3="#8B5CF6"; C4="#EF4444"; C5="#0EA5E9"',
    'C1="#00D4FF"; C2="#7C3AED"; C3="#10B981"; C4="#F97316"; C5="#EC4899"'
)
content = content.replace(
    'PAL=[C1,C2,C3,C4,C5,"#F97316","#EC4899"]',
    'PAL=[C1,C2,C3,C4,C5,"#FBB724","#EF4444"]'
)

# ── Update sidebar logo accent ────────────────────────────────────────────────
content = content.replace(
    'background:linear-gradient(135deg,#FBB724,#F59E0B);',
    'background:linear-gradient(135deg,#00D4FF,#7C3AED);'
)

# ── Update hero gradient ──────────────────────────────────────────────────────
content = content.replace(
    'background:linear-gradient(135deg,#0D0D14 0%,#1A1A2E 50%,#16213E 100%);',
    'background:linear-gradient(135deg,#060818 0%,#0B0F2A 50%,#0D1B3E 100%);'
)
content = content.replace(
    'border:1px solid rgba(255,255,255,0.06);border-radius:20px;',
    'border:1px solid rgba(0,212,255,0.15);border-radius:20px;'
)

# ── Update hero title gradient ────────────────────────────────────────────────
content = content.replace(
    'background:linear-gradient(135deg,#FFFFFF 0%,#FBB724 50%,#F59E0B 100%);',
    'background:linear-gradient(135deg,#FFFFFF 0%,#00D4FF 50%,#7C3AED 100%);'
)
content = content.replace(
    'background:linear-gradient(90deg,#FFFFFF 0%,#FBB724 100%);',
    'background:linear-gradient(90deg,#FFFFFF 0%,#00D4FF 60%,#7C3AED 100%);'
)

# ── Update robot SVG glow ─────────────────────────────────────────────────────
content = content.replace(
    'filter:drop-shadow(0 0 18px rgba(251,183,36,0.45))',
    'filter:drop-shadow(0 0 18px rgba(0,212,255,0.6))'
)
content = content.replace(
    'filter:drop-shadow(0 0 16px rgba(251,183,36,0.4))',
    'filter:drop-shadow(0 0 16px rgba(0,212,255,0.6))'
)
content = content.replace(
    'filter:drop-shadow(0 0 10px rgba(251,183,36,0.4))',
    'filter:drop-shadow(0 0 10px rgba(0,212,255,0.5))'
)

# ── Update robot card border ──────────────────────────────────────────────────
content = content.replace(
    'background:radial-gradient(ellipse at center,\n                rgba(251,183,36,0.07) 0%,rgba(139,92,246,0.04) 60%,transparent 80%);\n            border:1px solid rgba(251,183,36,0.18);',
    'background:radial-gradient(ellipse at center,\n                rgba(0,212,255,0.08) 0%,rgba(124,58,237,0.05) 60%,transparent 80%);\n            border:1px solid rgba(0,212,255,0.2);'
)
content = content.replace(
    'background:rgba(251,183,36,0.06);border:1px solid rgba(251,183,36,0.18);',
    'background:rgba(0,212,255,0.05);border:1px solid rgba(0,212,255,0.2);'
)

# ── Update badge colors ───────────────────────────────────────────────────────
content = content.replace(
    'background:rgba(251,183,36,0.1);border:1px solid rgba(251,183,36,0.25);color:#FBB724',
    'background:rgba(0,212,255,0.1);border:1px solid rgba(0,212,255,0.3);color:#00D4FF'
)
content = content.replace(
    'background:rgba(251,183,36,0.1);border:1px solid rgba(251,183,36,0.3);\n                    color:#FBB724',
    'background:rgba(0,212,255,0.1);border:1px solid rgba(0,212,255,0.3);\n                    color:#00D4FF'
)

# ── Update section labels ─────────────────────────────────────────────────────
content = content.replace(
    "border-left:3px solid #FBB724;padding-left:0.6rem;\">&#128202;",
    "border-left:3px solid #00D4FF;padding-left:0.6rem;\">&#128202;"
)
content = content.replace(
    "border-left:3px solid #FBB724;padding-left:0.6rem;\">&#128269;",
    "border-left:3px solid #00D4FF;padding-left:0.6rem;\">&#128269;"
)
content = content.replace(
    "border-left:3px solid #FBB724;padding-left:0.6rem;\">&#128203;",
    "border-left:3px solid #00D4FF;padding-left:0.6rem;\">&#128203;"
)

# ── Update insight banner ─────────────────────────────────────────────────────
content = content.replace(
    'background:linear-gradient(90deg,rgba(251,183,36,0.08),rgba(16,185,129,0.05));\n            border:1px solid rgba(251,183,36,0.2)',
    'background:linear-gradient(90deg,rgba(0,212,255,0.08),rgba(124,58,237,0.05));\n            border:1px solid rgba(0,212,255,0.2)'
)
content = content.replace(
    '<span style="color:#FBB724;font-weight:700;">&#10022; Key Insights',
    '<span style="color:#00D4FF;font-weight:700;">&#10022; Key Insights'
)

# ── Update dashboard header ───────────────────────────────────────────────────
content = content.replace(
    'border:1px solid rgba(251,183,36,0.2);border-radius:16px;\n        padding:1.5rem 2rem;margin-bottom:1.2rem',
    'border:1px solid rgba(0,212,255,0.2);border-radius:16px;\n        padding:1.5rem 2rem;margin-bottom:1.2rem'
)
content = content.replace(
    'background:radial-gradient(circle,rgba(251,183,36,0.06) 0%,transparent 70%)',
    'background:radial-gradient(circle,rgba(0,212,255,0.06) 0%,transparent 70%)'
)
content = content.replace(
    'color:#FBB724;\n                    text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.4rem;',
    'color:#00D4FF;\n                    text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.4rem;'
)

# ── Update KPI tile top borders ───────────────────────────────────────────────
content = content.replace(
    "border-top:3px solid {_clr};border-radius:12px",
    "border-top:3px solid {_clr};border-radius:12px"
)

# ── Update query input pulse dot ─────────────────────────────────────────────
content = content.replace(
    'width:8px;height:8px;background:#FBB724;border-radius:50%;box-shadow:0 0 6px #FBB724',
    'width:8px;height:8px;background:#00D4FF;border-radius:50%;box-shadow:0 0 6px #00D4FF'
)

# ── Update ONLINE status ──────────────────────────────────────────────────────
content = content.replace(
    'box-shadow:0 0 7px #10B981;animation:pulse-dot 2s ease-in-out infinite;"></div>\n                <span style="font-size:0.7rem;color:#10B981',
    'box-shadow:0 0 7px #10B981;animation:pulse-dot 2s ease-in-out infinite;"></div>\n                <span style="font-size:0.7rem;color:#10B981'
)

open("app.py", "w", encoding="utf-8").write(content)
print("✓ Theme updated to Navy + Cyan + Purple")

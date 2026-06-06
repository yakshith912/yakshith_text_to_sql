# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
from datetime import datetime
import re
import time
import io
import sqlite3
from text_to_sql import question_to_sql, query_uploaded_datasets, generate_ai_insight
from database import execute_query, test_connection, get_db_type, get_connection, get_connection_status, get_connection
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

st.set_page_config(
    page_title="AaiTech · AI SQL Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ══════════════════════════════════════════════════════════════════════════════
# GLOBAL CSS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

*,*::before,*::after{box-sizing:border-box;}

/* ── Base ── */
html,body,[data-testid="stAppViewContainer"]{
    font-family:'Inter',sans-serif!important;
    background:linear-gradient(135deg,#0A0A0A 0%,#0F1923 40%,#071A12 100%)!important;
    color:#E2E8F0!important;
}
[data-testid="stAppViewContainer"]>.main{padding:0!important;}
.block-container{padding:0.5rem 2rem 2rem!important;max-width:100%!important;}

/* ── Hide Streamlit header ── */
[data-testid="stHeader"],header.stAppHeader,.stAppHeader{display:none!important;height:0!important;}
[data-testid="stToolbar"],.stAppToolbar,.stDeployButton,[data-testid="stMainMenu"],.stMainMenu{display:none!important;}
[data-testid="collapsedControl"]{display:flex!important;visibility:visible!important;color:#10B981!important;}

/* ── Sidebar ── */
[data-testid="stSidebar"]{
    background:linear-gradient(180deg,#0A0A0A 0%,#0F1923 100%)!important;
    border-right:1px solid rgba(16,185,129,0.15)!important;
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
    background:rgba(16,185,129,0.1)!important;color:#10B981!important;transform:none!important;
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
    background:rgba(16,185,129,0.04)!important;
    border:1.5px solid rgba(16,185,129,0.15)!important;
    border-radius:12px!important;color:#F1F5F9!important;
    font-size:1rem!important;padding:0.75rem 1rem!important;
}
.stTextInput>div>div>input:focus,.stTextArea>div>div>textarea:focus{
    border-color:#10B981!important;box-shadow:0 0 0 3px rgba(16,185,129,0.12)!important;
}
.stTextInput>div>div>input::placeholder,.stTextArea>div>div>textarea::placeholder{color:#334155!important;}

/* ── Buttons ── */
.stButton>button{
    background:linear-gradient(135deg,#10B981,#059669)!important;
    color:#FFFFFF!important;border:none!important;border-radius:10px!important;
    font-weight:700!important;font-size:0.9rem!important;padding:0.6rem 1.4rem!important;
    transition:all 0.2s ease!important;box-shadow:0 4px 15px rgba(16,185,129,0.25)!important;
}
.stButton>button:hover{
    transform:translateY(-2px)!important;box-shadow:0 8px 25px rgba(16,185,129,0.4)!important;
}

/* ── Selectbox ── */
.stSelectbox>div>div{
    background:rgba(16,185,129,0.04)!important;
    border:1.5px solid rgba(16,185,129,0.15)!important;
    border-radius:10px!important;color:#F1F5F9!important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"]{
    background:rgba(16,185,129,0.04)!important;border-radius:12px!important;
    padding:4px!important;gap:4px!important;border:1px solid rgba(16,185,129,0.1)!important;
}
.stTabs [data-baseweb="tab"]{border-radius:8px!important;color:#64748B!important;font-weight:600!important;}
.stTabs [aria-selected="true"]{background:rgba(16,185,129,0.15)!important;color:#10B981!important;}

/* ── Dataframe ── */
[data-testid="stDataFrame"]{border-radius:12px!important;overflow:hidden!important;
    border:1px solid rgba(16,185,129,0.1)!important;}

/* ── Scrollbar ── */
::-webkit-scrollbar{width:6px;height:6px;}
::-webkit-scrollbar-track{background:#060818;}
::-webkit-scrollbar-thumb{background:#134E3A;border-radius:3px;}
::-webkit-scrollbar-thumb:hover{background:#10B981;}

/* ── Cards ── */
.glass-card{
    background:rgba(16,185,129,0.03);
    border:1px solid rgba(16,185,129,0.1);
    border-radius:16px;padding:1.5rem;
    backdrop-filter:blur(10px);transition:all 0.3s ease;
}
.glass-card:hover{
    border-color:rgba(16,185,129,0.3);
    box-shadow:0 8px 32px rgba(16,185,129,0.08);transform:translateY(-2px);
}
.kpi-tile{
    background:rgba(16,185,129,0.03);border:1px solid rgba(16,185,129,0.1);
    border-radius:14px;padding:1.2rem 1rem;text-align:center;transition:all 0.2s;
}
.kpi-tile:hover{border-color:rgba(16,185,129,0.3);box-shadow:0 4px 20px rgba(16,185,129,0.1);}
.kpi-tile-val{font-size:1.8rem;font-weight:800;color:#10B981!important;}
.kpi-tile-lbl{font-size:0.72rem;color:#475569!important;text-transform:uppercase;
    letter-spacing:0.08em;margin-top:4px;font-weight:600;}
.feature-card{
    background:rgba(16,185,129,0.02);border:1px solid rgba(16,185,129,0.08);
    border-radius:16px;padding:1.5rem;height:100%;transition:all 0.3s ease;
}
.feature-card:hover{
    background:rgba(16,185,129,0.05);border-color:rgba(16,185,129,0.25);
    transform:translateY(-4px);box-shadow:0 12px 40px rgba(16,185,129,0.1);
}
.feature-icon{
    width:48px;height:48px;background:rgba(16,185,129,0.1);
    border:1px solid rgba(16,185,129,0.2);border-radius:12px;
    font-size:1.4rem;margin-bottom:1rem;display:flex;align-items:center;justify-content:center;
}
.feature-title{font-size:1rem;font-weight:700;color:#F1F5F9!important;margin-bottom:0.4rem;}
.feature-desc{font-size:0.83rem;color:#64748B!important;line-height:1.6;}
.history-item{
    background:rgba(16,185,129,0.02);border:1px solid rgba(16,185,129,0.08);
    border-radius:12px;padding:1rem 1.2rem;margin-bottom:0.6rem;transition:all 0.2s;
}
.history-item:hover{border-color:rgba(16,185,129,0.25);background:rgba(16,185,129,0.04);}
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
@keyframes glow{0%,100%{box-shadow:0 0 10px rgba(16,185,129,0.3);}50%{box-shadow:0 0 25px rgba(16,185,129,0.6);}}
hr{border-color:rgba(16,185,129,0.08)!important;}

/* ── Dashboard Enhanced Styles ── */
.upload-zone{
    background:rgba(16,185,129,0.03);border:2px dashed rgba(16,185,129,0.2);
    border-radius:16px;padding:2rem;text-align:center;transition:all 0.3s;
    cursor:pointer;
}
.upload-zone:hover{border-color:rgba(16,185,129,0.5);background:rgba(16,185,129,0.06);}
.action-toolbar{
    display:flex;gap:0.4rem;flex-wrap:wrap;margin:0.5rem 0;
}
.action-btn{
    display:inline-flex;align-items:center;gap:4px;
    background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);
    border-radius:8px;padding:0.35rem 0.7rem;font-size:0.72rem;
    color:#94A3B8;font-weight:600;cursor:pointer;transition:all 0.2s;
}
.action-btn:hover{background:rgba(16,185,129,0.1);color:#10B981;border-color:rgba(16,185,129,0.3);}
.rec-badge{
    display:inline-flex;align-items:center;gap:5px;
    background:linear-gradient(135deg,rgba(139,92,246,0.1),rgba(16,185,129,0.08));
    border:1px solid rgba(139,92,246,0.25);
    border-radius:20px;padding:0.3rem 0.8rem;font-size:0.72rem;
    color:#A78BFA;font-weight:600;margin:0.2rem;transition:all 0.2s;
}
.rec-badge:hover{background:linear-gradient(135deg,rgba(139,92,246,0.2),rgba(16,185,129,0.15));transform:scale(1.02);}
.col-drill{
    background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.06);
    border-radius:10px;padding:0.8rem;margin-bottom:0.4rem;transition:all 0.2s;
}
.col-drill:hover{border-color:rgba(16,185,129,0.2);background:rgba(16,185,129,0.03);}
.sparkline-box{
    background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.05);
    border-radius:8px;padding:0.4rem;margin-top:0.3rem;
}
@keyframes shimmer{0%{background-position:-200% 0;}100%{background-position:200% 0;}}
.loading-shimmer{
    background:linear-gradient(90deg,rgba(16,185,129,0.05) 25%,rgba(16,185,129,0.12) 50%,rgba(16,185,129,0.05) 75%);
    background-size:200% 100%;animation:shimmer 1.5s ease-in-out infinite;
    border-radius:8px;height:20px;
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════════════════════════
_defaults = {
    "history":[], "submit":False, "db_status":None,
    "saved_queries":[], "active_page":"🏠 Home",
    "question_input":"", "last_sql":"", "last_df":None,
}

# Initialize database connection status
if "db_status" not in st.session_state:
    st.session_state.db_status = (False, "Not checked")
# Attempt connection and update status
try:
    conn_ok, status_msg = get_connection_status()
    st.session_state.db_status = (conn_ok, status_msg)
except Exception as e:
    st.session_state.db_status = (False, str(e))

for _k,_v in _defaults.items():
    if _k not in st.session_state:
        st.session_state[_k] = _v

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    # Logo
    st.markdown("""
    <div style="padding:1.5rem 1rem 1rem;border-bottom:1px solid rgba(255,255,255,0.06);margin-bottom:0.5rem;">
        <div style="display:flex;align-items:center;gap:10px;">
            <div style="width:38px;height:38px;
                background:linear-gradient(135deg,#10B981,#059669);
                border-radius:10px;display:flex;align-items:center;
                justify-content:center;font-size:1.2rem;flex-shrink:0;">🤖</div>
            <div>
                <div style="font-size:1rem;font-weight:800;color:#F1F5F9!important;">AaiTech</div>
                <div style="font-size:0.7rem;color:#475569!important;">AI SQL Assistant</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # DB status (auto-check)
    from database import get_connection_status
    _db_ok, _db_msg = get_connection_status()
    st.session_state.db_status = ( _db_ok, _db_msg )
    _dot = "status-dot-green" if _db_ok else "status-dot-red"
    _stxt = _db_msg if _db_ok else "Offline"
    st.markdown(f"""
    <div style="padding:0.4rem 1rem 0.6rem;">
        <span class="{_dot}"></span>
        <span style="font-size:0.76rem;color:#64748B!important;">{_stxt}</span>
    </div>""", unsafe_allow_html=True)
    if not _db_ok:
        st.markdown(f'<div style="padding:0 1rem 0.6rem;font-size:0.72rem;color:#EF4444!important;">Database is offline.</div>', unsafe_allow_html=True)

    # Navigation
    st.markdown('<div class="section-label">Navigation</div>', unsafe_allow_html=True)
    _nav = [("🏠","Home"),("💬","Query"),("📊","Dashboard"),
            ("📜","History"),("💾","Saved"),("📋","Schema"),("⚙️","Settings")]
    for _icon,_lbl in _nav:
        if st.button(f"{_icon}  {_lbl}", key=f"nav_{_lbl}", use_container_width=True):
            st.session_state.active_page = f"{_icon} {_lbl}"
            st.rerun()

    # Quick Ask
    st.markdown('<div class="section-label">Quick Ask</div>', unsafe_allow_html=True)
    _quick = ["Show all customers","Revenue by category","Top 5 products",
              "Orders by country","List all suppliers","Total freight cost"]
    for _s in _quick:
        if st.button(f"↗  {_s}", key=f"qs_{_s}", use_container_width=True):
            st.session_state.pending_question = _s
            st.session_state.submit = True
            st.session_state.active_page = "💬 Query"
            st.rerun()

    st.markdown("---")
    st.markdown("""
    <div style="padding:0 1rem;font-size:0.72rem;color:#334155!important;">
        <div>📧 info@aaitech.com</div>
        <div style="margin-top:4px;">© 2025 AaiTech Industries</div>
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# HELPER
# ══════════════════════════════════════════════════════════════════════════════
def run_query(question:str):
    try:
        sql = question_to_sql(question)
        df  = execute_query(sql)
        return sql, df, None
    except Exception as e:
        return None, None, str(e)

_page = st.session_state.active_page

# ══════════════════════════════════════════════════════════════════════════════
# HOME PAGE
# ══════════════════════════════════════════════════════════════════════════════
if _page == "🏠 Home":

    # ── Hero ──────────────────────────────────────────────────────────────────
    _hl, _hr = st.columns([3, 2])
    with _hl:
        st.markdown("""
        <div style="
            background:linear-gradient(135deg,#071A12 0%,#0A1F14 50%,#0F1A0A 100%);
            border:1px solid rgba(16,185,129,0.15);border-radius:20px;
            padding:2.5rem 2rem;position:relative;overflow:hidden;min-height:320px;">
            <div style="position:absolute;top:-40px;right:-40px;width:300px;height:300px;
                background:radial-gradient(circle,rgba(251,183,36,0.07) 0%,transparent 70%);
                pointer-events:none;"></div>
            <div style="display:inline-block;background:rgba(251,183,36,0.1);
                border:1px solid rgba(251,183,36,0.25);color:#FBB724!important;
                padding:0.3rem 0.9rem;border-radius:20px;font-size:0.75rem;
                font-weight:700;letter-spacing:0.06em;text-transform:uppercase;
                margin-bottom:1.2rem;">&#10022; Powered by Azure OpenAI + RAG</div>
            <div style="font-size:2.6rem;font-weight:900;line-height:1.1;margin:0.5rem 0;
                background:linear-gradient(135deg,#FFFFFF 0%,#10B981 50%,#F59E0B 100%);
                -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                background-clip:text;">AI-Powered<br>Text-to-SQL<br>Assistant</div>
            <div style="font-size:1rem;color:#64748B!important;max-width:480px;
                line-height:1.7;margin:1rem 0 1.5rem;">
                Transform plain English into precise SQL queries instantly.
                No SQL expertise needed — just ask your business question.
            </div>
            <div style="display:flex;gap:0.7rem;flex-wrap:wrap;">
                <span style="background:rgba(251,183,36,0.1);border:1px solid rgba(251,183,36,0.3);
                    border-radius:8px;padding:0.35rem 0.8rem;font-size:0.75rem;
                    color:#FBB724!important;font-weight:600;">&#9889; GPT-4 Powered</span>
                <span style="background:rgba(16,185,129,0.1);border:1px solid rgba(16,185,129,0.3);
                    border-radius:8px;padding:0.35rem 0.8rem;font-size:0.75rem;
                    color:#10B981!important;font-weight:600;">&#128994; Live Database</span>
                <span style="background:rgba(139,92,246,0.1);border:1px solid rgba(139,92,246,0.3);
                    border-radius:8px;padding:0.35rem 0.8rem;font-size:0.75rem;
                    color:#8B5CF6!important;font-weight:600;">&#128269; Schema-Aware RAG</span>
            </div>
            <div style="display:flex;gap:2rem;margin-top:2rem;padding-top:1.5rem;
                border-top:1px solid rgba(255,255,255,0.06);">
                <div><div style="font-size:1.6rem;font-weight:800;color:#FBB724!important;">5</div>
                    <div style="font-size:0.75rem;color:#475569!important;">Tables</div></div>
                <div><div style="font-size:1.6rem;font-weight:800;color:#FBB724!important;">&#8734;</div>
                    <div style="font-size:0.75rem;color:#475569!important;">Queries</div></div>
                <div><div style="font-size:1.6rem;font-weight:800;color:#FBB724!important;">AI</div>
                    <div style="font-size:0.75rem;color:#475569!important;">GPT-4</div></div>
                <div><div style="font-size:1.6rem;font-weight:800;color:#FBB724!important;">RAG</div>
                    <div style="font-size:0.75rem;color:#475569!important;">Context</div></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with _hr:
        st.markdown("""
        <div style="
            background:radial-gradient(ellipse at center,
                rgba(16,185,129,0.08) 0%,rgba(245,158,11,0.05) 60%,transparent 80%);
            border:1px solid rgba(16,185,129,0.2);border-radius:24px;
            padding:2rem 1rem 1.5rem;text-align:center;position:relative;
            overflow:hidden;min-height:320px;display:flex;flex-direction:column;
            align-items:center;justify-content:center;">
            <div style="position:absolute;top:50%;left:50%;width:260px;height:260px;
                border-radius:50%;border:1px solid rgba(251,183,36,0.07);
                transform:translate(-50%,-50%);pointer-events:none;"></div>
            <div style="animation:float 3s ease-in-out infinite;position:relative;z-index:2;">
                <svg viewBox="0 0 120 140" xmlns="http://www.w3.org/2000/svg"
                     style="width:150px;filter:drop-shadow(0 0 18px rgba(16,185,129,0.7));">
                    <line x1="60" y1="8" x2="60" y2="22" stroke="#FBB724" stroke-width="2.5" stroke-linecap="round"/>
                    <circle cx="60" cy="6" r="4" fill="#FBB724"/>
                    <circle cx="60" cy="6" r="7" fill="none" stroke="rgba(251,183,36,0.3)" stroke-width="1.5"/>
                    <rect x="28" y="22" width="64" height="50" rx="14" fill="#1A1A2E" stroke="#FBB724" stroke-width="1.5"/>
                    <ellipse cx="45" cy="42" rx="9" ry="9" fill="rgba(251,183,36,0.15)"/>
                    <ellipse cx="75" cy="42" rx="9" ry="9" fill="rgba(251,183,36,0.15)"/>
                    <circle cx="45" cy="42" r="6" fill="#FBB724"/>
                    <circle cx="75" cy="42" r="6" fill="#FBB724"/>
                    <circle cx="47" cy="40" r="2" fill="#0A0A0F"/>
                    <circle cx="77" cy="40" r="2" fill="#0A0A0F"/>
                    <circle cx="48" cy="39" r="1" fill="white" opacity="0.8"/>
                    <circle cx="78" cy="39" r="1" fill="white" opacity="0.8"/>
                    <rect x="40" y="58" width="40" height="7" rx="3.5" fill="rgba(251,183,36,0.15)" stroke="rgba(251,183,36,0.4)" stroke-width="1"/>
                    <rect x="43" y="60" width="6" height="3" rx="1.5" fill="#FBB724"/>
                    <rect x="52" y="60" width="6" height="3" rx="1.5" fill="#FBB724"/>
                    <rect x="61" y="60" width="6" height="3" rx="1.5" fill="#FBB724"/>
                    <rect x="70" y="60" width="6" height="3" rx="1.5" fill="#FBB724"/>
                    <rect x="52" y="72" width="16" height="10" rx="4" fill="#1A1A2E" stroke="rgba(251,183,36,0.3)" stroke-width="1"/>
                    <rect x="22" y="82" width="76" height="52" rx="14" fill="#1A1A2E" stroke="#FBB724" stroke-width="1.5"/>
                    <rect x="34" y="92" width="52" height="32" rx="8" fill="rgba(251,183,36,0.06)" stroke="rgba(251,183,36,0.2)" stroke-width="1"/>
                    <circle cx="48" cy="102" r="5" fill="rgba(251,183,36,0.2)" stroke="#FBB724" stroke-width="1"/>
                    <circle cx="48" cy="102" r="3" fill="#FBB724"/>
                    <circle cx="60" cy="102" r="5" fill="rgba(16,185,129,0.2)" stroke="#10B981" stroke-width="1"/>
                    <circle cx="60" cy="102" r="3" fill="#10B981"/>
                    <circle cx="72" cy="102" r="5" fill="rgba(139,92,246,0.2)" stroke="#8B5CF6" stroke-width="1"/>
                    <circle cx="72" cy="102" r="3" fill="#8B5CF6"/>
                    <rect x="42" y="114" width="4" height="6" rx="1" fill="rgba(251,183,36,0.4)"/>
                    <rect x="49" y="111" width="4" height="9" rx="1" fill="rgba(251,183,36,0.6)"/>
                    <rect x="56" y="108" width="4" height="12" rx="1" fill="#FBB724"/>
                    <rect x="63" y="111" width="4" height="9" rx="1" fill="rgba(251,183,36,0.6)"/>
                    <rect x="70" y="114" width="4" height="6" rx="1" fill="rgba(251,183,36,0.4)"/>
                    <rect x="4" y="84" width="18" height="36" rx="9" fill="#1A1A2E" stroke="rgba(251,183,36,0.4)" stroke-width="1.5"/>
                    <rect x="98" y="84" width="18" height="36" rx="9" fill="#1A1A2E" stroke="rgba(251,183,36,0.4)" stroke-width="1.5"/>
                    <circle cx="13" cy="84" r="5" fill="#FBB724" opacity="0.6"/>
                    <circle cx="107" cy="84" r="5" fill="#FBB724" opacity="0.6"/>
                    <circle cx="15" cy="55" r="2.5" fill="#FBB724" opacity="0.5"/>
                    <circle cx="105" cy="50" r="2" fill="#10B981" opacity="0.6"/>
                    <circle cx="108" cy="65" r="1.5" fill="#8B5CF6" opacity="0.5"/>
                    <circle cx="12" cy="70" r="1.5" fill="#FBB724" opacity="0.4"/>
                </svg>
            </div>
            <div style="margin-top:0.8rem;z-index:2;position:relative;">
                <div style="font-size:0.8rem;font-weight:700;color:#FBB724!important;letter-spacing:0.06em;">AI AGENT</div>
                <div style="font-size:0.68rem;color:#475569!important;margin-top:2px;">Powered by GPT-4</div>
            </div>
            <div style="display:flex;align-items:center;justify-content:center;
                gap:6px;margin-top:0.6rem;z-index:2;position:relative;">
                <div style="width:7px;height:7px;background:#10B981;border-radius:50%;
                    box-shadow:0 0 7px #10B981;animation:pulse-dot 2s ease-in-out infinite;"></div>
                <span style="font-size:0.7rem;color:#10B981!important;font-weight:700;letter-spacing:0.06em;">ONLINE</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Live KPIs ─────────────────────────────────────────────────────────────
    try:
        _nc = execute_query("SELECT COUNT(*) as c FROM customers").iloc[0]["c"]
        _no = execute_query("SELECT COUNT(*) as c FROM orders").iloc[0]["c"]
        _np = execute_query("SELECT COUNT(*) as c FROM products").iloc[0]["c"]
        _nh = len(st.session_state.history)
        st.markdown(f"""
        <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:0.8rem;margin-bottom:1.5rem;">
            <div class="kpi-tile"><div class="kpi-tile-val">{_nc}</div><div class="kpi-tile-lbl">Customers</div></div>
            <div class="kpi-tile"><div class="kpi-tile-val">{_no}</div><div class="kpi-tile-lbl">Orders</div></div>
            <div class="kpi-tile"><div class="kpi-tile-val">{_np}</div><div class="kpi-tile-lbl">Products</div></div>
            <div class="kpi-tile"><div class="kpi-tile-val">{_nh}</div><div class="kpi-tile-lbl">Queries Run</div></div>
        </div>""", unsafe_allow_html=True)
    except Exception:
        pass

    # ── Quick Query ───────────────────────────────────────────────────────────
    st.markdown("""
    <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);
        border-radius:16px;padding:1.5rem;margin-bottom:1rem;">
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:0.8rem;">
            <div style="width:8px;height:8px;background:#FBB724;border-radius:50%;
                box-shadow:0 0 6px #FBB724;"></div>
            <span style="font-size:0.9rem;font-weight:700;color:#F1F5F9!important;">&#9889; Ask the AI</span>
            <span style="font-size:0.72rem;color:#475569!important;margin-left:4px;">Type in plain English — no SQL needed</span>
        </div>
    """, unsafe_allow_html=True)

    def _sub_home(): st.session_state.submit = True

    _pq = st.session_state.pop("pending_question","") or ""
    if _pq: st.session_state["question_input"] = _pq

    st.text_input("Ask AI", value=st.session_state.get("question_input",""),
                  key="question_input",
                  placeholder="e.g.  Show total revenue by product category...",
                  on_change=_sub_home, label_visibility="collapsed")

    # Chip buttons
    _chips = ["Show customers","Revenue by category","Top 5 products",
              "Orders by country","List suppliers","Total freight"]
    _cc = st.columns(6)
    for _col,_chip in zip(_cc,_chips):
        with _col:
            if st.button(_chip, key=f"hchip_{_chip}", use_container_width=True):
                st.session_state.pending_question = _chip
                st.session_state.submit = True
                st.rerun()

    _b1,_b2,_b3,_ = st.columns([1.2,1.2,1,4])
    with _b1:
        if st.button("&#9654; Run Query", use_container_width=True, key="h_run"):
            st.session_state.submit = True
    with _b2:
        if st.button("&#128190; Save Query", use_container_width=True, key="h_save"):
            _q = st.session_state.get("question_input","").strip()
            if _q and _q not in st.session_state.saved_queries:
                st.session_state.saved_queries.append(_q)
                st.toast("Query saved!", icon="💾")
    with _b3:
        if st.button("&#10005; Clear", use_container_width=True, key="h_clear"):
            st.session_state.pending_question = ""
            st.session_state["question_input"] = ""
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Process ───────────────────────────────────────────────────────────────
    if st.session_state.submit and st.session_state.get("question_input","").strip():
        _uq = st.session_state["question_input"].strip()
        if _uq.lower() in {"hi","hello","hey"}:
            st.markdown('<div class="toast-success">&#128075; Hello! Ask me any business question about your data.</div>', unsafe_allow_html=True)
        else:
            with st.spinner("&#129504; AI is generating SQL..."):
                _sql,_df,_err = run_query(_uq)
            if _err:
                st.markdown(f'<div class="toast-error">&#10060; {_err}</div>', unsafe_allow_html=True)
            else:
                st.session_state.last_sql = _sql
                st.session_state.last_df  = _df
                st.session_state.history.append({
                    "question":_uq,"sql":_sql,
                    "rows":len(_df) if _df is not None else 0,
                    "time":datetime.now().strftime("%H:%M:%S"),
                    "date":datetime.now().strftime("%b %d")
                })
                st.markdown('<div class="toast-success">&#10003; Query executed successfully</div>', unsafe_allow_html=True)
                _rc,_sc = st.columns([3,2])
                with _rc:
                    st.markdown('<div style="font-size:0.78rem;font-weight:700;color:#FBB724;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:0.4rem;">&#128202; Results</div>', unsafe_allow_html=True)
                    if _df is not None and not _df.empty:
                        st.markdown(f"<span style='color:#10B981;font-size:0.8rem;font-weight:600;'>&#10003; {len(_df)} row(s) &middot; {len(_df.columns)} col(s)</span>", unsafe_allow_html=True)
                        st.dataframe(_df, use_container_width=True, hide_index=True)
                        _d1,_d2 = st.columns(2)
                        with _d1:
                            st.download_button("&#11015; CSV", data=_df.to_csv(index=False), file_name="results.csv", mime="text/csv", use_container_width=True)
                        with _d2:
                            st.download_button("&#11015; Excel", data=_df.to_csv(index=False).encode(), file_name="results.xlsx", mime="application/vnd.ms-excel", use_container_width=True)
                    else:
                        st.info("No results found.")
                with _sc:
                    st.markdown('<div style="font-size:0.78rem;font-weight:700;color:#FBB724;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:0.4rem;">&#128295; Generated SQL</div>', unsafe_allow_html=True)
                    st.code(_sql, language="sql")
                    if _df is not None and not _df.empty:
                        _num = _df.select_dtypes(include='number').columns.tolist()
                        _cat = _df.select_dtypes(exclude='number').columns.tolist()
                        if _num and _cat:
                            import plotly.express as px
                            st.markdown('<div style="font-size:0.78rem;font-weight:700;color:#FBB724;text-transform:uppercase;letter-spacing:0.08em;margin:0.6rem 0 0.3rem;">&#128200; Auto Chart</div>', unsafe_allow_html=True)
                            _fig = px.bar(_df.head(10), x=_cat[0], y=_num[0], color_discrete_sequence=["#FBB724"])
                            _fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
                                font=dict(color="#94A3B8",size=10),height=220,margin=dict(t=5,b=5,l=5,r=5),
                                xaxis=dict(showgrid=False,color="#475569"),
                                yaxis=dict(showgrid=True,gridcolor="rgba(255,255,255,0.05)",color="#475569"))
                            st.plotly_chart(_fig, use_container_width=True)
        st.session_state.submit = False

    # ── Feature Cards ─────────────────────────────────────────────────────────
    st.markdown("""
    <div style="display:flex;align-items:center;gap:10px;margin:2rem 0 1rem;">
        <span style="font-size:1.1rem;font-weight:700;color:#F1F5F9!important;">Everything you need</span>
        <span style="background:rgba(251,183,36,0.1);color:#FBB724!important;font-size:0.7rem;
            font-weight:700;padding:0.15rem 0.6rem;border-radius:20px;text-transform:uppercase;">Features</span>
    </div>""", unsafe_allow_html=True)
    _feats = [
        ("&#128172;","Natural Language","Ask in plain English — no SQL knowledge required."),
        ("&#9889;","Instant Results","GPT-4 powered SQL generation in seconds."),
        ("&#128269;","Schema-Aware","RAG-based context for accurate queries."),
        ("&#128220;","Query History","Every query saved with timestamps."),
        ("&#11015;","Export Results","Download CSV or Excel with one click."),
        ("&#128202;","Visualizations","Auto-charts generated from your results."),
        ("&#128190;","Saved Queries","Bookmark queries for instant reuse."),
        ("&#129504;","AI Suggestions","Smart recommendations from your schema."),
    ]
    for _row in [_feats[:4],_feats[4:]]:
        _cols = st.columns(4)
        for _col,(_icon,_title,_desc) in zip(_cols,_row):
            with _col:
                st.markdown(f"""<div class="feature-card">
                    <div class="feature-icon">{_icon}</div>
                    <div class="feature-title">{_title}</div>
                    <div class="feature-desc">{_desc}</div>
                </div>""", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# QUERY PAGE
# ══════════════════════════════════════════════════════════════════════════════
elif _page == "💬 Query":
    st.markdown("""
    <div style="margin-bottom:1.5rem;">
        <div style="font-size:1.8rem;font-weight:800;color:#FFFFFF!important;-webkit-text-fill-color:#FFFFFF!important;">&#128172; Query Assistant</div>
        <div style="font-size:0.9rem;color:#94A3B8!important;-webkit-text-fill-color:#94A3B8!important;margin-top:4px;">Ask any business question — get SQL + results instantly</div>
    </div>""", unsafe_allow_html=True)

    # AI Suggestions
    st.markdown("""
    <div class="glass-card" style="margin-bottom:1rem;">
        <div style="font-size:0.78rem;font-weight:700;color:#FBB724!important;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:0.6rem;">&#129504; AI Suggestions</div>
        <div style="font-size:0.82rem;color:#64748B!important;margin-bottom:0.5rem;">Based on your schema, try these:</div>
        <span style="display:inline-block;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);color:#94A3B8!important;font-size:0.78rem;padding:0.3rem 0.8rem;border-radius:20px;margin:0.2rem;">Show all customers</span>
        <span style="display:inline-block;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);color:#94A3B8!important;font-size:0.78rem;padding:0.3rem 0.8rem;border-radius:20px;margin:0.2rem;">Revenue by category</span>
        <span style="display:inline-block;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);color:#94A3B8!important;font-size:0.78rem;padding:0.3rem 0.8rem;border-radius:20px;margin:0.2rem;">Top 5 expensive products</span>
        <span style="display:inline-block;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);color:#94A3B8!important;font-size:0.78rem;padding:0.3rem 0.8rem;border-radius:20px;margin:0.2rem;">Orders by country</span>
        <span style="display:inline-block;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);color:#94A3B8!important;font-size:0.78rem;padding:0.3rem 0.8rem;border-radius:20px;margin:0.2rem;">Total freight per country</span>
        <span style="display:inline-block;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);color:#94A3B8!important;font-size:0.78rem;padding:0.3rem 0.8rem;border-radius:20px;margin:0.2rem;">Supplier with most products</span>
    </div>""", unsafe_allow_html=True)

    # Pre-fill from pending
    _pq2 = st.session_state.pop("pending_question","") or ""
    if _pq2: st.session_state["form_q"] = _pq2

    with st.form("qform", clear_on_submit=False):
        _question = st.text_area("Your question", height=120,
            placeholder="e.g.  What is the total revenue per product category?\ne.g.  Show me all customers from Germany",
            key="form_q", label_visibility="collapsed")
        _qc1,_qc2,_qc3 = st.columns([2,1,3])
        with _qc1:
            _qsub = st.form_submit_button("&#9654; Generate & Run SQL", use_container_width=True)
        with _qc2:
            _maxr = st.selectbox("Rows", [25,50,100,500], index=1, label_visibility="collapsed")

    if _qsub and _question.strip():
        with st.spinner("&#129504; Processing..."):
            _sql,_df,_err = run_query(_question.strip())
        if _err:
            st.markdown(f'<div class="toast-error">&#10060; {_err}</div>', unsafe_allow_html=True)
        else:
            st.session_state.history.append({
                "question":_question.strip(),"sql":_sql,
                "rows":len(_df) if _df is not None else 0,
                "time":datetime.now().strftime("%H:%M:%S"),
                "date":datetime.now().strftime("%b %d")
            })
            st.markdown('<div class="toast-success">&#10003; Query executed successfully</div>', unsafe_allow_html=True)
            st.markdown('<div style="font-size:0.78rem;font-weight:700;color:#FBB724;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:0.4rem;">&#128295; Generated SQL</div>', unsafe_allow_html=True)
            st.code(_sql, language="sql")
            if _df is not None:
                _qm1,_qm2,_qm3,_qm4 = st.columns(4)
                for _qcol,_qval,_qlbl in [(_qm1,len(_df),"Rows"),(_qm2,len(_df.columns),"Columns"),
                    (_qm3,_df.memory_usage(deep=True).sum()//1024,"Size KB"),(_qm4,len(_sql.split()),"SQL Tokens")]:
                    with _qcol:
                        st.markdown(f'<div class="kpi-tile"><div class="kpi-tile-val">{_qval}</div><div class="kpi-tile-lbl">{_qlbl}</div></div>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            if _df is not None and not _df.empty:
                st.dataframe(_df.head(_maxr), use_container_width=True, hide_index=True)
                _qd1,_qd2,_qd3 = st.columns([1,1,4])
                with _qd1:
                    st.download_button("&#11015; CSV", data=_df.to_csv(index=False), file_name="results.csv", mime="text/csv", use_container_width=True)
                with _qd2:
                    if st.button("&#128190; Save", key="q_save", use_container_width=True):
                        if _question.strip() not in st.session_state.saved_queries:
                            st.session_state.saved_queries.append(_question.strip())
                            st.toast("Saved!", icon="💾")
                # Auto chart
                _num = _df.select_dtypes(include='number').columns.tolist()
                _cat = _df.select_dtypes(exclude='number').columns.tolist()
                if _num and _cat:
                    import plotly.express as px
                    st.markdown('<div style="font-size:0.78rem;font-weight:700;color:#FBB724;text-transform:uppercase;letter-spacing:0.08em;margin:1rem 0 0.4rem;">&#128200; Auto Visualization</div>', unsafe_allow_html=True)
                    _fig = px.bar(_df.head(20), x=_cat[0], y=_num[0], color_discrete_sequence=["#FBB724"])
                    _fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
                        font=dict(color="#94A3B8",size=11),height=320,margin=dict(t=10,b=10,l=10,r=10),
                        xaxis=dict(showgrid=False,color="#475569"),
                        yaxis=dict(showgrid=True,gridcolor="rgba(255,255,255,0.05)",color="#475569"))
                    st.plotly_chart(_fig, use_container_width=True)
            else:
                st.info("No results found.")


# ══════════════════════════════════════════════════════════════════════════════
# DASHBOARD PAGE  — Strategic Business Performance Dashboard
# ══════════════════════════════════════════════════════════════════════════════
elif _page == "📊 Dashboard":
    import plotly.express as px
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    # ── Color palette ─────────────────────────────────────────────────────────
    C1="#10B981"; C2="#F59E0B"; C3="#8B5CF6"; C4="#EF4444"; C5="#0EA5E9"
    PAL=[C1,C2,C3,C4,C5,"#06B6D4","#EC4899"]
    BG="rgba(0,0,0,0)"; GRID="rgba(255,255,255,0.05)"
    FONT=dict(family="Inter,sans-serif",size=11,color="#94A3B8")
    LO=dict(paper_bgcolor=BG,plot_bgcolor=BG,font=FONT,
            margin=dict(t=20,b=20,l=10,r=10))

    # Initialize session states for uploaded datasets
    if "uploaded_datasets" not in st.session_state:
        st.session_state.uploaded_datasets = {}
    if "dataset_sqlite_conn" not in st.session_state:
        st.session_state.dataset_sqlite_conn = sqlite3.connect(":memory:", check_same_thread=False)
        st.session_state.dataset_sqlite_conn.row_factory = sqlite3.Row

    # ── Dataset Upload Section ────────────────────────────────────────────────
    st.markdown("""<div class='section-label'>Upload Datasets</div>""", unsafe_allow_html=True)
    uploaded_files = st.file_uploader(
        "Select CSV or Excel files",
        type=["csv", "xlsx"],
        accept_multiple_files=True,
        key="dashboard_uploads",
    )
    if uploaded_files:
        for f in uploaded_files:
            try:
                if f.name.lower().endswith('.csv'):
                    df = pd.read_csv(f)
                else:
                    df = pd.read_excel(f)
                table_name = re.sub(r'[^a-zA-Z0-9_]', '_', f.name.split('.')[0]).lower()
                st.session_state.uploaded_datasets[table_name] = df
                # Load into in‑memory SQLite for SQL queries
                df.to_sql(table_name, st.session_state.dataset_sqlite_conn, if_exists='replace', index=False)
                st.toast(f"✅ Uploaded & indexed `{table_name}` ({len(df)} rows)", icon="✅")
            except Exception as e:
                st.toast(f"❌ Failed to load `{f.name}`: {e}", icon="❌")
    # Show list of uploaded datasets
    if st.session_state.uploaded_datasets:
        st.markdown("""<div class='section-label'>Available Datasets</div>""", unsafe_allow_html=True)
        for name, df in st.session_state.uploaded_datasets.items():
            with st.expander(name, expanded=False):
                st.dataframe(df.head(10), hide_index=True, use_container_width=True)
                st.download_button(
                    label="Download CSV",
                    data=df.to_csv(index=False).encode(),
                    file_name=f"{name}.csv",
                    mime="text/csv",
                )
        # ── AI Query on Uploaded Datasets ────────────────────────────────────────
        st.markdown("""\n<div class='section-label'>AI Query on Uploaded Data</div>\n""", unsafe_allow_html=True)
        uploaded_question = st.text_input("Ask AI about your uploaded datasets", key="uploaded_ai_question")
        if st.button("Run AI Query", key="run_uploaded_ai"):
            if uploaded_question:
                try:
                    # Build schema context from uploaded tables
                    def get_uploaded_schema():
                        conn = st.session_state.dataset_sqlite_conn
                        schema_parts = []
                        for tbl in st.session_state.uploaded_datasets.keys():
                            cols = [row[1] for row in conn.execute(f'PRAGMA table_info("{tbl}")').fetchall()]
                            schema_parts.append(f"Table {tbl}: columns ({', '.join(cols)})")
                        return "\n".join(schema_parts)
                    schema_ctx = get_uploaded_schema()
                    sql = query_uploaded_datasets(uploaded_question, schema_ctx)
                    df = pd.read_sql_query(sql, st.session_state.dataset_sqlite_conn)
                    st.subheader("AI Generated SQL")
                    st.code(sql, language="sql")
                    st.subheader("Results")
                    st.dataframe(df)
                except Exception as e:
                    st.error(f"AI query failed: {e}")



    # ── Overhauled Dashboard Page Header ──────────────────────────────────────
    st.markdown("""
    <div style="background:linear-gradient(135deg,#0D0D14 0%,#1A1A2E 60%,#16213E 100%);
        border:1px solid rgba(16,185,129,0.2);border-radius:16px;
        padding:1.5rem 2rem;margin-bottom:1.2rem;position:relative;overflow:hidden;">
        <div style="position:absolute;top:-60px;right:-60px;width:300px;height:300px;
            background:radial-gradient(circle,rgba(16,185,129,0.06) 0%,transparent 70%);
            pointer-events:none;"></div>
        <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:1rem;">
            <div>
                <div style="font-size:0.72rem;font-weight:700;color:#10B981;
                    text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.4rem;">
                    &#10022; AaiTech Industries &nbsp;&middot;&nbsp; Advanced Analytics
                </div>
                <span style="font-size:1.7rem;font-weight:900;
                    background:linear-gradient(90deg,#FFFFFF 0%,#10B981 60%,#F59E0B 100%);
                    -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                    background-clip:text;display:block;line-height:1.2;">
                    Strategic Business Dashboard &amp; Analytics Hub
                </span>
                <span style="font-size:0.85rem;color:#64748B;display:block;margin-top:0.3rem;">
                    Analyze live database records or upload and merge your custom CSV/Excel datasets.
                </span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    _sub_tabs = st.tabs(["🏛️ Live Database Insights", "📁 Multi-Dataset File Analyzer"])

    # ══════════════════════════════════════════════════════════════════════════
    # SUB-TAB 1: Live Database Insights (Original pre-built dashboard)
    # ══════════════════════════════════════════════════════════════════════════
    with _sub_tabs[0]:
        try:
            # ── Load data ─────────────────────────────────────────────────────────
            _dc  = execute_query("SELECT * FROM customers")
            _do  = execute_query("SELECT * FROM orders")
            _dp  = execute_query("SELECT * FROM products")
            _ds  = execute_query("SELECT * FROM suppliers")
            _dod = execute_query("SELECT * FROM order_details")
            _dof = _do.merge(_dc, on="customer_id", how="left")
            _dr  = _dod.merge(_dp, on="product_id", how="left")
            _dr["line_total"] = _dr["quantity"] * _dr["unit_price_x"]

            # ── Filters ───────────────────────────────────────────────────────────
            st.markdown('<div class="glass-card" style="padding:0.8rem 1.2rem;margin-bottom:1rem;">', unsafe_allow_html=True)
            _fc1,_fc2,_fc3,_fc4,_fc5 = st.columns([2,2,2,1,1])
            with _fc1:
                _ctries=["All Countries"]+sorted(_dc["country"].dropna().unique().tolist())
                _sc=st.selectbox("&#127757; Country",_ctries,key="db_c")
            with _fc2:
                _cats=["All Categories"]+sorted(_dp["category"].dropna().unique().tolist())
                _sk=st.selectbox("&#127991; Category",_cats,key="db_k")
            with _fc3:
                _tn=st.select_slider("&#128202; Top N",[3,5,7,10],value=5,key="db_n")
            with _fc4:
                st.markdown("<br>",unsafe_allow_html=True)
                st.button("&#8635; Reset",use_container_width=True,key="db_rst")
            with _fc5:
                st.markdown("<br>",unsafe_allow_html=True)
                _export_all = st.button("&#11015; Export",use_container_width=True,key="db_exp")
            st.markdown('</div>', unsafe_allow_html=True)

            # Apply filters
            _fo=_dof.copy(); _fr=_dr.copy()
            if _sc!="All Countries":
                _fo=_fo[_fo["country"]==_sc]
                _fr=_fr[_fr["order_id"].isin(_fo["order_id"])]
            if _sk!="All Categories":
                _fr=_fr[_fr["category"]==_sk]

            # ── KPI Calculations ──────────────────────────────────────────────────
            _nc  = len(_dc) if _sc=="All Countries" else len(_dc[_dc["country"]==_sc])
            _no  = len(_fo)
            _rev = round(_fr["line_total"].sum(), 2)
            _ao  = round(_fr.groupby("order_id")["line_total"].sum().mean(), 2) if not _fr.empty else 0
            _np2 = len(_dp) if _sk=="All Categories" else len(_dp[_dp["category"]==_sk])
            _af  = round(_fo["freight"].mean(), 2) if not _fo.empty else 0
            _tfreight = round(_fo["freight"].sum(), 2) if not _fo.empty else 0
            _top_country = _fo.groupby("country").size().idxmax() if not _fo.empty else "N/A"
            _cat_rev = _fr.groupby("category")["line_total"].sum()
            _top_cat = _cat_rev.idxmax() if not _cat_rev.empty else "N/A"
            _top_cat_v = round(float(_cat_rev.max()), 2) if not _cat_rev.empty else 0
            _prod_rev = _fr.groupby("product_name")["line_total"].sum()
            _top_prod = _prod_rev.idxmax() if not _prod_rev.empty else "N/A"

            # ── Row 1: 6 KPI Tiles ────────────────────────────────────────────────
            _k = st.columns(6)
            _kpis = [
                (_k[0], C1, "&#128101;", "Customers",    f"{_nc}",           "Active accounts"),
                (_k[1], C2, "&#128230;", "Total Orders",  f"{_no}",           "Processed"),
                (_k[2], C3, "&#128176;", "Total Revenue", f"${_rev:,.0f}",    "Gross sales"),
                (_k[3], C4, "&#128200;", "Avg Order",     f"${_ao:,.0f}",     "Per order"),
                (_k[4], C5, "&#128717;", "Products",      f"{_np2}",          "In catalog"),
                (_k[5], C1, "&#128666;", "Total Freight", f"${_tfreight:,.0f}","Shipping cost"),
            ]
            for _col,_clr,_ico,_lbl,_val,_sub in _kpis:
                with _col:
                    st.markdown(f"""
                    <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);
                        border-top:3px solid {_clr};border-radius:12px;padding:1rem 0.8rem;
                        transition:all 0.2s;">
                        <div style="font-size:1.3rem;margin-bottom:0.3rem;">{_ico}</div>
                        <div style="font-size:0.68rem;font-weight:700;color:#64748B;
                            text-transform:uppercase;letter-spacing:0.08em;">{_lbl}</div>
                        <div style="font-size:1.6rem;font-weight:800;color:{_clr};
                            line-height:1.1;margin:0.2rem 0;">{_val}</div>
                        <div style="font-size:0.68rem;color:#475569;">{_sub}</div>
                    </div>""", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # ── Insight Banner ────────────────────────────────────────────────────
            st.markdown(f"""
            <div style="background:linear-gradient(90deg,rgba(16,185,129,0.08),rgba(245,158,11,0.05));
                border:1px solid rgba(16,185,129,0.2);border-radius:10px;
                padding:0.7rem 1.2rem;margin-bottom:1rem;font-size:0.82rem;">
                <span style="color:#10B981;font-weight:700;">&#10022; Key Insights &nbsp;</span>
                <span style="color:#94A3B8;">
                    Top market: <b style="color:#FFFFFF;">{_top_country}</b> &nbsp;&middot;&nbsp;
                    Best category: <b style="color:#FFFFFF;">{_top_cat}</b>
                    <span style="color:#10B981;">(${_top_cat_v:,.0f})</span> &nbsp;&middot;&nbsp;
                    Top product: <b style="color:#FFFFFF;">{_top_prod}</b>
                </span>
            </div>""", unsafe_allow_html=True)

            # ── Row 2: Revenue Donut + Orders Bar ─────────────────────────────────
            st.markdown('<p style="font-size:0.72rem;font-weight:700;color:#FBB724;text-transform:uppercase;letter-spacing:0.1em;margin:0 0 0.6rem;border-left:3px solid #10B981;padding-left:0.6rem;">&#128202; Sales Performance</p>', unsafe_allow_html=True)
            _r1,_r2 = st.columns(2)

            with _r1:
                st.markdown('<div class="glass-card" style="padding:1rem;">', unsafe_allow_html=True)
                st.markdown('<span style="font-size:0.82rem;font-weight:700;color:#F1F5F9;">Revenue by Category</span>', unsafe_allow_html=True)
                st.markdown('<span style="font-size:0.72rem;color:#475569;display:block;margin-bottom:0.4rem;">Proportional revenue contribution</span>', unsafe_allow_html=True)
                _cr=_fr.groupby("category")["line_total"].sum().reset_index()
                _cr.columns=["Category","Revenue"]
                if not _cr.empty:
                    _f1=go.Figure(go.Pie(
                        labels=_cr["Category"],values=_cr["Revenue"],hole=0.58,
                        marker_colors=PAL,textinfo="label+percent",
                        hovertemplate="<b>%{label}</b><br>$%{value:,.2f}<extra></extra>"))
                    _f1.update_layout(**LO,height=280,showlegend=False)
                    _f1.add_annotation(text=f"<b>${_rev:,.0f}</b><br><span style='font-size:9px'>Total</span>",
                        x=0.5,y=0.5,showarrow=False,font_size=13,font_color=C1)
                    st.plotly_chart(_f1,use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

            with _r2:
                st.markdown('<div class="glass-card" style="padding:1rem;">', unsafe_allow_html=True)
                st.markdown('<span style="font-size:0.82rem;font-weight:700;color:#F1F5F9;">Orders by Country</span>', unsafe_allow_html=True)
                st.markdown('<span style="font-size:0.72rem;color:#475569;display:block;margin-bottom:0.4rem;">Order volume per destination market</span>', unsafe_allow_html=True)
                _co=_fo.groupby("country").size().reset_index(name="Orders")
                _co=_co.sort_values("Orders",ascending=False).head(_tn)
                if not _co.empty:
                    _f2=go.Figure(go.Bar(
                        x=_co["country"],y=_co["Orders"],
                        marker=dict(color=_co["Orders"],
                            colorscale=[[0,"rgba(251,183,36,0.2)"],[1,C1]],showscale=False),
                        text=_co["Orders"],textposition="outside",
                        hovertemplate="<b>%{x}</b><br>%{y} orders<extra></extra>"))
                    _f2.update_layout(**LO,height=280,
                        xaxis=dict(showgrid=False,color="#475569"),
                        yaxis=dict(showgrid=True,gridcolor=GRID,color="#475569"))
                    st.plotly_chart(_f2,use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

            # ── Row 3: Top Products + Freight ─────────────────────────────────────
            _r3,_r4 = st.columns(2)

            with _r3:
                st.markdown('<div class="glass-card" style="padding:1rem;">', unsafe_allow_html=True)
                st.markdown(f'<span style="font-size:0.82rem;font-weight:700;color:#F1F5F9;">Top {_tn} Products by Revenue</span>', unsafe_allow_html=True)
                st.markdown('<span style="font-size:0.72rem;color:#475569;display:block;margin-bottom:0.4rem;">Best performing products ranked by sales</span>', unsafe_allow_html=True)
                _pr=_fr.groupby("product_name")["line_total"].sum().reset_index()
                _pr.columns=["Product","Revenue"]
                _pr=_pr.sort_values("Revenue",ascending=True).tail(_tn)
                if not _pr.empty:
                    _f3=go.Figure(go.Bar(
                        y=_pr["Product"],x=_pr["Revenue"],orientation="h",
                        marker=dict(color=_pr["Revenue"],
                            colorscale=[[0,"rgba(16,185,129,0.2)"],[1,C2]],showscale=False),
                        text=_pr["Revenue"].apply(lambda v:f"${v:,.0f}"),textposition="outside",
                        hovertemplate="<b>%{y}</b><br>$%{x:,.2f}<extra></extra>"))
                    _f3.update_layout(**LO,height=280,
                        xaxis=dict(showgrid=True,gridcolor=GRID,color="#475569"),
                        yaxis=dict(showgrid=False,color="#475569"))
                    st.plotly_chart(_f3,use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

            with _r4:
                st.markdown('<div class="glass-card" style="padding:1rem;">', unsafe_allow_html=True)
                st.markdown('<span style="font-size:0.82rem;font-weight:700;color:#F1F5F9;">Freight Cost Analysis</span>', unsafe_allow_html=True)
                st.markdown('<span style="font-size:0.72rem;color:#475569;display:block;margin-bottom:0.4rem;">Shipping expenditure by destination country</span>', unsafe_allow_html=True)
                _fg=_fo.groupby("country")["freight"].sum().reset_index()
                _fg=_fg.sort_values("freight",ascending=False).head(_tn)
                if not _fg.empty:
                    _f4=go.Figure(go.Bar(
                        x=_fg["country"],y=_fg["freight"],
                        marker=dict(color=_fg["freight"],
                            colorscale=[[0,"rgba(139,92,246,0.2)"],[1,C3]],showscale=False),
                        text=_fg["freight"].apply(lambda v:f"${v:,.1f}"),textposition="outside",
                        hovertemplate="<b>%{x}</b><br>$%{y:,.2f}<extra></extra>"))
                    _f4.update_layout(**LO,height=280,
                        xaxis=dict(showgrid=False,color="#475569"),
                        yaxis=dict(showgrid=True,gridcolor=GRID,color="#475569"))
                    st.plotly_chart(_f4,use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

            # ── Row 4: Treemap + Supplier Performance ─────────────────────────────
            st.markdown('<p style="font-size:0.72rem;font-weight:700;color:#FBB724;text-transform:uppercase;letter-spacing:0.1em;margin:0.5rem 0 0.6rem;border-left:3px solid #10B981;padding-left:0.6rem;">&#128269; Product & Supplier Intelligence</p>', unsafe_allow_html=True)
            _r5,_r6 = st.columns([3,2])

            with _r5:
                st.markdown('<div class="glass-card" style="padding:1rem;">', unsafe_allow_html=True)
                st.markdown('<span style="font-size:0.82rem;font-weight:700;color:#F1F5F9;">Product Revenue Treemap</span>', unsafe_allow_html=True)
                st.markdown('<span style="font-size:0.72rem;color:#475569;display:block;margin-bottom:0.4rem;">Click a category to drill into products</span>', unsafe_allow_html=True)
                _tree=_fr.groupby(["category","product_name"])["line_total"].sum().reset_index()
                _tree.columns=["Category","Product","Revenue"]
                if not _tree.empty:
                    _f5=px.treemap(_tree,path=["Category","Product"],values="Revenue",
                        color="Revenue",
                        color_continuous_scale=[[0,"rgba(251,183,36,0.15)"],[0.5,C1],[1,"#78350F"]])
                    _f5.update_traces(
                        texttemplate="<b>%{label}</b><br>$%{value:,.0f}",
                        hovertemplate="<b>%{label}</b><br>$%{value:,.2f}<extra></extra>")
                    _f5.update_layout(margin=dict(t=10,b=10,l=10,r=10),height=340,
                        coloraxis_showscale=False,paper_bgcolor=BG,
                        font=dict(family="Inter,sans-serif",size=11,color="#F1F5F9"))
                    st.plotly_chart(_f5,use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

            with _r6:
                st.markdown('<div class="glass-card" style="padding:1rem;">', unsafe_allow_html=True)
                st.markdown('<span style="font-size:0.82rem;font-weight:700;color:#F1F5F9;">Supplier Performance</span>', unsafe_allow_html=True)
                st.markdown('<span style="font-size:0.72rem;color:#475569;display:block;margin-bottom:0.4rem;">Products supplied per vendor</span>', unsafe_allow_html=True)
                _sup=_ds.merge(
                    _dp.groupby("supplier_id").size().reset_index(name="Products"),
                    on="supplier_id",how="left").fillna(0)
                _sup["Products"]=_sup["Products"].astype(int)
                _sup=_sup[["company_name","country","Products"]].rename(
                    columns={"company_name":"Supplier","country":"Country"})
                _sup=_sup.sort_values("Products",ascending=False)
                _f6=go.Figure(go.Bar(
                    x=_sup["Products"],y=_sup["Supplier"],orientation="h",
                    marker_color=C2,
                    text=_sup["Products"],textposition="outside",
                    hovertemplate="<b>%{y}</b><br>Products: %{x}<extra></extra>"))
                _f6.update_layout(margin=dict(t=5,b=5,l=5,r=30),height=340,
                    paper_bgcolor=BG,plot_bgcolor=BG,font=FONT,
                    xaxis=dict(showgrid=True,gridcolor=GRID,color="#475569"),
                    yaxis=dict(showgrid=False,color="#475569",autorange="reversed"))
                st.plotly_chart(_f6,use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

            # ── Row 5: Orders Explorer ────────────────────────────────────────────
            st.markdown('<p style="font-size:0.72rem;font-weight:700;color:#FBB724;text-transform:uppercase;letter-spacing:0.1em;margin:0.5rem 0 0.6rem;border-left:3px solid #10B981;padding-left:0.6rem;">&#128203; Orders Explorer</p>', unsafe_allow_html=True)
            st.markdown('<div class="glass-card" style="padding:1rem;">', unsafe_allow_html=True)
            _srch=st.text_input("Search orders",placeholder="Search by company or country...",
                key="db_srch",label_visibility="collapsed")
            _tbl=_fo[["order_id","company_name","country","order_date","ship_city","freight"]].copy()
            _tbl.columns=["Order ID","Company","Country","Date","Ship City","Freight ($)"]
            if _srch:
                _mask=(_tbl["Company"].str.contains(_srch,case=False,na=False)|
                       _tbl["Country"].str.contains(_srch,case=False,na=False))
                _tbl=_tbl[_mask]
            st.dataframe(_tbl,use_container_width=True,hide_index=True,height=220)
            _oe1,_oe2,_ = st.columns([1,1,4])
            with _oe1:
                st.caption(f"Showing {len(_tbl)} of {len(_fo)} orders")
            with _oe2:
                if not _tbl.empty:
                    st.download_button("&#11015; Export CSV",
                        data=_tbl.to_csv(index=False),
                        file_name="orders_export.csv",mime="text/csv",
                        use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # Export all data
            if _export_all:
                _all = _fo[["order_id","company_name","country","order_date","ship_city","freight"]].copy()
                st.download_button("&#11015; Download Full Dataset",
                    data=_all.to_csv(index=False),
                    file_name="full_dashboard_export.csv",mime="text/csv")

            # ── Footer ────────────────────────────────────────────────────────────
            st.markdown("""
            <div style="text-align:center;padding:1rem 0 0.5rem;
                color:#334155;font-size:0.72rem;
                border-top:1px solid rgba(255,255,255,0.05);margin-top:1rem;">
                AaiTech Industries &nbsp;&middot;&nbsp;
                Strategic Business Performance Dashboard &nbsp;&middot;&nbsp;
                Data Analytics &amp; Business Intelligence &nbsp;&middot;&nbsp;
                &copy; 2025
            </div>""", unsafe_allow_html=True)

        except Exception as _e:
            st.markdown(f'<div class="toast-error">&#10060; Dashboard error: {_e}</div>',
                unsafe_allow_html=True)
            st.info("Make sure MySQL is running. Use the sidebar DB status indicator.")

    # ══════════════════════════════════════════════════════════════════════════
    # SUB-TAB 2: Multi-Dataset File Analyzer (Enhanced)
    # ══════════════════════════════════════════════════════════════════════════
    with _sub_tabs[1]:
        # ── Workspace Header ──
        st.markdown("""
        <div style="background:linear-gradient(135deg,rgba(16,185,129,0.06) 0%,rgba(139,92,246,0.04) 50%,rgba(245,158,11,0.03) 100%);
            border:1px solid rgba(16,185,129,0.2);border-radius:16px;
            padding:1.5rem 2rem;margin-bottom:1.5rem;position:relative;overflow:hidden;">
            <div style="position:absolute;top:-30px;right:-30px;width:200px;height:200px;
                background:radial-gradient(circle,rgba(139,92,246,0.08) 0%,transparent 70%);
                pointer-events:none;"></div>
            <div style="display:flex;align-items:center;gap:12px;margin-bottom:0.5rem;">
                <div style="width:42px;height:42px;background:linear-gradient(135deg,#10B981,#8B5CF6);
                    border-radius:12px;display:flex;align-items:center;justify-content:center;
                    font-size:1.3rem;flex-shrink:0;">📁</div>
                <div>
                    <div style="font-size:1.2rem;font-weight:800;
                        background:linear-gradient(90deg,#FFFFFF 0%,#10B981 60%,#8B5CF6 100%);
                        -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                        background-clip:text;">Multi-Dataset Analytics Workspace</div>
                    <div style="font-size:0.78rem;color:#64748B;">
                        Upload · Preview · Merge · Filter · Visualize · AI Analysis · Export
                    </div>
                </div>
            </div>
            <div style="display:flex;gap:0.5rem;flex-wrap:wrap;margin-top:0.6rem;">
                <span style="background:rgba(16,185,129,0.1);border:1px solid rgba(16,185,129,0.25);
                    border-radius:20px;padding:0.2rem 0.7rem;font-size:0.7rem;
                    color:#10B981;font-weight:600;">CSV &amp; Excel</span>
                <span style="background:rgba(139,92,246,0.1);border:1px solid rgba(139,92,246,0.25);
                    border-radius:20px;padding:0.2rem 0.7rem;font-size:0.7rem;
                    color:#8B5CF6;font-weight:600;">AI-Powered Insights</span>
                <span style="background:rgba(245,158,11,0.1);border:1px solid rgba(245,158,11,0.25);
                    border-radius:20px;padding:0.2rem 0.7rem;font-size:0.7rem;
                    color:#F59E0B;font-weight:600;">Interactive Charts</span>
                <span style="background:rgba(14,165,233,0.1);border:1px solid rgba(14,165,233,0.25);
                    border-radius:20px;padding:0.2rem 0.7rem;font-size:0.7rem;
                    color:#0EA5E9;font-weight:600;">Cross-Dataset Analysis</span>
                <span style="background:rgba(236,72,153,0.1);border:1px solid rgba(236,72,153,0.25);
                    border-radius:20px;padding:0.2rem 0.7rem;font-size:0.7rem;
                    color:#EC4899;font-weight:600;">Excel Export</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── 1. FILE UPLOAD & MANAGEMENT ──
        _up_col1, _up_col2 = st.columns([1, 1])
        with _up_col1:
            st.markdown("""
            <div class="glass-card" style="padding:1.2rem;min-height:240px;">
                <div style="display:flex;align-items:center;gap:8px;margin-bottom:0.8rem;">
                    <div style="width:32px;height:32px;background:rgba(16,185,129,0.15);
                        border:1px solid rgba(16,185,129,0.3);border-radius:8px;
                        display:flex;align-items:center;justify-content:center;font-size:1rem;">⚡</div>
                    <span style="font-size:0.9rem;font-weight:700;color:#F1F5F9;">Upload Datasets</span>
                </div>
                <div style="font-size:0.78rem;color:#64748B;margin-bottom:0.8rem;">
                    Drag and drop CSV or Excel files (max 50MB each). Each file becomes a queryable table.
                </div>
            """, unsafe_allow_html=True)
            _uploaded_files = st.file_uploader(
                "Upload CSV or Excel files",
                type=["csv", "xlsx"],
                accept_multiple_files=True,
                key="ds_uploader",
                label_visibility="collapsed"
            )

            if _uploaded_files:
                for _f in _uploaded_files:
                    _fname = _f.name
                    _tbl_name_chk = re.sub(r'[^a-zA-Z0-9_]', '_', _fname.split('.')[0]).lower()
                    if _tbl_name_chk not in st.session_state.uploaded_datasets:
                        # Validate file size (50MB limit)
                        _f.seek(0, 2)
                        _fsize = _f.tell()
                        _f.seek(0)
                        if _fsize > 50 * 1024 * 1024:
                            st.error(f"'{_fname}' exceeds 50MB limit ({round(_fsize/1024/1024,1)}MB)")
                            continue
                        try:
                            if _fname.endswith(".csv"):
                                _df_file = pd.read_csv(_f)
                            else:
                                _df_file = pd.read_excel(_f)
                            if _df_file.empty:
                                st.warning(f"'{_fname}' is empty — skipped.")
                                continue
                            # Clean column names to be SQL-safe
                            _clean_cols = {}
                            for _col in _df_file.columns:
                                _clean_name = re.sub(r'[^a-zA-Z0-9_]', '_', str(_col).strip())
                                if not _clean_name or (not _clean_name[0].isalpha() and _clean_name[0] != '_'):
                                    _clean_name = '_' + _clean_name
                                _clean_cols[_col] = _clean_name
                            _df_file = _df_file.rename(columns=_clean_cols)

                            _tbl_name = re.sub(r'[^a-zA-Z0-9_]', '_', _fname.split('.')[0]).lower()
                            st.session_state.uploaded_datasets[_tbl_name] = _df_file
                            _df_file.to_sql(_tbl_name, st.session_state.dataset_sqlite_conn, if_exists='replace', index=False)
                            _fsize_str = f"{round(_fsize/1024,1)} KB" if _fsize < 1048576 else f"{round(_fsize/1048576,1)} MB"
                            st.toast(f"✅ '{_fname}' loaded → '{_tbl_name}' ({len(_df_file):,} rows · {_fsize_str})", icon="✅")
                        except Exception as _ue:
                            st.error(f"Error parsing '{_fname}': {_ue}")
            st.markdown('</div>', unsafe_allow_html=True)

        with _up_col2:
            st.markdown("""
            <div class="glass-card" style="padding:1.2rem;min-height:240px;">
                <div style="display:flex;align-items:center;gap:8px;margin-bottom:0.8rem;">
                    <div style="width:32px;height:32px;background:rgba(139,92,246,0.15);
                        border:1px solid rgba(139,92,246,0.3);border-radius:8px;
                        display:flex;align-items:center;justify-content:center;font-size:1rem;">📋</div>
                    <span style="font-size:0.9rem;font-weight:700;color:#F1F5F9;">Loaded Datasets</span>
                    <span style="background:rgba(16,185,129,0.15);color:#10B981;font-size:0.68rem;
                        font-weight:700;padding:0.15rem 0.5rem;border-radius:10px;margin-left:auto;">""" + str(len(st.session_state.uploaded_datasets)) + """ loaded</span>
                </div>
            """, unsafe_allow_html=True)

            if not st.session_state.uploaded_datasets:
                st.markdown("""
                <div style="text-align:center;padding:1.5rem 0;">
                    <div style="font-size:2.5rem;margin-bottom:0.5rem;opacity:0.4;">📂</div>
                    <div style="font-size:0.85rem;color:#475569;font-weight:600;">No datasets yet</div>
                    <div style="font-size:0.75rem;color:#334155;margin-top:0.2rem;">Upload CSV or Excel files to begin</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                _ds_list = []
                for _name, _df in st.session_state.uploaded_datasets.items():
                    _tbl_name = re.sub(r'[^a-zA-Z0-9_]', '_', _name.split('.')[0]).lower()
                    _mem = _df.memory_usage(deep=True).sum()
                    _mem_str = f"{round(_mem/1024,1)}KB" if _mem < 1048576 else f"{round(_mem/1048576,1)}MB"
                    _ds_list.append({
                        "📄 File": _name,
                        "🗃️ Table": _tbl_name,
                        "📊 Rows": f"{len(_df):,}",
                        "📐 Cols": str(len(_df.columns)),
                        "💾 Size": _mem_str
                    })
                st.dataframe(pd.DataFrame(_ds_list), use_container_width=True, hide_index=True)

                _del_c1, _del_c2 = st.columns([3, 1])
                with _del_c1:
                    _del_sel = st.selectbox("Remove:", list(st.session_state.uploaded_datasets.keys()), key="del_ds_sel", label_visibility="collapsed")
                with _del_c2:
                    if st.button("🗑️ Delete", use_container_width=True, key="del_ds_btn"):
                        if _del_sel in st.session_state.uploaded_datasets:
                            del st.session_state.uploaded_datasets[_del_sel]
                            st.toast(f"Removed '{_del_sel}'", icon="🗑️")
                            st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ══════════════════════════════════════════════════════════════════════
        # ALL SECTIONS BELOW REQUIRE AT LEAST 1 UPLOADED DATASET
        # ══════════════════════════════════════════════════════════════════════
        if st.session_state.uploaded_datasets:

            # ── 2. AUTO-GENERATED DATASET INSIGHTS (KPI SUMMARY CARDS + SPARKLINES) ──
            st.markdown('<p style="font-size:0.72rem;font-weight:700;color:#FBB724;text-transform:uppercase;letter-spacing:0.1em;margin:0 0 0.6rem;border-left:3px solid #10B981;padding-left:0.6rem;">⚡ Dataset Overview &amp; Auto-Insights</p>', unsafe_allow_html=True)

            _insight_ds = st.selectbox("Select dataset for insights:", list(st.session_state.uploaded_datasets.keys()), key="insight_ds_sel")
            _df_ins = st.session_state.uploaded_datasets[_insight_ds]
            _num_cols_ins = _df_ins.select_dtypes(include='number').columns.tolist()
            _cat_cols_ins = _df_ins.select_dtypes(exclude='number').columns.tolist()
            _total_cells = _df_ins.shape[0] * _df_ins.shape[1]
            _total_missing = int(_df_ins.isna().sum().sum())
            _completeness = round((1 - _total_missing / _total_cells) * 100, 1) if _total_cells > 0 else 0
            _mem_ins = _df_ins.memory_usage(deep=True).sum()
            _mem_ins_str = f"{round(_mem_ins/1024,1)} KB" if _mem_ins < 1048576 else f"{round(_mem_ins/1048576,2)} MB"
            _dup_rows = int(_df_ins.duplicated().sum())

            # KPI Row
            _ik = st.columns(6)
            _insight_kpis = [
                (_ik[0], C1, "&#128202;", "Total Rows",     f"{len(_df_ins):,}",           "Records in dataset"),
                (_ik[1], C2, "&#128203;", "Columns",         f"{len(_df_ins.columns)}",     f"{len(_num_cols_ins)} numeric · {len(_cat_cols_ins)} text"),
                (_ik[2], C3, "&#9989;",   "Completeness",    f"{_completeness}%",           f"{_total_missing:,} missing cells"),
                (_ik[3], C4, "&#128260;", "Duplicates",      f"{_dup_rows:,}",              "Duplicate rows found"),
                (_ik[4], C5, "&#128190;", "Memory",          _mem_ins_str,                  "In-memory size"),
                (_ik[5], C1, "&#128290;", "Unique Ratio",    f"{round(_df_ins.nunique().mean(),1)}",  "Avg unique/column"),
            ]
            for _col, _clr, _ico, _lbl, _val, _sub in _insight_kpis:
                with _col:
                    st.markdown(f"""
                    <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);
                        border-top:3px solid {_clr};border-radius:12px;padding:0.8rem 0.6rem;
                        text-align:center;transition:all 0.2s;">
                        <div style="font-size:1.1rem;margin-bottom:0.2rem;">{_ico}</div>
                        <div style="font-size:0.65rem;font-weight:700;color:#64748B;
                            text-transform:uppercase;letter-spacing:0.08em;">{_lbl}</div>
                        <div style="font-size:1.3rem;font-weight:800;color:{_clr};
                            line-height:1.1;margin:0.15rem 0;">{_val}</div>
                        <div style="font-size:0.62rem;color:#475569;">{_sub}</div>
                    </div>""", unsafe_allow_html=True)

            # ── Auto-Summary Text ──
            _auto_summary_parts = []
            _auto_summary_parts.append(f"This dataset contains **{len(_df_ins):,} rows** and **{len(_df_ins.columns)} columns** ({len(_num_cols_ins)} numeric, {len(_cat_cols_ins)} categorical).")
            if _completeness == 100:
                _auto_summary_parts.append("Data quality is **excellent** — no missing values detected.")
            elif _completeness >= 90:
                _auto_summary_parts.append(f"Data quality is **good** — {_completeness}% complete with {_total_missing:,} missing cells.")
            else:
                _auto_summary_parts.append(f"⚠️ Data quality **needs attention** — only {_completeness}% complete ({_total_missing:,} missing cells).")
            if _dup_rows > 0:
                _auto_summary_parts.append(f"Found **{_dup_rows:,} duplicate rows** — consider deduplication.")
            if _num_cols_ins:
                _top_num = _num_cols_ins[0]
                _auto_summary_parts.append(f"Top numeric column: `{_top_num}` (mean: {_df_ins[_top_num].mean():.2f}, range: {_df_ins[_top_num].min():.2f}–{_df_ins[_top_num].max():.2f}).")

            st.markdown(f"""
            <div style="background:linear-gradient(90deg,rgba(16,185,129,0.06),rgba(139,92,246,0.04));
                border:1px solid rgba(16,185,129,0.15);border-radius:10px;
                padding:0.8rem 1.2rem;margin:0.8rem 0;font-size:0.82rem;">
                <span style="color:#10B981;font-weight:700;">&#10022; Auto-Summary</span>
                <span style="color:#94A3B8;display:block;margin-top:0.3rem;line-height:1.7;">
                    {" ".join(_auto_summary_parts)}
                </span>
            </div>""", unsafe_allow_html=True)

            # ── Sparkline Mini-Charts for Numeric Columns ──
            if _num_cols_ins:
                _spark_cols = st.columns(min(len(_num_cols_ins), 4))
                for _si, _scol_name in enumerate(_num_cols_ins[:4]):
                    with _spark_cols[_si]:
                        _spark_data = _df_ins[_scol_name].dropna().head(50)
                        if len(_spark_data) > 1:
                            _spark_fig = go.Figure(go.Scatter(
                                y=_spark_data.values, mode='lines',
                                line=dict(color=PAL[_si % len(PAL)], width=2),
                                fill='tozeroy',
                                fillcolor=f"rgba({int(PAL[_si % len(PAL)][1:3],16)},{int(PAL[_si % len(PAL)][3:5],16)},{int(PAL[_si % len(PAL)][5:7],16)},0.1)"
                            ))
                            _spark_fig.update_layout(
                                margin=dict(t=5, b=5, l=5, r=5), height=60,
                                paper_bgcolor=BG, plot_bgcolor=BG,
                                xaxis=dict(visible=False), yaxis=dict(visible=False),
                                showlegend=False
                            )
                            st.markdown(f'<div style="font-size:0.68rem;font-weight:600;color:#64748B;text-align:center;margin-bottom:2px;">{_scol_name}</div>', unsafe_allow_html=True)
                            st.plotly_chart(_spark_fig, use_container_width=True, key=f"spark_{_insight_ds}_{_scol_name}")

            st.markdown("<br>", unsafe_allow_html=True)

            # ── 3. QUICK ACTION TOOLBAR ──
            st.markdown('<p style="font-size:0.72rem;font-weight:700;color:#FBB724;text-transform:uppercase;letter-spacing:0.1em;margin:0 0 0.6rem;border-left:3px solid #10B981;padding-left:0.6rem;">⚡ Quick Actions</p>', unsafe_allow_html=True)
            _qa1, _qa2, _qa3, _qa4, _qa5 = st.columns(5)
            with _qa1:
                _show_head = st.button("📄 Head (10)", use_container_width=True, key="qa_head")
            with _qa2:
                _show_tail = st.button("📄 Tail (10)", use_container_width=True, key="qa_tail")
            with _qa3:
                _show_describe = st.button("📊 Describe", use_container_width=True, key="qa_desc")
            with _qa4:
                _show_uniques = st.button("🔢 Unique Counts", use_container_width=True, key="qa_uniq")
            with _qa5:
                _show_nulls = st.button("🩺 Null Analysis", use_container_width=True, key="qa_nulls")

            if _show_head:
                st.markdown('<div class="glass-card" style="padding:1rem;">', unsafe_allow_html=True)
                st.markdown(f'<span style="font-size:0.82rem;font-weight:700;color:#10B981;">First 10 rows of {_insight_ds}</span>', unsafe_allow_html=True)
                st.dataframe(_df_ins.head(10), use_container_width=True, hide_index=True)
                st.markdown('</div>', unsafe_allow_html=True)
            if _show_tail:
                st.markdown('<div class="glass-card" style="padding:1rem;">', unsafe_allow_html=True)
                st.markdown(f'<span style="font-size:0.82rem;font-weight:700;color:#10B981;">Last 10 rows of {_insight_ds}</span>', unsafe_allow_html=True)
                st.dataframe(_df_ins.tail(10), use_container_width=True, hide_index=True)
                st.markdown('</div>', unsafe_allow_html=True)
            if _show_describe:
                st.markdown('<div class="glass-card" style="padding:1rem;">', unsafe_allow_html=True)
                st.markdown(f'<span style="font-size:0.82rem;font-weight:700;color:#F59E0B;">Statistical Summary of {_insight_ds}</span>', unsafe_allow_html=True)
                st.dataframe(_df_ins.describe(include='all').round(2), use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            if _show_uniques:
                st.markdown('<div class="glass-card" style="padding:1rem;">', unsafe_allow_html=True)
                st.markdown(f'<span style="font-size:0.82rem;font-weight:700;color:#8B5CF6;">Unique Value Counts — {_insight_ds}</span>', unsafe_allow_html=True)
                _uniq_df = pd.DataFrame({
                    "Column": _df_ins.columns,
                    "Unique": [_df_ins[c].nunique() for c in _df_ins.columns],
                    "Total": len(_df_ins),
                    "Ratio": [f"{round(_df_ins[c].nunique()/max(len(_df_ins),1)*100,1)}%" for c in _df_ins.columns]
                })
                st.dataframe(_uniq_df, use_container_width=True, hide_index=True)
                st.markdown('</div>', unsafe_allow_html=True)
            if _show_nulls:
                st.markdown('<div class="glass-card" style="padding:1rem;">', unsafe_allow_html=True)
                st.markdown(f'<span style="font-size:0.82rem;font-weight:700;color:#EF4444;">Null Analysis — {_insight_ds}</span>', unsafe_allow_html=True)
                _null_data = []
                for _c in _df_ins.columns:
                    _n = int(_df_ins[_c].isna().sum())
                    _pct = round(_n / max(len(_df_ins), 1) * 100, 1)
                    _bar = "█" * int(_pct / 5) + "░" * (20 - int(_pct / 5))
                    _null_data.append({"Column": _c, "Missing": _n, "% Missing": f"{_pct}%", "Bar": _bar})
                st.dataframe(pd.DataFrame(_null_data), use_container_width=True, hide_index=True)
                st.markdown('</div>', unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # ── 4. DATA QUALITY PROFILING WITH DISTRIBUTION PLOTS ──
            st.markdown('<p style="font-size:0.72rem;font-weight:700;color:#FBB724;text-transform:uppercase;letter-spacing:0.1em;margin:0 0 0.6rem;border-left:3px solid #10B981;padding-left:0.6rem;">🔬 Data Quality Profile</p>', unsafe_allow_html=True)
            st.markdown('<div class="glass-card" style="padding:1.2rem;">', unsafe_allow_html=True)

            _quality_tabs = st.tabs(["📄 Data Preview", "📋 Column Profile", "📈 Statistics", "📊 Distributions", "🩺 Data Health"])

            with _quality_tabs[0]:
                _num_rows = st.slider("Rows to display:", 5, min(200, len(_df_ins)), 15, key="ds_prev_rows")
                st.dataframe(_df_ins.head(_num_rows), use_container_width=True, hide_index=True)

            with _quality_tabs[1]:
                _cols_info = []
                for _c in _df_ins.columns:
                    _dtype = str(_df_ins[_c].dtype)
                    _nulls = int(_df_ins[_c].isna().sum())
                    _uniques = int(_df_ins[_c].nunique())
                    _sample = str(_df_ins[_c].dropna().iloc[0])[:30] if not _df_ins[_c].dropna().empty else "—"
                    _cols_info.append({
                        "Column": _c,
                        "Type": _dtype,
                        "Missing": f"{_nulls:,} ({round((_nulls/len(_df_ins))*100,1)}%)" if len(_df_ins) > 0 else "0",
                        "Unique": f"{_uniques:,}",
                        "Sample": _sample
                    })
                st.dataframe(pd.DataFrame(_cols_info), use_container_width=True, hide_index=True)

            with _quality_tabs[2]:
                if not _num_cols_ins:
                    st.info("No numerical columns in this dataset.")
                else:
                    st.dataframe(_df_ins[_num_cols_ins].describe().round(2), use_container_width=True)

            with _quality_tabs[3]:
                # Distribution histograms for numeric columns
                if not _num_cols_ins:
                    st.info("No numerical columns to plot distributions.")
                else:
                    _dist_cols_to_show = _num_cols_ins[:6]  # Max 6 distributions
                    _dist_rows = [_dist_cols_to_show[i:i+3] for i in range(0, len(_dist_cols_to_show), 3)]
                    for _drow in _dist_rows:
                        _dcols = st.columns(len(_drow))
                        for _di, _dcol_name in enumerate(_drow):
                            with _dcols[_di]:
                                _dist_data = _df_ins[_dcol_name].dropna()
                                if len(_dist_data) > 0:
                                    _dfig = px.histogram(
                                        _dist_data, x=_dcol_name, nbins=25,
                                        color_discrete_sequence=[PAL[_di % len(PAL)]],
                                        opacity=0.85
                                    )
                                    _dfig.update_layout(
                                        **LO, height=200,
                                        title=dict(text=_dcol_name, font=dict(size=11, color="#94A3B8"), x=0.5),
                                        xaxis=dict(showgrid=False, color="#475569", title=""),
                                        yaxis=dict(showgrid=True, gridcolor=GRID, color="#475569", title=""),
                                        showlegend=False
                                    )
                                    st.plotly_chart(_dfig, use_container_width=True, key=f"dist_{_insight_ds}_{_dcol_name}")

            with _quality_tabs[4]:
                # Data health score
                _health_score = _completeness
                _health_color = "#10B981" if _health_score >= 90 else "#F59E0B" if _health_score >= 70 else "#EF4444"
                _health_label = "Excellent" if _health_score >= 90 else "Good" if _health_score >= 70 else "Needs Attention"

                st.markdown(f"""
                <div style="text-align:center;padding:1.5rem 0;">
                    <div style="font-size:3rem;font-weight:900;color:{_health_color};line-height:1;">{_health_score}%</div>
                    <div style="font-size:0.85rem;font-weight:700;color:{_health_color};margin-top:0.3rem;">{_health_label}</div>
                    <div style="font-size:0.72rem;color:#475569;margin-top:0.2rem;">Data Quality Score</div>
                </div>
                """, unsafe_allow_html=True)

                _health_items = []
                if _total_missing == 0:
                    _health_items.append(("✅", "No missing values", "All cells have data"))
                elif _completeness >= 95:
                    _health_items.append(("⚠️", f"{_total_missing:,} missing values", f"Data is {_completeness}% complete"))
                else:
                    _health_items.append(("❌", f"{_total_missing:,} missing values", f"Only {_completeness}% complete — consider cleaning"))
                if _dup_rows == 0:
                    _health_items.append(("✅", "No duplicate rows", "All records are unique"))
                else:
                    _health_items.append(("⚠️", f"{_dup_rows:,} duplicate rows found", "Consider deduplication"))
                _health_items.append(("ℹ️", f"{len(_num_cols_ins)} numeric, {len(_cat_cols_ins)} categorical columns", "Column type distribution"))

                for _hi_icon, _hi_title, _hi_desc in _health_items:
                    st.markdown(f"""
                    <div class="col-drill">
                        <div style="display:flex;align-items:center;gap:10px;">
                            <span style="font-size:1.1rem;">{_hi_icon}</span>
                            <div>
                                <div style="font-size:0.82rem;font-weight:600;color:#E2E8F0;">{_hi_title}</div>
                                <div style="font-size:0.72rem;color:#475569;">{_hi_desc}</div>
                            </div>
                        </div>
                    </div>""", unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

            # ── 5. CORRELATION HEATMAP ──
            if len(_num_cols_ins) >= 2:
                st.markdown('<p style="font-size:0.72rem;font-weight:700;color:#FBB724;text-transform:uppercase;letter-spacing:0.1em;margin:0 0 0.6rem;border-left:3px solid #10B981;padding-left:0.6rem;">🔥 Correlation Heatmap</p>', unsafe_allow_html=True)
                st.markdown('<div class="glass-card" style="padding:1.2rem;">', unsafe_allow_html=True)
                st.markdown('<p style="font-size:0.8rem;color:#94A3B8;margin-bottom:0.8rem;">Pearson correlation between numeric columns. Stronger correlations are highlighted.</p>', unsafe_allow_html=True)

                try:
                    _corr = _df_ins[_num_cols_ins].corr().round(2)
                    _heatmap_fig = go.Figure(data=go.Heatmap(
                        z=_corr.values,
                        x=_corr.columns.tolist(),
                        y=_corr.columns.tolist(),
                        colorscale=[[0,"#1E1B4B"],[0.25,"#312E81"],[0.5,"#0F172A"],[0.75,"#065F46"],[1,"#10B981"]],
                        text=_corr.values.round(2),
                        texttemplate="%{text}",
                        textfont=dict(size=11, color="#E2E8F0"),
                        hovertemplate="<b>%{x} vs %{y}</b><br>Correlation: %{z:.2f}<extra></extra>",
                        showscale=True,
                        colorbar=dict(tickfont=dict(color="#64748B"), title=dict(text="r", font=dict(color="#64748B")))
                    ))
                    _heatmap_fig.update_layout(
                        paper_bgcolor=BG, plot_bgcolor=BG, font=FONT,
                        height=max(280, len(_num_cols_ins) * 40),
                        margin=dict(t=10, b=10, l=10, r=10),
                        xaxis=dict(color="#475569", tickangle=45),
                        yaxis=dict(color="#475569", autorange="reversed")
                    )
                    st.plotly_chart(_heatmap_fig, use_container_width=True)
                except Exception as _he:
                    st.error(f"Heatmap error: {_he}")

                st.markdown('</div>', unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)

            # ── 6. DATASET COMBINER / JOIN BUILDER ──
            if len(st.session_state.uploaded_datasets) >= 2:
                st.markdown('<p style="font-size:0.72rem;font-weight:700;color:#FBB724;text-transform:uppercase;letter-spacing:0.1em;margin:0 0 0.6rem;border-left:3px solid #10B981;padding-left:0.6rem;">🔀 Dataset Combiner / Join Builder</p>', unsafe_allow_html=True)
                st.markdown('<div class="glass-card" style="padding:1.2rem;">', unsafe_allow_html=True)
                st.markdown('<p style="font-size:0.8rem;color:#94A3B8;margin-bottom:1rem;">Merge two uploaded datasets on a shared key column.</p>', unsafe_allow_html=True)

                _join_col1, _join_col2, _join_col3 = st.columns([2, 2, 1])
                with _join_col1:
                    _left_sel = st.selectbox("Left Dataset:", list(st.session_state.uploaded_datasets.keys()), index=0, key="join_left")
                    _left_key = st.selectbox("Left Join Column:", st.session_state.uploaded_datasets[_left_sel].columns.tolist(), key="join_left_key")
                with _join_col2:
                    _right_index = 1 if len(st.session_state.uploaded_datasets) > 1 else 0
                    _right_sel = st.selectbox("Right Dataset:", list(st.session_state.uploaded_datasets.keys()), index=_right_index, key="join_right")
                    _right_key = st.selectbox("Right Join Column:", st.session_state.uploaded_datasets[_right_sel].columns.tolist(), key="join_right_key")
                with _join_col3:
                    _join_how = st.selectbox("Join Type:", ["inner", "left", "right", "outer"], index=1, key="join_how")
                    st.markdown("<br>", unsafe_allow_html=True)
                    _do_join = st.button("⚡ Merge Datasets", use_container_width=True)

                if _do_join:
                    if _left_sel == _right_sel:
                        st.error("Cannot join a dataset with itself.")
                    else:
                        try:
                            _df_l = st.session_state.uploaded_datasets[_left_sel]
                            _df_r = st.session_state.uploaded_datasets[_right_sel]
                            _df_merged = pd.merge(_df_l, _df_r, left_on=_left_key, right_on=_right_key, how=_join_how, suffixes=('_left', '_right'))
                            _mname = f"merged_{_left_sel.split('.')[0]}_{_right_sel.split('.')[0]}.csv"
                            st.session_state.uploaded_datasets[_mname] = _df_merged
                            _tbl_m = re.sub(r'[^a-zA-Z0-9_]', '_', _mname.split('.')[0]).lower()
                            _df_merged.to_sql(_tbl_m, st.session_state.dataset_sqlite_conn, if_exists='replace', index=False)
                            st.success(f"Created '{_tbl_m}' — {len(_df_merged):,} rows × {len(_df_merged.columns)} columns")
                            st.toast(f"Merged table '{_tbl_m}' ready!", icon="🔀")
                            time.sleep(1)
                            st.rerun()
                        except Exception as _je:
                            st.error(f"Merge failed: {_je}")
                st.markdown('</div>', unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)

            # ── 7. CROSS-DATASET COMPARISON ──
            if len(st.session_state.uploaded_datasets) >= 2:
                st.markdown('<p style="font-size:0.72rem;font-weight:700;color:#FBB724;text-transform:uppercase;letter-spacing:0.1em;margin:0 0 0.6rem;border-left:3px solid #10B981;padding-left:0.6rem;">⚖️ Cross-Dataset Comparison</p>', unsafe_allow_html=True)
                st.markdown('<div class="glass-card" style="padding:1.2rem;">', unsafe_allow_html=True)
                st.markdown('<p style="font-size:0.8rem;color:#94A3B8;margin-bottom:0.8rem;">Compare key statistics side-by-side between two datasets.</p>', unsafe_allow_html=True)

                _cmp_c1, _cmp_c2 = st.columns(2)
                with _cmp_c1:
                    _cmp_left = st.selectbox("Dataset A:", list(st.session_state.uploaded_datasets.keys()), index=0, key="cmp_left")
                with _cmp_c2:
                    _cmp_right_idx = min(1, len(st.session_state.uploaded_datasets) - 1)
                    _cmp_right = st.selectbox("Dataset B:", list(st.session_state.uploaded_datasets.keys()), index=_cmp_right_idx, key="cmp_right")

                _df_cmp_a = st.session_state.uploaded_datasets[_cmp_left]
                _df_cmp_b = st.session_state.uploaded_datasets[_cmp_right]

                _cmp_data = {
                    "Metric": ["Rows", "Columns", "Numeric Cols", "Text Cols", "Missing Cells", "Duplicate Rows", "Memory"],
                    f"📄 {_cmp_left[:20]}": [
                        f"{len(_df_cmp_a):,}",
                        str(len(_df_cmp_a.columns)),
                        str(len(_df_cmp_a.select_dtypes(include='number').columns)),
                        str(len(_df_cmp_a.select_dtypes(exclude='number').columns)),
                        f"{int(_df_cmp_a.isna().sum().sum()):,}",
                        f"{int(_df_cmp_a.duplicated().sum()):,}",
                        f"{round(_df_cmp_a.memory_usage(deep=True).sum()/1024,1)} KB"
                    ],
                    f"📄 {_cmp_right[:20]}": [
                        f"{len(_df_cmp_b):,}",
                        str(len(_df_cmp_b.columns)),
                        str(len(_df_cmp_b.select_dtypes(include='number').columns)),
                        str(len(_df_cmp_b.select_dtypes(exclude='number').columns)),
                        f"{int(_df_cmp_b.isna().sum().sum()):,}",
                        f"{int(_df_cmp_b.duplicated().sum()):,}",
                        f"{round(_df_cmp_b.memory_usage(deep=True).sum()/1024,1)} KB"
                    ]
                }
                st.dataframe(pd.DataFrame(_cmp_data), use_container_width=True, hide_index=True)

                _shared_cols = list(set(_df_cmp_a.columns) & set(_df_cmp_b.columns))
                if _shared_cols:
                    st.markdown(f"""
                    <div style="background:rgba(14,165,233,0.06);border:1px solid rgba(14,165,233,0.2);
                        border-radius:8px;padding:0.6rem 1rem;margin-top:0.6rem;">
                        <span style="color:#0EA5E9;font-weight:700;font-size:0.8rem;">🔗 Shared Columns ({len(_shared_cols)}):</span>
                        <span style="color:#94A3B8;font-size:0.78rem;margin-left:0.4rem;">{", ".join(_shared_cols[:10])}{" ..." if len(_shared_cols) > 10 else ""}</span>
                    </div>""", unsafe_allow_html=True)

                st.markdown('</div>', unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)

            # ── 8. INTERACTIVE FILTER SLICER ──
            st.markdown('<p style="font-size:0.72rem;font-weight:700;color:#FBB724;text-transform:uppercase;letter-spacing:0.1em;margin:0 0 0.6rem;border-left:3px solid #10B981;padding-left:0.6rem;">🎛️ Interactive Data Slicer</p>', unsafe_allow_html=True)
            st.markdown('<div class="glass-card" style="padding:1.2rem;">', unsafe_allow_html=True)

            _slice_ds = st.selectbox("Dataset to filter:", list(st.session_state.uploaded_datasets.keys()), key="slice_ds")
            _df_slice = st.session_state.uploaded_datasets[_slice_ds]

            _s1, _s2, _s3 = st.columns([2, 1, 3])
            with _s1:
                _slice_col = st.selectbox("Column:", _df_slice.columns.tolist(), key="slice_col")
            with _s2:
                _is_num = pd.api.types.is_numeric_dtype(_df_slice[_slice_col])
                _ops = ["==", "contains", "!=", ">", "<", ">=", "<="] if _is_num else ["==", "contains", "!=", "starts with"]
                _slice_op = st.selectbox("Operator:", _ops, key="slice_op")
            with _s3:
                if _is_num:
                    _min_v = float(_df_slice[_slice_col].min()) if not _df_slice[_slice_col].isna().all() else 0.0
                    _max_v = float(_df_slice[_slice_col].max()) if not _df_slice[_slice_col].isna().all() else 100.0
                    _slice_val = st.number_input("Value:", value=float((_min_v + _max_v) / 2), key="slice_val_num")
                else:
                    _unq_vals = _df_slice[_slice_col].dropna().unique().tolist()
                    if len(_unq_vals) < 40:
                        _slice_val = st.selectbox("Value:", _unq_vals, key="slice_val_select")
                    else:
                        _slice_val = st.text_input("Search Term:", key="slice_val_text")

            _df_filtered = _df_slice.copy()
            try:
                if _slice_op == "==":
                    _df_filtered = _df_filtered[_df_filtered[_slice_col] == _slice_val]
                elif _slice_op == "!=":
                    _df_filtered = _df_filtered[_df_filtered[_slice_col] != _slice_val]
                elif _slice_op == "contains" and not _is_num:
                    _df_filtered = _df_filtered[_df_filtered[_slice_col].astype(str).str.contains(str(_slice_val), case=False, na=False)]
                elif _slice_op == "contains" and _is_num:
                    _df_filtered = _df_filtered[_df_filtered[_slice_col].astype(str).str.contains(str(_slice_val), na=False)]
                elif _slice_op == "starts with":
                    _df_filtered = _df_filtered[_df_filtered[_slice_col].astype(str).str.startswith(str(_slice_val), na=False)]
                elif _slice_op == ">":
                    _df_filtered = _df_filtered[_df_filtered[_slice_col] > float(_slice_val)]
                elif _slice_op == "<":
                    _df_filtered = _df_filtered[_df_filtered[_slice_col] < float(_slice_val)]
                elif _slice_op == ">=":
                    _df_filtered = _df_filtered[_df_filtered[_slice_col] >= float(_slice_val)]
                elif _slice_op == "<=":
                    _df_filtered = _df_filtered[_df_filtered[_slice_col] <= float(_slice_val)]

                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:8px;margin:0.4rem 0;">
                    <span style="color:#10B981;font-size:0.8rem;font-weight:600;">✓ {len(_df_filtered):,} of {len(_df_slice):,} rows</span>
                    <span style="color:#475569;font-size:0.72rem;">({round(len(_df_filtered)/max(len(_df_slice),1)*100,1)}% match)</span>
                </div>""", unsafe_allow_html=True)
                st.dataframe(_df_filtered.head(100), use_container_width=True, hide_index=True)

                _fd1, _fd2, _fd3 = st.columns([1.5, 1.5, 4])
                with _fd1:
                    st.download_button(
                        "📥 Export CSV",
                        data=_df_filtered.to_csv(index=False),
                        file_name=f"filtered_{_slice_ds}",
                        mime="text/csv",
                        use_container_width=True
                    )
                with _fd2:
                    # Excel export
                    _xl_buf = io.BytesIO()
                    try:
                        with pd.ExcelWriter(_xl_buf, engine='xlsxwriter') as _xlw:
                            _df_filtered.to_excel(_xlw, index=False, sheet_name='Filtered')
                        st.download_button(
                            "📥 Export Excel",
                            data=_xl_buf.getvalue(),
                            file_name=f"filtered_{_slice_ds.replace('.csv','.xlsx').replace('.xlsx','.xlsx')}",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            use_container_width=True,
                            key="dl_filter_xlsx"
                        )
                    except Exception:
                        pass
            except Exception as _fe:
                st.error(f"Filter error: {_fe}")

            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

            # ── 9. SMART CHART RECOMMENDATIONS + ENHANCED CHART BUILDER ──
            st.markdown('<p style="font-size:0.72rem;font-weight:700;color:#FBB724;text-transform:uppercase;letter-spacing:0.1em;margin:0 0 0.6rem;border-left:3px solid #10B981;padding-left:0.6rem;">📊 Interactive Chart Builder</p>', unsafe_allow_html=True)
            st.markdown('<div class="glass-card" style="padding:1.2rem;">', unsafe_allow_html=True)

            _vis_ds = st.selectbox("Select dataset:", list(st.session_state.uploaded_datasets.keys()), key="vis_ds")
            _df_vis = st.session_state.uploaded_datasets[_vis_ds]
            _num_cols_vis = _df_vis.select_dtypes(include='number').columns.tolist()
            _cat_cols_vis = _df_vis.select_dtypes(exclude='number').columns.tolist()

            # Smart Chart Recommendations
            _recs = []
            if _num_cols_vis and _cat_cols_vis:
                _recs.append(("📊 Bar Chart", f"{_cat_cols_vis[0]} vs {_num_cols_vis[0]}"))
                if len(_df_vis) > 5:
                    _recs.append(("📈 Line Chart", f"Trend of {_num_cols_vis[0]}"))
            if len(_num_cols_vis) >= 2:
                _recs.append(("🔵 Scatter Plot", f"{_num_cols_vis[0]} vs {_num_cols_vis[1]}"))
            if _cat_cols_vis and _num_cols_vis:
                _recs.append(("🍩 Pie Chart", f"Distribution of {_cat_cols_vis[0]}"))
            if _num_cols_vis:
                _recs.append(("📊 Histogram", f"Distribution of {_num_cols_vis[0]}"))

            if _recs:
                st.markdown('<div style="margin-bottom:0.8rem;">', unsafe_allow_html=True)
                st.markdown('<span style="font-size:0.75rem;font-weight:700;color:#8B5CF6;">🤖 Smart Recommendations:</span>', unsafe_allow_html=True)
                _rec_html = " ".join([f'<span class="rec-badge">{r[0]} — {r[1]}</span>' for r in _recs[:4]])
                st.markdown(f'<div style="margin-top:0.3rem;">{_rec_html}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            _v1, _v2, _v3, _v4 = st.columns([1.5, 1.5, 1.5, 1.5])
            with _v1:
                _vtype = st.selectbox("Chart Type:", [
                    "Bar Chart", "Line Chart", "Scatter Plot", "Pie Chart",
                    "Area Chart", "Histogram", "Box Plot"
                ], key="vis_type")
            with _v2:
                _vx = st.selectbox("X-Axis:", _df_vis.columns.tolist(), key="vis_x")
            with _v3:
                _all_cols_vis = _df_vis.columns.tolist()
                if _vtype in ["Histogram", "Box Plot"]:
                    _vy_opts = _num_cols_vis if _num_cols_vis else _all_cols_vis
                elif _vtype == "Pie Chart":
                    _vy_opts = _all_cols_vis
                else:
                    _vy_opts = _num_cols_vis if _num_cols_vis else _all_cols_vis
                if not _vy_opts:
                    _vy_opts = ["None"]
                _vy = st.selectbox("Y-Axis / Metric:", _vy_opts, key="vis_y")
            with _v4:
                _vcolor = st.selectbox("Group By (color):", ["None"] + _cat_cols_vis, key="vis_color")

            # Extra options row
            _vo1, _vo2, _vo3 = st.columns([2, 1, 3])
            with _vo1:
                _chart_title = st.text_input("Chart Title (optional):", "", key="vis_title", placeholder="My Custom Chart")
            with _vo2:
                _agg_mode = st.selectbox("Aggregation:", ["Raw", "Sum", "Mean", "Count"], key="vis_agg")

            try:
                _chart_df = _df_vis.copy()
                # Apply aggregation if needed
                if _agg_mode != "Raw" and _vtype in ["Bar Chart", "Line Chart", "Area Chart"] and _vy in _num_cols_vis:
                    _group_col = _vx
                    if _agg_mode == "Sum":
                        _chart_df = _chart_df.groupby(_group_col, as_index=False)[_vy].sum()
                    elif _agg_mode == "Mean":
                        _chart_df = _chart_df.groupby(_group_col, as_index=False)[_vy].mean().round(2)
                    elif _agg_mode == "Count":
                        _chart_df = _chart_df.groupby(_group_col, as_index=False)[_vy].count()
                else:
                    _chart_df = _chart_df.head(200)

                _color_arg = None if _vcolor == "None" else _vcolor

                _fig = None
                if _vtype == "Bar Chart":
                    _fig = px.bar(_chart_df, x=_vx, y=_vy, color=_color_arg, color_discrete_sequence=PAL)
                elif _vtype == "Line Chart":
                    _fig = px.line(_chart_df, x=_vx, y=_vy, color=_color_arg, color_discrete_sequence=PAL, markers=True)
                elif _vtype == "Scatter Plot":
                    _fig = px.scatter(_chart_df, x=_vx, y=_vy, color=_color_arg, color_discrete_sequence=PAL, opacity=0.7)
                elif _vtype == "Area Chart":
                    _fig = px.area(_chart_df, x=_vx, y=_vy, color=_color_arg, color_discrete_sequence=PAL)
                elif _vtype == "Pie Chart":
                    _fig = px.pie(_chart_df, names=_vx, values=_vy, color_discrete_sequence=PAL, hole=0.45)
                elif _vtype == "Histogram":
                    _fig = px.histogram(_chart_df, x=_vy, nbins=30, color=_color_arg,
                                         color_discrete_sequence=PAL, opacity=0.85)
                elif _vtype == "Box Plot":
                    _fig = px.box(_chart_df, x=_color_arg if _color_arg else _vx, y=_vy,
                                  color=_color_arg, color_discrete_sequence=PAL)

                if _fig is not None:
                    _fig.update_layout(**LO, height=380)
                    if _chart_title:
                        _fig.update_layout(title=dict(text=_chart_title, font=dict(size=14, color="#F1F5F9"), x=0.5))
                    if _vtype not in ["Pie Chart"]:
                        _fig.update_layout(
                            xaxis=dict(showgrid=False, color="#475569"),
                            yaxis=dict(showgrid=True, gridcolor=GRID, color="#475569")
                        )
                    st.plotly_chart(_fig, use_container_width=True)
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;justify-content:space-between;padding:0.4rem 0.8rem;
                        background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.05);
                        border-radius:8px;margin-top:0.3rem;">
                        <span style="font-size:0.72rem;color:#475569;">
                            {_vtype} · {_vis_ds} · {_agg_mode} · {len(_chart_df)} data points
                        </span>
                        <span style="font-size:0.68rem;color:#334155;">
                            X: {_vx} · Y: {_vy}{f" · Color: {_vcolor}" if _vcolor != "None" else ""}
                        </span>
                    </div>""", unsafe_allow_html=True)
            except Exception as _ve:
                st.error(f"Chart error: {_ve}")

            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

            # ── 10. AI COPILOT FOR UPLOADED DATASETS ──
            st.markdown('<p style="font-size:0.72rem;font-weight:700;color:#FBB724;text-transform:uppercase;letter-spacing:0.1em;margin:0 0 0.6rem;border-left:3px solid #10B981;padding-left:0.6rem;">🧠 AI Copilot — Natural Language Analysis</p>', unsafe_allow_html=True)
            st.markdown("""
            <div class="glass-card" style="padding:1.2rem;border-top:3px solid #8B5CF6;">
                <div style="display:flex;align-items:center;gap:10px;margin-bottom:0.8rem;">
                    <div style="width:36px;height:36px;background:linear-gradient(135deg,#8B5CF6,#6D28D9);
                        border-radius:10px;display:flex;align-items:center;justify-content:center;
                        font-size:1.1rem;animation:glow 3s ease-in-out infinite;">🧠</div>
                    <div>
                        <div style="font-size:0.9rem;font-weight:700;color:#F1F5F9;">AI Dataset Copilot</div>
                        <div style="font-size:0.72rem;color:#64748B;">Ask questions about your data in plain English — AI writes SQL, runs it, and summarizes findings.</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            # Schema context
            _schema_desc = []
            for _name, _df in st.session_state.uploaded_datasets.items():
                _t_name = _name
                _cols_str = ", ".join(f"{_col}" for _col in _df.columns)
                _schema_desc.append(f"Table: {_t_name} - Columns: [{_cols_str}] ({len(_df)} rows)")
            _schema_context_str = "\n".join(_schema_desc)

            with st.expander("👁️ View Schema Context (sent to AI)"):
                st.code(_schema_context_str, language="text")

            # Example queries
            _example_queries = [
                "Count total rows in each table",
                "Show top 10 records by highest numeric column",
                "Find average values grouped by first text column",
                "What are the unique values in the first column?"
            ]
            st.markdown('<div style="display:flex;gap:0.4rem;flex-wrap:wrap;margin-bottom:0.6rem;">', unsafe_allow_html=True)
            for _eq in _example_queries:
                st.markdown(f"""<span style="display:inline-block;background:rgba(139,92,246,0.08);
                    border:1px solid rgba(139,92,246,0.2);color:#A78BFA;font-size:0.72rem;
                    padding:0.25rem 0.6rem;border-radius:20px;">{_eq}</span>""", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            with st.form("ds_ai_form"):
                _ds_question = st.text_area(
                    "Ask the AI Copilot:",
                    placeholder="e.g. Find the average sales grouped by category...\ne.g. What is the total quantity ordered per product?",
                    key="ds_ai_q",
                    height=100
                )
                _ds_sub = st.form_submit_button("⚡ Analyze with AI Copilot", use_container_width=True)

            if _ds_sub and _ds_question.strip():
                with st.spinner("🧠 AI is analyzing your datasets..."):
                    try:
                        _ds_sql = query_uploaded_datasets(_ds_question.strip(), _schema_context_str)

                        st.markdown('<span style="font-size:0.8rem;font-weight:700;color:#8B5CF6;">Generated SQLite Query</span>', unsafe_allow_html=True)
                        st.code(_ds_sql, language="sql")

                        _df_res = pd.read_sql_query(_ds_sql, st.session_state.dataset_sqlite_conn)

                        if _df_res is not None and not _df_res.empty:
                            # Results KPIs
                            _rk1, _rk2, _rk3 = st.columns(3)
                            with _rk1:
                                st.markdown(f'<div class="kpi-tile"><div class="kpi-tile-val">{len(_df_res):,}</div><div class="kpi-tile-lbl">Result Rows</div></div>', unsafe_allow_html=True)
                            with _rk2:
                                st.markdown(f'<div class="kpi-tile"><div class="kpi-tile-val">{len(_df_res.columns)}</div><div class="kpi-tile-lbl">Columns</div></div>', unsafe_allow_html=True)
                            with _rk3:
                                _res_mem = round(_df_res.memory_usage(deep=True).sum() / 1024, 1)
                                st.markdown(f'<div class="kpi-tile"><div class="kpi-tile-val">{_res_mem} KB</div><div class="kpi-tile-lbl">Result Size</div></div>', unsafe_allow_html=True)

                            st.markdown("<br>", unsafe_allow_html=True)
                            st.dataframe(_df_res, use_container_width=True, hide_index=True)

                            # Auto-chart for results
                            _res_num = _df_res.select_dtypes(include='number').columns.tolist()
                            _res_cat = _df_res.select_dtypes(exclude='number').columns.tolist()
                            if _res_num and _res_cat and len(_df_res) > 1:
                                try:
                                    _auto_fig = px.bar(_df_res.head(20), x=_res_cat[0], y=_res_num[0],
                                                        color_discrete_sequence=["#8B5CF6"])
                                    _auto_fig.update_layout(**LO, height=280,
                                        xaxis=dict(showgrid=False, color="#475569"),
                                        yaxis=dict(showgrid=True, gridcolor=GRID, color="#475569"))
                                    st.plotly_chart(_auto_fig, use_container_width=True)
                                except Exception:
                                    pass

                            # AI Insight
                            _df_summary = _df_res.head(15).to_string()
                            _ai_insight_txt = generate_ai_insight(_ds_question.strip(), _ds_sql, _df_summary)

                            st.markdown(f"""
                            <div style="background:linear-gradient(135deg,rgba(139,92,246,0.06),rgba(16,185,129,0.04));
                                border:1px solid rgba(139,92,246,0.25);
                                border-radius:12px;padding:1rem 1.2rem;margin-top:0.8rem;">
                                <div style="display:flex;align-items:center;gap:8px;margin-bottom:0.4rem;">
                                    <span style="font-size:1.1rem;">💡</span>
                                    <span style="color:#A78BFA;font-weight:700;font-size:0.85rem;">AI Executive Summary</span>
                                </div>
                                <p style="color:#E2E8F0;font-size:0.83rem;margin:0;line-height:1.7;">{_ai_insight_txt}</p>
                            </div>
                            """, unsafe_allow_html=True)

                            st.markdown("<br>", unsafe_allow_html=True)
                            _dl1, _dl2, _dl3 = st.columns([1, 1, 2])
                            with _dl1:
                                st.download_button(
                                    "📥 Download CSV",
                                    data=_df_res.to_csv(index=False),
                                    file_name="ai_copilot_results.csv",
                                    mime="text/csv",
                                    use_container_width=True
                                )
                            with _dl2:
                                _xl_res_buf = io.BytesIO()
                                try:
                                    with pd.ExcelWriter(_xl_res_buf, engine='xlsxwriter') as _xlw2:
                                        _df_res.to_excel(_xlw2, index=False, sheet_name='AI Results')
                                    st.download_button(
                                        "📥 Download Excel",
                                        data=_xl_res_buf.getvalue(),
                                        file_name="ai_copilot_results.xlsx",
                                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                        use_container_width=True,
                                        key="dl_ai_xlsx"
                                    )
                                except Exception:
                                    pass
                        else:
                            st.info("Query returned 0 rows.")
                    except Exception as _aie:
                        st.markdown(f'<div class="toast-error">❌ Copilot Error: {_aie}</div>', unsafe_allow_html=True)
                        st.info("Tip: Check table/column names in the schema context above.")

            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

            # ── 11. DOWNLOADABLE SUMMARY REPORT ──
            st.markdown('<p style="font-size:0.72rem;font-weight:700;color:#FBB724;text-transform:uppercase;letter-spacing:0.1em;margin:0 0 0.6rem;border-left:3px solid #10B981;padding-left:0.6rem;">📋 Downloadable Summary Report</p>', unsafe_allow_html=True)
            st.markdown('<div class="glass-card" style="padding:1.2rem;">', unsafe_allow_html=True)
            st.markdown('<p style="font-size:0.8rem;color:#94A3B8;margin-bottom:0.8rem;">Generate a comprehensive report of all loaded datasets — download as CSV, Excel, or text.</p>', unsafe_allow_html=True)

            _rpt_c1, _rpt_c2 = st.columns([1, 1])
            with _rpt_c1:
                if st.button("📋 Generate Summary Report", use_container_width=True, key="gen_report"):
                    _report_lines = []
                    _report_lines.append("=" * 70)
                    _report_lines.append("  AAITECH — MULTI-DATASET ANALYTICS SUMMARY REPORT")
                    _report_lines.append(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                    _report_lines.append("=" * 70)
                    _report_lines.append("")

                    for _rname, _rdf in st.session_state.uploaded_datasets.items():
                        _tbl = re.sub(r'[^a-zA-Z0-9_]', '_', _rname.split('.')[0]).lower()
                        _r_num = _rdf.select_dtypes(include='number').columns.tolist()
                        _r_cat = _rdf.select_dtypes(exclude='number').columns.tolist()
                        _r_miss = int(_rdf.isna().sum().sum())
                        _r_dups = int(_rdf.duplicated().sum())
                        _r_total = _rdf.shape[0] * _rdf.shape[1]
                        _r_comp = round((1 - _r_miss / _r_total) * 100, 1) if _r_total > 0 else 0

                        _report_lines.append(f"━━━ Dataset: {_rname} (table: {_tbl}) ━━━")
                        _report_lines.append(f"  Rows: {len(_rdf):,}  |  Columns: {len(_rdf.columns)}")
                        _report_lines.append(f"  Numeric columns: {len(_r_num)}  |  Text columns: {len(_r_cat)}")
                        _report_lines.append(f"  Missing values: {_r_miss:,}  |  Completeness: {_r_comp}%")
                        _report_lines.append(f"  Duplicate rows: {_r_dups:,}")
                        _report_lines.append(f"  Columns: {', '.join(_rdf.columns.tolist())}")
                        _report_lines.append("")

                        if _r_num:
                            _desc = _rdf[_r_num].describe().round(2)
                            _report_lines.append("  Numeric Summary:")
                            for _stat_row in _desc.to_string().split('\n'):
                                _report_lines.append(f"    {_stat_row}")
                            _report_lines.append("")

                        _report_lines.append("")

                    _report_lines.append("=" * 70)
                    _report_lines.append("  END OF REPORT")
                    _report_lines.append("=" * 70)

                    _report_text = "\n".join(_report_lines)
                    st.code(_report_text, language="text")

                    _rpt_d1, _rpt_d2 = st.columns([1, 1])
                    with _rpt_d1:
                        st.download_button(
                            "📥 Download Report (.txt)",
                            data=_report_text,
                            file_name=f"dataset_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                            mime="text/plain",
                            use_container_width=True
                        )
                    with _rpt_d2:
                        # Excel report with all datasets
                        _xl_rpt_buf = io.BytesIO()
                        try:
                            with pd.ExcelWriter(_xl_rpt_buf, engine='xlsxwriter') as _xlw3:
                                for _rname2, _rdf2 in st.session_state.uploaded_datasets.items():
                                    _sheet = re.sub(r'[^a-zA-Z0-9_]', '_', _rname2.split('.')[0])[:31]
                                    _rdf2.to_excel(_xlw3, index=False, sheet_name=_sheet)
                            st.download_button(
                                "📥 Download All Data (.xlsx)",
                                data=_xl_rpt_buf.getvalue(),
                                file_name=f"all_datasets_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                use_container_width=True,
                                key="dl_all_xlsx"
                            )
                        except Exception:
                            pass

            st.markdown('</div>', unsafe_allow_html=True)

            # ── Workspace Footer ──
            st.markdown(f"""
            <div style="text-align:center;padding:1rem 0 0.5rem;
                color:#334155;font-size:0.72rem;
                border-top:1px solid rgba(255,255,255,0.05);margin-top:1rem;">
                AaiTech Industries &nbsp;&middot;&nbsp;
                Multi-Dataset Analytics Workspace &nbsp;&middot;&nbsp;
                {len(st.session_state.uploaded_datasets)} dataset(s) loaded &nbsp;&middot;&nbsp;
                &copy; 2025
            </div>""", unsafe_allow_html=True)
# ══════════════════════════════════════════════════════════════════════════════
# HISTORY PAGE
# ══════════════════════════════════════════════════════════════════════════════
elif _page == "📜 History":
    st.markdown('<div style="font-size:1.8rem;font-weight:800;color:#FFFFFF!important;-webkit-text-fill-color:#FFFFFF!important;margin-bottom:0.4rem;">&#128220; Query History</div><div style="font-size:0.9rem;color:#475569!important;margin-bottom:1.5rem;">All your recent queries — re-run, copy, or save them</div>',unsafe_allow_html=True)
    if not st.session_state.history:
        st.markdown('<div class="glass-card" style="text-align:center;padding:3rem;"><div style="font-size:3rem;margin-bottom:1rem;">&#128219;</div><div style="font-size:1rem;font-weight:600;color:#64748B!important;">No queries yet</div><div style="font-size:0.85rem;color:#334155!important;margin-top:0.4rem;">Go to Query page and ask your first question</div></div>',unsafe_allow_html=True)
    else:
        if st.button("&#128465; Clear All", key="hist_clear"):
            st.session_state.history=[];st.rerun()
        for _i,_item in enumerate(reversed(st.session_state.history),1):
            with st.expander(f"#{_i} — {_item['question'][:70]}{'...' if len(_item['question'])>70 else ''}"):
                _hc1,_hc2,_hc3=st.columns([3,1,1])
                with _hc1:
                    st.markdown(f"**{_item['question']}**")
                    st.markdown(f"<span style='color:#475569;font-size:0.78rem;'>&#128336; {_item.get('date','')} {_item.get('time','')} &nbsp;&middot;&nbsp; &#128202; {_item['rows']} rows</span>",unsafe_allow_html=True)
                with _hc2:
                    if st.button("&#9654; Re-run",key=f"hr_{_i}",use_container_width=True):
                        st.session_state.pending_question=_item["question"]
                        st.session_state.submit=True
                        st.session_state.active_page="💬 Query";st.rerun()
                with _hc3:
                    if st.button("&#128190; Save",key=f"hs_{_i}",use_container_width=True):
                        if _item["question"] not in st.session_state.saved_queries:
                            st.session_state.saved_queries.append(_item["question"])
                            st.toast("Saved!",icon="💾")
                st.code(_item["sql"],language="sql")

# ══════════════════════════════════════════════════════════════════════════════
# SAVED PAGE
# ══════════════════════════════════════════════════════════════════════════════
elif _page == "💾 Saved":
    st.markdown('<div style="font-size:1.8rem;font-weight:800;color:#FFFFFF!important;-webkit-text-fill-color:#FFFFFF!important;margin-bottom:0.4rem;">&#128190; Saved Queries</div><div style="font-size:0.9rem;color:#475569!important;margin-bottom:1.5rem;">Your bookmarked queries for quick access</div>',unsafe_allow_html=True)
    if not st.session_state.saved_queries:
        st.markdown('<div class="glass-card" style="text-align:center;padding:3rem;"><div style="font-size:3rem;margin-bottom:1rem;">&#128278;</div><div style="font-size:1rem;font-weight:600;color:#64748B!important;">No saved queries</div><div style="font-size:0.85rem;color:#334155!important;margin-top:0.4rem;">Save queries from the Query or History pages</div></div>',unsafe_allow_html=True)
    else:
        for _i,_q in enumerate(st.session_state.saved_queries,1):
            st.markdown(f'<div class="history-item"><div style="font-size:0.88rem;font-weight:600;color:#E2E8F0!important;">&#128278; {_q}</div></div>',unsafe_allow_html=True)
            _sc1,_sc2,_sc3=st.columns([1,1,6])
            with _sc1:
                if st.button("&#9654; Run",key=f"sv_{_i}",use_container_width=True):
                    st.session_state.pending_question=_q;st.session_state.submit=True
                    st.session_state.active_page="💬 Query";st.rerun()
            with _sc2:
                if st.button("&#128465; Del",key=f"sd_{_i}",use_container_width=True):
                    st.session_state.saved_queries.remove(_q);st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# SCHEMA PAGE
# ══════════════════════════════════════════════════════════════════════════════
elif _page == "📋 Schema":
    st.markdown('<div style="font-size:1.8rem;font-weight:800;color:#FFFFFF!important;-webkit-text-fill-color:#FFFFFF!important;margin-bottom:0.4rem;">&#128203; Schema Explorer</div><div style="font-size:0.9rem;color:#475569!important;margin-bottom:1.5rem;">Browse your database structure and preview data</div>',unsafe_allow_html=True)
    _tables={"customers":{"desc":"Customer accounts","emoji":"&#128101;","cols":[("customer_id","VARCHAR(10)","PK"),("company_name","VARCHAR(100)",""),("contact_name","VARCHAR(100)",""),("city","VARCHAR(50)",""),("country","VARCHAR(50)","")]},
        "orders":{"desc":"Customer orders","emoji":"&#128230;","cols":[("order_id","INT","PK"),("customer_id","VARCHAR(10)","FK&#8594;customers"),("order_date","DATE",""),("ship_city","VARCHAR(50)",""),("freight","FLOAT","")]},
        "order_details":{"desc":"Order line items","emoji":"&#128203;","cols":[("order_id","INT","FK&#8594;orders"),("product_id","INT","FK&#8594;products"),("quantity","INT",""),("unit_price","FLOAT","")]},
        "products":{"desc":"Product catalog","emoji":"&#128717;","cols":[("product_id","INT","PK"),("product_name","VARCHAR(100)",""),("supplier_id","INT","FK&#8594;suppliers"),("category","VARCHAR(50)",""),("unit_price","FLOAT","")]},
        "suppliers":{"desc":"Product suppliers","emoji":"&#127981;","cols":[("supplier_id","INT","PK"),("company_name","VARCHAR(100)",""),("contact_name","VARCHAR(100)",""),("city","VARCHAR(50)",""),("country","VARCHAR(50)","")]}}
    _tcols=st.columns(5)
    for _tc,(_tn2,_ti) in zip(_tcols,_tables.items()):
        with _tc:
            st.markdown(f'<div class="glass-card" style="text-align:center;padding:1rem;"><div style="font-size:1.8rem;">{_ti["emoji"]}</div><div style="font-size:0.85rem;font-weight:700;color:#F1F5F9!important;margin-top:0.4rem;">{_tn2}</div><div style="font-size:0.72rem;color:#475569!important;">{_ti["desc"]}</div></div>',unsafe_allow_html=True)
    st.markdown("<br>",unsafe_allow_html=True)
    _sel=st.selectbox("Select a table:",list(_tables.keys()))
    if _sel:
        _sc1,_sc2=st.columns([1,2])
        with _sc1:
            st.markdown(f"**{_tables[_sel]['emoji']} {_sel}** — {_tables[_sel]['desc']}")
            st.dataframe(pd.DataFrame(_tables[_sel]["cols"],columns=["Column","Type","Notes"]),use_container_width=True,hide_index=True)
        with _sc2:
            st.markdown("**&#128196; Data Preview**")
            try:
                st.dataframe(execute_query(f"SELECT * FROM {_sel} LIMIT 10"),use_container_width=True,hide_index=True)
            except Exception as _e:
                st.error(f"Could not load: {_e}")
    st.markdown("---")
    st.markdown("**&#128279; Relationships**")
    st.code("customers ──< orders ──< order_details >── products >── suppliers",language="text")

# ══════════════════════════════════════════════════════════════════════════════
# SETTINGS PAGE
# ══════════════════════════════════════════════════════════════════════════════
elif _page == "⚙️ Settings":
    st.markdown('<div style="font-size:1.8rem;font-weight:800;color:#FFFFFF!important;-webkit-text-fill-color:#FFFFFF!important;margin-bottom:0.4rem;">&#9881; Settings</div><div style="font-size:0.9rem;color:#475569!important;margin-bottom:1.5rem;">Database connection, API configuration, and app info</div>',unsafe_allow_html=True)

    # DB
    st.markdown('<div class="glass-card" style="margin-bottom:1rem;"><div style="font-size:0.85rem;font-weight:700;color:#FBB724!important;margin-bottom:1rem;">&#128451; Database Connection Settings</div>',unsafe_allow_html=True)
    from database import get_connection_status, update_db_config, get_db_type
    
    # Connection parameters from env
    import os
    current_db_type = get_db_type()
    
    _dok, _dmsg = get_connection_status()
    _ddot="status-dot-green" if _dok else "status-dot-red"
    st.markdown(f'<div style="display:flex;align-items:center;justify-content:space-between;background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.06);border-radius:10px;padding:0.8rem 1rem;margin-bottom:1rem;"><div><div style="font-size:0.85rem;font-weight:600;color:#E2E8F0!important;">Active Database</div><div style="font-size:0.75rem;color:#475569!important;">{_dmsg}</div></div><div><span class="{_ddot}"></span><span style="font-size:0.8rem;color:{"#10B981" if _dok else "#EF4444"}!important;">{"Online" if _dok else "Offline"}</span></div></div>',unsafe_allow_html=True)
    
    st.markdown('<p style="font-size:0.82rem;font-weight:700;color:#F1F5F9;margin-bottom:0.5rem;">Configure Database:</p>', unsafe_allow_html=True)
    
    # Form for updating database connection properties
    with st.form("db_config_form"):
        db_choice = st.selectbox("Database Type", ["sqlite", "mysql"], index=0 if current_db_type == "sqlite" else 1)
        
        # MySQL parameters
        col1, col2 = st.columns(2)
        with col1:
            host_val = st.text_input("MySQL Host", value=os.getenv("MYSQL_HOST", "127.0.0.1"))
            user_val = st.text_input("MySQL User", value=os.getenv("MYSQL_USER", "root"))
            db_val = st.text_input("MySQL Database", value=os.getenv("MYSQL_DATABASE", "aaitech"))
        with col2:
            port_val = st.number_input("MySQL Port", min_value=1, max_value=65535, value=int(os.getenv("MYSQL_PORT", 3306)))
            pass_val = st.text_input("MySQL Password", value=os.getenv("MYSQL_PASSWORD", ""), type="password")
            
        save_db_btn = st.form_submit_button("💾 Save & Connect Database")
        
    if save_db_btn:
        with st.spinner("Connecting to database..."):
            try:
                update_db_config(
                    db_type=db_choice,
                    host=host_val,
                    port=port_val,
                    user=user_val,
                    password=pass_val,
                    database=db_val
                )
                # Test connection immediately
                _ok, _msg = get_connection_status()
                if _ok:
                    st.markdown(f'<div class="toast-success">&#10003; Successfully Connected! Database set to {db_choice.upper()} ({_msg})</div>', unsafe_allow_html=True)
                    time.sleep(1)
                    st.rerun()
                else:
                    st.markdown(f'<div class="toast-error">❌ Connection failed with new settings: {_msg}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.markdown(f'<div class="toast-error">❌ Configuration error: {e}</div>', unsafe_allow_html=True)
                
    if st.button("&#8635; Test Connection"):
        _ok2, _msg2 = get_connection_status()
        if _ok2:
            st.markdown(f'<div class="toast-success">&#10003; Connected: {_msg2}</div>',unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="toast-error">&#10060; Cannot connect to database.</div>',unsafe_allow_html=True)
    st.markdown('</div>',unsafe_allow_html=True)

    # Azure
    st.markdown('<div class="glass-card" style="margin-bottom:1rem;"><div style="font-size:0.85rem;font-weight:700;color:#FBB724!important;margin-bottom:1rem;">&#129504; Azure OpenAI Configuration</div>',unsafe_allow_html=True)
    import os; from dotenv import load_dotenv; load_dotenv()
    for _ek,_el in [("AZURE_OPENAI_ENDPOINT","OpenAI Endpoint"),("DEPLOYMENT_NAME","Model Deployment"),
        ("API_VERSION","API Version"),("AZURE_SEARCH_ENDPOINT","Search Endpoint"),("INDEX_NAME","Search Index")]:
        _ev=os.getenv(_ek,"")
        _eset=bool(_ev and "your_" not in _ev.lower())
        _edot="status-dot-green" if _eset else "status-dot-red"
        _edisp=(_ev[:40]+"..." if len(_ev)>40 else _ev) if _ev else "Not configured"
        st.markdown(f'<div style="display:flex;align-items:center;justify-content:space-between;background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.06);border-radius:10px;padding:0.7rem 1rem;margin-bottom:0.4rem;"><div><div style="font-size:0.82rem;font-weight:600;color:#E2E8F0!important;">{_el}</div><div style="font-size:0.72rem;color:#475569!important;font-family:monospace;">{_edisp}</div></div><span class="{_edot}"></span></div>',unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.78rem;color:#475569!important;margin-top:0.5rem;">Edit the <code style="color:#FBB724;">.env</code> file to update credentials.</div></div>',unsafe_allow_html=True)

    # App info
    st.markdown('<div class="glass-card"><div style="font-size:0.85rem;font-weight:700;color:#FBB724!important;margin-bottom:1rem;">&#8505; Application Info</div>',unsafe_allow_html=True)
    for _ik,_iv in [("Version","1.0.0"),("Framework","Streamlit 1.51"),("Python","3.13"),
        ("Database","MySQL 8.0 (XAMPP)"),("AI Model","Azure OpenAI GPT-4"),("Search","Azure Cognitive Search")]:
        st.markdown(f'<div style="display:flex;justify-content:space-between;padding:0.4rem 0;border-bottom:1px solid rgba(255,255,255,0.04);"><span style="font-size:0.82rem;color:#64748B!important;">{_ik}</span><span style="font-size:0.82rem;color:#E2E8F0!important;font-weight:600;">{_iv}</span></div>',unsafe_allow_html=True)
    st.markdown('</div>',unsafe_allow_html=True)

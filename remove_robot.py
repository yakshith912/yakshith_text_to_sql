content = open("app.py", encoding="utf-8").read()

start_marker = 'if page == "🏠 Home":'
end_marker   = '# ══════════════════════════════════════════════════════════════════════════════\n# QUERY PAGE'

start_idx = content.index(start_marker)
end_idx   = content.index(end_marker)

new_home = '''if page == "🏠 Home":

    # ── Hero (full width, no image) ───────────────────────────────────────────
    st.markdown("""
    <div class="hero-section">
        <div class="hero-badge">&#10022; Powered by Azure OpenAI + RAG</div>
        <div class="hero-title">AI-Powered Text-to-SQL Assistant</div>
        <div class="hero-sub">
            Transform plain English into precise SQL queries instantly.
            No SQL expertise needed — just ask your business question and get results in seconds.
        </div>
        <div style="display:flex;gap:0.7rem;flex-wrap:wrap;margin-top:1rem;">
            <span style="background:rgba(251,183,36,0.1);border:1px solid rgba(251,183,36,0.3);
                border-radius:8px;padding:0.35rem 0.8rem;font-size:0.78rem;color:#FBB724;font-weight:600;">
                &#9889; GPT-4 Powered</span>
            <span style="background:rgba(16,185,129,0.1);border:1px solid rgba(16,185,129,0.3);
                border-radius:8px;padding:0.35rem 0.8rem;font-size:0.78rem;color:#10B981;font-weight:600;">
                &#128994; Live Database</span>
            <span style="background:rgba(139,92,246,0.1);border:1px solid rgba(139,92,246,0.3);
                border-radius:8px;padding:0.35rem 0.8rem;font-size:0.78rem;color:#8B5CF6;font-weight:600;">
                &#128269; Schema-Aware RAG</span>
        </div>
        <div class="hero-stats">
            <div><div class="hero-stat-val">5</div><div class="hero-stat-lbl">Tables</div></div>
            <div><div class="hero-stat-val">&#8734;</div><div class="hero-stat-lbl">Queries</div></div>
            <div><div class="hero-stat-val">AI</div><div class="hero-stat-lbl">GPT-4</div></div>
            <div><div class="hero-stat-val">RAG</div><div class="hero-stat-lbl">Context</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Live KPI bar ──────────────────────────────────────────────────────────
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
        </div>
        """, unsafe_allow_html=True)
    except Exception:
        pass

    # ── Query Input ───────────────────────────────────────────────────────────
    st.markdown(\'<div class="query-input-wrap">\', unsafe_allow_html=True)
    st.markdown("""
    <div style="display:flex;align-items:center;gap:8px;margin-bottom:0.8rem;">
        <div style="width:8px;height:8px;background:#FBB724;border-radius:50%;box-shadow:0 0 6px #FBB724;"></div>
        <span style="font-size:0.9rem;font-weight:700;color:#F1F5F9;">&#9889; Ask the AI</span>
        <span style="font-size:0.72rem;color:#475569;margin-left:4px;">Type in plain English</span>
    </div>
    """, unsafe_allow_html=True)

    def _submit_home(): st.session_state.submit = True

    st.text_input("Your question", value=st.session_state.get("question_input", ""),
                  key="question_input",
                  placeholder="e.g.  Show total revenue by product category...",
                  on_change=_submit_home, label_visibility="collapsed")

    chip_cols = st.columns(6)
    chips = ["Show customers","Revenue by category","Top 5 products",
             "Orders by country","List suppliers","Total freight"]
    for _col, _chip in zip(chip_cols, chips):
        with _col:
            if st.button(_chip, key=f"chip_{_chip}", use_container_width=True):
                st.session_state.question_input = _chip
                st.session_state.submit = True
                st.rerun()

    _c1, _c2, _c3, _ = st.columns([1.2, 1.2, 1, 4])
    with _c1:
        if st.button("&#9654;  Run Query", use_container_width=True, key="home_run"):
            st.session_state.submit = True
    with _c2:
        if st.button("&#128190;  Save Query", use_container_width=True, key="home_save"):
            _q = st.session_state.get("question_input","").strip()
            if _q and _q not in st.session_state.saved_queries:
                st.session_state.saved_queries.append(_q)
                st.toast("Saved!", icon="&#128190;")
    with _c3:
        if st.button("&#10005;  Clear", use_container_width=True, key="home_clear"):
            st.session_state.question_input = ""
            st.rerun()
    st.markdown(\'</div>\', unsafe_allow_html=True)

    # ── Process Query ─────────────────────────────────────────────────────────
    if st.session_state.submit and st.session_state.get("question_input","").strip():
        _uq = st.session_state["question_input"].strip()
        if _uq.lower() in {"hi","hello","hey"}:
            st.markdown(\'<div class="toast-success">&#128075; Hello! Ask me any business question.</div>\',
                        unsafe_allow_html=True)
        else:
            with st.spinner("&#129504; AI is generating SQL..."):
                _sql, _df, _err = run_query(_uq)
            if _err:
                st.markdown(f\'<div class="toast-error">&#10060; {_err}</div>\', unsafe_allow_html=True)
            else:
                st.session_state.last_sql = _sql
                st.session_state.last_df  = _df
                st.session_state.history.append({
                    "question": _uq, "sql": _sql,
                    "rows": len(_df) if _df is not None else 0,
                    "time": datetime.now().strftime("%H:%M:%S"),
                    "date": datetime.now().strftime("%b %d")
                })
                st.markdown(\'<div class="toast-success">&#10003; Query executed successfully</div>\',
                            unsafe_allow_html=True)
                _rc, _sc = st.columns([3, 2])
                with _rc:
                    st.markdown(\'<div style="font-size:0.78rem;font-weight:700;color:#FBB724;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:0.4rem;">&#128202; Results</div>\', unsafe_allow_html=True)
                    if _df is not None and not _df.empty:
                        st.markdown(f"<span style=\'color:#10B981;font-size:0.8rem;font-weight:600;\'>&#10003; {len(_df)} row(s) &middot; {len(_df.columns)} col(s)</span>", unsafe_allow_html=True)
                        st.dataframe(_df, use_container_width=True, hide_index=True)
                        _dc1, _dc2 = st.columns(2)
                        with _dc1:
                            st.download_button("&#11015; CSV", data=_df.to_csv(index=False),
                                               file_name="results.csv", mime="text/csv", use_container_width=True)
                        with _dc2:
                            st.download_button("&#11015; Excel", data=_df.to_csv(index=False).encode(),
                                               file_name="results.xlsx", mime="application/vnd.ms-excel", use_container_width=True)
                    else:
                        st.info("No results found.")
                with _sc:
                    st.markdown(\'<div style="font-size:0.78rem;font-weight:700;color:#FBB724;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:0.4rem;">&#128295; Generated SQL</div>\', unsafe_allow_html=True)
                    st.code(_sql, language="sql")
                    if _df is not None and not _df.empty:
                        _num = _df.select_dtypes(include=\'number\').columns.tolist()
                        _cat = _df.select_dtypes(exclude=\'number\').columns.tolist()
                        if _num and _cat:
                            import plotly.express as px
                            st.markdown(\'<div style="font-size:0.78rem;font-weight:700;color:#FBB724;text-transform:uppercase;letter-spacing:0.08em;margin:0.6rem 0 0.3rem;">&#128200; Auto Chart</div>\', unsafe_allow_html=True)
                            _fig = px.bar(_df.head(10), x=_cat[0], y=_num[0], color_discrete_sequence=["#FBB724"])
                            _fig.update_layout(
                                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                font=dict(color="#94A3B8",size=10), height=220,
                                margin=dict(t=5,b=5,l=5,r=5),
                                xaxis=dict(showgrid=False,color="#475569"),
                                yaxis=dict(showgrid=True,gridcolor="rgba(255,255,255,0.05)",color="#475569"))
                            st.plotly_chart(_fig, use_container_width=True)
        st.session_state.submit = False

    # ── Feature Cards ─────────────────────────────────────────────────────────
    st.markdown("""
    <div style="display:flex;align-items:center;gap:10px;margin:2rem 0 1rem;">
        <span style="font-size:1.1rem;font-weight:700;color:#F1F5F9;">Everything you need</span>
        <span style="background:rgba(251,183,36,0.1);color:#FBB724;font-size:0.7rem;
            font-weight:700;padding:0.15rem 0.6rem;border-radius:20px;text-transform:uppercase;">Features</span>
    </div>
    """, unsafe_allow_html=True)
    _features = [
        ("&#128172;","Natural Language","Ask in plain English — no SQL knowledge required."),
        ("&#9889;","Instant Results","GPT-4 powered SQL generation in seconds."),
        ("&#128269;","Schema-Aware","RAG-based context for accurate queries."),
        ("&#128220;","Query History","Every query saved with timestamps."),
        ("&#11015;","Export Results","Download CSV or Excel with one click."),
        ("&#128202;","Visualizations","Auto-charts generated from your results."),
        ("&#128190;","Saved Queries","Bookmark queries for instant reuse."),
        ("&#129504;","AI Suggestions","Smart recommendations from your schema."),
    ]
    _rows = [_features[i:i+4] for i in range(0,len(_features),4)]
    for _row in _rows:
        _cols = st.columns(len(_row))
        for _col,(_icon,_title,_desc) in zip(_cols,_row):
            with _col:
                st.markdown(f"""<div class="feature-card">
                    <div class="feature-icon">{_icon}</div>
                    <div class="feature-title">{_title}</div>
                    <div class="feature-desc">{_desc}</div>
                </div>""", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

'''

new_content = content[:start_idx] + new_home + content[end_idx:]
open("app.py", "w", encoding="utf-8").write(new_content)
print("Done - robot image removed")

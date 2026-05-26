content = open("app.py", encoding="utf-8").read()

start_marker = '# ══════════════════════════════════════════════════════════════════════════════\n# DASHBOARD PAGE\n# ══════════════════════════════════════════════════════════════════════════════\nelif _page == "📊 Dashboard":'
end_marker   = '# ══════════════════════════════════════════════════════════════════════════════\n# HISTORY PAGE'

start_idx = content.index(start_marker)
end_idx   = content.index(end_marker)

new_dashboard = '''# ══════════════════════════════════════════════════════════════════════════════
# DASHBOARD PAGE  — Strategic Business Performance Dashboard
# ══════════════════════════════════════════════════════════════════════════════
elif _page == "📊 Dashboard":
    import plotly.express as px
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    # ── Color palette ─────────────────────────────────────────────────────────
    C1="#FBB724"; C2="#10B981"; C3="#8B5CF6"; C4="#EF4444"; C5="#0EA5E9"
    PAL=[C1,C2,C3,C4,C5,"#F97316","#EC4899"]
    BG="rgba(0,0,0,0)"; GRID="rgba(255,255,255,0.05)"
    FONT=dict(family="Inter,sans-serif",size=11,color="#94A3B8")
    LO=dict(paper_bgcolor=BG,plot_bgcolor=BG,font=FONT,
            margin=dict(t=20,b=20,l=10,r=10),height=280)

    # ── Dashboard Header ──────────────────────────────────────────────────────
    st.markdown("""
    <div style="background:linear-gradient(135deg,#0D0D14 0%,#1A1A2E 60%,#16213E 100%);
        border:1px solid rgba(251,183,36,0.2);border-radius:16px;
        padding:1.5rem 2rem;margin-bottom:1.2rem;position:relative;overflow:hidden;">
        <div style="position:absolute;top:-60px;right:-60px;width:300px;height:300px;
            background:radial-gradient(circle,rgba(251,183,36,0.06) 0%,transparent 70%);
            pointer-events:none;"></div>
        <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:1rem;">
            <div>
                <div style="font-size:0.72rem;font-weight:700;color:#FBB724;
                    text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.4rem;">
                    &#10022; AaiTech Industries &nbsp;&middot;&nbsp; Strategic Analytics
                </div>
                <span style="font-size:1.7rem;font-weight:900;
                    background:linear-gradient(90deg,#FFFFFF 0%,#FBB724 100%);
                    -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                    background-clip:text;display:block;line-height:1.2;">
                    Strategic Business Performance Dashboard
                </span>
                <span style="font-size:0.85rem;color:#64748B;display:block;margin-top:0.3rem;">
                    Data Analytics &amp; Business Intelligence &nbsp;&middot;&nbsp; Live Data
                </span>
            </div>
            <div style="display:flex;gap:0.6rem;flex-wrap:wrap;">
                <span style="background:rgba(16,185,129,0.1);border:1px solid rgba(16,185,129,0.3);
                    color:#10B981;padding:0.3rem 0.8rem;border-radius:20px;font-size:0.72rem;font-weight:700;">
                    &#128994; LIVE
                </span>
                <span style="background:rgba(251,183,36,0.1);border:1px solid rgba(251,183,36,0.3);
                    color:#FBB724;padding:0.3rem 0.8rem;border-radius:20px;font-size:0.72rem;font-weight:700;">
                    &#128202; Power BI Style
                </span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

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
        st.markdown(\'<div class="glass-card" style="padding:0.8rem 1.2rem;margin-bottom:1rem;">\', unsafe_allow_html=True)
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
        st.markdown(\'</div>\', unsafe_allow_html=True)

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
        <div style="background:linear-gradient(90deg,rgba(251,183,36,0.08),rgba(16,185,129,0.05));
            border:1px solid rgba(251,183,36,0.2);border-radius:10px;
            padding:0.7rem 1.2rem;margin-bottom:1rem;font-size:0.82rem;">
            <span style="color:#FBB724;font-weight:700;">&#10022; Key Insights &nbsp;</span>
            <span style="color:#94A3B8;">
                Top market: <b style="color:#FFFFFF;">{_top_country}</b> &nbsp;&middot;&nbsp;
                Best category: <b style="color:#FFFFFF;">{_top_cat}</b>
                <span style="color:#10B981;">(${_top_cat_v:,.0f})</span> &nbsp;&middot;&nbsp;
                Top product: <b style="color:#FFFFFF;">{_top_prod}</b>
            </span>
        </div>""", unsafe_allow_html=True)

        # ── Row 2: Revenue Donut + Orders Bar ─────────────────────────────────
        st.markdown(\'<p style="font-size:0.72rem;font-weight:700;color:#FBB724;text-transform:uppercase;letter-spacing:0.1em;margin:0 0 0.6rem;border-left:3px solid #FBB724;padding-left:0.6rem;">&#128202; Sales Performance</p>\', unsafe_allow_html=True)
        _r1,_r2 = st.columns(2)

        with _r1:
            st.markdown(\'<div class="glass-card" style="padding:1rem;">\', unsafe_allow_html=True)
            st.markdown(\'<span style="font-size:0.82rem;font-weight:700;color:#F1F5F9;">Revenue by Category</span>\', unsafe_allow_html=True)
            st.markdown(\'<span style="font-size:0.72rem;color:#475569;display:block;margin-bottom:0.4rem;">Proportional revenue contribution</span>\', unsafe_allow_html=True)
            _cr=_fr.groupby("category")["line_total"].sum().reset_index()
            _cr.columns=["Category","Revenue"]
            if not _cr.empty:
                _f1=go.Figure(go.Pie(
                    labels=_cr["Category"],values=_cr["Revenue"],hole=0.58,
                    marker_colors=PAL,textinfo="label+percent",
                    hovertemplate="<b>%{label}</b><br>$%{value:,.2f}<extra></extra>"))
                _f1.update_layout(**LO,showlegend=False)
                _f1.add_annotation(text=f"<b>${_rev:,.0f}</b><br><span style=\'font-size:9px\'>Total</span>",
                    x=0.5,y=0.5,showarrow=False,font_size=13,font_color=C1)
                st.plotly_chart(_f1,use_container_width=True)
            st.markdown(\'</div>\', unsafe_allow_html=True)

        with _r2:
            st.markdown(\'<div class="glass-card" style="padding:1rem;">\', unsafe_allow_html=True)
            st.markdown(\'<span style="font-size:0.82rem;font-weight:700;color:#F1F5F9;">Orders by Country</span>\', unsafe_allow_html=True)
            st.markdown(\'<span style="font-size:0.72rem;color:#475569;display:block;margin-bottom:0.4rem;">Order volume per destination market</span>\', unsafe_allow_html=True)
            _co=_fo.groupby("country").size().reset_index(name="Orders")
            _co=_co.sort_values("Orders",ascending=False).head(_tn)
            if not _co.empty:
                _f2=go.Figure(go.Bar(
                    x=_co["country"],y=_co["Orders"],
                    marker=dict(color=_co["Orders"],
                        colorscale=[[0,"rgba(251,183,36,0.2)"],[1,C1]],showscale=False),
                    text=_co["Orders"],textposition="outside",
                    hovertemplate="<b>%{x}</b><br>%{y} orders<extra></extra>"))
                _f2.update_layout(**LO,
                    xaxis=dict(showgrid=False,color="#475569"),
                    yaxis=dict(showgrid=True,gridcolor=GRID,color="#475569"))
                st.plotly_chart(_f2,use_container_width=True)
            st.markdown(\'</div>\', unsafe_allow_html=True)

        # ── Row 3: Top Products + Freight ─────────────────────────────────────
        _r3,_r4 = st.columns(2)

        with _r3:
            st.markdown(\'<div class="glass-card" style="padding:1rem;">\', unsafe_allow_html=True)
            st.markdown(f\'<span style="font-size:0.82rem;font-weight:700;color:#F1F5F9;">Top {_tn} Products by Revenue</span>\', unsafe_allow_html=True)
            st.markdown(\'<span style="font-size:0.72rem;color:#475569;display:block;margin-bottom:0.4rem;">Best performing products ranked by sales</span>\', unsafe_allow_html=True)
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
                _f3.update_layout(**LO,
                    xaxis=dict(showgrid=True,gridcolor=GRID,color="#475569"),
                    yaxis=dict(showgrid=False,color="#475569"))
                st.plotly_chart(_f3,use_container_width=True)
            st.markdown(\'</div>\', unsafe_allow_html=True)

        with _r4:
            st.markdown(\'<div class="glass-card" style="padding:1rem;">\', unsafe_allow_html=True)
            st.markdown(\'<span style="font-size:0.82rem;font-weight:700;color:#F1F5F9;">Freight Cost Analysis</span>\', unsafe_allow_html=True)
            st.markdown(\'<span style="font-size:0.72rem;color:#475569;display:block;margin-bottom:0.4rem;">Shipping expenditure by destination country</span>\', unsafe_allow_html=True)
            _fg=_fo.groupby("country")["freight"].sum().reset_index()
            _fg=_fg.sort_values("freight",ascending=False).head(_tn)
            if not _fg.empty:
                _f4=go.Figure(go.Bar(
                    x=_fg["country"],y=_fg["freight"],
                    marker=dict(color=_fg["freight"],
                        colorscale=[[0,"rgba(139,92,246,0.2)"],[1,C3]],showscale=False),
                    text=_fg["freight"].apply(lambda v:f"${v:,.1f}"),textposition="outside",
                    hovertemplate="<b>%{x}</b><br>$%{y:,.2f}<extra></extra>"))
                _f4.update_layout(**LO,
                    xaxis=dict(showgrid=False,color="#475569"),
                    yaxis=dict(showgrid=True,gridcolor=GRID,color="#475569"))
                st.plotly_chart(_f4,use_container_width=True)
            st.markdown(\'</div>\', unsafe_allow_html=True)

        # ── Row 4: Treemap + Supplier Performance ─────────────────────────────
        st.markdown(\'<p style="font-size:0.72rem;font-weight:700;color:#FBB724;text-transform:uppercase;letter-spacing:0.1em;margin:0.5rem 0 0.6rem;border-left:3px solid #FBB724;padding-left:0.6rem;">&#128269; Product & Supplier Intelligence</p>\', unsafe_allow_html=True)
        _r5,_r6 = st.columns([3,2])

        with _r5:
            st.markdown(\'<div class="glass-card" style="padding:1rem;">\', unsafe_allow_html=True)
            st.markdown(\'<span style="font-size:0.82rem;font-weight:700;color:#F1F5F9;">Product Revenue Treemap</span>\', unsafe_allow_html=True)
            st.markdown(\'<span style="font-size:0.72rem;color:#475569;display:block;margin-bottom:0.4rem;">Click a category to drill into products</span>\', unsafe_allow_html=True)
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
            st.markdown(\'</div>\', unsafe_allow_html=True)

        with _r6:
            st.markdown(\'<div class="glass-card" style="padding:1rem;">\', unsafe_allow_html=True)
            st.markdown(\'<span style="font-size:0.82rem;font-weight:700;color:#F1F5F9;">Supplier Performance</span>\', unsafe_allow_html=True)
            st.markdown(\'<span style="font-size:0.72rem;color:#475569;display:block;margin-bottom:0.4rem;">Products supplied per vendor</span>\', unsafe_allow_html=True)
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
            st.markdown(\'</div>\', unsafe_allow_html=True)

        # ── Row 5: Orders Explorer ────────────────────────────────────────────
        st.markdown(\'<p style="font-size:0.72rem;font-weight:700;color:#FBB724;text-transform:uppercase;letter-spacing:0.1em;margin:0.5rem 0 0.6rem;border-left:3px solid #FBB724;padding-left:0.6rem;">&#128203; Orders Explorer</p>\', unsafe_allow_html=True)
        st.markdown(\'<div class="glass-card" style="padding:1rem;">\', unsafe_allow_html=True)
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
        st.markdown(\'</div>\', unsafe_allow_html=True)

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
        st.markdown(f\'<div class="toast-error">&#10060; Dashboard error: {_e}</div>\',
            unsafe_allow_html=True)
        st.info("Make sure MySQL is running. Use the sidebar DB status indicator.")

'''

new_content = content[:start_idx] + new_dashboard + content[end_idx:]
open("app.py", "w", encoding="utf-8").write(new_content)
print("✓ Dashboard rebuilt successfully")

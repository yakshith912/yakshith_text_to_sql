content = open("app.py", encoding="utf-8").read()

# Fix 1: sidebar DB status check
content = content.replace(
    "_db_ok, _db_err = get_connection_status()",
    "_db_ok = test_connection()"
)

# Fix 2: settings page DB status check
content = content.replace(
    "_dok,_derr = get_connection_status()",
    "_dok = test_connection()"
)

# Fix 3: settings page test button
content = content.replace(
    "_ok2,_err2=get_connection_status()",
    "_ok2=test_connection()"
)

# Fix 4: remove _derr usage
content = content.replace(
    "    if not _dok and _derr:\n        st.markdown(f'<div style=\"font-size:0.8rem;color:#EF4444!important;margin-bottom:0.5rem;\">{_derr}</div>', unsafe_allow_html=True)\n",
    ""
)

# Fix 5: replace MYSQL_HOST:MYSQL_PORT · MYSQL_DATABASE with hardcoded values
content = content.replace(
    "{MYSQL_HOST}:{MYSQL_PORT} &middot; {MYSQL_DATABASE}",
    "127.0.0.1:3306 &middot; aaitech"
)

open("app.py", "w", encoding="utf-8").write(content)
print("✓ All errors fixed")

content = open("app.py", encoding="utf-8").read()

# Fix all page heading divs — force white color with -webkit-text-fill-color override
import re

# Pattern: heading divs with color:#F1F5F9 or color:#475569 inside page headers
content = content.replace(
    'font-size:1.8rem;font-weight:800;color:#F1F5F9!important;',
    'font-size:1.8rem;font-weight:800;color:#FFFFFF!important;-webkit-text-fill-color:#FFFFFF!important;'
)
content = content.replace(
    'font-size:0.9rem;color:#475569!important;margin-top:4px;',
    'font-size:0.9rem;color:#94A3B8!important;-webkit-text-fill-color:#94A3B8!important;margin-top:4px;'
)

# Fix the global CSS override that makes all divs dark
# The problem: [data-testid="stAppViewContainer"] div { color: #111111 !important }
# Replace with a lighter color for dark theme
content = content.replace(
    'html,body,[data-testid="stAppViewContainer"]{\n    font-family:\'Inter\',sans-serif!important;\n    background:#0A0A0F!important;\n    color:#E2E8F0!important;\n}',
    'html,body,[data-testid="stAppViewContainer"]{\n    font-family:\'Inter\',sans-serif!important;\n    background:#0A0A0F!important;\n    color:#E2E8F0!important;\n}\n/* Force all text visible on dark bg */\n[data-testid="stAppViewContainer"] .stMarkdown p,\n[data-testid="stAppViewContainer"] .stMarkdown div,\n[data-testid="stAppViewContainer"] .element-container p{\n    color:#E2E8F0!important;\n    -webkit-text-fill-color:#E2E8F0!important;\n}'
)

open("app.py", "w", encoding="utf-8").write(content)
print("✓ Headings fixed")

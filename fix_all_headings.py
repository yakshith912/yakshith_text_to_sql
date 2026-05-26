import re

content = open("app.py", encoding="utf-8").read()

# Fix all page headings that use the pattern:
# <div style="..."><div style="font-size:1.8rem;font-weight:800;color:#F1F5F9!important;">TITLE</div>
# Replace with span using gradient text (always visible)

# Pattern to find heading divs with color that might be invisible
old_heading = re.compile(
    r'<div style="font-size:1\.8rem;font-weight:800;color:#F1F5F9!important;">(.*?)</div>',
    re.DOTALL
)
def replace_heading(m):
    text = m.group(1).strip()
    return (
        f'<span style="font-size:1.8rem;font-weight:800;'
        f'background:linear-gradient(90deg,#FFFFFF,#FBB724);'
        f'-webkit-background-clip:text;-webkit-text-fill-color:transparent;'
        f'background-clip:text;display:block;line-height:1.2;margin-bottom:0.3rem;">'
        f'{text}</span>'
    )

content = old_heading.sub(replace_heading, content)

# Fix subtitle divs
old_sub = re.compile(
    r'<div style="font-size:0\.9rem;color:#475569!important;margin-top:4px;">(.*?)</div>',
    re.DOTALL
)
def replace_sub(m):
    text = m.group(1).strip()
    return f'<span style="font-size:0.9rem;color:#94A3B8;display:block;margin-bottom:1rem;">{text}</span>'

content = old_sub.sub(replace_sub, content)

open("app.py", "w", encoding="utf-8").write(content)
print("✓ All headings fixed")

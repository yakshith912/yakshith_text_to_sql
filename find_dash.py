content = open('app.py', encoding='utf-8').read()
idx = content.find('elif _page == "\U0001f4ca Dashboard"')
print(f"Dashboard page starts at line: {content[:idx].count(chr(10))+1}")
# Find the header section
h_idx = content.find('# Header with robot', idx)
print(f"Header section at line: {content[:h_idx].count(chr(10))+1}")
print(content[h_idx:h_idx+600])

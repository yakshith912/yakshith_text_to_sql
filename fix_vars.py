content = open('app.py', encoding='utf-8').read()

# Fix variable references in chart code
content = content.replace('colorscale=[[0,"#FEF9C3"],[1,C_AMBER]]',
                           'colorscale=[[0,"#FEF9C3"],[1,C_AMBER]]')
content = content.replace('colorscale=[[0,"#FEF9C3"],[1,C_GOLD]]',
                           'colorscale=[[0,"#FEF9C3"],[1,C_GOLD]]')
content = content.replace('[[0,"#FEF9C3"],[0.5,C_AMBER],[1,"#78350F"]]',
                           '[[0,"#FEF9C3"],[0.5,C_AMBER],[1,C_DARK]]')
content = content.replace('colorscale=[[0,"#fde68a"],[1,C_AMBER]]',
                           'colorscale=[[0,"#FEF9C3"],[1,C_AMBER]]')
content = content.replace('marker_color=C_GOLD', 'marker_color=C_GOLD')

# Fix orders bar chart color scale reference
content = content.replace('[[0,"#bfdbfe"],[1,C_BLUE]]', '[[0,"#FEF9C3"],[1,C_AMBER]]')
content = content.replace('[[0,"#99f6e4"],[1,C_TEAL]]', '[[0,"#FEF9C3"],[1,C_GOLD]]')

# Remove any leftover C_BLUE / C_TEAL references
content = content.replace('C_BLUE', 'C_AMBER')
content = content.replace('C_TEAL', 'C_GOLD')

open('app.py', 'w', encoding='utf-8').write(content)
print("Done - variable names fixed")

import re

fp = r'c:\Users\natarani\job-hunt-app\index.html'

with open(fp, 'r', encoding='utf-8') as f:
    text = f.read()

print(f"Before: {len(text)} chars, {text.count(chr(10))} lines")

# 1. Remove double-spacing: collapse consecutive blank lines
# The file has \r\n line endings with every other line blank
text = text.replace('\r\n\r\n', '\r\n')

# 2. Replace ??? remnants (garbled emojis that became question marks)
# In context: these appear where emojis used to be
text = text.replace('???', '')

# 3. Fix tab-icon spans that are now empty
text = re.sub(r'<span class="tab-icon">\s*</span>', '', text)

# 4. Clean up leading/trailing spaces in tags
text = re.sub(r'>\s+([A-Z])', r'>\1', text)  # "> Job" -> ">Job" only at tag boundary

# 5. Fix specific text that lost separators
text = text.replace('Since_9five95 AI Career Intelligence Powered by GROQ',
                     'Since_9five95 | AI Career Intelligence | Powered by GROQ')
text = text.replace('Amretha AI Career Intelligence',
                     'Amretha | AI Career Intelligence')

# 6. Fix streak badge text
text = text.replace(' 0 day streak', '0 day streak')

# 7. Fix Daily Goal label
text = text.replace('<div class="goal-label"> Daily Goal:</div>',
                     '<div class="goal-label">Daily Goal:</div>')

# 8. Clean any remaining double spaces  
text = re.sub(r'  +', ' ', text)

# Count final state
lines = text.count('\n')
remaining_q = text.count('???')
print(f"After: {len(text)} chars, {lines} lines, remaining ???: {remaining_q}")

# Show important sections
for label, search in [('Title', '<title>'), ('Header', 'header-title'), 
                       ('Tabs', 'tab-nav'), ('Streak', 'streakBadge')]:
    idx = text.find(search)
    if idx > 0:
        snippet = text[idx:idx+100].replace('\r','').replace('\n',' ')
        print(f"{label}: {snippet}")

with open(fp, 'w', encoding='utf-8') as f:
    f.write(text)

print("Done!")

import re

with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Extract the bulk-mode async IIFE by looking for the pattern
# The bookmarklet builds a JS string via concatenation of single-quoted strings
# Find all string fragments between copyBookmarklet and copyBookmarkletToClipboard
s = c.find('function copyBookmarklet()')
e = c.find('function copyBookmarkletToClipboard()')
block = c[s:e]

# Extract all single-quoted string literals and concatenate them
# Pattern: 'content' + (optionally with // comments between)
fragments = re.findall(r"'([^']*)'", block)
js_code = ''.join(fragments)

print(f"Extracted JS code length: {len(js_code)}")
print(f"Starts with: {js_code[:100]}")
print(f"Ends with: {js_code[-100:]}")

# Check brace balance
opens = js_code.count('{')
closes = js_code.count('}')
print(f"Open braces: {opens}, Close braces: {closes}, balanced: {opens == closes}")

# Check paren balance
po = js_code.count('(')
pc = js_code.count(')')
print(f"Open parens: {po}, Close parens: {pc}, balanced: {po == pc}")

# Check for the key structures
print(f"\nHas async IIFE: {'(async function()' in js_code}")
print(f"Has IIFE close: {'})()' in js_code}")
print(f"Has fetch call: {'fetch(' in js_code}")
print(f"Has Voyager API: {'voyager/api' in js_code}")
print(f"Has allJobs: {'allJobs' in js_code}")
print(f"Has scrapeCards: {'scrapeCards' in js_code}")

# Check if the URL condition is right
print(f"\nURL check: {'my-items' in js_code}")
print(f"URL check2: {'linkedin.com' in js_code}")

# Look for common JS errors - missing semicolons after var declarations
if 'var ' in js_code:
    # Find all var declarations
    var_decls = [(m.start(), m.group()) for m in re.finditer(r'var \w+=', js_code)]
    print(f"\nVar declarations found: {len(var_decls)}")

# Check for the saved jobs GraphQL query
print(f"\nGraphQL query: {'voyagerJobsDashSavedJobPostingsByMember' in js_code}")

# Write out the full JS for manual inspection
with open('_bookmarklet_debug.js', 'w', encoding='utf-8') as f:
    f.write(js_code)
print("\nFull JS written to _bookmarklet_debug.js")

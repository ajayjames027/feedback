import re
import sys

filepath = "C:/Users/ajayj/Downloads/feedback/index.html"
with open(filepath, "r", encoding="utf-8") as f:
    html = f.read()

# Replace the form tag
form_regex = re.compile(r'<form\s+id="facultyForm"\s+onsubmit="submitFacultyFeedback\(event\)"\s*>')
if form_regex.search(html):
    html = form_regex.sub(r'<form id="facultyForm" onsubmit="submitFacultyFeedback(event)" novalidate>', html)
    print("Replaced successfully")
else:
    print("WARNING: Could not find form tag!")
    sys.exit(1)

with open(filepath, "w", encoding="utf-8") as f:
    f.write(html)

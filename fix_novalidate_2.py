import re

with open('C:/Users/ajayj/Downloads/feedback/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace <form ...> with <form ... novalidate>
html = re.sub(r'<form id="facultyForm" onsubmit="submitFacultyFeedback\(event\)"([^>]*)>', r'<form id="facultyForm" onsubmit="submitFacultyFeedback(event)"\1 novalidate>', html)

with open('C:/Users/ajayj/Downloads/feedback/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("novalidate added successfully.")

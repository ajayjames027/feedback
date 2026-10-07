import re

filepath = "C:/Users/ajayj/Downloads/feedback/admin.html"
with open(filepath, "r", encoding="utf-8") as f:
    html = f.read()

# Remove the call to seedSampleBenchmarkData
html = re.sub(r'// Seed sample benchmark responses if empty[\s\S]*?seedSampleBenchmarkData\(false\);\n\s*\}', '', html)

# Remove the button for adding sample data
html = re.sub(r'<button onclick="seedSampleBenchmarkData\(\)"[^>]*>[\s\S]*?</button>', '', html)

# Remove the function seedSampleBenchmarkData completely
html = re.sub(r'function seedSampleBenchmarkData\((?:.*?)\)\s*\{[\s\S]*?\}\n\n', '', html)

# Make sure window.loadFirebaseResponses does NOT append anything incorrectly
# It does localStorage.setItem("sjc_faculty_feedback_records_2025", JSON.stringify(firebaseRecords)); which is fine.

with open(filepath, "w", encoding="utf-8") as f:
    f.write(html)
print("Dummy data seeding logic removed!")

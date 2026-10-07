import re

filepath = "C:/Users/ajayj/Downloads/feedback/index.html"
with open(filepath, "r", encoding="utf-8") as f:
    html = f.read()

# Replace the submission block
old_block_regex = re.compile(r'// Also attempt backend submit if server is running\s*fetch\([\s\S]*?\}\)\.catch\(\(\) => \{\}\);')

new_firestore = """            // Submit directly to Firebase Firestore
            if (window.db) {
                window.addDoc(window.collection(window.db, "responses"), payload)
                    .then(() => { console.log('Successfully saved to Firestore'); })
                    .catch(e => { console.error('Error saving to Firestore:', e); });
            }"""

if old_block_regex.search(html):
    html = old_block_regex.sub(new_firestore, html)
else:
    print("WARNING: Could not find fetch logic to replace!")

with open(filepath, "w", encoding="utf-8") as f:
    f.write(html)
print("Submit button logic successfully patched.")

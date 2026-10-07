import re

filepath = "C:/Users/ajayj/Downloads/feedback/index.html"
with open(filepath, "r", encoding="utf-8") as f:
    html = f.read()

# I will replace the showModalError function to ALSO do an alert to ensure they see it if the modal is broken.
modal_err = """        function showModalError(msg) {
            alert("Validation Error: " + msg);
            document.getElementById('errorMessage').innerText = msg;
            document.getElementById('errorModal').classList.remove('hidden');
        }"""
html = re.sub(r'function showModalError\(msg\) \{[\s\S]*?\}', modal_err, html)

# Let's also wrap the firebase fetch to surface errors
old_firebase = """            if (window.db) {
                window.addDoc(window.collection(window.db, "responses"), payload)
                    .then(() => { 
                        console.log('Successfully saved to Firestore'); 
                        document.getElementById('mainContainer').classList.add('hidden');
                        document.getElementById('successView').classList.remove('hidden');
                        window.scrollTo({ top: 0, behavior: 'smooth' });
                    })
                    .catch(e => { console.error('Error saving to Firestore:', e); });
            }"""

new_firebase = """            if (window.db) {
                window.addDoc(window.collection(window.db, "responses"), payload)
                    .then(() => { 
                        console.log('Successfully saved to Firestore'); 
                        document.getElementById('mainContainer').classList.add('hidden');
                        document.getElementById('successView').classList.remove('hidden');
                        window.scrollTo({ top: 0, behavior: 'smooth' });
                    })
                    .catch(e => { 
                        console.error('Error saving to Firestore:', e); 
                        alert("Firebase Save Error: " + e.message);
                    });
            } else {
                alert("Firebase not initialized! The module script hasn't loaded yet.");
            }"""

html = html.replace(old_firebase, new_firebase)

with open(filepath, "w", encoding="utf-8") as f:
    f.write(html)
print("Debug patches injected to index.html")

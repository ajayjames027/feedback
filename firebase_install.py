import re

firebase_setup = """
<!-- Firebase App (the core Firebase SDK) -->
<script type="module">
    import { initializeApp } from "https://www.gstatic.com/firebasejs/10.9.0/firebase-app.js";
    import { getFirestore, collection, addDoc } from "https://www.gstatic.com/firebasejs/10.9.0/firebase-firestore.js";

    const firebaseConfig = {
        apiKey: "AIzaSyC7FuA4XE3DYQevwoaSd7_G0G0Z7UPi2ms",
        authDomain: "feedback-4cb66.firebaseapp.com",
        projectId: "feedback-4cb66",
        storageBucket: "feedback-4cb66.firebasestorage.app",
        messagingSenderId: "1071690168576",
        appId: "1:1071690168576:web:fd0d2163495e3b928a5be5"
    };

    const app = initializeApp(firebaseConfig);
    const db = getFirestore(app);
    window.db = db;
    window.addDoc = addDoc;
    window.collection = collection;
</script>
"""

# Modify index.html
with open('C:/Users/ajayj/Downloads/feedback/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add Firebase SDKs before the existing <script> tags
script_idx = html.find('<!-- FontAwesome')
html = html[:script_idx] + firebase_setup + html[script_idx:]

# Replace the specific fetch placeholder with real Firebase logic
old_fetch = """            // Ensure payload gets posted
            fetch('http://127.0.0.1:5000/api/submit', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            }).then(resp => {
                console.log("Submitted!", resp);
            }).catch(err => {
                console.error("Submit error (ignored in front-end)", err);
            });"""

new_firestore = """            // Submit directly to Firebase Firestore
            if (window.db) {
                window.addDoc(window.collection(window.db, "responses"), payload)
                    .then(() => { console.log('Successfully saved to Firestore'); })
                    .catch(e => { console.error('Error saving to Firestore:', e); });
            }"""

html = html.replace(old_fetch, new_firestore)

with open('C:/Users/ajayj/Downloads/feedback/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
    
print("Updated index.html with Firebase SDK!")

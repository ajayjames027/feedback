import re

firebase_setup = """
<!-- Firebase App (the core Firebase SDK) -->
<script type="module">
    import { initializeApp } from "https://www.gstatic.com/firebasejs/10.9.0/firebase-app.js";
    import { getFirestore, collection, getDocs } from "https://www.gstatic.com/firebasejs/10.9.0/firebase-firestore.js";

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
    
    // Load responses from Firestore globally so the rest of the script can use them
    window.db = db;
    window.loadFirebaseResponses = async function() {
        const querySnapshot = await getDocs(collection(db, "responses"));
        let firebaseRecords = [];
        querySnapshot.forEach((doc) => {
            firebaseRecords.push(doc.data());
        });
        
        // Cache them into localStorage for the legacy functions to pick up for now
        // This makes sure the rest of admin.html works instantly without rewriting every function
        localStorage.setItem("sjc_faculty_feedback_records_2025", JSON.stringify(firebaseRecords));
        console.log("Firebase synced!", firebaseRecords.length, "records pulled.");
        
        // Trigger a re-render
        if(typeof renderRosterTable === 'function') renderRosterTable();
        if(typeof renderAnalyticsDashboard === 'function') renderAnalyticsDashboard();
        if(typeof renderResponsesTable === 'function') renderResponsesTable();
    };
    
    // Trigger sync on load
    window.loadFirebaseResponses();
</script>
"""

with open('C:/Users/ajayj/Downloads/feedback/admin.html', 'r', encoding='utf-8') as f:
    html = f.read()

script_idx = html.find('<!-- Chart.js -->')
if script_idx != -1:
    html = html[:script_idx] + firebase_setup + html[script_idx:]

with open('C:/Users/ajayj/Downloads/feedback/admin.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated admin.html with Firebase read logic")


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

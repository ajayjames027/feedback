import pandas as pd
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "feedback.db")
EXCEL_PATH = os.path.join(os.path.dirname(__file__), "Faculty_2026_2027.xlsx")

def sync_roster_to_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create faculty roster table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS faculty_roster (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        s_no INTEGER,
        department TEXT NOT NULL,
        category TEXT, -- Aided / Coordinator / Secretary
        shift TEXT,    -- Shift I / Shift II
        gender TEXT,
        name TEXT NOT NULL,
        designation TEXT,
        date_of_appointment TEXT,
        email TEXT UNIQUE,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)
    
    # Read Excel
    df = pd.read_excel(EXCEL_PATH, skiprows=2)
    df.columns = [str(c).strip() for c in df.columns]
    df = df.dropna(subset=['Name of the Teaching Staff'])
    
    inserted = 0
    updated = 0
    for _, row in df.iterrows():
        s_no = int(row.get('S.No')) if pd.notna(row.get('S.No')) else None
        dept = str(row.get('Department', '')).strip()
        cat = str(row.get('Aided/Coordinator/Secretary', '')).strip() if pd.notna(row.get('Aided/Coordinator/Secretary')) else ''
        shift = str(row.get('Shift (I/II)', '')).strip() if pd.notna(row.get('Shift (I/II)')) else ''
        gender = str(row.get('Gender', '')).strip() if pd.notna(row.get('Gender')) else ''
        name = str(row.get('Name of the Teaching Staff', '')).strip()
        desig = str(row.get('Designation', '')).strip() if pd.notna(row.get('Designation')) else ''
        doa = str(row.get('Date of Appointment', ''))[:10] if pd.notna(row.get('Date of Appointment')) else ''
        email = str(row.get('Institutional Email Address', '')).strip().lower() if pd.notna(row.get('Institutional Email Address')) else ''
        
        # Insert or replace
        cursor.execute("""
        INSERT INTO faculty_roster (s_no, department, category, shift, gender, name, designation, date_of_appointment, email)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(email) DO UPDATE SET
            department = excluded.department,
            category = excluded.category,
            shift = excluded.shift,
            gender = excluded.gender,
            name = excluded.name,
            designation = excluded.designation,
            date_of_appointment = excluded.date_of_appointment
        """, (s_no, dept, cat, shift, gender, name, desig, doa, email))
        inserted += 1
        
    conn.commit()
    
    count = cursor.execute("SELECT COUNT(*) FROM faculty_roster").fetchone()[0]
    print(f"Total faculty members in database roster: {count}")
    conn.close()

if __name__ == "__main__":
    sync_roster_to_db()

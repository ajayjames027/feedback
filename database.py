import sqlite3
import json
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "feedback.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Faculty Roster Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS faculty_roster (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        s_no INTEGER,
        department TEXT NOT NULL,
        category TEXT,
        shift TEXT,
        gender TEXT,
        name TEXT NOT NULL,
        designation TEXT,
        date_of_appointment TEXT,
        email TEXT UNIQUE,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Responses Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS responses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        department TEXT NOT NULL,
        faculty_name TEXT NOT NULL,
        faculty_email TEXT,
        course_level TEXT NOT NULL,
        
        -- Section 2: Overall Effectiveness (JSON object)
        overall_effectiveness TEXT,
        
        -- Section 3: OBE Evaluation (JSON object)
        obe_evaluation TEXT,
        
        -- Section 4: Curriculum Structure (JSON object)
        curriculum_structure TEXT,
        overlapping_courses TEXT,
        overlapping_details TEXT,
        
        -- Section 5: NEP Components
        multidisciplinary_rating INTEGER,
        flexible_learning_paths TEXT, -- JSON array
        electives_rating TEXT,
        experiential_learning TEXT, -- JSON object
        digital_learning TEXT, -- JSON object
        research_orientation TEXT, -- JSON array
        nep_challenges TEXT,
        
        -- Section 6: Emerging Trends
        emerging_areas TEXT, -- JSON array
        emerging_other TEXT,
        
        -- Section 7: NSQF Alignment
        nsqf_alignment TEXT,
        nsqf_courses TEXT,
        
        -- Section 8: Stakeholder Expectations
        stakeholder_sources TEXT, -- JSON array
        stakeholder_needs TEXT, -- JSON object
        
        -- Section 9: Indian Knowledge Systems (IKS)
        iks_effectiveness INTEGER,
        iks_integration_modes TEXT, -- JSON array
        iks_other TEXT,
        
        -- Section 10: Open-ended Suggestions
        courses_to_revise TEXT,
        other_recommendations TEXT
    );
    """)
    conn.commit()
    conn.close()

def save_response(data):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    INSERT INTO responses (
        department, faculty_name, faculty_email, course_level,
        overall_effectiveness, obe_evaluation,
        curriculum_structure, overlapping_courses, overlapping_details,
        multidisciplinary_rating, flexible_learning_paths, electives_rating,
        experiential_learning, digital_learning, research_orientation, nep_challenges,
        emerging_areas, emerging_other,
        nsqf_alignment, nsqf_courses,
        stakeholder_sources, stakeholder_needs,
        iks_effectiveness, iks_integration_modes, iks_other,
        courses_to_revise, other_recommendations
    ) VALUES (
        ?, ?, ?, ?,
        ?, ?,
        ?, ?, ?,
        ?, ?, ?,
        ?, ?, ?, ?,
        ?, ?,
        ?, ?,
        ?, ?,
        ?, ?, ?,
        ?, ?
    )
    """, (
        data.get("department", "").strip(),
        data.get("faculty_name", "Anonymous").strip(),
        data.get("faculty_email", "").strip().lower(),
        data.get("course_level", "UG").strip(),
        json.dumps(data.get("overall_effectiveness", {})),
        json.dumps(data.get("obe_evaluation", {})),
        json.dumps(data.get("curriculum_structure", {})),
        data.get("overlapping_courses", "NO"),
        data.get("overlapping_details", ""),
        int(data.get("multidisciplinary_rating") or 3),
        json.dumps(data.get("flexible_learning_paths", [])),
        data.get("electives_rating", "Good"),
        json.dumps(data.get("experiential_learning", {})),
        json.dumps(data.get("digital_learning", {})),
        json.dumps(data.get("research_orientation", [])),
        data.get("nep_challenges", ""),
        json.dumps(data.get("emerging_areas", [])),
        data.get("emerging_other", ""),
        str(data.get("nsqf_alignment", "4")),
        data.get("nsqf_courses", ""),
        json.dumps(data.get("stakeholder_sources", [])),
        json.dumps(data.get("stakeholder_needs", {})),
        int(data.get("iks_effectiveness") or 3),
        json.dumps(data.get("iks_integration_modes", [])),
        data.get("iks_other", ""),
        data.get("courses_to_revise", ""),
        data.get("other_recommendations", "")
    ))
    response_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return response_id

def get_all_responses(department=None, course_level=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM responses WHERE 1=1"
    params = []
    if department and department != "All":
        query += " AND department = ?"
        params.append(department)
    if course_level and course_level != "All":
        query += " AND course_level = ?"
        params.append(course_level)
    query += " ORDER BY timestamp DESC"
    
    rows = cursor.execute(query, params).fetchall()
    results = []
    for row in rows:
        d = dict(row)
        for json_col in [
            "overall_effectiveness", "obe_evaluation", "curriculum_structure",
            "flexible_learning_paths", "experiential_learning", "digital_learning",
            "research_orientation", "emerging_areas", "stakeholder_sources",
            "stakeholder_needs", "iks_integration_modes"
        ]:
            if d.get(json_col):
                try:
                    d[json_col] = json.loads(d[json_col])
                except:
                    pass
        results.append(d)
    conn.close()
    return results

def get_response_by_id(response_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    row = cursor.execute("SELECT * FROM responses WHERE id = ?", (response_id,)).fetchone()
    conn.close()
    if not row:
        return None
    d = dict(row)
    for json_col in [
        "overall_effectiveness", "obe_evaluation", "curriculum_structure",
        "flexible_learning_paths", "experiential_learning", "digital_learning",
        "research_orientation", "emerging_areas", "stakeholder_sources",
        "stakeholder_needs", "iks_integration_modes"
    ]:
        if d.get(json_col):
            try:
                d[json_col] = json.loads(d[json_col])
            except:
                pass
    return d

def get_faculty_by_dept(department=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    if department and department != "All":
        rows = cursor.execute("SELECT * FROM faculty_roster WHERE department = ? ORDER BY name ASC", (department,)).fetchall()
    else:
        rows = cursor.execute("SELECT * FROM faculty_roster ORDER BY department ASC, name ASC").fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_roster_departments():
    conn = get_db_connection()
    cursor = conn.cursor()
    rows = cursor.execute("SELECT DISTINCT department FROM faculty_roster WHERE department != '' ORDER BY department ASC").fetchall()
    conn.close()
    return [r["department"] for r in rows]

def get_faculty_tracking(department=None, status=None, search=None, shift=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Query to join faculty_roster with latest response
    sql = """
    SELECT 
        f.id as faculty_id,
        f.s_no,
        f.department,
        f.category,
        f.shift,
        f.gender,
        f.name,
        f.designation,
        f.email,
        r.id as response_id,
        r.timestamp as submission_time,
        r.course_level,
        CASE WHEN r.id IS NOT NULL THEN 'SUBMITTED' ELSE 'PENDING' END as status
    FROM faculty_roster f
    LEFT JOIN responses r ON (
        (f.email != '' AND LOWER(f.email) = LOWER(r.faculty_email)) 
        OR (LOWER(TRIM(f.name)) = LOWER(TRIM(r.faculty_name)) AND LOWER(TRIM(f.department)) = LOWER(TRIM(r.department)))
    )
    WHERE 1=1
    """
    params = []
    
    if department and department != "All":
        sql += " AND f.department = ?"
        params.append(department)
        
    if shift and shift != "All":
        sql += " AND f.shift = ?"
        params.append(shift)
        
    if status == "SUBMITTED":
        sql += " AND r.id IS NOT NULL"
    elif status == "PENDING":
        sql += " AND r.id IS NULL"
        
    if search:
        search_param = f"%{search.strip().lower()}%"
        sql += " AND (LOWER(f.name) LIKE ? OR LOWER(f.department) LIKE ? OR LOWER(f.email) LIKE ?)"
        params.extend([search_param, search_param, search_param])
        
    sql += " ORDER BY f.department ASC, f.name ASC"
    
    rows = cursor.execute(sql, params).fetchall()
    roster_list = [dict(r) for r in rows]
    
    # Summary metrics
    total_faculty = cursor.execute("SELECT COUNT(*) FROM faculty_roster").fetchone()[0]
    submitted_count = cursor.execute("""
        SELECT COUNT(DISTINCT f.id) FROM faculty_roster f
        JOIN responses r ON (
            (f.email != '' AND LOWER(f.email) = LOWER(r.faculty_email)) 
            OR (LOWER(TRIM(f.name)) = LOWER(TRIM(r.faculty_name)) AND LOWER(TRIM(f.department)) = LOWER(TRIM(r.department)))
        )
    """).fetchone()[0]
    
    pending_count = total_faculty - submitted_count
    completion_rate = round((submitted_count / total_faculty * 100), 1) if total_faculty > 0 else 0.0
    
    # Department breakdown
    dept_summary_rows = cursor.execute("""
        SELECT 
            f.department,
            COUNT(DISTINCT f.id) as total_dept,
            COUNT(DISTINCT r.id) as submitted_dept
        FROM faculty_roster f
        LEFT JOIN responses r ON (
            (f.email != '' AND LOWER(f.email) = LOWER(r.faculty_email)) 
            OR (LOWER(TRIM(f.name)) = LOWER(TRIM(r.faculty_name)) AND LOWER(TRIM(f.department)) = LOWER(TRIM(r.department)))
        )
        GROUP BY f.department
        ORDER BY f.department ASC
    """).fetchall()
    
    dept_breakdown = []
    for row in dept_summary_rows:
        tot = row["total_dept"]
        sub = row["submitted_dept"]
        pnd = tot - sub
        rate = round((sub / tot * 100), 1) if tot > 0 else 0.0
        dept_breakdown.append({
            "department": row["department"],
            "total": tot,
            "submitted": sub,
            "pending": pnd,
            "rate": rate
        })
        
    conn.close()
    
    return {
        "faculty_list": roster_list,
        "total_faculty": total_faculty,
        "submitted_count": submitted_count,
        "pending_count": pending_count,
        "completion_rate": completion_rate,
        "dept_breakdown": dept_breakdown
    }

def clear_all_responses():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM responses")
    conn.commit()
    conn.close()

# Segregated Faculty Curricular Feedback & IQAC Tracking System (2025-26)

A fully segregated digital feedback and administrative audit platform created for **St. Joseph's College (Autonomous)** based on the official **TEACHER FEEDBACK ON CURRICULAR DESIGN AND DEVELOPMENT: 2025-26** form and the **`Faculty_2026_2027.xlsx`** master faculty roster (319 teaching staff across 33 academic departments).

---

## 🔒 1. Faculty View (`/` or `/feedback`)

**Faculty cannot see any reports, analytics, or other responses.**

- **Google Form Aesthetic & 100% Fidelity**:
  - Header: Identical styling and typography to Google Forms with the institutional header (`#af4c10` / `#5746e3`), description, and `* Indicates required question` notation.
  - All 10 sections from the original Google Form are implemented.
- **Dynamic Faculty Roster Selector**:
  - Faculty member selects their Department, and their Name is automatically populated from the 319 official faculty list with their designation and institutional email.
- **Strict Mandatory Validation**:
  - The form **blocks submission** until every single required question and matrix row is answered.
- **Confirmation Page (`/submitted`)**:
  - Clean "Your response has been recorded" screen without any analytic elements.

---

## 📊 2. Admin & IQAC Portal (`/admin`)

Dedicated administrative dashboard accessible by IQAC / CDC administrators:

### A. Faculty Submission Tracker (`/admin/tracking`)
- **Live KPIs**:
  - Total Faculty Roster: **319**
  - Total Submitted
  - Total Pending (Yet to Submit)
  - Institutional Turnout Rate (%)
- **Department-Wise Progress Bars**:
  - Visual completion status for all 33 departments.
- **Master Faculty Compliance Table**:
  - Search by faculty name, designation, or email.
  - Filter tabs: `All Faculty`, `Pending / Yet to Submit`, `Submitted`.
  - Filter by Department and Shift (Shift I / Shift II).
- **1-Click Reminder Tools**:
  - **Copy Pending Emails**: Copies all pending faculty emails to clipboard for circulars/reminders.
  - **Export Pending List**: Download CSV of all pending faculty.

### B. Live Curricular Analytics Dashboard (`/admin/dashboard`)
- Radar charts for OBE alignment (POs, PSOs, COs, Attainment data).
- Horizontal bar chart across 12 Curricular Effectiveness dimensions.
- Stacked adequacy chart for Curriculum Balance (Theory, Practicals, Projects, Electives, Skills).
- Emerging Technology & Future Skills Demand Ranking.
- Stakeholder satisfaction comparison.
- Department & Course Level filters (UG / PG / Both).

### C. Response Explorer (`/admin/responses`)
- Full response log table with individual record detail modal.
- Export all responses to CSV or JSON.

### D. Official IQAC Curricular Audit Report (`/admin/report`)
- Formal printable evaluation report formatted for NAAC Criterion I (Curricular Aspects).
- Statistical tables with Mean scores and % Attainment.
- Formal sign-off blocks.

---

## 🚀 URLs Summary

| Portal | URL | Description |
|---|---|---|
| **Faculty Feedback Form** | `http://127.0.0.1:5000/` or `/feedback` | For faculty to fill out form (no analytics visible) |
| **Faculty Success Page** | `http://127.0.0.1:5000/submitted` | Response recorded confirmation |
| **Admin Faculty Tracker** | `http://127.0.0.1:5000/admin` or `/admin/tracking` | Tracks submitted vs pending faculty |
| **Admin Analytics Dashboard** | `http://127.0.0.1:5000/admin/dashboard` | Visual charts, matrices, and KPIs |
| **Admin Response Explorer** | `http://127.0.0.1:5000/admin/responses` | View all individual submissions |
| **Admin IQAC Audit Report** | `http://127.0.0.1:5000/admin/report` | Official printable audit report |
| **Export Pending List CSV** | `http://127.0.0.1:5000/api/export/pending` | Download pending faculty list |
| **Export Full Responses CSV** | `http://127.0.0.1:5000/api/export/csv` | Download all raw responses |

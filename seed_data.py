import random
from database import init_db, save_response, get_faculty_by_dept, clear_all_responses
from sync_roster import sync_roster_to_db

EFFECTIVENESS_ITEMS = [
    "Academically relevant",
    "Meets current industry needs",
    "Creates employability opportunities",
    "Prepares students for higher education and competitive exams",
    "Encourages research practices",
    "Prepares entrepreneurs",
    "Incorporates Emerging Developments in the Discipline",
    "Provides adequate Practical, Hands-on Training and Industrial Exposure",
    "Promotes critical thinking, problem-solving and creativity",
    "Content is appropriately distributed across semesters",
    "Provides opportunities for interdisciplinary learning",
    "Text and Reference Books are included within the period of last 5 years"
]

OBE_ITEMS = [
    "Programme Outcomes are clearly defined",
    "PSOs reflect specialization and career expectations",
    "COs are measurable and appropriate to the course level",
    "COs are appropriately mapped to POs and PSOs",
    "Outcomes are clearly communicated to the students",
    "Teaching-learning methods are aligned with intended COs and cognitive levels",
    "Assessment methods effectively measure attainment of COs",
    "CO Attainment data are analyzed and used to improve course content, teaching and assessment"
]

STRUCT_ITEMS = [
    "Theory Courses",
    "Practical Courses",
    "Project, Internship and Research",
    "Discipline Specific / Open Electives",
    "Skill / Ability Enhancement Courses",
    "Credit distribution across components",
    "Balance between foundational, advanced and specialization courses",
    "Opportunities for inter and multi-disciplinary course combinations"
]

EXP_ITEMS = [
    "Internship", "Field Visit", "Case Study", "Problem-Based Learning",
    "Project-Based Learning", "Community Engagement", "Simulations", "Industry-mentored Projects"
]

DIGITAL_ITEMS = ["SWAYAM/NPTEL", "Through Institutional LMS", "Other MOOCs", "Virtual Labs", "Blended Learning"]

EMERGING_POOL = [
    'Artificial Intelligence and Generative AI',
    'Data Science and Big Data Analytics',
    'Cybersecurity and Digital Privacy',
    'Cloud Computing, Internet of Things and Smart Systems',
    'Automation and Robotics',
    'Sustainability and Green Technologies',
    'Entrepreneurship, Innovation and Start-up Skills',
    'Digital Ethics, Governance and Responsible Technology',
    'Climate Change'
]

STAKEHOLDER_SOURCES_POOL = [
    'Student', 'Alumni', 'Employer', 'Industry expert consultations', 'Board of Studies discussions'
]

STAKEHOLDERS = ["Students", "Alumni", "Employers", "Parents", "Industry Experts"]

IKS_MODES_POOL = [
    'Dedicated courses', 'Selected units in existing courses', 'Certificate Courses', 'Projects', 'Interdisciplinary activities'
]

SAMPLE_OVERLAPS = [
    "Sem 3 Database Systems unit 4 overlaps with Sem 4 Advanced DBMS unit 1.",
    "Web Tech unit 2 HTML/CSS basics repeated from 1st year foundational IT.",
    "Operations Research syllabus has redundant manual calculation units that can be replaced with Python/R solvers.",
    "Environmental Science unit on climate action overlaps with Sustainability Open Elective.",
    ""
]

SAMPLE_CHALLENGES = [
    "Credit framework mapping between MOOCs and institutional transcripts requires more streamlined administrative approvals.",
    "Time table constraints for multidisciplinary elective slots across different faculties.",
    "Industry mentorship bandwidth and standardizing rubric assessments for field internships.",
    "Laboratory infrastructure upgrades needed for cutting-edge simulations.",
    "Need more faculty training workshops on OBE direct and indirect attainment automation."
]

SAMPLE_REVISIONS = [
    "CS301 (Machine Learning, Sem 5): Introduce LLMs and Prompt Engineering in Unit 5.",
    "COM204 (Financial Accounting, Sem 3): Add hands-on ERP & Tally Prime GST compliance module.",
    "AI402 (Deep Learning, Sem 6): Replace outdated CNN architectures with Vision Transformers.",
    "ENG102 (Professional Communication, Sem 2): Increase technical documentation and presentation skills lab hours.",
    "BT305 (Immunology, Sem 4): Include CRISPR therapeutics and bioinformatics pipeline case studies."
]

def generate_sample_responses(count=50):
    init_db()
    sync_roster_to_db()
    
    # Get all faculty from database roster
    roster = get_faculty_by_dept()
    if not roster:
        return
        
    sample_pool = random.sample(roster, min(count, len(roster)))
    
    for f in sample_pool:
        dept = f["department"]
        faculty = f["name"]
        email = f.get("email", "")
        course_level = random.choice(["UG", "PG", "Both"])
        
        # Overall effectiveness: 1-5
        eff = {}
        for item in EFFECTIVENESS_ITEMS:
            score = random.choices(["3 - Moderately Effective", "4 - Effective", "5 - Highly Effective", "2 - Less Effective", "1 - Not Effective"], weights=[0.2, 0.45, 0.28, 0.05, 0.02])[0]
            eff[item] = score
            
        # OBE: 1-5
        obe = {}
        for item in OBE_ITEMS:
            obe[item] = random.choices([3, 4, 5, 2], weights=[0.25, 0.45, 0.25, 0.05])[0]
            
        # Struct: 1-4
        struct = {}
        for item in STRUCT_ITEMS:
            struct[item] = random.choices(["3 - Adequate", "4 - Highly Adequate", "2 - Needs Improvement", "1 - Inadequate", "N/A - Not Applicable"], weights=[0.45, 0.35, 0.15, 0.03, 0.02])[0]
            
        overlap = random.choices(["NO", "YES", "NOT SURE"], weights=[0.75, 0.15, 0.1])[0]
        overlap_text = random.choice(SAMPLE_OVERLAPS) if overlap == "YES" else ""
        
        multi_rating = random.choices([3, 4, 5, 2, 1], weights=[0.25, 0.4, 0.25, 0.08, 0.02])[0]
        
        flex_paths = random.sample(
            ['MEME', 'Academic Flexibility', 'Credit Transfer', 'Recognition of Credits earned through MOOCs'],
            k=random.randint(1, 4)
        )
        
        electives_rating = random.choices(['Very Good', 'Good', 'Adequate', 'Poor'], weights=[0.35, 0.45, 0.18, 0.02])[0]
        
        exp = {}
        for item in EXP_ITEMS:
            exp[item] = random.choices(["3 - High", "4 - Very High", "2 - Moderate", "1 - Low"], weights=[0.4, 0.35, 0.2, 0.05])[0]
            
        dig = {}
        for item in DIGITAL_ITEMS:
            dig[item] = random.choices(["3 - High", "4 - Very High", "2 - Moderate", "1 - Low"], weights=[0.38, 0.32, 0.22, 0.08])[0]
            
        research_opts = random.sample(
            ['Faculty-Mentored Projects', 'Research Methodology', 'Publications', 'Patent Awareness', 'Design Thinking'],
            k=random.randint(2, 4)
        )
        
        nep_challenge = random.choice(SAMPLE_CHALLENGES) if random.random() > 0.4 else ""
        
        emerging = random.sample(EMERGING_POOL, k=random.randint(2, 6))
        
        nsqf_align = random.choices(["4", "5", "3", "2", "N.A."], weights=[0.4, 0.3, 0.2, 0.05, 0.05])[0]
        nsqf_course = f"{dept} Applied Skill Certification" if random.random() > 0.5 else ""
        
        stakeholder_src = random.sample(STAKEHOLDER_SOURCES_POOL, k=random.randint(2, 5))
        
        stakeholder_needs = {}
        for s in STAKEHOLDERS:
            stakeholder_needs[s] = random.choices([3, 4, 5, 2], weights=[0.25, 0.45, 0.25, 0.05])[0]
            
        iks_eff = random.choices([3, 4, 5, 2, 1], weights=[0.3, 0.35, 0.2, 0.12, 0.03])[0]
        iks_modes = random.sample(IKS_MODES_POOL, k=random.randint(1, 3))
        
        revisions = random.choice(SAMPLE_REVISIONS) if random.random() > 0.35 else ""
        recs = f"Strengthen industrial guest lectures and provide budget for research database subscriptions in {dept}." if random.random() > 0.4 else ""
        
        data = {
            "department": dept,
            "faculty_name": faculty,
            "faculty_email": email,
            "course_level": course_level,
            "overall_effectiveness": eff,
            "obe_evaluation": obe,
            "curriculum_structure": struct,
            "overlapping_courses": overlap,
            "overlapping_details": overlap_text,
            "multidisciplinary_rating": multi_rating,
            "flexible_learning_paths": flex_paths,
            "electives_rating": electives_rating,
            "experiential_learning": exp,
            "digital_learning": dig,
            "research_orientation": research_opts,
            "nep_challenges": nep_challenge,
            "emerging_areas": emerging,
            "emerging_other": "",
            "nsqf_alignment": nsqf_align,
            "nsqf_courses": nsqf_course,
            "stakeholder_sources": stakeholder_src,
            "stakeholder_needs": stakeholder_needs,
            "iks_effectiveness": iks_eff,
            "iks_integration_modes": iks_modes,
            "iks_other": "",
            "courses_to_revise": revisions,
            "other_recommendations": recs
        }
        save_response(data)

if __name__ == "__main__":
    clear_all_responses()
    generate_sample_responses(60)
    print("Populated 60 sample faculty feedback records mapped to actual roster!")

import pandas as pd
import numpy as np
import json
from collections import Counter
from database import get_all_responses

def compute_analytics(department="All", course_level="All"):
    responses = get_all_responses(department=department, course_level=course_level)
    total_responses = len(responses)
    
    if total_responses == 0:
        return {
            "total_responses": 0,
            "department": department,
            "course_level": course_level,
            "has_data": False
        }

    df = pd.DataFrame(responses)
    
    # 1. Department Distribution
    dept_counts = df["department"].value_counts().to_dict()
    
    # 2. Course Level Distribution
    course_level_counts = df["course_level"].value_counts().to_dict()
    
    # 3. Overall Effectiveness Analytics (Scale 1 to 5)
    # Extract numeric values from strings like "5 - Highly Effective" or integers
    def parse_scale_value(val):
        if val is None or val == "" or str(val).upper() == "N/A":
            return np.nan
        val_str = str(val).strip()
        try:
            return float(val_str[0])
        except:
            return np.nan

    effectiveness_items = [
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
    
    effectiveness_scores = {item: [] for item in effectiveness_items}
    for resp in responses:
        eff = resp.get("overall_effectiveness") or {}
        for item in effectiveness_items:
            v = parse_scale_value(eff.get(item))
            if not np.isnan(v):
                effectiveness_scores[item].append(v)
                
    effectiveness_stats = {}
    total_eff_sum = 0
    total_eff_count = 0
    for item, vals in effectiveness_scores.items():
        avg = round(float(np.mean(vals)), 2) if vals else 0.0
        effectiveness_stats[item] = {
            "average": avg,
            "count": len(vals),
            "percentage": round((avg / 5.0) * 100, 1)
        }
        if vals:
            total_eff_sum += sum(vals)
            total_eff_count += len(vals)
            
    overall_eff_index = round((total_eff_sum / total_eff_count / 5.0) * 100, 1) if total_eff_count > 0 else 0.0
    overall_eff_avg = round(total_eff_sum / total_eff_count, 2) if total_eff_count > 0 else 0.0

    # 4. OBE Evaluation Analytics (Scale 1 to 5)
    obe_items = [
        "Programme Outcomes are clearly defined",
        "PSOs reflect specialization and career expectations",
        "COs are measurable and appropriate to the course level",
        "COs are appropriately mapped to POs and PSOs",
        "Outcomes are clearly communicated to the students",
        "Teaching-learning methods are aligned with intended COs and cognitive levels",
        "Assessment methods effectively measure attainment of COs",
        "CO Attainment data are analyzed and used to improve course content, teaching and assessment"
    ]
    
    obe_scores = {item: [] for item in obe_items}
    for resp in responses:
        obe = resp.get("obe_evaluation") or {}
        for item in obe_items:
            v = parse_scale_value(obe.get(item))
            if not np.isnan(v):
                obe_scores[item].append(v)
                
    obe_stats = {}
    obe_total_sum = 0
    obe_total_count = 0
    for item, vals in obe_scores.items():
        avg = round(float(np.mean(vals)), 2) if vals else 0.0
        obe_stats[item] = {
            "average": avg,
            "count": len(vals),
            "percentage": round((avg / 5.0) * 100, 1)
        }
        if vals:
            obe_total_sum += sum(vals)
            obe_total_count += len(vals)
            
    overall_obe_index = round((obe_total_sum / obe_total_count / 5.0) * 100, 1) if obe_total_count > 0 else 0.0

    # 5. Curriculum Structure & Balance Analytics (Scale 1 to 4)
    struct_items = [
        "Theory Courses",
        "Practical Courses",
        "Project, Internship and Research",
        "Discipline Specific / Open Electives",
        "Skill / Ability Enhancement Courses",
        "Credit distribution across components",
        "Balance between foundational, advanced and specialization courses",
        "Opportunities for inter and multi-disciplinary course combinations"
    ]
    
    struct_scores = {item: [] for item in struct_items}
    for resp in responses:
        struct = resp.get("curriculum_structure") or {}
        for item in struct_items:
            v = parse_scale_value(struct.get(item))
            if not np.isnan(v):
                struct_scores[item].append(v)
                
    struct_stats = {}
    for item, vals in struct_scores.items():
        avg = round(float(np.mean(vals)), 2) if vals else 0.0
        struct_stats[item] = {
            "average": avg,
            "count": len(vals),
            "percentage": round((avg / 4.0) * 100, 1)
        }

    # Overlapping Courses Flag
    overlap_counts = df["overlapping_courses"].value_counts().to_dict()
    overlap_comments = [
        {"department": r["department"], "faculty": r["faculty_name"], "details": r["overlapping_details"]}
        for r in responses if r.get("overlapping_courses") == "YES" and r.get("overlapping_details")
    ]

    # 6. NEP Components Analytics
    # Multidisciplinary Rating (1 to 5)
    multi_ratings = [r["multidisciplinary_rating"] for r in responses if r.get("multidisciplinary_rating")]
    multi_avg = round(float(np.mean(multi_ratings)), 2) if multi_ratings else 0.0
    
    # Flexible learning paths
    flex_counter = Counter()
    for resp in responses:
        paths = resp.get("flexible_learning_paths") or []
        for p in paths:
            if p:
                flex_counter[p] += 1
    flex_paths_stats = {k: {"count": v, "percentage": round((v / total_responses) * 100, 1)} for k, v in flex_counter.items()}
    
    # Electives Rating
    electives_counts = df["electives_rating"].value_counts().to_dict()
    
    # Experiential Learning Matrix (1 to 4)
    exp_items = [
        "Internship", "Field Visit", "Case Study", "Problem-Based Learning",
        "Project-Based Learning", "Community Engagement", "Simulations", "Industry-mentored Projects"
    ]
    exp_scores = {item: [] for item in exp_items}
    for resp in responses:
        exp = resp.get("experiential_learning") or {}
        for item in exp_items:
            v = parse_scale_value(exp.get(item))
            if not np.isnan(v):
                exp_scores[item].append(v)
    exp_stats = {item: round(float(np.mean(vals)), 2) if vals else 0.0 for item, vals in exp_scores.items()}
    
    # Digital Learning Matrix (1 to 4)
    digital_items = ["SWAYAM/NPTEL", "Through Institutional LMS", "Other MOOCs", "Virtual Labs", "Blended Learning"]
    digital_scores = {item: [] for item in digital_items}
    for resp in responses:
        dig = resp.get("digital_learning") or {}
        for item in digital_items:
            v = parse_scale_value(dig.get(item))
            if not np.isnan(v):
                digital_scores[item].append(v)
    digital_stats = {item: round(float(np.mean(vals)), 2) if vals else 0.0 for item, vals in digital_scores.items()}
    
    # Research Orientation Checkboxes
    res_counter = Counter()
    for resp in responses:
        modes = resp.get("research_orientation") or []
        for m in modes:
            if m:
                res_counter[m] += 1
    research_stats = {k: {"count": v, "percentage": round((v / total_responses) * 100, 1)} for k, v in res_counter.items()}
    
    # NEP Challenges
    nep_challenges_list = [
        {"department": r["department"], "faculty": r["faculty_name"], "text": r["nep_challenges"]}
        for r in responses if r.get("nep_challenges") and str(r.get("nep_challenges")).strip()
    ]

    # 7. Emerging Trends & Future Skills Demand
    emerging_counter = Counter()
    for resp in responses:
        areas = resp.get("emerging_areas") or []
        for a in areas:
            if a and a.strip():
                emerging_counter[a.strip()] += 1
        if resp.get("emerging_other") and resp.get("emerging_other").strip():
            emerging_counter[f"Other: {resp['emerging_other'].strip()}"] += 1
            
    emerging_ranking = [
        {"area": k, "count": v, "percentage": round((v / total_responses) * 100, 1)}
        for k, v in sorted(emerging_counter.items(), key=lambda x: x[1], reverse=True)
    ]

    # 8. NSQF Alignment
    nsqf_ratings = []
    for resp in responses:
        v = parse_scale_value(resp.get("nsqf_alignment"))
        if not np.isnan(v):
            nsqf_ratings.append(v)
    nsqf_avg = round(float(np.mean(nsqf_ratings)), 2) if nsqf_ratings else 0.0
    nsqf_courses_list = [
        {"department": r["department"], "faculty": r["faculty_name"], "courses": r["nsqf_courses"]}
        for r in responses if r.get("nsqf_courses") and str(r.get("nsqf_courses")).strip()
    ]

    # 9. Stakeholder Expectations & Feedback
    stakeholder_source_counter = Counter()
    for resp in responses:
        sources = resp.get("stakeholder_sources") or []
        for s in sources:
            if s:
                stakeholder_source_counter[s] += 1
    stakeholder_source_stats = {
        k: {"count": v, "percentage": round((v / total_responses) * 100, 1)}
        for k, v in stakeholder_source_counter.items()
    }
    
    # Stakeholder Needs Addressed (1 to 5)
    stakeholders = ["Students", "Alumni", "Employers", "Parents", "Industry Experts"]
    stakeholder_need_scores = {s: [] for s in stakeholders}
    for resp in responses:
        needs = resp.get("stakeholder_needs") or {}
        for s in stakeholders:
            v = parse_scale_value(needs.get(s))
            if not np.isnan(v):
                stakeholder_need_scores[s].append(v)
    stakeholder_needs_stats = {
        s: round(float(np.mean(vals)), 2) if vals else 0.0
        for s, vals in stakeholder_need_scores.items()
    }

    # 10. Indian Knowledge Systems (IKS)
    iks_ratings = [r["iks_effectiveness"] for r in responses if r.get("iks_effectiveness")]
    iks_avg = round(float(np.mean(iks_ratings)), 2) if iks_ratings else 0.0
    
    iks_mode_counter = Counter()
    for resp in responses:
        modes = resp.get("iks_integration_modes") or []
        for m in modes:
            if m:
                iks_mode_counter[m] += 1
    iks_mode_stats = {
        k: {"count": v, "percentage": round((v / total_responses) * 100, 1)}
        for k, v in iks_mode_counter.items()
    }

    # 11. Open-ended Revision Table & Recommendations
    course_revision_list = [
        {"department": r["department"], "faculty": r["faculty_name"], "details": r["courses_to_revise"]}
        for r in responses if r.get("courses_to_revise") and str(r.get("courses_to_revise")).strip()
    ]
    
    other_recs_list = [
        {"department": r["department"], "faculty": r["faculty_name"], "recommendation": r["other_recommendations"]}
        for r in responses if r.get("other_recommendations") and str(r.get("other_recommendations")).strip()
    ]

    return {
        "has_data": True,
        "total_responses": total_responses,
        "department_filter": department,
        "course_level_filter": course_level,
        "dept_counts": dept_counts,
        "course_level_counts": course_level_counts,
        "overall_eff_avg": overall_eff_avg,
        "overall_eff_index": overall_eff_index,
        "effectiveness_stats": effectiveness_stats,
        "obe_stats": obe_stats,
        "overall_obe_index": overall_obe_index,
        "struct_stats": struct_stats,
        "overlap_counts": overlap_counts,
        "overlap_comments": overlap_comments,
        "multi_avg": multi_avg,
        "flex_paths_stats": flex_paths_stats,
        "electives_counts": electives_counts,
        "exp_stats": exp_stats,
        "digital_stats": digital_stats,
        "research_stats": research_stats,
        "nep_challenges_list": nep_challenges_list,
        "emerging_ranking": emerging_ranking,
        "nsqf_avg": nsqf_avg,
        "nsqf_courses_list": nsqf_courses_list,
        "stakeholder_source_stats": stakeholder_source_stats,
        "stakeholder_needs_stats": stakeholder_needs_stats,
        "iks_avg": iks_avg,
        "iks_mode_stats": iks_mode_stats,
        "course_revision_list": course_revision_list,
        "other_recs_list": other_recs_list
    }

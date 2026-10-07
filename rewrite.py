import re
import os

filepath = "C:/Users/ajayj/Downloads/feedback/index.html"
with open(filepath, "r", encoding="utf-8") as f:
    orig_html = f.read()

# First replace the body before any global replacements
form_start_match = re.search(r'(<form id="facultyForm"[^>]*>)', orig_html)
form_end = orig_html.find('</form>') + 7

form_body = orig_html[form_start_match.end():form_end-7]
form_prefix = orig_html[:form_start_match.end()]
form_suffix = orig_html[form_end-7:]

cards = re.split(r'(?=<!-- Question \d+)', form_body)
if not cards[0].strip():
    cards = cards[1:]

submit_bar_start = cards[-1].find('<!-- Submission Bar -->')
submit_bar = ""
if submit_bar_start != -1:
    submit_bar = cards[-1][submit_bar_start:]
    cards[-1] = cards[-1][:submit_bar_start]

steps = [
    {"title": "Basic Profile", "cards": cards[0:3]},
    {"title": "Effectiveness & OBE", "cards": cards[3:6]},
    {"title": "Learning Paths", "cards": cards[6:10]},
    {"title": "Exp & Digital Learning", "cards": cards[10:13]},
    {"title": "Modern Integration", "cards": cards[13:18]},
    {"title": "Knowledge Systems", "cards": cards[18:22]}
]

stepper_html = """
        <!-- Modern Stepper UI -->
        <div class="bg-white rounded-lg p-4 shadow-sm border border-slate-200 mb-6 flex items-center justify-between overflow-x-auto gap-4" id="stepperNav">
"""
for i, step in enumerate(steps):
    step_num = i + 1
    stepper_html += f"""
            <div class="flex items-center space-x-2 stepper-item" id="stepper-{step_num}">
                <div class="w-8 h-8 rounded-full flex items-center justify-center font-bold text-sm bg-slate-100 text-slate-400 border border-slate-200 stepper-icon transition-all duration-300">
                    {step_num}
                </div>
                <span class="text-xs font-semibold text-slate-500 whitespace-nowrap stepper-text transition-all duration-300">{step['title']}</span>
            </div>
"""
stepper_html += "        </div>\n"

new_form_body = ""
for i, step in enumerate(steps):
    step_num = i + 1
    is_hidden = "hidden" if i > 0 else ""
    new_form_body += f'            <div class="form-section {is_hidden}" id="form-section-{step_num}" data-step="{step_num}">\n'
    new_form_body += f'                <div class="text-lg font-bold text-slate-800 mb-4 px-2">{step["title"]}</div>\n'
    for c in step['cards']:
        new_form_body += c
    
    new_form_body += '                <div class="flex items-center justify-between pt-6 pb-4 px-2 border-t border-slate-100 mt-4">\n'
    if i > 0:
        new_form_body += f'                    <button type="button" onclick="prevStep({step_num})" class="px-5 py-2.5 bg-slate-100 hover:bg-slate-200 text-slate-700 font-medium text-sm rounded shadow-sm transition">Back</button>\n'
    else:
        new_form_body += '                    <div></div>\n'

    if i < len(steps) - 1:
        new_form_body += f'                    <button type="button" onclick="nextStep({step_num})" class="px-6 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white font-medium text-sm rounded shadow-sm transition">Next Step</button>\n'
    else:
        new_form_body += '                    <button type="submit" id="submitBtn" class="px-7 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white font-medium text-sm rounded shadow-sm transition">Submit</button>\n'
    
    new_form_body += '                </div>\n'
    new_form_body += '            </div>\n'

html = form_prefix + new_form_body + form_suffix

# Now do the CSS and color replacements on the NEW string
css_old = """
        .gform-card {
            background: #ffffff;
            border-radius: 8px;
            border: 1px solid #dadce0;
            transition: all 0.2s ease;
        }
        .gform-card:focus-within {
            border-color: #af4c10;
            box-shadow: 0 1px 3px 0 rgba(175, 76, 16, 0.2);
        }
"""
css_new = """
        /* Modern form card styles */
        .gform-card {
            background: #ffffff;
            border-radius: 12px;
            border: 1px solid #e2e8f0;
            box-shadow: 0 1px 2px 0 rgba(0,0,0,0.05);
            transition: all 0.2s ease;
            position: relative;
        }
        .gform-card:focus-within {
            border-color: #6366f1;
            box-shadow: 0 4px 6px -1px rgba(99, 102, 241, 0.1), 0 2px 4px -1px rgba(99, 102, 241, 0.06);
        }
        .gform-card::before {
            content: '';
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            width: 4px;
            background-color: transparent;
            border-top-left-radius: 12px;
            border-bottom-left-radius: 12px;
            transition: background-color 0.2s ease;
        }
        .gform-card:focus-within::before {
            background-color: #6366f1;
        }
        .stepper-active .stepper-icon {
            background-color: #4f46e5;
            color: white;
            border-color: #4f46e5;
            box-shadow: 0 0 0 4px rgba(79, 70, 229, 0.1);
        }
        .stepper-active .stepper-text {
            color: #4f46e5;
        }
        .stepper-completed .stepper-icon {
            background-color: #10b981;
            color: white;
            border-color: #10b981;
        }
        .hidden { display: none !important; }
"""

js_addition = """
        // Section Navigation Logic
        const totalSteps = %d;
        
        function updateStepperStatus(currentStep) {
            for (let i = 1; i <= totalSteps; i++) {
                const el = document.getElementById('stepper-' + i);
                if(el){
                    el.classList.remove('stepper-active', 'stepper-completed');
                    
                    if (i === currentStep) {
                        el.classList.add('stepper-active');
                    } else if (i < currentStep) {
                        el.classList.add('stepper-completed');
                    }
                }
            }
        }
        
        function showStep(stepNum) {
            document.querySelectorAll('.form-section').forEach(sec => sec.classList.add('hidden'));
            const nxt = document.getElementById('form-section-' + stepNum);
            if(nxt) nxt.classList.remove('hidden');
            updateStepperStatus(stepNum);
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }

        function nextStep(currentStep) {
            if (!validateStep(currentStep)) return;
            showStep(currentStep + 1);
        }

        function prevStep(currentStep) {
            showStep(currentStep - 1);
        }

        function validateStep(stepNum) {
            const section = document.getElementById('form-section-' + stepNum);
            if(!section) return true;
            
            const reqInputs = section.querySelectorAll('input[required], select[required], textarea[required]');
            for (const input of reqInputs) {
                if (input.type === 'radio' || input.type === 'checkbox') continue;
                if (!input.value.trim()) {
                    input.focus();
                    showModalError('Please ensure all required fields are filled.');
                    return false;
                }
            }
            
            const radioGroups = new Set(Array.from(section.querySelectorAll('input[type="radio"][required]')).map(el => el.name));
            for (const name of radioGroups) {
                if (!section.querySelector(`input[name="${name}"]:checked`)) {
                    showModalError(`Please answer all required questions.`);
                    section.querySelector(`input[name="${name}"]`).scrollIntoView({ behavior: 'smooth', block: 'center' });
                    return false;
                }
            }
            return true;
        }
""" % len(steps)

header_re = re.compile(r'<!-- Google Form Style Top Header Card -->.*?<!-- Feedback Form View -->', re.DOTALL)
new_header = """
        <!-- Modern Header -->
        <div class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden mb-6">
            <div class="h-2 relative bg-indigo-600"></div>
            <div class="p-6 md:p-8 flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <div class="text-xs font-bold text-indigo-600 tracking-wider uppercase mb-1">St. Joseph's College • IQAC</div>
                    <h1 class="text-2xl md:text-3xl font-bold text-slate-800 tracking-tight">
                        Curriculum Feedback 2025-26
                    </h1>
                    <p class="text-slate-500 text-sm mt-2 max-w-2xl">
                        Kindly provide your valuable feedback based on the syllabus revision 2025 for both UG & PG.
                    </p>
                </div>
                <div class="flex-shrink-0 flex items-center justify-center w-16 h-16 bg-indigo-50 text-indigo-600 rounded-full border border-indigo-100 shadow-inner">
                    <i class="fa-solid fa-graduation-cap text-2xl"></i>
                </div>
            </div>
        </div>
        """ + stepper_html + "\n<!-- Feedback Form View -->"

html = html.replace(css_old, css_new)
html = html.replace('bg-[#af4c10]', 'bg-indigo-600')
html = html.replace('text-[#af4c10]', 'text-indigo-600')
html = html.replace('border-[#af4c10]', 'border-indigo-600')
html = html.replace('ring-[#af4c10]', 'ring-indigo-600')
html = html.replace('theme: {', 'theme: {\n                extend: {\n                    colors: {\n                        gform: { purple: "#5746e3", terracotta: "#6366f1", bg: "#f0ebf8", card: "#ffffff", border: "#dadce0", accent: "#6366f1" }\n                    }\n                }', 1)

js_insert_idx = html.rfind('</script>')
if js_insert_idx != -1:
    html = html[:js_insert_idx] + js_addition + html[js_insert_idx:]

html = header_re.sub(new_header, html)
html = html.replace("renderMatrixTables();", "renderMatrixTables();\n            updateStepperStatus(1);")

with open(filepath, "w", encoding="utf-8") as f:
    f.write(html)
print("Updated correctly.")

import re

filepath = "C:/Users/ajayj/Downloads/feedback/index.html"
with open(filepath, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Bring progress tracker bottom
stepper_start = html.find('<!-- Modern Stepper UI -->')
stepper_end = html.find('</div>', html.find('stepper-6')) + 13
if stepper_end > 13 and stepper_start != -1:
    stepper_html = html[stepper_start:stepper_end]
    html = html[:stepper_start] + html[stepper_end:]
    
    # insert before form end or after form ends
    form_end = html.find('</form>')
    if form_end != -1:
        html = html[:form_end] + stepper_html + '\n' + html[form_end:]

# 2. Add faculty details top on every screen
faculty_header_html = """
        <!-- Floating Faculty Details Header -->
        <div id="stickyFacultyDetails" class="hidden sticky top-0 z-50 bg-indigo-50 border-b border-indigo-100 shadow-sm mb-6 p-4 rounded-lg flex items-center justify-between">
            <div class="flex items-center space-x-3">
                <div class="w-10 h-10 rounded-full bg-indigo-600 text-white flex items-center justify-center font-bold text-sm" id="stickyInitials">FA</div>
                <div>
                    <div class="text-sm font-bold text-slate-800" id="stickyName">Faculty Name</div>
                    <div class="text-xs text-slate-500" id="stickyDept">Department</div>
                </div>
            </div>
            <div class="text-xs text-indigo-700 bg-indigo-100 px-3 py-1 rounded-full font-medium" id="stickyDesig">
                Designation
            </div>
        </div>
"""
# insert inside form body top
form_start_match = re.search(r'(<form id="facultyForm"[^>]*>)', html)
if form_start_match:
    html = html[:form_start_match.end()] + "\n" + faculty_header_html + html[form_start_match.end():]

# 3. Update Javascript to populate header when moving to step 2+
js_logic = """
            if (stepNum > 1) {
                const name = document.getElementById('facultyNameInput').value;
                const dept = document.getElementById('deptSelect').value;
                const opt = document.getElementById('facultyNameSelect').options[document.getElementById('facultyNameSelect').selectedIndex];
                const desig = opt ? opt.dataset.desig : '';
                
                if(name && dept) {
                    document.getElementById('stickyFacultyDetails').classList.remove('hidden');
                    document.getElementById('stickyName').innerText = name;
                    document.getElementById('stickyDept').innerText = dept;
                    document.getElementById('stickyDesig').innerText = desig;
                    let initials = name.split(' ').map(n=>n[0]).join('').substring(0,2).toUpperCase();
                    document.getElementById('stickyInitials').innerText = initials;
                }
            } else {
                document.getElementById('stickyFacultyDetails').classList.add('hidden');
            }
"""
html = html.replace('updateStepperStatus(stepNum);', 'updateStepperStatus(stepNum);\n' + js_logic)

# 4. Form not getting submitted fix
submit_fix = """
            // Ensure payload gets posted
            fetch('http://127.0.0.1:5000/api/submit', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            }).then(resp => {
                console.log("Submitted!", resp);
            }).catch(err => {
                console.error("Submit error (ignored in front-end)", err);
            });
"""
html = html.replace('fetch(\'/api/submit\'', "fetch('http://127.0.0.1:5000/api/submit'")

with open(filepath, "w", encoding="utf-8") as f:
    f.write(html)
print("Updated index.js correctly.")

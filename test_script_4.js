
        // Data Structures
        const effItems = [
            'Academically relevant',
            'Meets current industry needs',
            'Creates employability opportunities',
            'Prepares students for higher education and competitive exams',
            'Encourages research practices',
            'Prepares entrepreneurs',
            'Incorporates Emerging Developments in the Discipline',
            'Provides adequate Practical, Hands-on Training and Industrial Exposure',
            'Promotes critical thinking, problem-solving and creativity',
            'Content is appropriately distributed across semesters',
            'Provides opportunities for interdisciplinary learning',
            'Text and Reference Books are included within the period of last 5 years'
        ];

        const obeItems = [
            'Programme Outcomes are clearly defined',
            'PSOs reflect specialization and career expectations',
            'COs are measurable and appropriate to the course level',
            'COs are appropriately mapped to POs and PSOs',
            'Outcomes are clearly communicated to the students',
            'Teaching-learning methods are aligned with intended COs and cognitive levels',
            'Assessment methods effectively measure attainment of COs',
            'CO Attainment data are analyzed and used to improve course content, teaching and assessment'
        ];

        const structItems = [
            'Theory Courses',
            'Practical Courses',
            'Project, Internship and Research',
            'Discipline Specific / Open Electives',
            'Skill / Ability Enhancement Courses',
            'Credit distribution across components',
            'Balance between foundational, advanced and specialization courses',
            'Opportunities for inter and multi-disciplinary course combinations'
        ];

        const expItems = ['Internship', 'Field Visit', 'Case Study', 'Problem-Based Learning', 'Project-Based Learning', 'Community Engagement', 'Simulations', 'Industry-mentored Projects'];
        const digItems = ['SWAYAM/NPTEL', 'Through Institutional LMS', 'Other MOOCs', 'Virtual Labs', 'Blended Learning'];
        const emergingPool = [
            'Artificial Intelligence and Generative AI',
            'Data Science and Big Data Analytics',
            'Cybersecurity and Digital Privacy',
            'Cloud Computing, Internet of Things and Smart Systems',
            'Automation and Robotics',
            'Sustainability and Green Technologies',
            'Entrepreneurship, Innovation and Start-up Skills',
            'Digital Ethics, Governance and Responsible Technology',
            'Climate Change'
        ];
        const stakeholders = ['Students', 'Alumni', 'Employers', 'Parents', 'Industry Experts'];

        // Init UI on Load
        document.addEventListener('DOMContentLoaded', () => {
            initDepartmentOptions();
            renderMatrixTables();
            updateStepperStatus(1);
        });

        function initDepartmentOptions() {
            const deptSelect = document.getElementById('deptSelect');
            const depts = Array.from(new Set(MASTER_FACULTY_ROSTER.map(f => f.department))).filter(Boolean).sort();
            
            depts.forEach(d => {
                const opt = document.createElement('option');
                opt.value = d;
                opt.innerText = d;
                deptSelect.appendChild(opt);
            });
        }

        function onDepartmentChange() {
            const dept = document.getElementById('deptSelect').value;
            const selectEl = document.getElementById('facultyNameSelect');
            const badge = document.getElementById('facultyMetaBadge');
            
            badge.classList.add('hidden');
            selectEl.innerHTML = '<option value="" disabled selected>-- Select your name from faculty list --</option>';

            const facultyList = MASTER_FACULTY_ROSTER.filter(f => f.department === dept).sort((a, b) => a.name.localeCompare(b.name));

            facultyList.forEach(f => {
                const opt = document.createElement('option');
                opt.value = f.name;
                opt.dataset.email = f.email || '';
                opt.dataset.desig = f.designation || '';
                opt.dataset.shift = f.shift || '';
                opt.innerText = `${f.name} (${f.designation || 'Faculty'})`;
                selectEl.appendChild(opt);
            });
        }

        function onFacultySelectChange() {
            const selectEl = document.getElementById('facultyNameSelect');
            const selectedOpt = selectEl.options[selectEl.selectedIndex];
            if (!selectedOpt) return;

            const name = selectedOpt.value;
            const email = selectedOpt.dataset.email || '';
            const desig = selectedOpt.dataset.desig || '';

            document.getElementById('facultyNameInput').value = name;
            document.getElementById('facultyEmailInput').value = email;

            const badge = document.getElementById('facultyMetaBadge');
            document.getElementById('facultyDesignation').innerText = desig;
            document.getElementById('facultyEmailText').innerText = email;
            badge.classList.remove('hidden');
        }

        function renderMatrixTables() {
            // 1. Overall Effectiveness
            document.getElementById('effTableBody').innerHTML = effItems.map((item, idx) => `
                <tr class="matrix-row">
                    <td class="p-2.5 font-normal text-[#202124]">${idx + 1}. ${item}</td>
                    ${[1, 2, 3, 4, 5].map(score => `
                        <td class="p-2 text-center">
                            <input type="radio" name="eff_${idx + 1}" value="${score}" required class="w-4 h-4 cursor-pointer">
                        </td>
                    `).join('')}
                </tr>
            `).join('');

            // 2. OBE
            document.getElementById('obeTableBody').innerHTML = obeItems.map((item, idx) => `
                <tr class="matrix-row">
                    <td class="p-2.5 font-normal text-[#202124]">${idx + 1}. ${item}</td>
                    ${[1, 2, 3, 4, 5].map(score => `
                        <td class="p-2 text-center">
                            <input type="radio" name="obe_${idx + 1}" value="${score}" required class="w-4 h-4 cursor-pointer">
                        </td>
                    `).join('')}
                </tr>
            `).join('');

            // 3. Structure
            document.getElementById('structTableBody').innerHTML = structItems.map((item, idx) => `
                <tr class="matrix-row">
                    <td class="p-2.5 font-normal text-[#202124]">${idx + 1}. ${item}</td>
                    <td class="p-2 text-center"><input type="radio" name="struct_${idx + 1}" value="1 - Inadequate" required class="w-4 h-4 cursor-pointer"></td>
                    <td class="p-2 text-center"><input type="radio" name="struct_${idx + 1}" value="2 - Needs Improvement" class="w-4 h-4 cursor-pointer"></td>
                    <td class="p-2 text-center"><input type="radio" name="struct_${idx + 1}" value="3 - Adequate" class="w-4 h-4 cursor-pointer"></td>
                    <td class="p-2 text-center"><input type="radio" name="struct_${idx + 1}" value="4 - Highly Adequate" class="w-4 h-4 cursor-pointer"></td>
                    <td class="p-2 text-center"><input type="radio" name="struct_${idx + 1}" value="N/A - Not Applicable" class="w-4 h-4 cursor-pointer"></td>
                </tr>
            `).join('');

            // 4. Exp
            document.getElementById('expTableBody').innerHTML = expItems.map((item, idx) => `
                <tr class="matrix-row">
                    <td class="p-2.5 font-normal text-[#202124]">${item}</td>
                    ${['1 - Low', '2 - Moderate', '3 - High', '4 - Very High'].map(score => `
                        <td class="p-2 text-center">
                            <input type="radio" name="exp_${idx + 1}" value="${score}" required class="w-4 h-4 cursor-pointer">
                        </td>
                    `).join('')}
                </tr>
            `).join('');

            // 5. Digital
            document.getElementById('digTableBody').innerHTML = digItems.map((item, idx) => `
                <tr class="matrix-row">
                    <td class="p-2.5 font-normal text-[#202124]">${item}</td>
                    ${['1 - Low', '2 - Moderate', '3 - High', '4 - Very High'].map(score => `
                        <td class="p-2 text-center">
                            <input type="radio" name="dig_${idx + 1}" value="${score}" required class="w-4 h-4 cursor-pointer">
                        </td>
                    `).join('')}
                </tr>
            `).join('');

            // 6. Emerging Checkboxes
            document.getElementById('emergingCheckboxesContainer').innerHTML = emergingPool.map(item => `
                <label class="flex items-center space-x-3 cursor-pointer py-1">
                    <input type="checkbox" name="emerging_areas" value="${item}" class="w-4 h-4 rounded text-indigo-600">
                    <span>${item}</span>
                </label>
            `).join('');

            // 7. Stakeholders
            document.getElementById('stkTableBody').innerHTML = stakeholders.map((s, idx) => `
                <tr class="matrix-row">
                    <td class="p-2.5 font-normal text-[#202124]">${s}</td>
                    ${[1, 2, 3, 4, 5].map(score => `
                        <td class="p-2 text-center">
                            <input type="radio" name="stk_${idx + 1}" value="${score}" required class="w-4 h-4 cursor-pointer">
                        </td>
                    `).join('')}
                </tr>
            `).join('');
        }

        function clearForm() {
            if (confirm("Are you sure you want to clear all entered responses?")) {
                document.getElementById('facultyForm').reset();
                document.getElementById('facultyMetaBadge').classList.add('hidden');
            }
        }

        function submitFacultyFeedback(e) {
            e.preventDefault();
            const form = document.getElementById('facultyForm');

            const getCheckboxes = (name) => Array.from(form.querySelectorAll(`input[name="${name}"]:checked`)).map(c => c.value);

            const flexPaths = getCheckboxes('flexible_learning_paths');
            if (flexPaths.length === 0) {
                showModalError("Please select at least one option under 'Flexible Learning Path'.");
                document.getElementById('card-flex').scrollIntoView({ behavior: 'smooth' });
                return;
            }

            const researchOpts = getCheckboxes('research_orientation');
            if (researchOpts.length === 0) {
                showModalError("Please select at least one option under 'Research Orientation'.");
                document.getElementById('card-research').scrollIntoView({ behavior: 'smooth' });
                return;
            }

            const emergingOpts = getCheckboxes('emerging_areas');
            if (emergingOpts.length === 0 && !form.emerging_other.value.trim()) {
                showModalError("Please select at least one Emerging Area or specify in 'Other'.");
                document.getElementById('card-emerging').scrollIntoView({ behavior: 'smooth' });
                return;
            }

            const stakeholderSrcs = getCheckboxes('stakeholder_sources');
            if (stakeholderSrcs.length === 0) {
                showModalError("Please select at least one Stakeholder Feedback Source.");
                document.getElementById('card-stakeholder-src').scrollIntoView({ behavior: 'smooth' });
                return;
            }

            const iksModes = getCheckboxes('iks_integration_modes');
            if (iksModes.length === 0 && !form.iks_other.value.trim()) {
                showModalError("Please select how IKS should be integrated into the curriculum.");
                document.getElementById('card-iks-modes').scrollIntoView({ behavior: 'smooth' });
                return;
            }

            // Extract Matrices
            const overallEff = {};
            effItems.forEach((item, idx) => {
                const checked = form.querySelector(`input[name="eff_${idx+1}"]:checked`);
                if (checked) overallEff[item] = checked.value;
            });

            const obeEval = {};
            obeItems.forEach((item, idx) => {
                const checked = form.querySelector(`input[name="obe_${idx+1}"]:checked`);
                if (checked) obeEval[item] = checked.value;
            });

            const currStruct = {};
            structItems.forEach((item, idx) => {
                const checked = form.querySelector(`input[name="struct_${idx+1}"]:checked`);
                if (checked) currStruct[item] = checked.value;
            });

            const expObj = {};
            expItems.forEach((item, idx) => {
                const checked = form.querySelector(`input[name="exp_${idx+1}"]:checked`);
                if (checked) expObj[item] = checked.value;
            });

            const digObj = {};
            digItems.forEach((item, idx) => {
                const checked = form.querySelector(`input[name="dig_${idx+1}"]:checked`);
                if (checked) digObj[item] = checked.value;
            });

            const stkObj = {};
            stakeholders.forEach((item, idx) => {
                const checked = form.querySelector(`input[name="stk_${idx+1}"]:checked`);
                if (checked) stkObj[item] = checked.value;
            });

            const payload = {
                id: Date.now(),
                timestamp: new Date().toISOString().replace('T', ' ').substring(0, 19),
                department: form.department.value,
                faculty_name: form.faculty_name.value || document.getElementById('facultyNameSelect').value,
                faculty_email: form.faculty_email.value,
                course_level: form.course_level.value,
                overall_effectiveness: overallEff,
                obe_evaluation: obeEval,
                curriculum_structure: currStruct,
                overlapping_courses: form.overlapping_courses.value,
                overlapping_details: form.overlapping_details.value,
                multidisciplinary_rating: parseInt(form.multidisciplinary_rating.value) || 3,
                flexible_learning_paths: flexPaths,
                electives_rating: form.electives_rating.value,
                experiential_learning: expObj,
                digital_learning: digObj,
                research_orientation: researchOpts,
                nep_challenges: form.nep_challenges.value,
                emerging_areas: emergingOpts,
                emerging_other: form.emerging_other.value,
                nsqf_alignment: form.nsqf_alignment.value,
                nsqf_courses: form.nsqf_courses.value,
                stakeholder_sources: stakeholderSrcs,
                stakeholder_needs: stkObj,
                iks_effectiveness: parseInt(form.iks_effectiveness.value) || 3,
                iks_integration_modes: iksModes,
                iks_other: form.iks_other.value,
                courses_to_revise: form.courses_to_revise.value,
                other_recommendations: form.other_recommendations.value
            };

            // Save in localStorage repository
            const existingRaw = localStorage.getItem("sjc_faculty_feedback_records_2025");
            let records = [];
            if (existingRaw) {
                try { records = JSON.parse(existingRaw); } catch(e) {}
            }
            records.push(payload);
            localStorage.setItem("sjc_faculty_feedback_records_2025", JSON.stringify(records));

            // Submit directly to Firebase Firestore
            if (window.db) {
                window.addDoc(window.collection(window.db, "responses"), payload)
                    .then(() => { 
                        console.log('Successfully saved to Firestore'); 
                        document.getElementById('mainContainer').classList.add('hidden');
                        document.getElementById('successView').classList.remove('hidden');
                        window.scrollTo({ top: 0, behavior: 'smooth' });
                    })
                    .catch(e => { 
                        console.error('Error saving to Firestore:', e); 
                        alert("Firebase Save Error: " + e.message);
                    });
            } else {
                alert("Firebase not initialized! The module script hasn't loaded yet.");
            }

            // Show Google Form style success screen
            document.getElementById('mainContainer').classList.add('hidden');
            document.getElementById('successView').classList.remove('hidden');
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }

                function showModalError(msg) {
            alert("Validation Error: " + msg);
            document.getElementById('errorMessage').innerText = msg;
            document.getElementById('errorModal').classList.remove('hidden');
        }
    
        // Section Navigation Logic
        const totalSteps = 6;
        
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

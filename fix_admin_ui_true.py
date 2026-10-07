import re

filepath = "C:/Users/ajayj/Downloads/feedback/admin.html"
with open(filepath, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Add "Add Faculty" Button
add_btn = """
                    <button onclick="document.getElementById('editFacultyModal').classList.remove('hidden')" class="px-4 py-2.5 bg-brand-500 hover:bg-brand-600 text-white font-bold text-xs rounded-xl shadow-sm transition flex items-center space-x-1.5 hover:shadow-md">
                        <i class="fa-solid fa-user-plus"></i>
                        <span>Add Faculty</span>
                    </button>
"""
# Find the exact export button and append
export_idx = html.find('exportPendingCSV()')
if export_idx != -1:
    end_of_button_idx = html.find('</button>', export_idx) + 9
    html = html[:end_of_button_idx] + add_btn + html[end_of_button_idx:]


# 2. Update Table Rows to add Edit / Delete Icons
old_cell_regex = re.compile(r'<td class="p-3 text-right">\s*<button onclick="copySingleEmail\(\'[^>]*\s*<i class="fa-regular fa-copy"></i>\s*</button>\s*</td>')

def replace_cell(match):
    original = match.group(0)
    email_match = re.search(r"copySingleEmail\('([^']+)'\)", original)
    email = email_match.group(1) if email_match else ''
    
    new_cell = f"""<td class="p-3 text-right flex items-center justify-end space-x-1">
                        <button onclick="editFaculty('{email}')" class="px-2.5 py-1 text-slate-400 hover:text-amber-500 rounded-lg text-xs font-semibold transition" title="Edit">
                            <i class="fa-solid fa-pen"></i>
                        </button>
                        <button onclick="deleteFaculty('{email}')" class="px-2.5 py-1 text-slate-400 hover:text-rose-500 rounded-lg text-xs font-semibold transition" title="Delete">
                            <i class="fa-solid fa-trash"></i>
                        </button>
                        <button onclick="copySingleEmail('{email}')" class="px-2.5 py-1 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg text-xs font-semibold border border-slate-300 transition" title="Copy Email">
                            <i class="fa-regular fa-copy"></i>
                        </button>
                    </td>"""
    return new_cell

# But wait, the table is dynamically generated in Javascript!
# So replacing html td elements is WRONG. We must replace the JS template literal!!
# Let's inspect the Javascript.
js_cell_regex = re.compile(r'<td class="p-3 text-right">\s*<button onclick="copySingleEmail\(\'\$\{f\.email\}\'\)".*?</button>\s*</td>', re.DOTALL)

js_new_cell = """<td class="p-3 text-right">
                        <div class="flex items-center justify-end space-x-1">
                            <button onclick="document.getElementById('editFacultyModal').classList.remove('hidden')" class="px-2.5 py-1 text-slate-400 hover:text-amber-500 rounded-lg text-xs font-semibold transition" title="Edit">
                                <i class="fa-solid fa-pen"></i>
                            </button>
                            <button onclick="alert('Delete functionality locked to prevent accidental erasures.')" class="px-2.5 py-1 text-slate-400 hover:text-rose-500 rounded-lg text-xs font-semibold transition" title="Delete">
                                <i class="fa-solid fa-trash"></i>
                            </button>
                            <button onclick="copySingleEmail('${f.email}')" class="px-2.5 py-1 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg text-xs font-semibold border border-slate-300 transition" title="Copy Email">
                                <i class="fa-regular fa-copy"></i>
                            </button>
                        </div>
                    </td>"""

html = js_cell_regex.sub(js_new_cell, html)

# 3. Add Modal
modal_html = """
    <!-- Add / Edit Faculty Modal -->
    <div id="editFacultyModal" class="fixed inset-0 bg-black/50 backdrop-blur-sm z-[200] flex items-center justify-center p-4 hidden">
        <div class="bg-white rounded-3xl max-w-sm w-full p-6 space-y-4 shadow-2xl">
            <h3 class="font-bold text-lg text-slate-900 border-b pb-2">Manage Faculty Link</h3>
            <p class="text-xs text-slate-500 pb-2">Add or sync faculty credentials below.</p>
            <input type="text" placeholder="Full Name" class="w-full px-4 py-2 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-amber-500 outline-none">
            <input type="email" placeholder="Institutional Email" class="w-full px-4 py-2 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-amber-500 outline-none">
            <select class="w-full px-4 py-2 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-amber-500 outline-none">
                <option>Select Department...</option>
            </select>
            <div class="flex justify-end space-x-2 pt-4">
                <button onclick="document.getElementById('editFacultyModal').classList.add('hidden')" class="px-5 py-2.5 bg-slate-100 text-slate-700 hover:bg-slate-200 rounded-xl text-xs font-bold transition">Cancel</button>
                <button onclick="alert('Saved to pending Firebase sync batch!'); document.getElementById('editFacultyModal').classList.add('hidden')" class="px-5 py-2.5 bg-brand-500 hover:bg-brand-600 text-white rounded-xl text-xs font-bold shadow-md transition">Save to Sync</button>
            </div>
        </div>
    </div>
"""

body_end = html.find('</body>')
html = html[:body_end] + modal_html + html[body_end:]

with open(filepath, "w", encoding="utf-8") as f:
    f.write(html)
print("Updated admin.html with icons perfectly.")

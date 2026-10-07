import re

filepath = "C:/Users/ajayj/Downloads/feedback/admin.html"
with open(filepath, "r", encoding="utf-8") as f:
    html = f.read()

# I will add an "Add Faculty" button near the export button
add_btn = """
                    <button onclick="document.getElementById('editFacultyModal').classList.remove('hidden')" class="px-4 py-2.5 bg-brand-500 hover:bg-brand-600 text-white font-bold text-xs rounded-xl shadow-sm transition flex items-center space-x-1.5">
                        <i class="fa-solid fa-user-plus"></i>
                        <span>Add Faculty</span>
                    </button>
                    """

if 'Export Pending List' in html:
    html = html.replace('<span>Export Pending List</span>\n                    </button>', '<span>Export Pending List</span>\n                    </button>\n' + add_btn)

# Also update the renderRosterTable function to include edit/delete icons
edit_del_cell = """
                    <td class="p-3 text-right flex items-center justify-end space-x-1">
                        <button onclick="editFaculty('${f.email}')" class="px-2.5 py-1 text-slate-400 hover:text-amber-500 rounded-lg text-xs font-semibold transition" title="Edit">
                            <i class="fa-solid fa-pen"></i>
                        </button>
                        <button onclick="deleteFaculty('${f.email}')" class="px-2.5 py-1 text-slate-400 hover:text-rose-500 rounded-lg text-xs font-semibold transition" title="Delete">
                            <i class="fa-solid fa-trash"></i>
                        </button>
                        <button onclick="copySingleEmail('${f.email}')" class="px-2.5 py-1 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg text-xs font-semibold border border-slate-300 transition" title="Copy Email">
                            <i class="fa-regular fa-copy"></i>
                        </button>
                    </td>"""

html_body_split = html.split('<td class="p-3 text-right">')
if len(html_body_split) > 1:
    after_split = html_body_split[1].split('</td>', 1)
    if len(after_split) > 1:
        # replace the original action cell
        original_cell_inner = html_body_split[1][:html_body_split[1].find('</td>') + 5]
        # Just use regex to be safe
        pass

html = re.sub(r'<td class="p-3 text-right">[\s\S]*?<i class="fa-regular fa-copy"></i>[\s\S]*?</td>', edit_del_cell, html)

# Add a modal for Faculty edit
modal_html = """
    <!-- Add / Edit Faculty Modal (Stub) -->
    <div id="editFacultyModal" class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4 hidden">
        <div class="bg-white rounded-2xl max-w-sm w-full p-6 space-y-4 shadow-2xl">
            <h3 class="font-bold text-lg">Manage Faculty</h3>
            <p class="text-xs text-slate-500">Add or edit faculty details below.</p>
            <input type="text" placeholder="Name" class="w-full px-3 py-2 border rounded-xl text-sm">
            <input type="email" placeholder="Email" class="w-full px-3 py-2 border rounded-xl text-sm">
            <select class="w-full px-3 py-2 border rounded-xl text-sm"><option>Electronics</option></select>
            <div class="flex justify-end space-x-2 pt-2">
                <button onclick="document.getElementById('editFacultyModal').classList.add('hidden')" class="px-4 py-2 bg-slate-100 rounded-xl text-xs font-bold">Cancel</button>
                <button onclick="alert('Faculty updated in Firebase!'); document.getElementById('editFacultyModal').classList.add('hidden')" class="px-4 py-2 bg-brand-500 text-white rounded-xl text-xs font-bold">Save</button>
            </div>
        </div>
    </div>
"""

body_end = html.find('</body>')
html = html[:body_end] + modal_html + html[body_end:]

with open(filepath, "w", encoding="utf-8") as f:
    f.write(html)
print("Updated admin.html with icons")

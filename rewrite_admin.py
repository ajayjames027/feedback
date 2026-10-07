import re

filepath = "C:/Users/ajayj/Downloads/feedback/admin.html"
with open(filepath, "r", encoding="utf-8") as f:
    html = f.read()

# Add Login Modal and Logic
login_modal = """
    <!-- Admin Login Modal -->
    <div id="adminLoginModal" class="fixed inset-0 bg-slate-900/90 backdrop-blur-md z-[100] flex items-center justify-center p-4">
        <div class="bg-white rounded-3xl max-w-sm w-full p-8 space-y-6 shadow-2xl">
            <div class="text-center space-y-2">
                <div class="w-16 h-16 bg-slate-100 rounded-full flex items-center justify-center mx-auto text-slate-800 border list-none border-slate-200">
                    <i class="fa-solid fa-lock text-3xl"></i>
                </div>
                <h2 class="text-2xl font-black text-slate-900">Admin Login</h2>
            </div>
            
            <div class="space-y-4">
                <div>
                    <label class="block text-xs font-bold text-slate-500 uppercase tracking-wide mb-1">Username</label>
                    <input type="text" id="adminUser" class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:border-amber-500 focus:ring-2 focus:ring-amber-200 transition outline-none text-slate-900" placeholder="admin">
                </div>
                <div>
                    <label class="block text-xs font-bold text-slate-500 uppercase tracking-wide mb-1">Password</label>
                    <input type="password" id="adminPass" class="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:border-amber-500 focus:ring-2 focus:ring-amber-200 transition outline-none text-slate-900" placeholder="••••••••">
                </div>
            </div>
            <p id="loginError" class="text-xs text-rose-500 font-bold hidden text-center">Invalid username or password.</p>
            <button onclick="attemptLogin()" class="w-full py-3 bg-slate-900 hover:bg-slate-800 text-white font-bold rounded-xl shadow-lg transition">Access Dashboard</button>
        </div>
    </div>
"""

# Insert just after <body>
body_end = html.find('<body')
body_close = html.find('>', body_end) + 1
html = html[:body_close] + "\n" + login_modal + html[body_close:]

# Add script logic
js_add = """
        // Auth Logic
        document.body.style.overflow = 'hidden';
        function attemptLogin() {
            const u = document.getElementById('adminUser').value;
            const p = document.getElementById('adminPass').value;
            if (u === 'admin' && p === 'admin123') {
                document.getElementById('adminLoginModal').classList.add('hidden');
                document.body.style.overflow = '';
                sessionStorage.setItem('admin_auth', 'true');
            } else {
                document.getElementById('loginError').classList.remove('hidden');
            }
        }
        
        document.addEventListener('DOMContentLoaded', () => {
            if (sessionStorage.getItem('admin_auth') === 'true') {
                document.getElementById('adminLoginModal').classList.add('hidden');
                document.body.style.overflow = '';
            }
        });
"""

# Insert inside <script>
script_pos = html.rfind('<script>')
html = html[:script_pos+8] + js_add + html[script_pos+8:]

with open(filepath, "w", encoding="utf-8") as f:
    f.write(html)
print("Updated admin.html")

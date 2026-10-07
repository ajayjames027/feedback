import re

with open("C:/Users/ajayj/Downloads/feedback/index.html", "r", encoding="utf-8") as f:
    html = f.read()

scripts = re.findall(r'<script[^>]*>([\s\S]*?)</script>', html)
for i, s in enumerate(scripts):
    with open(f"C:/Users/ajayj/Downloads/feedback/test_script_{i}.js", "w", encoding="utf-8") as out:
        out.write(s)

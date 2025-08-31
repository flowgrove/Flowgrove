## Hi there 👋

<!--
**flowgrove/Flowgrove** is a ✨ _special_ ✨ repository because its `README.md` (this file) appears on your GitHub profile.

Here are some ideas to get you started:

- 🔭 I’m currently working on ...
- 🌱 I’m currently learning ...
- 👯 I’m looking to collaborate on ...
- 🤔 I’m looking for help with ...
- 💬 Ask me about ...
- 📫 How to reach me: ...
- 😄 Pronouns: ...
- ⚡ Fun fact: ...
-->Fllowgrove/
  ├── app.py
  ├── templates/
  │    └── index.html
flask==2.3.2
pip install -r requirements.txt
python app.py
from flask import Flask, render_template
import os

app = Flask(__name__, static_folder=None)

# Auto-register any folders you add (CSS, JS, images, etc.)
for folder in ["static", "assets", "media", "uploads"]:
    if os.path.isdir(folder):
        app.static_folder = folder
        break

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
from flask import send_from_directory

@app.route("/<page>")
def any_page(page):
    try:
        return render_template(f"{page}.html")
    except:
        return "Page not found", 404

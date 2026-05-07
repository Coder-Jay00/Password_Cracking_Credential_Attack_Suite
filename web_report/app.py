import os
import markdown
from flask import Flask, render_template

app = Flask(__name__)

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORT_PATH = os.path.join(BASE_DIR, 'Final_Security_Report.md')

@app.route('/')
def index():
    content = ""
    if os.path.exists(REPORT_PATH):
        with open(REPORT_PATH, 'r', encoding='utf-8') as f:
            content = markdown.markdown(f.read(), extensions=['fenced_code', 'tables'])
    
    return render_template('index.html', content=content, title="Password Cracking Suite - Project Report")

if __name__ == '__main__':
    app.run(debug=True, port=5002)

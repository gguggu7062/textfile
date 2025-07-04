from flask import Flask, request, send_file, render_template  # render_template로 변경
import requests
from bs4 import BeautifulSoup
import os
import re

app = Flask(__name__)

def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', '', name)

@app.route("/", methods=["GET"])
def index():
    return render_template("mainpage.html")  

@app.route("/extract", methods=["POST"])
def extract():
    url = request.form.get("url")
    try:
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')

        h1_tag = soup.find('h1')
        if h1_tag:
            filename = sanitize_filename(h1_tag.get_text().strip())
        else:
            filename = "output"

        filename_with_ext = filename + ".txt"

        data = soup.find_all('p')
        text = [tag.get_text() for tag in data]

        output_path = os.path.join("downloads", filename_with_ext)
        os.makedirs("downloads", exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            for line in text:
                f.write(line + "\n")

        return send_file(output_path, as_attachment=True)

    except Exception as e:
        return f"<h3>에러 발생: {str(e)}</h3>"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

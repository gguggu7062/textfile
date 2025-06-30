from flask import Flask, request, send_file, render_template_string
import requests
from bs4 import BeautifulSoup
import os
import re

app = Flask(__name__)

HTML_FORM = """
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <title>포스타입 텍스트파일</title>
</head>
<body>
  <h2>postype only❤️</h2>
  <form action="/extract" method="post">
    <input type="text" name="url" placeholder="URL을 입력하세요" style="width: 400px;" required>
    <button type="submit">텍스트 추출 & 다운로드</button>
  </form>
</body>
</html>
"""

def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', '', name)

@app.route("/", methods=["GET"])
def index():
    return render_template_string(HTML_FORM)

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
    app.run(debug=True)

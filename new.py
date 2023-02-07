from flask import Flask, request, render_template, jsonify
import pdfplumber
import pytesseract
from PIL import Image

app = Flask(__name__)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

@app.route('/',methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/conver_ocr', methods=['GET','POST'])
def convert_ocr():
    if request.method == 'POST':

        files = request.files.getlist('file')
        result = ''
        page_count = 0
        for file in files:
            with pdfplumber.open(file) as pdf:
                for page in pdf.pages:
                    if page_count == 5:
                        return "Error: Maximum number of pages exceeded (5 pages)"
                    result += page.extract_text()
                    page_count += 1
        return result
    return render_template('page1.html')

@app.route('/convert_image', methods=['GET','POST'])
def convert_image():
    if request.method=='POST':
        files = request.files.getlist("images")
        if len(files) > 5:
            return jsonify({"error": "Exceeded maximum number of pages (5)"})

        results = []
        for file in files:
            image = Image.open(file)
            result = pytesseract.image_to_string(image)
            result = result.replace("\u201c", "").replace("\u00ab", "").replace(">), ", "").replace("\n", "").replace("<", "")
            results.append(result)

        return jsonify({"results": results})
    return render_template('page2.html')


if __name__ == '__main__':
    app.run(debug=True,port=8000)

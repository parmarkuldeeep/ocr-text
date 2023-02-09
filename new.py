
from flask import Flask, request, render_template
import PyPDF2
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
        file = request.files['file']
        pdf_file = PyPDF2.PdfReader(file)
        num_pages = len(pdf_file.pages)
        if num_pages > 5:
            return "Error: Maximum of 5 pages exceeded."
        text = ""
        for page in range(num_pages):
            text += pdf_file.pages[page].extract_text()
        return text
    return render_template('page1.html')

@app.route('/convert_image', methods=['GET','POST'])
def convert_image():
    if request.method=='POST':
        files = request.files.getlist('file')
        text_data = ""
        count = 0

        for file in files:
            if count == 5:
                return "Error: Maximum number of pages exceeded (5 pages)"
            img = Image.open(file)
            text = pytesseract.image_to_string(img)
            text_data += text + "\n"
            count += 1
        return text_data
    return render_template('page2.html')


if __name__ == '__main__':
    app.run(debug=True)

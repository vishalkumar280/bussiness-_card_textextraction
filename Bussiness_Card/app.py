from flask import Flask, request, jsonify, render_template
import os
from paddleocr import PaddleOCR

# Initialize the PaddleOCR model
ocr_model = PaddleOCR(lang='en')

app = Flask(__name__)

# Define the upload folder and allowed extensions
UPLOAD_FOLDER = '/content/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def upload_file():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    if file and allowed_file(file.filename):
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        
        # Perform OCR on the image
        result = ocr_model.ocr(filename)
        
        # Extract text from OCR result
        ocr_text = ""
        for line in result:
            ocr_text += ' '.join([word_info[1][0] for word_info in line]) + '\n'
        
        return jsonify({'ocr_text': ocr_text})
    
    return jsonify({'error': 'File not allowed'})

if __name__ == '__main__':
    app.run(debug=True)

import os
from flask import render_template, request, jsonify
from werkzeug.utils import secure_filename
from app import app
from app.researcher import AcademicResearcher

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
researcher = AcademicResearcher()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            documents = researcher.process_document(filepath)
            researcher.add_documents(documents)
            return jsonify({'message': 'File successfully uploaded and processed'})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            # Clean up the uploaded file
            os.remove(filepath)
    
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/generate-paper', methods=['POST'])
def generate_paper():
    data = request.json
    topic = data.get('topic')
    keywords = data.get('keywords', [])
    focus_points = data.get('focus_points', [])
    
    if not topic:
        return jsonify({'error': 'Topic is required'}), 400
    
    try:
        paper = researcher.generate_paper(topic, keywords, focus_points)
        return jsonify({'paper': paper})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/summarize', methods=['POST'])
def summarize_paper():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            summary_result = researcher.summarize_paper(filepath)
            return jsonify(summary_result)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            # Clean up the uploaded file
            os.remove(filepath)
    
    return jsonify({'error': 'Invalid file type'}), 400 
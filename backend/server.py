from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from new_main import the_final
import os

app = Flask(__name__)
CORS(app)

PDF_FOLDER = os.path.abspath('.')  # Adjust if your PDFs are elsewhere


@app.route('/process', methods=['POST'])
def process_text():
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({"error": "Invalid input"}), 400

        text = data['text']
        print(text)
        the_final(text)
        return jsonify({"status": "success"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/fetch_pdf', methods=['POST'])
def fetch_pdf():
    pdf_filename = 'dummy.pdf'
    # Check if file exists
    if not os.path.exists(os.path.join(PDF_FOLDER, pdf_filename)):
        return jsonify({'error': 'PDF not found'}), 404
    
    # Return URL for the frontend to use
    return jsonify({
        'pdf_url': f'http://127.0.0.1:5000/pdf/{pdf_filename}'
    })

# Add this route to serve the PDF file
@app.route('/pdf/dummy.pdf')
def serve_pdf(filename):
    return send_from_directory(PDF_FOLDER, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

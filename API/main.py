from flask import Flask, jsonify, request
from flask import Flask, request, jsonify, send_file
from werkzeug.exceptions import NotFound
from werkzeug.utils import secure_filename
import os

ip_public = "https://dcdc-157-100-108-85.ngrok-free.app/"
uploadimg = "upload_image"
uploadjson = "upload_json"

app = Flask(__name__)

@app.route("/")
def root():
    return "Vicente API is running"

@app.route("/download_image")
def download_image():
    image_path = "uploads/image_byte.jpg"
    return send_file(image_path, mimetype='image/jpeg')

@app.route("/download_json")
def download_json():
    json_path = "uploads/parameters.txt"
    return send_file(json_path, mimetype='text/txt')

@app.route('/upload_image', methods=['POST'])
def upload_image():
    try:
        # Guardar la imagen subida
        file = request.files['image']
        filename = secure_filename(file.filename)
        filepath = os.path.join('uploads', filename)
        file.save(filepath)

        return jsonify({'message': 'Image uploaded and results sent successfully'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/upload_json', methods=['POST'])
def upload_json():
    try:
        # Guardar la imagen subida
        file = request.files['txt']
        filename = secure_filename(file.filename)
        filepath = os.path.join('uploads', filename)
        file.save(filepath)

        return jsonify({'message': 'Txt uploaded and results sent successfully'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)



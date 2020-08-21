import os

from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from pathlib import Path
import dataset_analysis as da
import main as topsis

UPLOAD_FOLDER = Path("uploads/datasets")
ALLOWED_EXTENSIONS = {'csv'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/dataset/analysis', methods=['POST'])
def upload_file():
    file = request.files['dataset']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        response = da.main(file_path)
        return response


@app.route('/dataset/main', methods=['POST'])
def perform_mcdm():
    criteria = request.get_json()['user_criteria']
    response = jsonify(topsis.main(criteria))
    return response


if __name__ == "__main__":
    # Initialization
    UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

    # Run API
    app.run(host="localhost", port=8000, debug=True)

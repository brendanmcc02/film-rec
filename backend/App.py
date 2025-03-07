# the python flask backend service. contains methods that expose API endpoints and other utility methods.

from flask import Flask
from flask_cors import CORS
from Service import *

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://film-rec.onrender.com"}})
_service = Service()


@app.route('/verifyUserUploadedFile', methods=['POST'])
def verifyUserUploadedFile():
    global _service
    del _service
    _service = Service()
    return _service.verifyUserUploadedFile()


@app.route('/initRowsOfRecommendations')
def initRowsOfRecommendations():
    return _service.initRowsOfRecommendations()


@app.route('/reviewRecommendation')
def reviewRecommendation():
    return _service.reviewRecommendation()


@app.route('/regenerateRecommendations')
def regenerateRecommendations():
    return _service.regenerateRecommendations()


@app.route('/loadJsonFiles')
def loadJsonFiles():
    return _service.loadJsonFiles()


if __name__ == "__main__":
    app.run(host='localhost', port=60000)

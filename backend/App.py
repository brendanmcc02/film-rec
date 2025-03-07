# the python flask backend service. contains methods that expose API endpoints and other utility methods.

from flask import Flask
from flask_cors import CORS
from Service import *

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://film-rec.onrender.com"}})
service = Service()


@app.route('/verifyUserUploadedFile', methods=['POST'])
def verifyUserUploadedFile():
    global service
    del service
    service = Service()
    return service.verifyUserUploadedFile()


@app.route('/initRowsOfRecommendations')
def initRowsOfRecommendations():
    return service.initRowsOfRecommendations()


@app.route('/reviewRecommendation')
def reviewRecommendation():
    return service.reviewRecommendation()


@app.route('/regenerateRecommendations')
def regenerateRecommendations():
    return service.regenerateRecommendations()


@app.route('/loadJsonFiles')
def loadJsonFiles():
    return service.loadJsonFiles()


if __name__ == "__main__":
    app.run(host='localhost', port=60000)

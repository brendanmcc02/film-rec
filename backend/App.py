# the python flask backend service. contains methods that expose API endpoints and other utility methods.

from DocumentDatabase import *
from flask import Flask
from flask_cors import CORS
from Service import *

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://film-rec.onrender.com"}})
database = DocumentDatabase()
service = Service(database)


@app.route('/verifyUserUploadedFile', methods=['POST'])
def verifyUserUploadedFile():
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


if __name__ == "__main__":
    app.run(host='localhost', port=60000)

from DocumentDatabase import *
from flask import Flask
from flask_cors import CORS
from InitDocumentDatabase import *
from LetterboxdConversionUtilities import *
from Service import *
from ServiceUtilities import *
from VectorizeUtilities import *

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
database = DocumentDatabase("../")
letterboxdConversionUtilities = LetterboxdConversionUtilities()
initDocumentDatabase = InitDocumentDatabase()
serviceUtilities = ServiceUtilities()
vectorizeUtilities = VectorizeUtilities()
service = Service(database, serviceUtilities, vectorizeUtilities, letterboxdConversionUtilities, initDocumentDatabase)


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

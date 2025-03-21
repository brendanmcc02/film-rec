from DocumentDatabase import *
from flask import Flask
from flask_cors import CORS
from InitDatabase import *
from LetterboxdConversionUtilities import *
from Service import *
from ServiceUtilities import *
from VectorizeUtilities import *

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://film-rec.onrender.com"}})
database = DocumentDatabase("../")
letterboxdConversionUtilities = LetterboxdConversionUtilities()
initDatabase = InitDatabase(database)
serviceUtilities = ServiceUtilities()
vectorizeUtilities = VectorizeUtilities()
service = Service(database, serviceUtilities, vectorizeUtilities, letterboxdConversionUtilities, initDatabase)


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

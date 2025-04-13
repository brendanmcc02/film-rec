from DocumentDatabase import *
from flask import Flask
from flask_cors import CORS
from InitDatabase import *
from LetterboxdConversionUtilities import *
from ServiceInstance import *
from ServiceUtilities import *
from VectorizeUtilities import *

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["https://film-rec.onrender.com", "http://localhost:3000"]}})
database = DocumentDatabase("../")
letterboxdConversionUtilities = LetterboxdConversionUtilities()
initDatabase = InitDatabase(database)
serviceUtilities = ServiceUtilities()
vectorizeUtilities = VectorizeUtilities()
serviceInstance = ServiceInstance(database, serviceUtilities, vectorizeUtilities, letterboxdConversionUtilities, initDatabase)


@app.route('/getInitialRowsOfRecommendations', methods=['POST'])
def getInitialRowsOfRecommendations():
    return serviceInstance.getInitialRowsOfRecommendations()


@app.route('/reviewRecommendation')
def reviewRecommendation():
    return serviceInstance.reviewRecommendation()


@app.route('/regenerateRecommendations')
def regenerateRecommendations():
    return serviceInstance.regenerateRecommendations()


if __name__ == "__main__":
    app.run(host='localhost', port=60000)

from DocumentDatabase import *
from flask import Flask
from flask_cors import CORS
from InitDatabase import *
from LetterboxdConversionUtilities import *
from ServiceInstance import *
from ServiceUtilities import *
from VectorizeUtilities import *
import uuid

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["https://film-rec.onrender.com", "http://localhost:3000"]}})

serviceInstances = {}


@app.route('/getInitialRowsOfRecommendations', methods=['POST'])
def getInitialRowsOfRecommendations():
    guid = str(uuid.uuid4())
    database = DocumentDatabase("../")
    letterboxdConversionUtilities = LetterboxdConversionUtilities()
    initDatabase = InitDatabase(database)
    serviceUtilities = ServiceUtilities()
    vectorizeUtilities = VectorizeUtilities()
    serviceInstance = ServiceInstance(database, serviceUtilities, vectorizeUtilities, letterboxdConversionUtilities, initDatabase)

    serviceInstances[guid] = serviceInstance
    response = serviceInstances[guid].getInitialRowsOfRecommendations()

    return {"rowsOfRecommendations": response[0].get_json(), "guid": guid}, response[1]


@app.route('/reviewRecommendation')
def reviewRecommendation():
    guid = request.args.get('guid')
    return serviceInstances[guid].reviewRecommendation()


@app.route('/regenerateRecommendations')
def regenerateRecommendations():
    guid = request.args.get('guid')
    response = serviceInstances[guid].regenerateRecommendations()
    return {"rowsOfRecommendations": response[0].get_json(), "guid": guid}, response[1]


if __name__ == "__main__":
    app.run(host='localhost', port=60000)

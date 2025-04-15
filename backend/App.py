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

database = DocumentDatabase("../")
serviceUtilities = ServiceUtilities()
vectorizeUtilities = VectorizeUtilities()
letterboxdConversionUtilities = LetterboxdConversionUtilities()
initDatabase = InitDatabase(database)

serviceInstances = {}

@app.route('/getInitialRowsOfRecommendations', methods=['POST'])
def getInitialRowsOfRecommendations():
    serviceInstance = ServiceInstance(database, serviceUtilities, vectorizeUtilities, letterboxdConversionUtilities, initDatabase)
    guid = str(uuid.uuid4())
    serviceInstances[guid] = serviceInstance

    return serviceInstances[guid].getInitialRowsOfRecommendations()

@app.route('/reviewRecommendation')
def reviewRecommendation():
    guid = request.args.get('guid')
    return serviceInstances[guid].reviewRecommendation()

@app.route('/regenerateRecommendations')
def regenerateRecommendations():
    guid = request.args.get('guid')
    return serviceInstances[guid].regenerateRecommendations()


if __name__ == "__main__":
    app.run(host='localhost', port=60000)

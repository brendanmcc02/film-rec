from DocumentDatabase import *
from flask import Flask, request
from flask_cors import CORS
from ServiceInstance import ServiceInstance
from ServiceUtilities import initCachedDatabase
import uuid

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http://localhost:3000", "http://localhost:3000"]}})

database = DocumentDatabase("../")
cachedDatabase = initCachedDatabase(database)

serviceInstances = {}

@app.route('/getInitialRowsOfRecommendations', methods=['POST'])
def getInitialRowsOfRecommendations():
    guid = str(uuid.uuid4())
    serviceInstance = ServiceInstance(cachedDatabase, guid)
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

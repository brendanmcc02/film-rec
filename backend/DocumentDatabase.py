import json

class DocumentDatabase:

    # def __init__(self):

    def getAsync(self, fileName):
        try:
            file = open('../database/' + fileName + ".json")
            return json.load(file)
        except Exception:
            return None

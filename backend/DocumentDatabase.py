import json

class DocumentDatabase:

    def get(self, fileName):
        try:
            file = open('../database/' + fileName + ".json")
            return json.load(file)
        except Exception:
            return None

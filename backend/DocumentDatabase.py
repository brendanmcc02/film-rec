import json

class DocumentDatabase:

    def __init__(self, _repositoryRoot):
        self.repositoryRoot = _repositoryRoot

    def get(self, fileName):
        try:
            file = open(self.repositoryRoot + 'database/' + fileName + ".json")
            return json.load(file)
        except Exception:
            return None

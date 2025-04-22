import json

class DocumentDatabase:

    def __init__(self, repositoryRoot):
        self.repositoryRoot = repositoryRoot


    def read(self, fileName):
        try:
            file = open(self.repositoryRoot + 'database/' + fileName + ".json")
            return json.load(file)
        except Exception:
            return None
        

    def write(self, fileName, fileContent, replacements=[]):
        with open(self.repositoryRoot + 'database/' + fileName + '.json', 'w') as file:
            jsonDump = json.dumps(fileContent, indent=4, separators=(',', ': '))

            for replacement in replacements:
                jsonDump = jsonDump.replace(replacement[0], replacement[1])

            file.write(jsonDump)

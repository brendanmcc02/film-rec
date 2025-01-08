# import numpy as np
# import json
# from datetime import datetime
import os
import glob
import numpy as np
import requests
import json
import time


def main():
    cachedCountriesFile = open('../database/cached-countries.json')
    cachedCountries = json.load(cachedCountriesFile)

    newDict = {}

    for country in cachedCountries:
        newDict[country['shorthand']] = country['name']

    with open('../database/cached-countries.json', 'w') as convert_file:
        convert_file.write(json.dumps(newDict, indent=4, separators=(',', ': ')))

def getCountryFullName(cachedCountries, shorthand):
    for country in cachedCountries:
        if country['shorthand'] == shorthand:
            return country['name']
        
    return ""

if __name__ == "__main__":
    main()


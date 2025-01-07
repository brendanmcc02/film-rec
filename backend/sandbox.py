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

    cachedTmdbFile = open('../database/cached-tmdb-film-data.json')
    cachedTmdb = json.load(cachedTmdbFile)

    for entry in cachedTmdb:
        for i in range(len(cachedTmdb[entry]['countries'])):
            cachedTmdb[entry]['countries'][i] = getCountryFullName(cachedCountries, cachedTmdb[entry]['countries'][i])

    with open('../database/cached-tmdb-film-data.json', 'w') as convert_file:
        convert_file.write(json.dumps(cachedTmdb, indent=4, separators=(',', ': ')))

def getCountryFullName(cachedCountries, shorthand):
    for country in cachedCountries:
        if country['shorthand'] == shorthand:
            return country['name']
        
    return ""

if __name__ == "__main__":
    main()


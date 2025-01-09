# import numpy as np
# import json
# from datetime import datetime
import os
import glob
import urllib.error
import numpy as np
import requests
import json
import time
import urllib.request





def main():
    try:
        allFilmDataFile = open('../database/all-film-data.json')
    except FileNotFoundError:
        print("Check all-film-data.json exists.")
        raise FileNotFoundError
    allFilmData = json.load(allFilmDataFile)

    for imdbFilmId in allFilmData:
        allFilmData[imdbFilmId]['runtimeHoursMinutes'] = convertRuntimeToHoursMinutes(allFilmData[imdbFilmId]['runtime'])

    with open('../database/all-film-data.json', 'w') as convert_file:
            convert_file.write(json.dumps(allFilmData, indent=4, separators=(',', ': ')))

if __name__ == "__main__":
    main()


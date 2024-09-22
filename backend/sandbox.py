import numpy as np
import json
from datetime import datetime

def main():
    allFilmDataFile = open('../data/all-film-data.json')
    allFilmData = json.load(allFilmDataFile)
    allFilmDataKeys = list(allFilmData.keys())


if __name__ == "__main__":
    main()


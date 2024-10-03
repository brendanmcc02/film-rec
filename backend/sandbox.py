# import numpy as np
# import json
# from datetime import datetime
import os
import glob


def main():
    # allFilmDataFile = open('../data/all-film-data.json')
    # allFilmData = json.load(allFilmDataFile)
    # allFilmDataKeys = list(allFilmData.keys())

    for f in glob.glob("../data/*.csv"):
        os.remove(f)


if __name__ == "__main__":
    main()


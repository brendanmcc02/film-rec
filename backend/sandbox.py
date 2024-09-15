import numpy as np
import json


def main():
    allFilmDataFile = open('../data/all-film-data.json')
    allFilmData = json.load(allFilmDataFile)
    allFilmDataKeys = list(allFilmData.keys())

    title = allFilmData['tt4912910']['title']

    if title == "Mission: Impossible – Fallout":
        print("lfg")
    else:
        print("fuck")


if __name__ == "__main__":
    main()


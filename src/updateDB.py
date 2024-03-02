import pandas as pd
import json


def main():
    # import 5-over-10k-votes.json & my-film-data.json to variables
    allFilmData = open('../data/5-over-10k-votes.json')
    allFilmDataDict = json.load(allFilmData)
    myFilmData = open('../data/my-film-data.json')
    myFilmDataDict = json.load(myFilmData)

    # todo update the films by downloading dataset from imdb.com and adding new films

    # create a dictionary of id's of my-film-data
    myFilmIds = {}
    for film in myFilmDataDict:
        myFilmIds[film['id']] = '.'

    # remove films from all-film-data that are in my-film-data
    i = 0
    length = len(allFilmDataDict)
    while i < length:
        if allFilmDataDict[i]['id'] in myFilmIds:
            del allFilmDataDict[i]
            i = i - 1
            length = length - 1

        i = i + 1

    # write to file
    with open('../data/5-over-10k-votes.json', 'w') as convert_file:
        convert_file.write(json.dumps(allFilmDataDict, indent=4, separators=(',', ': ')))


if __name__ == "__main__":
    main()


# given ratings.csv, filter it, and then write to my-film-data.json
import json
import csv


# global constants
RUNTIME_THRESHOLD = 40


def main():
    # import ratings.csv
    myFilmData_list = []
    with open("../data/ratings.csv", 'r', encoding='utf-8', newline='') as myFilmData_file:
        reader = csv.DictReader(myFilmData_file, delimiter=',')
        for row in reader:
            myFilmData_list.append(dict(row))

    myFilmDataDict = {}  # create dict

    # for each film:
    for film in myFilmData_list:
        # filter out non-movies, <40 min runtime, and with no genres
        if film['Title Type'] == "movie" and int(film['Runtime (mins)']) >= RUNTIME_THRESHOLD and film['Genres'] != "":
            # convert genres to array
            genres = film['Genres'].replace("\"", "").split(", ")
            # map the film id to a dict of it's attributes
            try:
                myFilmDataDict[film['Const']] = {
                    "title": film['Title'],
                    "year": int(film['Year']),
                    "myRating": int(film['Your Rating']),
                    "imdbRating": float(film['IMDb Rating']),
                    "numberOfVotes": int(film['Num Votes']),
                    "runtime": int(film['Runtime (mins)']),
                    "genres": genres
                }
            except ValueError:
                print("value error with film: " + film['Const'])

    # vectorize todo


    # filter out films that the user has rated from all-film-data-vectorized.json

    # read in all-film-data-vectorized.json
    allFilmDataVecFile = open('../data/all-film-data-vectorized.json')
    allFilmDataVec = json.load(allFilmDataVecFile)
    allFilmDataKeys = list(allFilmDataVec.keys())

    allFilmDataVec_new = {}

    myFilmDataKeys = list(myFilmDataDict.keys())  # list of keys of my-film-data

    # for each film in all-film-data
    for key in allFilmDataKeys:
        # if the film has not been seen by the user
        if key not in myFilmDataKeys:
            # keep it in the dataset
            allFilmDataVec_new[key] = allFilmDataVec[key]

    # write to my-film-data-vectorized.json
    with open('../data/all-film-data-vectorized.json', 'w') as convert_file:
        convert_file.write(json.dumps(allFilmDataVec_new, indent=4, separators=(',', ': '))
                           .replace(",\n        ", ", ").replace("[\n        ", "[ ")
                           .replace("\n    ],", " ],"))


if __name__ == "__main__":
    main()

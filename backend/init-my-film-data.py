# given ratings.csv, filter it, and then write to my-film-data.json.
# filter out films that the user has rated from all-film-data.json
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

    # read in all-film-data.json
    allFilmDataFile = open('../data/all-film-data.json')
    allFilmData = json.load(allFilmDataFile)
    allFilmDataKeys = list(allFilmData.keys())

    myFilmDataDict = {}  # create dict

    # for each film:
    for film in myFilmData_list:
        # filter out non-movies, <40 min runtime, and with no genres
        if film['Title Type'] == "movie" and int(film['Runtime (mins)']) >= RUNTIME_THRESHOLD and film['Genres'] != "":
            # convert genres to array
            genres = film['Genres'].replace("\"", "").split(", ")
            # map the film id to a dict of it's attributes
            try:
                filmId = film['Const']
                if filmId in allFilmDataKeys:
                    englishTitle = allFilmData[filmId]['title']  # english title is stored in all-film-data.json
                else:
                    englishTitle = film['Title']
                myFilmDataDict[film['Const']] = {
                    "title": englishTitle,
                    "year": int(film['Year']),
                    "myRating": int(film['Your Rating']),
                    "imdbRating": float(film['IMDb Rating']),
                    "numberOfVotes": int(film['Num Votes']),
                    "runtime": int(film['Runtime (mins)']),
                    "genres": genres
                }
            except ValueError:
                print("value error with film: " + film['Const'])

    allFilmData_new = {}

    myFilmDataKeys = list(myFilmDataDict.keys())  # list of keys of my-film-data

    # filter out films that the user has rated from all-film-data.json
    for key in allFilmDataKeys:
        # if the film has not been seen by the user
        if key not in myFilmDataKeys:
            # keep it in the dataset
            allFilmData_new[key] = allFilmData[key]

    # write to all-film-data.json
    with open('../data/all-film-data.json', 'w') as convert_file:
        convert_file.write(json.dumps(allFilmData_new, indent=4, separators=(',', ': ')))

    # write to my-film-data.json
    with open('../data/my-film-data.json', 'w') as convert_file:
        convert_file.write(json.dumps(myFilmDataDict, indent=4, separators=(',', ': ')))


if __name__ == "__main__":
    main()

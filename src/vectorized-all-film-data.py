# vectorizes all-film-data.json into vectorized-all-film-data.json

# python files
import settings
# libraries
import json
import datetime


def main():
    # read in all-film-data.json
    allFilmDataFile = open('../data/all-film-data.json')
    allFilmData = json.load(allFilmDataFile)

    MAX_YEAR = int(datetime.datetime.now().year)  # get the current year

    vectorized_all_film_data = {}  # init the dictionary

    # get max & min imdbRating, and list of all film genres
    MAX_IMDB_RATING = allFilmData[0]['imdbRating']
    MIN_IMDB_RATING = allFilmData[0]['imdbRating']
    allGenres = []
    for film in allFilmData:
        for genre in film['genres']:
            if genre not in allGenres:
                allGenres.append(genre)

        MAX_IMDB_RATING = max(MAX_IMDB_RATING, film['imdbRating'])
        MIN_IMDB_RATING = min(MIN_IMDB_RATING, film['imdbRating'])

    # the max of my-film-data is almost certainly higher than the max of all-film-data (because films I have
    # rated have been taken out of all-film-data, and I've seen TDK, Shawshank, godfather, etc.)
    minMax_myFilmData = getMinMaxImdbRatingMyFilmData()
    MAX_IMDB_RATING = max(MAX_IMDB_RATING, minMax_myFilmData[1])
    # the min of my-film-data is almost certainly higher than the min of all-film-data, but still good
    # practice to do anyway
    MIN_IMDB_RATING = min(MIN_IMDB_RATING, minMax_myFilmData[0])
    allGenres = sorted(allGenres)  # sort alphabetically

    # perform some pre-computation to avoid repetitive computation
    year_diff = MAX_YEAR - settings.MIN_YEAR
    imdbRating_diff = MAX_IMDB_RATING - MIN_IMDB_RATING
    min_year = settings.MIN_YEAR

    # pre compute year_norm for each year
    year_norms = {}
    for y in range(min_year, MAX_YEAR + 1):
        year_norms[y] = round((y - min_year) / year_diff, 4)

    # for each film:
    for film in allFilmData:
        vectorList = []
        # 1. normalise the year
        vectorList.append(year_norms[film['year']])
        # 2. normalise imdbRating
        imdbRating_norm = round((film['imdbRating'] - MIN_IMDB_RATING) / imdbRating_diff, 4)
        vectorList.append(imdbRating_norm)
        # 3. one-hot encoding on genres
        oneHotEncode(vectorList, film['genres'], allGenres)
        # add to dictionary
        vectorized_all_film_data[film['id']] = vectorList

    # write to file
    with open('../data/vectorized-all-film-data.json', 'w') as convert_file:
        convert_file.write(json.dumps(vectorized_all_film_data, indent=4, separators=(',', ': '))
                           .replace(",\n        ", ", ").replace("[\n        ", "[ ")
                           .replace("\n    ],", " ],"))


# returns the min and max imdbRating in my-film-data
# return type: tuple. index 0 = min, index 1 = max.
def getMinMaxImdbRatingMyFilmData():
    # read in my-film-data.json
    myFilmDataFile = open('../data/my-film-data.json')
    myFilmData = json.load(myFilmDataFile)

    minImdbRating = myFilmData[0]['imdbRating']
    maxImdbRating = myFilmData[0]['imdbRating']

    for film in myFilmData:
        minImdbRating = min(minImdbRating, film['imdbRating'])
        maxImdbRating = max(maxImdbRating, film['imdbRating'])

    return minImdbRating, maxImdbRating


def oneHotEncode(vectorList, filmGenres, allGenres):
    for g in allGenres:
        if g in filmGenres:
            vectorList.append(1)
        else:
            vectorList.append(0)


if __name__ == "__main__":
    main()

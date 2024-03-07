# vectorizes both all-film-data.json & my-film-data.json into
# vectorized-all-film-data.json & vectorized-my-film-data.json respectively

# python files
import settings
# libraries
import json
import datetime

# global variables
MIN_IMDB_RATING = 0.0


def main():
    global MIN_IMDB_RATING
    # read in all-film-data.json & my-film-data.json
    allFilmDataFile = open('../data/all-film-data.json')
    allFilmData = json.load(allFilmDataFile)
    myFilmDataFile = open('../data/my-film-data.json')
    myFilmData = json.load(myFilmDataFile)

    MAX_YEAR = int(datetime.datetime.now().year)  # get the current year

    vectorized_all_film_data = {}  # init the dictionary
    vectorized_my_film_data = {}  # init the dictionary

    # get max & min imdbRating of all-film-data, and list of all film genres
    MAX_IMDB_RATING = allFilmData[0]['imdbRating']
    MIN_IMDB_RATING = allFilmData[0]['imdbRating']
    allGenres = []
    for film in allFilmData:
        for genre in film['genres']:
            if genre not in allGenres:
                allGenres.append(genre)

        MAX_IMDB_RATING = max(MAX_IMDB_RATING, film['imdbRating'])
        MIN_IMDB_RATING = min(MIN_IMDB_RATING, film['imdbRating'])

    # the max of all-film-data is almost certainly lower than the max of my-film-data (recall that I remove films from
    # all-film-data that I have seen before, so Shawshank, TDK, etc. wouldn't be in all-film-data).
    # the min of all-film-data is almost certainly lower than the min of my-film-data,
    # still good practice to check anyway.
    for film in myFilmData:
        MIN_IMDB_RATING = min(MIN_IMDB_RATING, film['imdbRating'])
        MAX_IMDB_RATING = max(MAX_IMDB_RATING, film['imdbRating'])

    allGenres = sorted(allGenres)  # sort alphabetically

    # perform some pre-computation to avoid repetitive computation
    year_diff = MAX_YEAR - settings.MIN_YEAR
    imdbRating_diff = MAX_IMDB_RATING - MIN_IMDB_RATING
    min_year = settings.MIN_YEAR

    # pre compute year_norm for each year
    year_norms = {}
    for y in range(min_year, MAX_YEAR + 1):
        year_norms[y] = round((y - min_year) / year_diff, 4)

    # vectorize all-film-data
    for film in allFilmData:
        vectorList = vectorize(film, year_norms, imdbRating_diff, allGenres)
        # add to dictionary
        vectorized_all_film_data[film['id']] = vectorList

    # write to vectorized-all-film-data.json
    with open('../data/vectorized-all-film-data.json', 'w') as convert_file:
        convert_file.write(json.dumps(vectorized_all_film_data, indent=4, separators=(',', ': '))
                           .replace(",\n        ", ", ").replace("[\n        ", "[ ")
                           .replace("\n    ],", " ],"))

    # vectorize my-film-data
    for film in myFilmData:
        vectorList = vectorize(film, year_norms, imdbRating_diff, allGenres)
        # add to dictionary
        vectorized_my_film_data[film['id']] = vectorList

    # write to vectorized-my-film-data.json
    with open('../data/vectorized-my-film-data.json', 'w') as convert_file:
        convert_file.write(json.dumps(vectorized_my_film_data, indent=4, separators=(',', ': '))
                           .replace(",\n        ", ", ").replace("[\n        ", "[ ")
                           .replace("\n    ],", " ],"))


# given a film, return it's vectorized form (return type: list)
def vectorize(film, year_norms, imdbRating_diff, allGenres):
    vectorList = []
    # 1. normalise the year
    vectorList.append(year_norms[film['year']])
    # 2. normalise imdbRating
    imdbRating_norm = round((film['imdbRating'] - MIN_IMDB_RATING) / imdbRating_diff, 4)
    vectorList.append(imdbRating_norm)
    # 3. one-hot encoding on genres
    oneHotEncode(vectorList, film['genres'], allGenres)

    return vectorList


# given a vector, append the one-hot encoding of genres to the vector
def oneHotEncode(vectorList, filmGenres, allGenres):
    for g in allGenres:
        if g in filmGenres:
            vectorList.append(1)
        else:
            vectorList.append(0)


if __name__ == "__main__":
    main()

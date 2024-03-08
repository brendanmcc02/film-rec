# vectorizes both all-film-data.json & my-film-data.json into
# all-film-data-vectorized.json & my-film-data-vectorized.json respectively.

# libraries
import json
import datetime

# global variables
MIN_IMDB_RATING = 0.0
MIN_YEAR = 0


def main():
    global MIN_IMDB_RATING
    global MIN_YEAR
    # read in all-film-data.json & my-film-data.json
    allFilmDataFile = open('../data/all-film-data.json')
    allFilmData = json.load(allFilmDataFile)
    allFilmDataKeys = list(allFilmData.keys())
    myFilmDataFile = open('../data/my-film-data.json')
    myFilmData = json.load(myFilmDataFile)
    myFilmDataKeys = list(myFilmData.keys())

    MAX_YEAR = int(datetime.datetime.now().year)  # get the current year

    vectorized_all_film_data = {}  # init the dictionary
    vectorized_my_film_data = {}  # init the dictionary

    # get min & max imdbRating & min_year of all-film-data, and get a (unique) list of all genres
    MIN_IMDB_RATING = allFilmData[allFilmDataKeys[0]]['imdbRating']
    MAX_IMDB_RATING = allFilmData[allFilmDataKeys[0]]['imdbRating']
    MIN_YEAR = allFilmData[allFilmDataKeys[0]]['year']
    MIN_MY_RATING = myFilmData[myFilmDataKeys[0]]['myRating']
    MAX_MY_RATING = myFilmData[myFilmDataKeys[0]]['myRating']

    allGenres = []
    for key in allFilmDataKeys:
        # if a genre is not in allGenres yet, append it
        for genre in allFilmData[key]['genres']:
            if genre not in allGenres:
                allGenres.append(genre)

        # modify max & min imdbRatings
        MAX_IMDB_RATING = max(MAX_IMDB_RATING, allFilmData[key]['imdbRating'])
        MIN_IMDB_RATING = min(MIN_IMDB_RATING, allFilmData[key]['imdbRating'])
        # modify min year
        MIN_YEAR = min(MIN_YEAR, allFilmData[key]['year'])

    # the max imdbRating of all-film-data is almost certainly lower than the max of my-film-data (recall
    # that I remove films from all-film-data that I have seen before, so Shawshank, TDK, etc. wouldn't be in
    # all-film-data).
    # the min imdbRating of all-film-data is almost certainly lower than the min of my-film-data,
    # still good practice to check anyway.
    # the min year of all-film-data is almost certainly lower than the min year of my-film-data,
    # still good practice to check anyway.
    for key in myFilmDataKeys:
        MIN_IMDB_RATING = min(MIN_IMDB_RATING, myFilmData[key]['imdbRating'])
        MAX_IMDB_RATING = max(MAX_IMDB_RATING, myFilmData[key]['imdbRating'])
        MIN_YEAR = min(MIN_YEAR, myFilmData[key]['year'])
        MIN_MY_RATING = min(MIN_MY_RATING, myFilmData[key]['myRating'])
        MAX_MY_RATING = max(MAX_MY_RATING, myFilmData[key]['myRating'])

    allGenres = sorted(allGenres)  # sort alphabetically

    # perform some pre-computation to avoid repetitive computation
    DIFF_YEAR = MAX_YEAR - MIN_YEAR
    DIFF_IMDB_RATING = MAX_IMDB_RATING - MIN_IMDB_RATING
    DIFF_MY_RATING = MAX_MY_RATING - MIN_MY_RATING

    # pre-compute normalised years for each year
    year_norms = {}
    for y in range(MIN_YEAR, MAX_YEAR + 1):
        year_norms[y] = (y - MIN_YEAR) / DIFF_YEAR

    # for each film in all-film-data:
    for key in allFilmDataKeys:
        # vectorize the film
        vector = vectorize(allFilmData[key], year_norms, DIFF_IMDB_RATING, allGenres)
        # add to dictionary
        vectorized_all_film_data[key] = vector

    # write to all-film-data-vectorized.json
    with open('../data/all-film-data-vectorized.json', 'w') as convert_file:
        convert_file.write(json.dumps(vectorized_all_film_data, indent=4, separators=(',', ': '))
                           .replace(",\n        ", ", ").replace("[\n        ", "[ ")
                           .replace("\n    ],", " ],"))

    # vectorize my-film-data
    for key in myFilmDataKeys:
        # vectorize the film
        vector = vectorize(myFilmData[key], year_norms, DIFF_IMDB_RATING, allGenres)
        # normalize myRating
        myRating_norm = (myFilmData[key]['myRating'] - MIN_MY_RATING) / DIFF_MY_RATING
        # scalar multiply by myRating
        len_vector = len(vector)
        for i in range(0, len_vector):
            vector[i] = vector[i] * myRating_norm
        # add to dictionary
        vectorized_my_film_data[key] = vector

    # write to my-film-data-vectorized.json
    with open('../data/my-film-data-vectorized.json', 'w') as convert_file:
        convert_file.write(json.dumps(vectorized_my_film_data, indent=4, separators=(',', ': '))
                           .replace(",\n        ", ", ").replace("[\n        ", "[ ")
                           .replace("\n    ],", " ],"))


# given a film, return it's vectorized form (return type: list)
def vectorize(film, year_norms, imdbRating_diff, allGenres):
    vector = []
    # 1. normalise the year
    year_norm = year_norms[film['year']] * 0.5
    vector.append(year_norm)
    # 2. normalise imdbRating
    imdbRating_norm = ((film['imdbRating'] - MIN_IMDB_RATING) / imdbRating_diff) * 1.0
    vector.append(imdbRating_norm)
    # 3. one-hot encoding on genres
    oneHotEncode(vector, film['genres'], allGenres)

    return vector


# given a vector, append the one-hot encoding of genres to the vector
def oneHotEncode(vector, filmGenres, allGenres):
    for g in allGenres:
        if g in filmGenres:
            vector.append(1)
        else:
            vector.append(0)

    return vector


if __name__ == "__main__":
    main()

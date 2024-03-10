# vectorizes both all-film-data.json & my-film-data.json into
# all-film-data-vectorized.json & my-film-data-vectorized.json respectively.

# libraries
import json
import datetime

# global variables
MIN_IMDB_RATING = 0.0
MIN_YEAR = 0
MIN_NUMBER_OF_VOTES = 0
MIN_RUNTIME = 0
DIFF_IMDB_RATING = 0.0
DIFF_YEAR = 0
DIFF_NUMBER_OF_VOTES = 0
DIFF_RUNTIME = 0
year_norms = {}


def main():
    global MIN_IMDB_RATING
    global MIN_YEAR
    global MIN_NUMBER_OF_VOTES
    global MIN_RUNTIME
    global DIFF_IMDB_RATING
    global DIFF_YEAR
    global DIFF_NUMBER_OF_VOTES
    global DIFF_RUNTIME
    global year_norms
    # read in all-film-data.json & my-film-data.json
    allFilmDataFile = open('../data/all-film-data.json')
    allFilmData = json.load(allFilmDataFile)
    allFilmDataKeys = list(allFilmData.keys())
    myFilmDataFile = open('../data/my-film-data.json')
    myFilmData = json.load(myFilmDataFile)
    myFilmDataKeys = list(myFilmData.keys())

    vectorized_all_film_data = {}  # init the dictionary
    vectorized_my_film_data = {}   # init the dictionary

    # initialise the min & max values of various attributes
    MIN_IMDB_RATING = allFilmData[allFilmDataKeys[0]]['imdbRating']
    MAX_IMDB_RATING = allFilmData[allFilmDataKeys[0]]['imdbRating']
    MIN_YEAR = allFilmData[allFilmDataKeys[0]]['year']
    MAX_YEAR = allFilmData[allFilmDataKeys[0]]['year']
    MIN_MY_RATING = myFilmData[myFilmDataKeys[0]]['myRating']
    MAX_MY_RATING = myFilmData[myFilmDataKeys[0]]['myRating']
    MIN_NUMBER_OF_VOTES = myFilmData[myFilmDataKeys[0]]['numberOfVotes']
    MAX_NUMBER_OF_VOTES = myFilmData[myFilmDataKeys[0]]['numberOfVotes']
    MIN_RUNTIME = myFilmData[myFilmDataKeys[0]]['runtime']
    MAX_RUNTIME = myFilmData[myFilmDataKeys[0]]['runtime']

    # get a list of unique genres
    allGenres = []
    for key in allFilmDataKeys:
        # if a genre is not in allGenres yet, append it
        for genre in allFilmData[key]['genres']:
            if genre not in allGenres:
                allGenres.append(genre)

        # modify min & max of the various attributes
        MIN_IMDB_RATING = min(MIN_IMDB_RATING, allFilmData[key]['imdbRating'])
        MAX_IMDB_RATING = max(MAX_IMDB_RATING, allFilmData[key]['imdbRating'])
        MIN_YEAR = min(MIN_YEAR, allFilmData[key]['year'])
        MAX_YEAR = max(MAX_YEAR, allFilmData[key]['year'])
        MIN_NUMBER_OF_VOTES = min(MIN_NUMBER_OF_VOTES, allFilmData[key]['numberOfVotes'])
        MAX_NUMBER_OF_VOTES = max(MAX_NUMBER_OF_VOTES, allFilmData[key]['numberOfVotes'])
        MIN_RUNTIME = min(MIN_RUNTIME, allFilmData[key]['runtime'])
        MAX_RUNTIME = max(MAX_RUNTIME, allFilmData[key]['runtime'])

    allGenres = sorted(allGenres)  # sort alphabetically

    # iterate through my-film-data and alter the min & max values to ensure they are the same across both datasets
    for key in myFilmDataKeys:
        MIN_IMDB_RATING = min(MIN_IMDB_RATING, myFilmData[key]['imdbRating'])
        MAX_IMDB_RATING = max(MAX_IMDB_RATING, myFilmData[key]['imdbRating'])
        MIN_YEAR = min(MIN_YEAR, myFilmData[key]['year'])
        MAX_YEAR = max(MAX_YEAR, myFilmData[key]['year'])
        MIN_MY_RATING = min(MIN_MY_RATING, myFilmData[key]['myRating'])
        MAX_MY_RATING = max(MAX_MY_RATING, myFilmData[key]['myRating'])
        MIN_NUMBER_OF_VOTES = min(MIN_NUMBER_OF_VOTES, myFilmData[key]['numberOfVotes'])
        MAX_NUMBER_OF_VOTES = max(MAX_NUMBER_OF_VOTES, myFilmData[key]['numberOfVotes'])
        MIN_RUNTIME = min(MIN_RUNTIME, myFilmData[key]['runtime'])
        MAX_RUNTIME = max(MAX_RUNTIME, myFilmData[key]['runtime'])

    # perform some pre-computation to avoid repetitive computation
    DIFF_IMDB_RATING = MAX_IMDB_RATING - MIN_IMDB_RATING
    DIFF_YEAR = MAX_YEAR - MIN_YEAR
    DIFF_MY_RATING = MAX_MY_RATING - MIN_MY_RATING
    DIFF_NUMBER_OF_VOTES = MAX_NUMBER_OF_VOTES - MIN_NUMBER_OF_VOTES
    DIFF_RUNTIME = MAX_RUNTIME - MIN_RUNTIME

    # pre-compute normalised years for each year
    for y in range(MIN_YEAR, MAX_YEAR + 1):
        year_norms[y] = (y - MIN_YEAR) / DIFF_YEAR

    # for each film in all-film-data:
    for key in allFilmDataKeys:
        # vectorize the film
        vector = vectorize(allFilmData[key], allGenres)
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
        vector = vectorize(myFilmData[key], allGenres)
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
def vectorize(film, allGenres):
    vector = []
    # 1. normalise the year; apply weight
    # from experimenting, 0.3 was a very good weight as it did not overvalue the year, but still took it into account.
    year_norm = year_norms[film['year']] * 0.3
    vector.append(year_norm)
    # 2. normalise imdbRating
    imdbRating_norm = (film['imdbRating'] - MIN_IMDB_RATING) / DIFF_IMDB_RATING
    vector.append(imdbRating_norm)
    # 3. normalise numberOfVotes; apply weight
    numberOfVotes_norm = ((film['numberOfVotes'] - MIN_NUMBER_OF_VOTES) / DIFF_NUMBER_OF_VOTES) * 0.3
    vector.append(numberOfVotes_norm)
    # 4. normalise runtime; apply weight
    runtime_norm = ((film['runtime'] - MIN_RUNTIME) / DIFF_RUNTIME) * 0.3
    vector.append(runtime_norm)
    # 5. one-hot encoding on genres
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

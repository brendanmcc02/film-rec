# given ratings.csv, vectorize both myFilmData & allFilmData, and then recommend 20 films

# imports
from flask import Flask, request
import json
import csv
import numpy as np

# global constants
RUNTIME_THRESHOLD = 40
MIN_IMDB_RATING = 0.0
MIN_YEAR = 0
MIN_NUMBER_OF_VOTES = 0
MIN_RUNTIME = 0
DIFF_IMDB_RATING = 0.0
DIFF_YEAR = 0
DIFF_NUMBER_OF_VOTES = 0
DIFF_RUNTIME = 0
year_norms = {}
VECTOR_LENGTH = 27

app = Flask(__name__)


@app.route('/verifyFile', methods=['POST'])
# verifies user-uploaded ratings.csv
def verifyFile():
    # check if there's a file in the post request
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']

    file.save("../data/" + file.filename)  # write to file

    # list of expected attributes of each film object; error handling.
    filmAttributes = ["Const", "Your Rating", "Date Rated", "Title", "URL", "Title Type", "IMDb Rating",
                      "Runtime (mins)", "Year", "Genres", "Num Votes", "Release Date", "Directors"]

    try:
        with open("../data/ratings.csv", newline='') as myFilmData_file:
            reader = csv.DictReader(myFilmData_file, delimiter=',', restkey='unexpectedData')

            for row in reader:
                # if there are more data than row headers:
                if 'unexpectedData' in row:
                    return "Error: ratings.csv does not conform to expected format.\n", 400

                # if any of the expected row headers are not to be found:
                keys = list(row.keys())
                for k in keys:
                    if k not in filmAttributes:
                        return "Error: Row headers in ratings.csv does not conform to expected format.\n", 400

        # ratings.csv has no issues
        return "Upload Success.", 200
    except FileNotFoundError:
        return "Error: ratings.csv not found, check file name & file type.", 404
    except Exception as e:
        return "Error occurred with reading ratings.csv.\n" + str(e), 400


@app.route('/rec')
# recommend films to user
def rec():
    # read in the file and append to list data structure
    try:
        myFilmData_list = []
        with open("../data/ratings.csv", newline='') as myFilmData_file:
            reader = csv.DictReader(myFilmData_file, delimiter=',', restkey='unexpectedData')

            for row in reader:
                myFilmData_list.append(row)
    except Exception as e:
        return "Error occurred with reading ratings.csv.\n" + str(e)

    # read in all-film-data.json
    allFilmDataFile = open('../data/all-film-data.json')
    allFilmData_temp = json.load(allFilmDataFile)
    allFilmDataKeys = list(allFilmData_temp.keys())

    myFilmData = {}  # init as a dict

    # for each film in ratings.csv:
    for film in myFilmData_list:
        # filter out non-movies, <40 min runtime, and with no genres
        if film['Title Type'] == "movie" and int(film['Runtime (mins)']) >= RUNTIME_THRESHOLD and film['Genres'] != "":
            # convert genres to array
            genres = film['Genres'].replace("\"", "").split(", ")
            # map the film id to a dict of it's attributes
            try:
                filmId = film['Const']
                # if the current film is also in all-film-data.json
                if filmId in allFilmDataKeys:
                    englishTitle = allFilmData_temp[filmId]['title']  # use the english title
                else:
                    # otherwise, use the title stored in ratings.csv (potentially non-english)
                    englishTitle = film['Title']

                myFilmData[film['Const']] = {
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

    allFilmData = {}  # init new allFilmDataDict

    myFilmDataKeys = list(myFilmData.keys())  # list of keys of my-film-data

    # these variables are globals because they are used in vectorize()
    global MIN_IMDB_RATING
    global MIN_YEAR
    global MIN_NUMBER_OF_VOTES
    global MIN_RUNTIME
    global DIFF_IMDB_RATING
    global DIFF_YEAR
    global DIFF_NUMBER_OF_VOTES
    global DIFF_RUNTIME
    global year_norms

    # initialise the min & max values of various attributes;
    # this is needed for normalising vector values.
    MIN_IMDB_RATING = allFilmData_temp[allFilmDataKeys[0]]['imdbRating']
    MAX_IMDB_RATING = allFilmData_temp[allFilmDataKeys[0]]['imdbRating']
    MIN_YEAR = allFilmData_temp[allFilmDataKeys[0]]['year']
    MAX_YEAR = allFilmData_temp[allFilmDataKeys[0]]['year']
    MIN_NUMBER_OF_VOTES = allFilmData_temp[allFilmDataKeys[0]]['numberOfVotes']
    MAX_NUMBER_OF_VOTES = allFilmData_temp[allFilmDataKeys[0]]['numberOfVotes']
    MIN_RUNTIME = allFilmData_temp[allFilmDataKeys[0]]['runtime']
    MAX_RUNTIME = allFilmData_temp[allFilmDataKeys[0]]['runtime']

    allGenres = []  # get a list of unique genres

    # iterate through each film in allFilmData:
    for key in allFilmDataKeys:
        # take films out from allFilmData that the user has seen; we don't want to recommend films that the user
        # has seen before.
        if key not in myFilmDataKeys:
            # add it to a new, filtered allFilmData dict
            allFilmData[key] = allFilmData_temp[key]

        # if a genre is not in allGenres yet, append it
        for genre in allFilmData_temp[key]['genres']:
            if genre not in allGenres:
                allGenres.append(genre)

        # modify min & max of the various attributes
        MIN_IMDB_RATING = min(MIN_IMDB_RATING, allFilmData_temp[key]['imdbRating'])
        MAX_IMDB_RATING = max(MAX_IMDB_RATING, allFilmData_temp[key]['imdbRating'])
        MIN_YEAR = min(MIN_YEAR, allFilmData_temp[key]['year'])
        MAX_YEAR = max(MAX_YEAR, allFilmData_temp[key]['year'])
        MIN_NUMBER_OF_VOTES = min(MIN_NUMBER_OF_VOTES, allFilmData_temp[key]['numberOfVotes'])
        MAX_NUMBER_OF_VOTES = max(MAX_NUMBER_OF_VOTES, allFilmData_temp[key]['numberOfVotes'])
        MIN_RUNTIME = min(MIN_RUNTIME, allFilmData_temp[key]['runtime'])
        MAX_RUNTIME = max(MAX_RUNTIME, allFilmData_temp[key]['runtime'])

    allGenres = sorted(allGenres)  # sort alphabetically

    # create a new list of allFilmData keys after filtering some films out of allFilmData_temp
    allFilmDataKeys = list(allFilmData.keys())

    # init dicts for vectorized allFilmData & myFilmData
    allFilmDataVec = {}
    myFilmDataVec = {}

    # iterate through my-film-data and alter the min & max values to ensure they are the same across both datasets
    for key in myFilmDataKeys:
        MIN_IMDB_RATING = min(MIN_IMDB_RATING, myFilmData[key]['imdbRating'])
        MAX_IMDB_RATING = max(MAX_IMDB_RATING, myFilmData[key]['imdbRating'])
        MIN_YEAR = min(MIN_YEAR, myFilmData[key]['year'])
        MAX_YEAR = max(MAX_YEAR, myFilmData[key]['year'])
        MIN_NUMBER_OF_VOTES = min(MIN_NUMBER_OF_VOTES, myFilmData[key]['numberOfVotes'])
        MAX_NUMBER_OF_VOTES = max(MAX_NUMBER_OF_VOTES, myFilmData[key]['numberOfVotes'])
        MIN_RUNTIME = min(MIN_RUNTIME, myFilmData[key]['runtime'])
        MAX_RUNTIME = max(MAX_RUNTIME, myFilmData[key]['runtime'])

    # perform some pre-computation to avoid repetitive computation
    DIFF_IMDB_RATING = MAX_IMDB_RATING - MIN_IMDB_RATING
    DIFF_YEAR = MAX_YEAR - MIN_YEAR
    DIFF_NUMBER_OF_VOTES = MAX_NUMBER_OF_VOTES - MIN_NUMBER_OF_VOTES
    DIFF_RUNTIME = MAX_RUNTIME - MIN_RUNTIME

    # pre-compute normalised years for each year
    for y in range(MIN_YEAR, MAX_YEAR + 1):
        year_norms[y] = (y - MIN_YEAR) / DIFF_YEAR

    # vectorize all-film-data
    for key in allFilmDataKeys:
        # vectorize the film
        vector = vectorize(allFilmData[key], allGenres)
        # add to dict
        allFilmDataVec[key] = vector

    # vectorize my-film-data
    for key in myFilmDataKeys:
        # vectorize the film
        vector = vectorize(myFilmData[key], allGenres)
        # scalar multiply by myRating
        len_vector = len(vector)
        for i in range(0, len_vector):
            vector[i] *= (myFilmData[key]['myRating'] / 10.0)
        # add to dict
        myFilmDataVec[key] = vector

    global VECTOR_LENGTH

    VECTOR_LENGTH = len(myFilmDataVec[myFilmDataKeys[0]])  # length of each vector

    weightedAverageSum = 0.0  # init to some temp value

    # create user profile based on my-film-data-vectorized:

    userProfileList = [0.0] * VECTOR_LENGTH  # initialise a list to have 0 in each entry
    # convert from list to vector; this is a zero-vector of length VECTOR_LENGTH
    userProfile = np.array(userProfileList)
    for key in myFilmDataKeys:
        # sum the (already weighted) vectors together
        userProfile += myFilmDataVec[key]
        # increment the weighted average
        weightedAverageSum += (myFilmData[key]['myRating'] / 10.0)

    # divide the userProfile vector by the weighted average
    userProfile = np.divide(userProfile, weightedAverageSum)

    normaliseGenres(userProfile)

    # Similarity dict:
    # key = filmId, value = similarity to userProfile (float; 0-100)
    similarities = {}

    # for each film in all-film-data-vectorized
    for filmId in allFilmDataKeys:
        # calculate similarity to userProfile
        similarities[filmId] = cosineSimilarity(allFilmDataVec[filmId], userProfile)

    # sort similarities in descending order.
    similarities = sorted(similarities.items(), key=lambda x: x[1], reverse=True)

    result = []

    for i in range(0, 20):
        filmId = similarities[i][0]
        film = allFilmData[filmId]
        similarity_score = similarities[i][1]
        film['similarity_score'] = similarity_score
        result.append(film)

    return result


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
    # 3. normalise numberOfVotes
    numberOfVotes_norm = (film['numberOfVotes'] - MIN_NUMBER_OF_VOTES) / DIFF_NUMBER_OF_VOTES
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


# gets the cosine similarity between two vectors
def cosineSimilarity(A, B):
    return np.dot(A, B) / (np.linalg.norm(A) * np.linalg.norm(B))


# given a user profile vector, normalise the genres
# for example, if drama is the highest rated genre with a score of 0.4, make the value 1.0 and then scale
# the other genres accordingly.
# after the genres are normalised, I apply a weight of 0.68 to all genres. See comments below.
def normaliseGenres(userProfile):
    # normalise the genres in the user profile
    MIN_GENRE_VALUE = userProfile[4]
    MAX_GENRE_VALUE = userProfile[4]

    for i in range(4, VECTOR_LENGTH):
        MIN_GENRE_VALUE = min(MIN_GENRE_VALUE, userProfile[i])
        MAX_GENRE_VALUE = max(MAX_GENRE_VALUE, userProfile[i])

    DIFF_GENRE = MAX_GENRE_VALUE - MIN_GENRE_VALUE

    for i in range(4, VECTOR_LENGTH):
        userProfile[i] = (userProfile[i] - MIN_GENRE_VALUE) / DIFF_GENRE  # normalise the genres
        # from experimenting (year_norm weight was fixed at 0.3), ~0.75 was a good sweet spot in the sense that
        # it picked both single- and multi-genre films. The algorithm still heavily favoured the 4 genres that had the
        # highest weighing, but this is expected and good behaviour.
        userProfile[i] = userProfile[i] * 0.75


# todo temp
def stringifyFilm(film, similarity, vector):
    return (film['title'] + " (" + str(film['year']) + "). " + str(film['imdbRating']) + " Genres: " +
            str(film['genres']) + " (" + str(round(similarity * 100.0, 2)) + "% match)\n" + str(vector) + "\n")


if __name__ == "__main__":
    app.run(host='localhost', port=60000)

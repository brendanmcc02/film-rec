# given ratings.csv, vectorize both myFilmData & allFilmData, and then recommend N films

# imports
from flask import Flask, request, jsonify
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
YEAR_NORMS = {}
VECTOR_LENGTH = 27
NUM_RECS = 10
NUM_WILDCARDS = 2
TOTAL_RECS = NUM_RECS + NUM_WILDCARDS
FEEDBACK_FACTOR = 0.05  # the rate at which feedback changes the user profile
WILDCARD_FEEDBACK_FACTOR = 0.2  # the rate at which wildcard recs affect the wildcard profile
# from experimenting (yearNorm weight was fixed at 0.3), ~0.75 was a good sweet spot in the sense that
# it picked both single- and multi-genre films. The algorithm still heavily favoured the 4 genres that had the
# highest weighing, but this is expected and good behaviour.
GENRE_WEIGHT = 0.75
# from experimenting, 0.3 was a very good weight as it did not overvalue the year, but still took it into account.
YEAR_WEIGHT = 0.3
RUNTIME_WEIGHT = 0.3


# global variables
userProfile = np.zeros(VECTOR_LENGTH)
profileChanges = []
wildcardProfile = np.zeros(VECTOR_LENGTH)
allFilmData = {}
allFilmDataVec = {}
recs = []
recStates = [0] * TOTAL_RECS

app = Flask(__name__)


# verifies that user-uploaded ratings.csv is ok
@app.route('/verifyFile', methods=['POST'])
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
        with open("../data/ratings.csv", newline='') as myFilmDataFile:
            reader = csv.DictReader(myFilmDataFile, delimiter=',', restkey='unexpectedData')

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


# initial recommendation of films to user
@app.route('/initRec')
def initRec():
    global VECTOR_LENGTH
    global profileChanges

    # init profileChanges vector
    for i in range(0, TOTAL_RECS):
        profileChanges.append(np.zeros(VECTOR_LENGTH))

    # read in the file and append to list data structure
    try:
        myFilmDataList = []
        with open("../data/ratings.csv", newline='') as myFilmDataFile:
            reader = csv.DictReader(myFilmDataFile, delimiter=',', restkey='unexpectedData')

            for row in reader:
                myFilmDataList.append(row)
    except Exception as e:
        return "Error occurred with reading ratings.csv.\n" + str(e)

    # read in all-film-data.json
    allFilmDataFile = open('../data/all-film-data.json')
    allFilmDataFull = json.load(allFilmDataFile)
    allFilmDataKeys = list(allFilmDataFull.keys())

    myFilmData = {}  # init as a dict

    # for each film in ratings.csv:
    for film in myFilmDataList:
        # filter out non-movies, <40 min runtime, and with no genres
        if film['Title Type'] == "movie" and int(film['Runtime (mins)']) >= RUNTIME_THRESHOLD and film['Genres'] != "":
            # convert genres to array
            genres = film['Genres'].replace("\"", "").split(", ")
            # map the film id to a dict of it's attributes
            try:
                filmId = film['Const']
                # if the current film is also in all-film-data.json
                if filmId in allFilmDataKeys:
                    englishTitle = allFilmDataFull[filmId]['title']  # use the english title
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
                return ("value error with film: " + film['Const']), 400

    global allFilmData

    myFilmDataKeys = list(myFilmData.keys())  # list of keys of my-film-data

    global MIN_IMDB_RATING
    global MIN_YEAR
    global MIN_NUMBER_OF_VOTES
    global MIN_RUNTIME
    global DIFF_IMDB_RATING
    global DIFF_YEAR
    global DIFF_NUMBER_OF_VOTES
    global DIFF_RUNTIME
    global YEAR_NORMS

    # initialise the min & max values of various attributes;
    # this is needed for normalising vector values.
    MIN_IMDB_RATING = allFilmDataFull[allFilmDataKeys[0]]['imdbRating']
    MAX_IMDB_RATING = allFilmDataFull[allFilmDataKeys[0]]['imdbRating']
    MIN_YEAR = allFilmDataFull[allFilmDataKeys[0]]['year']
    MAX_YEAR = allFilmDataFull[allFilmDataKeys[0]]['year']
    MIN_NUMBER_OF_VOTES = allFilmDataFull[allFilmDataKeys[0]]['numberOfVotes']
    MAX_NUMBER_OF_VOTES = allFilmDataFull[allFilmDataKeys[0]]['numberOfVotes']
    MIN_RUNTIME = allFilmDataFull[allFilmDataKeys[0]]['runtime']
    MAX_RUNTIME = allFilmDataFull[allFilmDataKeys[0]]['runtime']

    allGenres = []  # get a list of unique genres

    # iterate through each film in allFilmData:
    for key in allFilmDataKeys:
        # take films out from allFilmData that the user has seen; we don't want to recommend films that the user
        # has seen before.
        if key not in myFilmDataKeys:
            # add it to a new, filtered allFilmData dict
            allFilmData[key] = allFilmDataFull[key]

        # if a genre is not in allGenres yet, append it
        for genre in allFilmDataFull[key]['genres']:
            if genre not in allGenres:
                allGenres.append(genre)

        # modify min & max of the various attributes
        MIN_IMDB_RATING = min(MIN_IMDB_RATING, allFilmDataFull[key]['imdbRating'])
        MAX_IMDB_RATING = max(MAX_IMDB_RATING, allFilmDataFull[key]['imdbRating'])
        MIN_YEAR = min(MIN_YEAR, allFilmDataFull[key]['year'])
        MAX_YEAR = max(MAX_YEAR, allFilmDataFull[key]['year'])
        MIN_NUMBER_OF_VOTES = min(MIN_NUMBER_OF_VOTES, allFilmDataFull[key]['numberOfVotes'])
        MAX_NUMBER_OF_VOTES = max(MAX_NUMBER_OF_VOTES, allFilmDataFull[key]['numberOfVotes'])
        MIN_RUNTIME = min(MIN_RUNTIME, allFilmDataFull[key]['runtime'])
        MAX_RUNTIME = max(MAX_RUNTIME, allFilmDataFull[key]['runtime'])

    allGenres = sorted(allGenres)  # sort alphabetically

    # create a new list of allFilmData keys after filtering some films out of allFilmDataFull
    allFilmDataKeys = list(allFilmData.keys())

    # init dicts for vectorized allFilmData & myFilmData
    global allFilmDataVec
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

    # todo temp
    print("max runtime:" + str(MAX_RUNTIME))

    # perform some pre-computation to avoid repetitive computation
    DIFF_IMDB_RATING = MAX_IMDB_RATING - MIN_IMDB_RATING
    DIFF_YEAR = MAX_YEAR - MIN_YEAR
    DIFF_NUMBER_OF_VOTES = MAX_NUMBER_OF_VOTES - MIN_NUMBER_OF_VOTES
    DIFF_RUNTIME = MAX_RUNTIME - MIN_RUNTIME

    # pre-compute normalised years for each year
    for y in range(MIN_YEAR, MAX_YEAR + 1):
        YEAR_NORMS[y] = (y - MIN_YEAR) / DIFF_YEAR

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
        for i in range(0, VECTOR_LENGTH):
            vector[i] *= (myFilmData[key]['myRating'] / 10.0)
        # add to dict
        myFilmDataVec[key] = vector

    weightedAverageSum = 0.0  # init to some temp value

    # create user profile based on my-film-data-vectorized:
    global userProfile

    for key in myFilmDataKeys:
        # sum the (already weighted) vectors together
        userProfile += myFilmDataVec[key]
        # increment the weighted average
        weightedAverageSum += (myFilmData[key]['myRating'] / 10.0)

    # divide the userProfile vector by the weighted average
    userProfile = np.divide(userProfile, weightedAverageSum)

    # curveGenres()

    print("Initial userProfile:\n" + str(userProfile))

    initWildcardProfile()

    print("Initial wildcardProfile:\n" + str(wildcardProfile))

    genRecs()

    return jsonify(recs), 200


# initialises the wildcard profile.
# imdbRating, runtime & numOfVotes are fixed, the rest (year & all genres) are inverted
def initWildcardProfile():
    global wildcardProfile
    for i in range(0, VECTOR_LENGTH):
        # don't invert imdbRating, runtime, or numOfVotes
        if i != 1 and i != 2 and i != 3:
            weightHalf = getWeight(i) / 2.0
            wildcardProfile[i] = weightHalf - (userProfile[i] - weightHalf)  # invert the vector feature
        else:
            wildcardProfile[i] = userProfile[i]


# given an index of a vector, return the associated weight
def getWeight(i):
    match i:
        case 0:  # year
            return YEAR_WEIGHT
        case 1:  # imdbRating
            return 1.0
        case 2:  # numOfVotes
            return 1.0
        case 3:  # runtime
            return RUNTIME_WEIGHT
        case _:  # genres
            return GENRE_WEIGHT


# generate both non-wildcard & wildcard recs
def genRecs():
    allFilmDataKeys = list(allFilmData.keys())

    # generate recs
    getRecs(False, allFilmDataKeys)  # generate non-wildcard recs
    getRecs(True, allFilmDataKeys)  # generate wildcard recs


# get film recommendations
def getRecs(isWildcard, allFilmDataKeys):
    global recs

    if not isWildcard:
        recs = []
        maxRec = NUM_RECS
        vector = userProfile
    else:
        maxRec = NUM_WILDCARDS
        vector = wildcardProfile

    # Similarity dict:
    # key = filmId, value = similarity to userProfile (float: 0 - 100.0)
    similarities = {}

    # for each film in all-film-data-vectorized
    for filmId in allFilmDataKeys:
        # calculate similarity to userProfile
        similarities[filmId] = cosineSimilarity(allFilmDataVec[filmId], vector)

    # sort similarities in descending order.
    similarities = sorted(similarities.items(), key=lambda x: x[1], reverse=True)

    for i in range(0, maxRec):
        filmId = similarities[i][0]
        film = allFilmData[filmId]
        similarityScore = similarities[i][1]
        film['id'] = filmId
        film['similarityScore'] = round(similarityScore * 100.0, 2)
        film['isWildcard'] = isWildcard
        recs.append(film)


# given a film, return it's vectorized form (return type: list)
def vectorize(film, allGenres):
    vector = []
    # 1. normalise the year; apply weight
    yearNorm = YEAR_NORMS[film['year']] * YEAR_WEIGHT
    vector.append(yearNorm)
    # 2. normalise imdbRating
    imdbRatingNorm = (film['imdbRating'] - MIN_IMDB_RATING) / DIFF_IMDB_RATING
    vector.append(imdbRatingNorm)
    # 3. normalise numberOfVotes
    numberOfVotesNorm = (film['numberOfVotes'] - MIN_NUMBER_OF_VOTES) / DIFF_NUMBER_OF_VOTES
    vector.append(numberOfVotesNorm)
    # 4. normalise runtime; apply weight
    runtimeNorm = ((film['runtime'] - MIN_RUNTIME) / DIFF_RUNTIME) * RUNTIME_WEIGHT
    vector.append(runtimeNorm)
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
def cosineSimilarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


# given a user profile vector, curve the genres
# for example, if drama is the highest rated genre with a score of 0.4, make the value = 1.0 and then scale
# the other genres relative to this max value (1.0 in this case).
# after the genres are normalised, I apply a weight of GENRE_WEIGHT to all genres.
def curveGenres():
    global userProfile
    # normalise the genres in the user profile
    MIN_GENRE_VALUE = userProfile[4]
    MAX_GENRE_VALUE = userProfile[4]

    for i in range(4, VECTOR_LENGTH):
        MIN_GENRE_VALUE = min(MIN_GENRE_VALUE, userProfile[i])
        MAX_GENRE_VALUE = max(MAX_GENRE_VALUE, userProfile[i])

    DIFF_GENRE = MAX_GENRE_VALUE - MIN_GENRE_VALUE

    for i in range(4, VECTOR_LENGTH):
        userProfile[i] = (userProfile[i] - MIN_GENRE_VALUE) / DIFF_GENRE  # normalise the genres
        userProfile[i] = userProfile[i] * GENRE_WEIGHT


# called when user responds (thumbs up/down) to a film
@app.route('/response')
def response():
    index = int(request.args.get('index'))
    add = request.args.get('add').lower() == 'true'

    # non-wildcard rec
    if index < NUM_RECS:
        returnText = changeVector(index, add, False)
    # wildcard rec
    else:
        returnText = changeVector(index, add, True)

    return returnText, 200


# changes vector parameters of either user profile or wildcard profile
def changeVector(index, add, isWildcard):
    global userProfile
    global wildcardProfile
    global profileChanges

    recVector = allFilmDataVec[recs[index]['id']]

    if isWildcard:
        vectorChange = (recVector - wildcardProfile) * WILDCARD_FEEDBACK_FACTOR
    else:
        vectorChange = (recVector - userProfile) * FEEDBACK_FACTOR

    profileChanges[index] = vectorChange  # store the vector change

    # if the rec was liked
    if add:
        if isWildcard:
            wildcardProfile += vectorChange
        else:
            userProfile += vectorChange
        recStates[index] = 1
    # else, the rec was disliked
    else:
        if isWildcard:
            wildcardProfile -= vectorChange
        else:
            userProfile -= vectorChange
        recStates[index] = -1

    # after changing vector parameters, ensure that all vector features are >= 0.0 && <= 1.0
    if isWildcard:
        keepBoundary(wildcardProfile)
    else:
        keepBoundary(userProfile)

    # todo temp
    if isWildcard:
        print("wildcard profile:\n" + str(wildcardProfile))
    else:
        print("user profile:\n" + str(userProfile))

    return ("changed " + ("wildcard" if isWildcard else "user") + " profile due to " +
            ("liking" if add else "disliking") + " of " + recs[index]['title'])


# ensures that all vector features are >= 0.0 && <= 1.0
def keepBoundary(vector):
    for i in range(0, VECTOR_LENGTH):
        if vector[i] < 0.0:
            vector[i] = 0.0
        elif vector[i] > 1.0:
            vector[i] = 1.0


# called when a user undoes a response, e.g. they have 'thumbs down' pressed on a film, and then they press the
# button again to undo the response.
@app.route('/undoResponse')
def undoResponse():
    index = int(request.args.get('index'))
    add = request.args.get('add').lower() == 'true'

    # non-wildcard rec
    if index < NUM_RECS:
        return undoChange(index, add, False), 200
    # wildcard rec
    else:
        return undoChange(index, add, True), 200


# undo the vector parameter changes
def undoChange(index, add, isWildcard):
    global userProfile
    global wildcardProfile
    global profileChanges

    vectorChange = profileChanges[index]

    # if the film was previously disliked
    if add:
        if isWildcard:
            wildcardProfile += vectorChange
        else:
            userProfile += vectorChange

        recStates[index] = 0
    # else, the film was previously liked
    else:
        if isWildcard:
            wildcardProfile -= vectorChange
        else:
            userProfile -= vectorChange

        recStates[index] = 0

    # todo temp
    if isWildcard:
        print("wildcard profile:\n" + str(wildcardProfile))
    else:
        print("user profile:\n" + str(userProfile))

    # make the profile change a zero vector at the specified index
    profileChanges[index] = np.zeros(VECTOR_LENGTH)

    return ("undid " + ("wildcard" if isWildcard else "user") + " profile change due to previous " +
            ("disliking" if add else "liking") + " of " + recs[index]['title'])


@app.route('/regen')
def regen():
    global recStates
    # for each film that was liked or disliked:
    for i in range(0, TOTAL_RECS):
        if recStates[i] != 0:
            # remove from allFilmData & allFilmDataVec
            filmId = recs[i]['id']
            del allFilmData[filmId]
            del allFilmDataVec[filmId]

    # reset recStates
    recStates = [0] * TOTAL_RECS

    # re-calculate new recs
    genRecs()

    return jsonify(recs), 200


# getter for the number of recommendations
@app.route('/getTotalRecs')
def getTotalRecs():
    return str(TOTAL_RECS), 200


if __name__ == "__main__":
    app.run(host='localhost', port=60000)

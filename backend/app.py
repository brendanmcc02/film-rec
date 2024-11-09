from flask import Flask, request, jsonify
from datetime import datetime
import json
import csv
import numpy as np
import os
import glob
import importlib
from vectorize import *
# it's not possible to import filenames with hyphens, so I'm using a library to do it :/
letterboxd_conversion = importlib.import_module('../letterboxd-conversion')
all_film_data = importlib.import_module('../init-all-film-data')

RUNTIME_THRESHOLD = all_film_data.RUNTIME_THRESHOLD
PROFILE_VECTOR_LENGTH = 1
NUM_USER_RECS = 4
NUM_RECENCY_RECS = 2
NUM_WILDCARD_RECS = 2
TOTAL_RECS = NUM_USER_RECS + NUM_RECENCY_RECS + NUM_WILDCARD_RECS
USER_PROFILE_FEEDBACK_FACTOR = 0.05  # the rate at which feedback changes the user profile
RECENCY_FEEDBACK_FACTOR = 0.05
WILDCARD_FEEDBACK_FACTOR = 0.2
# from experimenting (yearNorm weight was fixed at 0.3), ~0.75 was a good sweet spot in the sense that
# it picked both single- and multi-genre films. The algorithm still heavily favoured the 4 genres that had the
# highest weighing, but this is expected and good behaviour.
GENRE_WEIGHT = 0.75
# from experimenting, 0.3 was a very good weight as it did not overvalue the year, but still took it into account.
YEAR_WEIGHT = 0.3
RUNTIME_WEIGHT = 0.3
DATE_RATED_WEIGHT = 0.5
DIFF_IMDB_RATING = 0.0
DIFF_YEAR = 0
DIFF_NUMBER_OF_VOTES = 0
DIFF_RUNTIME = 0
DIFF_DATE_RATED = datetime(1, 1, 1)

userProfile = np.zeros(PROFILE_VECTOR_LENGTH)
recencyProfile = np.zeros(PROFILE_VECTOR_LENGTH)
wildcardProfile = np.zeros(PROFILE_VECTOR_LENGTH)
vectorProfileChanges = []
allFilmData = {}
allFilmDataVectorized = {}
recs = []
recStates = [0] * TOTAL_RECS
minImdbRating = 0.0
minYear = 0
minNumberOfVotes = 0
minRuntime = 0
minDateRated = datetime(1, 1, 1)
isImdbFile = True
userFilmDataFilename = ""

app = Flask(__name__)


def resetGlobalVariables():
    global userProfile
    global recencyProfile
    global wildcardProfile
    global vectorProfileChanges
    global allFilmData
    global allFilmDataVectorized
    global recs
    global recStates
    global minImdbRating
    global minYear
    global minNumberOfVotes
    global minRuntime
    global minDateRated
    global isImdbFile

    userProfile = np.zeros(PROFILE_VECTOR_LENGTH)
    recencyProfile = np.zeros(PROFILE_VECTOR_LENGTH)
    wildcardProfile = np.zeros(PROFILE_VECTOR_LENGTH)
    vectorProfileChanges = []
    allFilmData = {}
    allFilmDataVectorized = {}
    recs = []
    recStates = [0] * TOTAL_RECS
    minImdbRating = 0.0
    minYear = 0
    minNumberOfVotes = 0
    minRuntime = 0
    minDateRated = datetime(1, 1, 1)


@app.route('/verifyUserUploadedFile', methods=['POST'])
def verifyUserUploadedFile():
    global isImdbFile
    global userFilmDataFilename

    isImdbFile = True
    userFilmDataFilename = ""

    if 'file' not in request.files:
        return 'No file found in the request', 400

    file = request.files['file']
    userFilmDataFilename = file.filename
    file.save("../database/" + file.filename)
    expectedImdbFileFilmAttributes = ["Const", "Your Rating", "Date Rated", "Title", "Original Title", "URL",
                                      "Title Type", "IMDb Rating", "Runtime (mins)", "Year", "Genres", "Num Votes",
                                      "Release Date", "Directors"]

    try:
        with open("../database/" + userFilmDataFilename, encoding='utf-8') as userFilmDataFile:
            reader = csv.DictReader(userFilmDataFile, delimiter=',', restkey='unexpectedData')

            for row in reader:
                if 'unexpectedData' in row:
                    return "Error: " + userFilmDataFilename + " has more data than row headers.\n", 400

                keys = list(row.keys())
                for k in keys:
                    if k not in expectedImdbFileFilmAttributes:
                        isImdbFile = False
                        if k not in letterboxd_conversion.expectedLetterboxdFileFilmAttributes:
                            return ("Error: Row headers in " + userFilmDataFilename +
                                    " does not conform to expected format.\n", 400)

        resetGlobalVariables()
        return "Upload Success.", 200
    except FileNotFoundError:
        return "Error: file not found.", 404
    except Exception as e:
        deleteCsvFiles()
        return "Error occurred with reading " + userFilmDataFilename + ".\n" + str(e), 400


# initial recommendation of films to user
@app.route('/initRec')
def initRec():
    try:
        userFilmDataList = []
        with open("../database/" + userFilmDataFilename, encoding='utf8') as userFilmDataFile:
            reader = csv.DictReader(userFilmDataFile, delimiter=',', restkey='unexpectedData')

            for row in reader:
                userFilmDataList.append(row)
    except FileNotFoundError:
        return "Error: " + userFilmDataFilename + " not found, check file name & file type.", 404
    except Exception as e:
        deleteCsvFiles()
        return "Error occurred with reading " + userFilmDataFilename + ".\n" + str(e), 400

    deleteCsvFiles()
    allFilmDataFile = open('../database/all-film-data.json')
    allFilmDataFull = json.load(allFilmDataFile)
    allFilmDataKeys = list(allFilmDataFull.keys())

    if not isImdbFile:
        userFilmDataList = letterboxd_conversion.convertLetterboxdFormatToImdbFormat(userFilmDataList, allFilmDataFull,
                                                                                     allFilmDataKeys)

    userFilmData = {}

    for film in userFilmDataList:
        if film['Title Type'] == "Movie" and int(film['Runtime (mins)']) >= RUNTIME_THRESHOLD and film['Genres'] != "":
            if isImdbFile:
                genres = film['Genres'].replace("\"", "").split(", ")
            else:
                genres = film['Genres']
            try:
                userFilmData[film['Const']] = {
                    "title": film['Title'],
                    "year": int(film['Year']),
                    "userRating": int(film['Your Rating']),
                    "dateRated": datetime.strptime(film['Date Rated'], "%Y-%m-%d"),
                    "imdbRating": float(film['IMDb Rating']),
                    "numberOfVotes": int(film['Num Votes']),
                    "runtime": int(film['Runtime (mins)']),
                    "genres": genres
                }
            except ValueError:
                return ("value error with film: " + film['Const']), 400

    userFilmDataKeys = list(userFilmData.keys())

    global DIFF_IMDB_RATING
    global DIFF_YEAR
    global DIFF_NUMBER_OF_VOTES
    global DIFF_RUNTIME
    global DIFF_DATE_RATED
    global minImdbRating
    global minYear
    global minNumberOfVotes
    global minRuntime
    global minDateRated

    # this is needed for normalising vector values.
    minImdbRating = allFilmDataFull[allFilmDataKeys[0]]['imdbRating']
    maxImdbRating = allFilmDataFull[allFilmDataKeys[0]]['imdbRating']
    minYear = allFilmDataFull[allFilmDataKeys[0]]['year']
    maxYear = allFilmDataFull[allFilmDataKeys[0]]['year']
    minNumberOfVotes = allFilmDataFull[allFilmDataKeys[0]]['numberOfVotes']
    maxNumberOfVotes = allFilmDataFull[allFilmDataKeys[0]]['numberOfVotes']
    minRuntime = allFilmDataFull[allFilmDataKeys[0]]['runtime']
    maxRuntime = allFilmDataFull[allFilmDataKeys[0]]['runtime']
    minDateRated = userFilmData[userFilmDataKeys[0]]['dateRated']
    maxDateRated = datetime.now()

    global allFilmData
    allGenres = []
    allLanguages = []
    allCountries = []

    for key in allFilmDataKeys:
        # take films out from allFilmData that the user has seen
        if key not in userFilmDataKeys:
            allFilmData[key] = allFilmDataFull[key]

        for genre in allFilmDataFull[key]['genres']:
            if genre not in allGenres:
                allGenres.append(genre)

        filmLanguage = allFilmDataFull[key]['language']
        if filmLanguage not in allLanguages:
            allLanguages.append(filmLanguage)

        for country in allFilmDataFull[key]['countries']:
            if country not in allCountries:
                allCountries.append(country)

        minImdbRating = min(minImdbRating, allFilmDataFull[key]['imdbRating'])
        maxImdbRating = max(maxImdbRating, allFilmDataFull[key]['imdbRating'])
        minYear = min(minYear, allFilmDataFull[key]['year'])
        maxYear = max(maxYear, allFilmDataFull[key]['year'])
        minNumberOfVotes = min(minNumberOfVotes, allFilmDataFull[key]['numberOfVotes'])
        maxNumberOfVotes = max(maxNumberOfVotes, allFilmDataFull[key]['numberOfVotes'])
        minRuntime = min(minRuntime, allFilmDataFull[key]['runtime'])
        maxRuntime = max(maxRuntime, allFilmDataFull[key]['runtime'])

    allGenres = sorted(allGenres)
    allLanguages = sorted(allLanguages)
    allCountries = sorted(allCountries)

    # create a new list of allFilmData keys after filtering some films out of allFilmDataFull
    allFilmDataKeys = list(allFilmData.keys())

    global allFilmDataVectorized
    userFilmDataVectorized = {}

    # alter the min & max values to ensure they are the same across both datasets
    for key in userFilmDataKeys:
        minImdbRating = min(minImdbRating, userFilmData[key]['imdbRating'])
        maxImdbRating = max(maxImdbRating, userFilmData[key]['imdbRating'])
        minYear = min(minYear, userFilmData[key]['year'])
        maxYear = max(maxYear, userFilmData[key]['year'])
        minNumberOfVotes = min(minNumberOfVotes, userFilmData[key]['numberOfVotes'])
        maxNumberOfVotes = max(maxNumberOfVotes, userFilmData[key]['numberOfVotes'])
        minRuntime = min(minRuntime, userFilmData[key]['runtime'])
        maxRuntime = max(maxRuntime, userFilmData[key]['runtime'])
        minDateRated = min(minDateRated, userFilmData[key]['dateRated'])

    # perform some pre-computation to avoid repetitive computation
    DIFF_IMDB_RATING = maxImdbRating - minImdbRating
    DIFF_YEAR = maxYear - minYear
    DIFF_NUMBER_OF_VOTES = maxNumberOfVotes - minNumberOfVotes
    DIFF_RUNTIME = maxRuntime - minRuntime
    DIFF_DATE_RATED = maxDateRated - minDateRated

    cachedNormalizedYears = {}
    for y in range(minYear, maxYear + 1):
        cachedNormalizedYears[y] = ((y - minYear) / DIFF_YEAR) * YEAR_WEIGHT

    cachedNormalizedImdbRatings = {}
    for i in np.arange(minImdbRating, maxImdbRating + 0.1, 0.1):
        i = round(i, 1)
        cachedNormalizedImdbRatings[str(i)] = (i - minImdbRating) / DIFF_IMDB_RATING

    global PROFILE_VECTOR_LENGTH

    # vectorize all-film-database
    for key in allFilmDataKeys:
        vector = vectorizeFilm(allFilmData[key], allGenres, allLanguages, allCountries, cachedNormalizedYears,
                               cachedNormalizedImdbRatings, minNumberOfVotes, DIFF_NUMBER_OF_VOTES, minRuntime,
                               DIFF_RUNTIME)
        if PROFILE_VECTOR_LENGTH == 1:
            PROFILE_VECTOR_LENGTH = len(vector)
        allFilmDataVectorized[key] = vector

    # init a dict to store pre-computed dateRatedScalar values; more efficient.
    # key: film id, value: dateRatedScalar
    cachedDateRatedScalars = {}

    # init a dict to store pre-computed normalised userRating values; more efficient.
    # key: film id, value: normalisedUserRating
    cachedUserRatingScalars = {}

    # vectorize user-film-database
    for key in userFilmDataKeys:
        vector = vectorizeFilm(userFilmData[key], allGenres, allLanguages, allCountries, cachedNormalizedYears,
                               cachedNormalizedImdbRatings, minNumberOfVotes, DIFF_NUMBER_OF_VOTES, minRuntime,
                               DIFF_RUNTIME)
        # dateRatedScalar: normalize the dateRatedScalar as a float between DATE_RATED_WEIGHT and 1.0.
        dateRatedScalar = (((userFilmData[key]['dateRated'] - minDateRated) / DIFF_DATE_RATED) *
                           (1 - DATE_RATED_WEIGHT)) + DATE_RATED_WEIGHT
        cachedDateRatedScalars[key] = dateRatedScalar

        # imdbRatings run from 1-10, we want values to run from 0.1 - 1.0
        userRatingScalar = round((userFilmData[key]['userRating'] / 10.0), 1)
        cachedUserRatingScalars[key] = userRatingScalar

        # recall that vectors are scalar multiplied by userRating & dateRated
        userFilmDataVectorized[key] = vector * userRatingScalar * dateRatedScalar

    weightedAverageSum = 0.0

    global vectorProfileChanges
    for i in range(0, TOTAL_RECS):
        vectorProfileChanges.append(np.zeros(PROFILE_VECTOR_LENGTH))

    global userProfile
    userProfile = np.zeros(PROFILE_VECTOR_LENGTH)

    for key in userFilmDataKeys:
        userProfile += userFilmDataVectorized[key]
        weightedAverageSum += cachedUserRatingScalars[key] + cachedDateRatedScalars[key]

    userProfile = np.divide(userProfile, weightedAverageSum)

    # print("Initial userProfile:\n" + str(userProfile))

    initRecencyProfile(userFilmData, userFilmDataKeys, userFilmDataVectorized, maxDateRated)

    # print("Initial recencyProfile:\n" + str(recencyProfile))

    initWildcardProfile()

    # print("Initial wildcardProfile:\n" + str(wildcardProfile))

    generateRecs()

    return jsonify(recs), 200


def initRecencyProfile(userFilmData, userFilmDataKeys, userFilmDataVectorized, maxDateRated):
    global recencyProfile
    recencyProfile = np.zeros(PROFILE_VECTOR_LENGTH)
    weightedAverageSum = 0.0

    for key in userFilmDataKeys:
        daysDiff = maxDateRated - userFilmData[key]['dateRated']
        if daysDiff.days <= 30:
            recencyProfile += userFilmDataVectorized[key]
            # note: not adding dateRatedScalar to the weightedAverageSum because I don't want vectors to be
            # scalar multiplied because we are only dealing with films in the last 30 days
            weightedAverageSum += (userFilmData[key]['userRating'] / 10.0)
        else:
            # terminate; user-uploaded .csv file is sorted by date (latest first, oldest last),
            # so no need to look further
            break

    # todo div by 0 error - what if there's no recent films?
    recencyProfile = np.divide(recencyProfile, weightedAverageSum)


# todo invert country & language
def initWildcardProfile():
    global wildcardProfile
    wildcardProfile = np.zeros(PROFILE_VECTOR_LENGTH)

    for i in range(0, PROFILE_VECTOR_LENGTH):
        # don't invert imdbRating, runtime, or numVotes
        if i != 1 and i != 2 and i != 3:
            weightHalf = getWeightByVectorIndex(i) / 2.0
            wildcardProfile[i] = weightHalf - (userProfile[i] - weightHalf)  # invert the vector feature
        else:
            wildcardProfile[i] = userProfile[i]


def getWeightByVectorIndex(vectorIndex):
    # any index over 27 in the vector is either a country or language
    if vectorIndex >= 27:
        return 1.0
    match vectorIndex:
        case 0:  # year
            return YEAR_WEIGHT
        case 1:  # imdbRating
            return 1.0
        case 2:  # numVotes
            return 1.0
        case 3:  # runtime
            return RUNTIME_WEIGHT
        case _:  # genres
            return GENRE_WEIGHT


def generateRecs():
    allFilmDataKeys = list(allFilmData.keys())
    getFilmRecs("user", allFilmDataKeys)      # generate user recs
    getFilmRecs("recency", allFilmDataKeys)   # generate recency recs
    getFilmRecs("wildcard", allFilmDataKeys)  # generate wildcard recs


def getFilmRecs(recType, allFilmDataKeys):
    global recs

    if recType == "wildcard":
        maxRec = NUM_WILDCARD_RECS
        vector = wildcardProfile
    elif recType == "recency":
        maxRec = NUM_RECENCY_RECS
        vector = recencyProfile
    elif recType == "user":
        recs = []
        maxRec = NUM_USER_RECS
        vector = userProfile
    else:
        print("unknown rec type: " + str(recType))
        return "unknown rec type: ", 400

    # pre-compute the vector magnitude to make cosine sim calculations more efficient
    vectorMagnitude = np.linalg.norm(vector)

    cosineSimilarities = {}

    for filmId in allFilmDataKeys:
        cosineSimilarities[filmId] = cosineSimilarity(allFilmDataVectorized[filmId], vector, vectorMagnitude)

    # sort in descending order.
    cosineSimilarities = sorted(cosineSimilarities.items(), key=lambda x: x[1], reverse=True)

    duplicateRec = False

    for i in range(0, maxRec):
        filmId = cosineSimilarities[i][0]
        # check if the recommended film has already been recommended by another vector:
        # this check exists because we don't want the userProfile vector recommending the same films as
        # the recencyProfile for example
        for rec in recs:
            if rec['id'] == filmId:
                maxRec += 1
                duplicateRec = True
                # todo temp
                print(str(rec['id']))
                break

        if not duplicateRec:
            film = allFilmData[filmId]
            similarityScore = cosineSimilarities[i][1]
            film['id'] = filmId
            film['similarityScore'] = round(similarityScore * 100.0, 2)
            film['recType'] = recType
            recs.append(film)

        duplicateRec = False


# called when user responds (thumbs up/down) to a film
@app.route('/response')
def response():
    index = int(request.args.get('index'))
    add = request.args.get('add').lower() == 'true'

    SUM_USER_RECENCY_RECS = NUM_USER_RECS + NUM_RECENCY_RECS

    if index < NUM_USER_RECS:
        returnText = changeVector(index, add, "user")
    elif index < SUM_USER_RECENCY_RECS:
        returnText = changeVector(index, add, "recency")
    else:
        returnText = changeVector(index, add, "wildcard")

    return returnText, 200


# changes vector parameters
def changeVector(index, add, recType):
    global userProfile
    global recencyProfile
    global wildcardProfile
    global vectorProfileChanges

    recVector = allFilmDataVectorized[recs[index]['id']]

    # todo can these repetitive if-else chains be simplified?

    if recType == "wildcard":
        vectorChange = (recVector - wildcardProfile) * WILDCARD_FEEDBACK_FACTOR
    elif recType == "recency":
        vectorChange = (recVector - recencyProfile) * RECENCY_FEEDBACK_FACTOR
    elif recType == "user":
        vectorChange = (recVector - userProfile) * USER_PROFILE_FEEDBACK_FACTOR
    else:
        return "unknown rec type:" + str(recType)

    vectorProfileChanges[index] = vectorChange  # store the vector change

    # if the rec was liked
    if add:
        if recType == "wildcard":
            wildcardProfile += vectorChange
        elif recType == "recency":
            recencyProfile += vectorChange
        elif recType == "user":
            userProfile += vectorChange
        else:
            return "unknown rec type:" + str(recType)
        recStates[index] = 1
    # else, the rec was disliked
    else:
        if recType == "wildcard":
            wildcardProfile -= vectorChange
        elif recType == "recency":
            recencyProfile -= vectorChange
        elif recType == "user":
            userProfile -= vectorChange
        else:
            return "unknown rec type:" + str(recType)
        recStates[index] = -1

    # after changing vector parameters, ensure that all vector features are >= 0.0 && <= 1.0
    if recType == "wildcard":
        keepVectorBoundary(wildcardProfile, PROFILE_VECTOR_LENGTH)
    elif recType == "recency":
        keepVectorBoundary(recencyProfile, PROFILE_VECTOR_LENGTH)
    elif recType == "user":
        keepVectorBoundary(userProfile, PROFILE_VECTOR_LENGTH)
    else:
        return "unknown rec type:" + str(recType)

    return ("changed " + recs[index]['recType'] + " profile due to " +
            ("liking" if add else "disliking") + " of " + recs[index]['title'])


# called when a user undoes a response, e.g. they have 'thumbs down' pressed on a film, and then they press the
# button again to undo the response.
@app.route('/undoResponse')
def undoResponse():
    index = int(request.args.get('index'))
    add = request.args.get('add').lower() == 'true'
    SUM_USER_RECENCY_RECS = NUM_USER_RECS + NUM_RECENCY_RECS

    if index < NUM_USER_RECS:
        return undoChange(index, add, "user"), 200
    if index < SUM_USER_RECENCY_RECS:
        return undoChange(index, add, "recency"), 200
    else:
        return undoChange(index, add, "wildcard"), 200


# undo the vector parameter changes
def undoChange(index, add, recType):
    global userProfile
    global recencyProfile
    global wildcardProfile
    global vectorProfileChanges

    vectorChange = vectorProfileChanges[index]

    # todo can these repetitive if-else chains be simplified?
    # if the film was previously disliked
    if add:
        if recType == "wildcard":
            wildcardProfile += vectorChange
        elif recType == "recency":
            recencyProfile += vectorChange
        elif recType == "user":
            userProfile += vectorChange
        else:
            return "unknown rec type:" + str(recType)

        recStates[index] = 0
    # else, the film was previously liked
    else:
        if recType == "wildcard":
            wildcardProfile -= vectorChange
        elif recType == "recency":
            recencyProfile -= vectorChange
        elif recType == "user":
            userProfile -= vectorChange
        else:
            return "unknown rec type:" + str(recType)

        recStates[index] = 0

    # make the profile change a zero vector at the specified index
    vectorProfileChanges[index] = np.zeros(PROFILE_VECTOR_LENGTH)

    return ("undid " + recType + " profile change due to previous " +
            ("disliking" if add else "liking") + " of " + recs[index]['title'])


@app.route('/regen')
def regen():
    global recStates
    # for each film that was liked or disliked:
    for i in range(0, TOTAL_RECS):
        if recStates[i] != 0:
            # remove from allFilmData & allFilmDataVectorized
            filmId = recs[i]['id']
            del allFilmData[filmId]
            del allFilmDataVectorized[filmId]

    # reset recStates
    recStates = [0] * TOTAL_RECS

    generateRecs()

    return jsonify(recs), 200


# getter for the number of recommendations
@app.route('/getTotalRecs')
def getTotalRecs():
    return str(TOTAL_RECS), 200


def deleteCsvFiles():
    for f in glob.glob("../database/*.csv"):
        os.remove(f)


if __name__ == "__main__":
    app.run(host='localhost', port=60000)

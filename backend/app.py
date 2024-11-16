from flask import Flask, request, jsonify
from datetime import datetime
import json
import csv
import numpy as np
import os
import glob
from vectorize import *
from init_all_film_data import YEAR_WEIGHT, GENRE_WEIGHT, RUNTIME_THRESHOLD, NUM_OF_VOTES_THRESHOLD
from letterboxd_conversion import expectedLetterboxdFileFilmAttributes, convertLetterboxdFormatToImdbFormat

DATE_RATED_WEIGHT = 0.5
NUM_USER_RECS = 4
NUM_RECENCY_RECS = 2
NUM_WILDCARD_RECS = 2
TOTAL_RECS = NUM_USER_RECS + NUM_RECENCY_RECS + NUM_WILDCARD_RECS
USER_PROFILE_FEEDBACK_FACTOR = 0.05  # the rate at which feedback changes the user profile
RECENCY_FEEDBACK_FACTOR = 0.05
WILDCARD_FEEDBACK_FACTOR = 0.2
PROFILE_VECTOR_LENGTH = 0

allFilmDataUnseen = {}
allFilmDataVectorized = {}
allFilmDataVectorizedMagnitudes = {}
diffDateRated = datetime(1, 1, 1)
minDateRated = datetime.now()
userProfile = np.zeros(0)
recencyProfile = np.zeros(0)
wildcardProfile = np.zeros(0)
vectorProfileChanges = []
recs = []
recStates = [0] * TOTAL_RECS
isImdbFile = True
userFilmDataFilename = ""

app = Flask(__name__)


def resetGlobalVariables():
    global userProfile
    global recencyProfile
    global wildcardProfile
    global vectorProfileChanges
    global allFilmDataUnseen
    global recs
    global recStates
    global minDateRated
    global isImdbFile
    global userFilmDataFilename

    userProfile = np.zeros(0)
    recencyProfile = np.zeros(0)
    wildcardProfile = np.zeros(0)
    vectorProfileChanges = []
    allFilmDataUnseen = {}
    recs = []
    recStates = [0] * TOTAL_RECS
    minDateRated = datetime.now()
    isImdbFile = True
    userFilmDataFilename = ""


@app.route('/verifyUserUploadedFile', methods=['POST'])
def verifyUserUploadedFile():
    global isImdbFile
    global userFilmDataFilename
    resetGlobalVariables()

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
                        if k not in expectedLetterboxdFileFilmAttributes:
                            return ("Error: Row headers in " + userFilmDataFilename +
                                    " does not conform to expected format.\n", 400)

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
        return f"Error: {userFilmDataFilename} not found, check file name & file type.", 404
    except Exception as e:
        deleteCsvFiles()
        return f"Error occurred with reading {userFilmDataFilename}.\n" + str(e), 400

    deleteCsvFiles()
    allFilmDataFile = open('../database/all-film-data.json')
    allFilmData = json.load(allFilmDataFile)
    allFilmDataKeys = list(allFilmData.keys())

    global allFilmDataVectorized
    global allFilmDataVectorizedMagnitudes

    allFilmDataVectorizedFile = open('../database/all-film-data-vectorized.json')
    allFilmDataVectorized = json.load(allFilmDataVectorizedFile)
    allFilmDataVectorizedMagnitudesFile = open('../database/all-film-data-vectorized-magnitudes.json')
    allFilmDataVectorizedMagnitudes = json.load(allFilmDataVectorizedMagnitudesFile)
    cachedLetterboxdTitleYearFile = open('../database/cached-letterboxd-title-year.json')
    cachedLetterboxdTitleYear = json.load(cachedLetterboxdTitleYearFile)

    if not isImdbFile:
        userFilmDataList = convertLetterboxdFormatToImdbFormat(userFilmDataList, allFilmData, cachedLetterboxdTitleYear)

    userFilmData = {}
    global diffDateRated
    global minDateRated

    minDateRated = datetime.now()
    maxDateRated = datetime.now()

    for film in userFilmDataList:
        if film['Title Type'] == "Movie" and int(film['Runtime (mins)']) >= RUNTIME_THRESHOLD and film['Genres'] != ""\
                and int(film['Num Votes']) >= NUM_OF_VOTES_THRESHOLD:
            if isImdbFile:
                genres = film['Genres'].replace("\"", "").split(", ")
            else:
                genres = film['Genres']
            try:
                filmId = film['Const']
                if filmId in allFilmData:
                    dateRated = datetime.strptime(film['Date Rated'], "%Y-%m-%d")

                    userFilmData[film['Const']] = {
                        "title": film['Title'],
                        "year": int(film['Year']),
                        "userRating": int(film['Your Rating']),
                        "dateRated": dateRated,
                        "imdbRating": float(film['IMDb Rating']),
                        "numberOfVotes": int(film['Num Votes']),
                        "runtime": int(film['Runtime (mins)']),
                        "genres": genres,
                        "languages": allFilmData[filmId]['languages'],
                        "countries": allFilmData[filmId]['countries']
                    }

                    minDateRated = min(minDateRated, dateRated)
                else:
                    print(f"Film in userFilmData not found in allFilmData, {filmId}\n")
            except ValueError:
                return ("value error with film: " + film['Const']), 400

    # perform some pre-computation to avoid repetitive computation
    diffDateRated = maxDateRated - minDateRated
    userFilmDataKeys = list(userFilmData.keys())

    global allFilmDataUnseen

    for key in allFilmDataKeys:
        # take films out from allFilmData that the user has seen
        if key not in userFilmData:
            allFilmDataUnseen[key] = allFilmData[key]

    userFilmDataVectorized = {}

    global PROFILE_VECTOR_LENGTH

    # init a dict to store pre-computed dateRatedScalar values; more efficient.
    # key: film id, value: dateRatedScalar
    cachedDateRatedScalars = {}

    # init a dict to store pre-computed normalised userRating values; more efficient.
    # key: film id, value: normalisedUserRating
    cachedUserRatingScalars = {}

    cacheFile = open('../database/cache.json')
    cache = json.load(cacheFile)

    # vectorize user-film-data
    for key in userFilmDataKeys:
        vector = vectorizeFilm(userFilmData[key], cache['allGenres'], cache['allLanguages'], cache['allCountries'],
                               cache['normalizedYears'], cache['normalizedImdbRatings'], cache['minNumberOfVotes'],
                               cache['diffNumberOfVotes'], cache['minRuntime'], cache['diffRuntime'])
        # dateRatedScalar: normalize the dateRatedScalar as a float between DATE_RATED_WEIGHT and 1.0.
        dateRatedScalar = (((userFilmData[key]['dateRated'] - minDateRated) / diffDateRated) *
                           (1 - DATE_RATED_WEIGHT)) + DATE_RATED_WEIGHT
        cachedDateRatedScalars[key] = dateRatedScalar

        # imdbRatings run from 1-10, we want values to run from 0.1 - 1.0
        userRatingScalar = round((userFilmData[key]['userRating'] / 10.0), 1)
        cachedUserRatingScalars[key] = userRatingScalar

        # recall that vectors are scalar multiplied by userRating & dateRated
        userFilmDataVectorized[key] = vector * userRatingScalar * dateRatedScalar

    weightedAverageSum = 0.0
    PROFILE_VECTOR_LENGTH = cache['profileVectorLength']

    global vectorProfileChanges
    for i in range(0, TOTAL_RECS):
        vectorProfileChanges.append(np.zeros(PROFILE_VECTOR_LENGTH))

    global userProfile
    userProfile = np.zeros(PROFILE_VECTOR_LENGTH)

    for key in userFilmDataKeys:
        userProfile += userFilmDataVectorized[key]
        weightedAverageSum += cachedUserRatingScalars[key] + cachedDateRatedScalars[key]

    userProfile = np.divide(userProfile, weightedAverageSum)

    print("Initial userProfile:\n" + str(userProfile))

    initRecencyProfile(userFilmData, userFilmDataKeys, userFilmDataVectorized, maxDateRated)

    print("Initial recencyProfile:\n" + str(recencyProfile))

    initWildcardProfile()

    print("Initial wildcardProfile:\n" + str(wildcardProfile))

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
    allFilmDataKeys = list(allFilmDataUnseen.keys())
    getFilmRecs("user", allFilmDataKeys)      # generate user recs
    getFilmRecs("recency", allFilmDataKeys)   # generate recency recs
    getFilmRecs("wildcard", allFilmDataKeys)  # generate wildcard recs


def getFilmRecs(recType, allFilmDataKeys):
    global recs

    if recType == "wildcard":
        maxRec = NUM_WILDCARD_RECS
        profileVector = wildcardProfile
    elif recType == "recency":
        maxRec = NUM_RECENCY_RECS
        profileVector = recencyProfile
    elif recType == "user":
        recs = []
        maxRec = NUM_USER_RECS
        profileVector = userProfile
    else:
        print("unknown rec type: " + str(recType))
        return "unknown rec type: ", 400

    # pre-compute the vector magnitude to make cosine sim calculations more efficient
    profileVectorMagnitude = np.linalg.norm(profileVector)

    cosineSimilarities = {}

    for filmId in allFilmDataKeys:
        filmVectorMagnitude = allFilmDataVectorizedMagnitudes[filmId]
        cosineSimilarities[filmId] = cosineSimilarity(allFilmDataVectorized[filmId], profileVector,
                                                      filmVectorMagnitude, profileVectorMagnitude)

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
            film = allFilmDataUnseen[filmId]
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
            # remove from allFilmDataUnseen
            filmId = recs[i]['id']
            del allFilmDataUnseen[filmId]

    # reset recStates
    recStates = [0] * TOTAL_RECS

    generateRecs()

    return jsonify(recs), 200


@app.route('/getTotalRecs')
def getTotalRecs():
    return str(TOTAL_RECS), 200


def deleteCsvFiles():
    for f in glob.glob("../database/*.csv"):
        os.remove(f)


if __name__ == "__main__":
    app.run(host='localhost', port=60000)

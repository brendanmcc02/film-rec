from flask import Flask, request, jsonify
from datetime import datetime
import json
import csv
import numpy as np
import os
import glob
from vectorize import *
from init_all_film_data import RUNTIME_THRESHOLD, NUM_VOTES_THRESHOLD
from letterboxd_conversion import *

DATE_RATED_WEIGHT = 0.5
NUM_FILMS_WATCHED_IN_GENRE_THRESHOLD = 10
NUM_TOP_GENRE_PROFILES = 2
NUM_GENRE_PROFILE_RECS = 1
NUM_RECENCY_RECS = 1
NUM_OLD_RECS = 1
NUM_OBSCURE_RECS = 1
NUM_INTERNATIONAL_RECS = 1
NUM_FAVOURITE_RECS = 3
TOTAL_RECS = ((NUM_GENRE_PROFILE_RECS * NUM_TOP_GENRE_PROFILES) + NUM_RECENCY_RECS + NUM_OLD_RECS + NUM_OBSCURE_RECS 
              + NUM_INTERNATIONAL_RECS + NUM_FAVOURITE_RECS)
USER_PROFILE_FEEDBACK_FACTOR = 0.05
RECENCY_FEEDBACK_FACTOR = 0.05
WILDCARD_FEEDBACK_FACTOR = 0.2

profileVectorLength = 0
allFilmDataUnseen = {}
allFilmDataVectorized = {}
allFilmDataVectorizedMagnitudes = {}
cachedLetterboxdTitles = {}
cache = {}
diffDateRated = datetime(1, 1, 1)
minDateRated = datetime.now()
genreProfiles = []
recencyProfile = np.zeros(profileVectorLength)
oldProfiles = []
obscureProfiles = []
internationalProfiles = []
favouriteProfile = np.zeros(profileVectorLength)
vectorProfileChanges = []
recs = []
recStates = [0] * TOTAL_RECS
isImdbFile = True
userFilmDataFilename = ""
allGenresLength = 0
allCountriesLength = 0

app = Flask(__name__)


def resetGlobalVariables():
    global genreProfiles
    global recencyProfile
    global oldProfiles
    global obscureProfiles
    global internationalProfiles
    global favouriteProfile
    global vectorProfileChanges
    global allFilmDataUnseen
    global recs
    global recStates
    global minDateRated
    global isImdbFile
    global userFilmDataFilename
    global allGenresLength
    global allCountriesLength

    genreProfiles = []
    recencyProfile = np.zeros(profileVectorLength)
    oldProfiles = []
    obscureProfiles = []
    internationalProfiles = []
    favouriteProfile = np.zeros(profileVectorLength)
    vectorProfileChanges = []
    allFilmDataUnseen = {}
    recs = []
    recStates = [0] * TOTAL_RECS
    minDateRated = datetime.now()
    isImdbFile = True
    userFilmDataFilename = ""
    allGenresLength = 0
    allCountriesLength = 0


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
    global allFilmDataVectorized
    global allFilmDataVectorizedMagnitudes
    global diffDateRated
    global minDateRated
    global allFilmDataUnseen
    global profileVectorLength
    global vectorProfileChanges
    global allGenresLength
    global allCountriesLength
    global genreProfiles
    global recencyProfile
    global oldProfiles
    global obscureProfiles
    global internationalProfiles
    global favouriteProfile

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
    allFilmDataIds = list(allFilmData.keys())

    if not isImdbFile:
        userFilmDataList = convertLetterboxdFormatToImdbFormat(userFilmDataList, allFilmData, cachedLetterboxdTitles)

    userFilmData = {}
    favouriteFilmIds = []
    minDateRated = datetime.now()
    maxDateRated = datetime.now()

    for film in userFilmDataList:
        if film['Title Type'] == "Movie" and int(film['Runtime (mins)']) >= RUNTIME_THRESHOLD and film['Genres'] != ""\
                and int(film['Num Votes']) >= NUM_VOTES_THRESHOLD:
            if isImdbFile:
                genres = film['Genres'].replace("\"", "").split(", ")
            else:
                genres = film['Genres']
            try:
                filmId = film['Const']
                if filmId in allFilmData:
                    dateRated = datetime.strptime(film['Date Rated'], "%Y-%m-%d")
                    minDateRated = min(minDateRated, dateRated)

                    userFilmData[film['Const']] = {
                        "title": film['Title'],
                        "year": int(film['Year']),
                        "userRating": int(film['Your Rating']),
                        "dateRated": dateRated,
                        "imdbRating": float(film['IMDb Rating']),
                        "numberOfVotes": int(film['Num Votes']),
                        "runtime": int(film['Runtime (mins)']),
                        "genres": genres,
                        "countries": allFilmData[filmId]['countries']
                    }

                    if userFilmData[filmId]['userRating'] >= 9:
                        favouriteFilmIds.append(filmId)
                else:
                    print(f"Film in userFilmData not found in allFilmData, {filmId}\n")
            except ValueError:
                return ("value error with film: " + film['Const']), 400

    diffDateRated = maxDateRated - minDateRated

    if diffDateRated == 0.0:
        print("Note: diffDateRated = 0.")
        diffDateRated = 1.0

    userFilmDataIds = list(userFilmData.keys())

    for imdbFilmId in allFilmDataIds:
        # take films out from allFilmData that the user has seen
        if imdbFilmId not in userFilmData:
            allFilmDataUnseen[imdbFilmId] = allFilmData[imdbFilmId]

    userFilmDataVectorized = {}

    # init a dict with pre-computed scalar values
    cachedDateRatedScalars = {}
    cachedUserRatingScalars = {}
    
    allGenresLength = len(cache['allGenres'])
    allCountriesLength = len(cache['allCountries'])

    # vectorize user-film-data
    for imdbFilmId in userFilmDataIds:
        vector = vectorizeFilm(userFilmData[imdbFilmId], cache['allGenres'], cache['allCountries'],
                               cache['normalizedYears'], cache['normalizedImdbRatings'], cache['minNumberOfVotes'],
                               cache['diffNumberOfVotes'], cache['normalizedRuntimes'])
        # normalize the dateRatedScalar as a float between DATE_RATED_WEIGHT and 1.0.
        dateRatedScalar = (((userFilmData[imdbFilmId]['dateRated'] - minDateRated) / diffDateRated) *
                           (1 - DATE_RATED_WEIGHT)) + DATE_RATED_WEIGHT
        cachedDateRatedScalars[imdbFilmId] = dateRatedScalar

        # imdbRatings run from 1-10, we want values to run from 0.1 - 1.0
        userRatingScalar = round((userFilmData[imdbFilmId]['userRating'] / 10.0), 1)
        cachedUserRatingScalars[imdbFilmId] = userRatingScalar

        userFilmDataVectorized[imdbFilmId] = vector * userRatingScalar * dateRatedScalar

    profileVectorLength = cache['profileVectorLength']

    for _ in range(0, TOTAL_RECS):
        vectorProfileChanges.append(np.zeros(profileVectorLength))

    genreProfiles = initGenreProfiles(userFilmDataIds, userFilmDataVectorized, cachedUserRatingScalars, cachedDateRatedScalars,
                      cache['allGenres'], profileVectorLength, NUM_FILMS_WATCHED_IN_GENRE_THRESHOLD)
    # for genreProfile in genreProfiles:
    #     print(f"{genreProfile['genre']}:")
    #     printStringifiedVector(genreProfile['profile'], cache['allGenres'], cache['allCountries'])

    recencyProfile = initRecencyProfile(userFilmData, userFilmDataIds, userFilmDataVectorized, maxDateRated, profileVectorLength, 
                                        cachedUserRatingScalars, cachedDateRatedScalars)
    # printStringifiedVector(recencyProfile, cache['allGenres'], cache['allCountries'])

    oldProfiles = initOldProfiles(genreProfiles, NUM_TOP_GENRE_PROFILES)
    # for profile in oldProfiles:
    #     printStringifiedVector(profile, cache['allGenres'], cache['allCountries'])

    obscureProfiles = initObscureProfiles(genreProfiles, NUM_TOP_GENRE_PROFILES)
    # for profile in obscureProfiles:
    #     printStringifiedVector(profile, cache['allGenres'], cache['allCountries'])

    internationalProfiles = initInternationalProfiles(genreProfiles, NUM_TOP_GENRE_PROFILES, cache['allCountries'], allGenresLength)
    # for profile in internationalProfiles:
    #     printStringifiedVector(profile, cache['allGenres'], cache['allCountries'])

    favouriteProfile = initFavouriteProfile(userFilmDataIds, userFilmDataVectorized, profileVectorLength,
                                            cachedUserRatingScalars, cachedDateRatedScalars, favouriteFilmIds)
    printStringifiedVector(favouriteProfile, cache['allGenres'], cache['allCountries'])

    generateRecs()

    return jsonify(recs), 200


def generateRecs():
    global recs
    recs = []

    allFilmDataIds = list(allFilmDataUnseen.keys())

    for i in range(0, NUM_TOP_GENRE_PROFILES):
        getFilmRecs(genreProfiles[i]['genre'], allFilmDataIds, NUM_GENRE_PROFILE_RECS, genreProfiles[i]['profile'])

    if np.array_equal(recencyProfile, np.zeros(profileVectorLength)):
        print("No recency profile.")
    else:
        getFilmRecs("recency", allFilmDataIds, NUM_RECENCY_RECS, recencyProfile)

    for oldProfile in oldProfiles:
        getFilmRecs("old", allFilmDataIds, NUM_OLD_RECS, oldProfile)
        
    for obscureProfile in obscureProfiles:
        getFilmRecs("obscure", allFilmDataIds, NUM_OBSCURE_RECS, obscureProfile)

    for internationalProfile in internationalProfiles:
        getFilmRecs("international", allFilmDataIds, NUM_INTERNATIONAL_RECS, internationalProfile)

    if np.array_equal(favouriteProfile, np.zeros(profileVectorLength)):
        print("No favourite profile.")
    else:
        getFilmRecs("favourite", allFilmDataIds, NUM_FAVOURITE_RECS, favouriteProfile)


def getFilmRecs(recType, allFilmDataIds, maxNumberOfRecs, profileVector):
    global recs
    global allFilmDataVectorizedMagnitudes

    profileVectorMagnitude = np.linalg.norm(profileVector)
    cosineSimilarities = {}

    for filmId in allFilmDataIds:
        filmVectorMagnitude = allFilmDataVectorizedMagnitudes[filmId]
        cosineSimilarities[filmId] = cosineSimilarity(allFilmDataVectorized[filmId], profileVector,
                                                      filmVectorMagnitude, profileVectorMagnitude)

    # sort in descending order
    cosineSimilarities = sorted(cosineSimilarities.items(), key=lambda x: x[1], reverse=True)

    isDuplicateRec = False

    i = 0
    while i < maxNumberOfRecs:
        filmId = cosineSimilarities[i][0]
        # check if the recommended film has already been recommended earlier
        for rec in recs:
            if rec['id'] == filmId:
                maxNumberOfRecs += 1
                isDuplicateRec = True

        if not isDuplicateRec:
            film = allFilmDataUnseen[filmId]
            similarityScore = cosineSimilarities[i][1]
            film['id'] = filmId
            film['similarityScore'] = round(similarityScore * 100.0, 2)
            film['recType'] = recType
            recs.append(film)

        isDuplicateRec = False
        i += 1


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
    global oldProfile
    global vectorProfileChanges

    recVector = allFilmDataVectorized[recs[index]['id']]

    # todo can these repetitive if-else chains be simplified?

    if recType == "wildcard":
        vectorChange = (recVector - oldProfile) * WILDCARD_FEEDBACK_FACTOR
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
            oldProfile += vectorChange
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
            oldProfile -= vectorChange
        elif recType == "recency":
            recencyProfile -= vectorChange
        elif recType == "user":
            userProfile -= vectorChange
        else:
            return "unknown rec type:" + str(recType)
        recStates[index] = -1

    # after changing vector parameters, ensure that all vector features are >= 0.0 && <= 1.0
    if recType == "wildcard":
        keepVectorBoundary(oldProfile, profileVectorLength)
    elif recType == "recency":
        keepVectorBoundary(recencyProfile, profileVectorLength)
    elif recType == "user":
        keepVectorBoundary(userProfile, profileVectorLength)
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
    global oldProfile
    global vectorProfileChanges

    vectorChange = vectorProfileChanges[index]

    # todo can these repetitive if-else chains be simplified?
    # if the film was previously disliked
    if add:
        if recType == "wildcard":
            oldProfile += vectorChange
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
            oldProfile -= vectorChange
        elif recType == "recency":
            recencyProfile -= vectorChange
        elif recType == "user":
            userProfile -= vectorChange
        else:
            return "unknown rec type:" + str(recType)

        recStates[index] = 0

    # make the profile change a zero vector at the specified index
    vectorProfileChanges[index] = np.zeros(profileVectorLength)

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


@app.route('/loadJsonFiles')
def loadJsonFiles():
    global allFilmDataVectorized
    global allFilmDataVectorizedMagnitudes
    global cachedLetterboxdTitles
    global cache

    try:
        allFilmDataVectorizedFile = open('../database/all-film-data-vectorized.json')
        allFilmDataVectorized = json.load(allFilmDataVectorizedFile)
        allFilmDataVectorizedMagnitudesFile = open('../database/all-film-data-vectorized-magnitudes.json')
        allFilmDataVectorizedMagnitudes = json.load(allFilmDataVectorizedMagnitudesFile)
        cachedLetterboxdTitlesFile = open('../database/cached-letterboxd-titles.json')
        cachedLetterboxdTitles = json.load(cachedLetterboxdTitlesFile)
        cacheFile = open('../database/cache.json')
        cache = json.load(cacheFile)
    except FileNotFoundError:
        return "File Not Found Error", 404
    except Exception as e:
        return f"Error: {e}", 400

    return "Files read successfully", 200


def deleteCsvFiles():
    for f in glob.glob("../database/*.csv"):
        os.remove(f)


if __name__ == "__main__":
    app.run(host='localhost', port=60000)

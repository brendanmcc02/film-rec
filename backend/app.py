# the python flask backend service. contains methods that expose API endpoints and other utility methods.

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import json
import csv
import numpy as np
import os
import glob
from vectorizeUtilities import *
from initAllFilmData import RUNTIME_THRESHOLD, NUMBER_OF_VOTES_THRESHOLD
from letterboxdConversionUtilities import *

DATE_RATED_WEIGHT = 0.8
NUMBER_OF_RECOMMENDATIONS_PER_ROW = 6
NUMBER_OF_FILMS_WATCHED_IN_GENRE_THRESHOLD = 30
NUMBER_OF_GENRE_RECOMMENDATION_ROWS = 3
RECOMMENDATION_REVIEW_FACTOR = 0.2
USER_UPLOADED_DATA_DIRECTORY_NAME = "user-uploaded-data/"
UNSUPPORTED_MEDIA_TYPE_ERROR_MESSAGE = "File must be .csv or .zip."
NO_FILE_IN_REQUEST_ERROR_MESSAGE = "No file found in the request"
FILE_MORE_DATA_THAN_ROW_HEADERS_ERROR_MESSAGE = "File has more data than row headers."
FILE_ROW_HEADERS_UNEXPECTED_FORMAT_ERROR_MESSAGE = "Row headers do not conform to expected format."
FILE_UPLOAD_SUCCESS_MESSAGE = "Upload Success."
JSON_FILES_LOAD_SUCCESS_MESSAGE = "JSON files loaded successfully."
JSON_FILES_ALREADY_LOADED_MESSAGE = "JSON files have already been loaded."
JSON_FILES_NOT_FOUND_ERROR_MESSAGE = "JSON files not found."
JSON_FILES_DECODE_ERROR_MESSAGE = "JSON files decode error."
INVALID_ZIP_FILE_ERROR_MESSAGE = "Zip file is invalid."

profileVectorLength = 0
allFilmDataUnseen = {}
allFilmDataVectorized = {}
allFilmDataVectorizedMagnitudes = {}
cachedLetterboxdTitles = {}
cache = {}
cachedNormalizedYearsKeys = []
cachedNormalizedImdbRatingsKeys = []
cachedNormalizedRuntimesKeys = []
diffDateRated = datetime(1, 1, 1)
minDateRated = datetime.now()
favouriteProfile = {'profile': np.zeros(profileVectorLength), 'profileId': 'favourite'}
genreProfiles = []
recencyProfile = {'profile': np.zeros(profileVectorLength), 'profileId': 'recency'}
internationalProfile = {'profile': np.zeros(profileVectorLength), 'profileId': 'international'}
oldProfile = {'profile': np.zeros(profileVectorLength), 'profileId': 'old'}
rowsOfRecommendations = []
isImdbFile = True
userFilmDataFilename = ""
allGenresLength = 0
allCountriesLength = 0
haveJsonFilesAlreadyBeenLoaded = False

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://film-rec.onrender.com"}})


def resetGlobalVariables():
    global genreProfiles
    global recencyProfile
    global internationalProfile
    global oldProfile
    global favouriteProfile
    global allFilmDataUnseen
    global rowsOfRecommendations
    global minDateRated
    global isImdbFile
    global userFilmDataFilename
    global allGenresLength
    global allCountriesLength

    favouriteProfile = {'profile': np.zeros(profileVectorLength), 'profileId': 'favourite'}
    genreProfiles = []
    recencyProfile = {'profile': np.zeros(profileVectorLength), 'profileId': 'receny'}
    internationalProfile = {'profile': np.zeros(profileVectorLength), 'profileId': 'international'}
    oldProfile = {'profile': np.zeros(profileVectorLength), 'profileId': 'old'}
    allFilmDataUnseen = {}
    rowsOfRecommendations = []
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

    deleteUserUploadedData()

    if 'file' not in request.files:
        return NO_FILE_IN_REQUEST_ERROR_MESSAGE, 400

    file = request.files['file']
    userFilmDataFilename = file.filename

    if isUnacceptableMediaType(userFilmDataFilename):
        return UNSUPPORTED_MEDIA_TYPE_ERROR_MESSAGE, 415

    try:
        userUploadedFileLocation = USER_UPLOADED_DATA_DIRECTORY_NAME + userFilmDataFilename
        file.save(userUploadedFileLocation)

        if userUploadedFileLocation.endswith(".zip"):
            if isLetterboxdZipFileInvalid(USER_UPLOADED_DATA_DIRECTORY_NAME, userFilmDataFilename):
                return INVALID_ZIP_FILE_ERROR_MESSAGE, 400
            else:
                userFilmDataFilename = "ratings.csv"
                userUploadedFileLocation = USER_UPLOADED_DATA_DIRECTORY_NAME + userFilmDataFilename

        expectedImdbFileFilmAttributes = ["Const", "Your Rating", "Date Rated", "Title", "Original Title", "URL",
                                        "Title Type", "IMDb Rating", "Runtime (mins)", "Year", "Genres", "Num Votes",
                                        "Release Date", "Directors"]

        with open(userUploadedFileLocation, encoding='utf-8') as userFilmDataFile:
            reader = csv.DictReader(userFilmDataFile, delimiter=',', restkey='unexpectedData')

            for row in reader:
                if 'unexpectedData' in row:
                    return FILE_MORE_DATA_THAN_ROW_HEADERS_ERROR_MESSAGE, 400

                keys = list(row.keys())
                for k in keys:
                    if k not in expectedImdbFileFilmAttributes:
                        isImdbFile = False
                        if k not in expectedLetterboxdFileFilmAttributes:
                            return FILE_ROW_HEADERS_UNEXPECTED_FORMAT_ERROR_MESSAGE, 400

        return FILE_UPLOAD_SUCCESS_MESSAGE, 200
    except Exception as e:
        deleteUserUploadedData()
        return f"Error occurred with reading {userFilmDataFilename}.\n{e}", 400


@app.route('/initRowsOfRecommendations')
def initRowsOfRecommendations():
    global allFilmDataVectorized
    global allFilmDataVectorizedMagnitudes
    global diffDateRated
    global minDateRated
    global allFilmDataUnseen
    global profileVectorLength
    global allGenresLength
    global allCountriesLength
    global genreProfiles
    global recencyProfile
    global internationalProfile
    global oldProfile
    global favouriteProfile

    try:
        userFilmDataList = []
        userUploadedFileLocation = USER_UPLOADED_DATA_DIRECTORY_NAME + userFilmDataFilename
        with open(userUploadedFileLocation, encoding='utf8') as userFilmDataFile:
            reader = csv.DictReader(userFilmDataFile, delimiter=',', restkey='unexpectedData')

            for row in reader:
                userFilmDataList.append(row)
    except Exception as e:
        deleteUserUploadedData()
        return f"Error occurred with reading {userFilmDataFilename}.\n" + str(e), 400

    deleteUserUploadedData()
    allFilmDataFile = open('../database/all-film-data.json')
    allFilmData = json.load(allFilmDataFile)

    if not isImdbFile:
        userFilmDataList = convertLetterboxdFormatToImdbFormat(userFilmDataList, allFilmData, cachedLetterboxdTitles)

    userFilmData = {}
    favouriteFilmIds = []
    minDateRated = datetime.now()
    maxDateRated = minDateRated

    for film in userFilmDataList:
        if film['Title Type'] == "Movie" and int(film['Runtime (mins)']) >= RUNTIME_THRESHOLD and film['Genres'] != ""\
                and int(film['Num Votes']) >= NUMBER_OF_VOTES_THRESHOLD:
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
                deleteUserUploadedData()
                return f"value error with film: {film['Const']}", 400

    diffDateRated = maxDateRated - minDateRated
    isDiffDateRatedZero = False
    if diffDateRated == 0.0:
        isDiffDateRatedZero = True

    for imdbFilmId in allFilmData:
        if imdbFilmId not in userFilmData:
            allFilmDataUnseen[imdbFilmId] = allFilmData[imdbFilmId]

    userFilmDataVectorized = {}

    # init a dict with pre-computed scalar values
    cachedDateRatedAndUserRatingWeights = {}
    
    allGenresLength = len(cache['allGenres'])
    allCountriesLength = len(cache['allCountries'])

    # vectorize user-film-data
    for imdbFilmId in userFilmData:
        vector = vectorizeFilm(userFilmData[imdbFilmId], cache['allGenres'], cache['allCountries'],
                               cache['normalizedYears'], cache['normalizedImdbRatings'], cache['minNumberOfVotes'],
                               cache['diffNumberOfVotes'], cache['normalizedRuntimes'])
        if isDiffDateRatedZero:
            dateRatedWeight = 1.0
        else:
            # normalize the dateRatedWeight as a float between DATE_RATED_WEIGHT and 1.0.
            dateRatedWeight = (((userFilmData[imdbFilmId]['dateRated'] - minDateRated) / diffDateRated) *
                                (1 - DATE_RATED_WEIGHT)) + DATE_RATED_WEIGHT

        # imdbRatings run from 1-10, we want values to run from 0.1 - 1.0
        userRatingWeight = round((userFilmData[imdbFilmId]['userRating'] / 10.0), 1)
        cachedDateRatedAndUserRatingWeights[imdbFilmId] = dateRatedWeight * userRatingWeight

        userFilmDataVectorized[imdbFilmId] = vector * cachedDateRatedAndUserRatingWeights[imdbFilmId]

    profileVectorLength = cache['profileVectorLength']

    favouriteProfile = initFavouriteProfile(userFilmData, userFilmDataVectorized, profileVectorLength,
                                            cachedDateRatedAndUserRatingWeights, favouriteFilmIds,
                                            cache['allGenres'], cache['allCountries'])

    recencyProfile = initRecencyProfile(userFilmData, userFilmDataVectorized, maxDateRated, 
                                        profileVectorLength, cachedDateRatedAndUserRatingWeights, cache['allGenres'],
                                        cache['allCountries'])

    genreProfiles = initGenreProfiles(userFilmData, userFilmDataVectorized, cachedDateRatedAndUserRatingWeights,
                                      cache['allGenres'], profileVectorLength, NUMBER_OF_FILMS_WATCHED_IN_GENRE_THRESHOLD, 
                                      cache['allCountries'])

    userProfile = initUserProfile(userFilmData, userFilmDataVectorized, profileVectorLength,
                                  cachedDateRatedAndUserRatingWeights, cache['allGenres'], cache['allCountries'])

    internationalProfile = initInternationalProfile(userProfile['profile'], cache['allCountries'], allGenresLength,
                                                    profileVectorLength)

    oldProfile = initOldProfile(userProfile['profile'])

    generateRecommendations()

    return jsonify(rowsOfRecommendations), 200


def generateRecommendations():
    global rowsOfRecommendations
    global genreProfiles
    rowsOfRecommendations = []

    if np.array_equal(favouriteProfile['profile'], np.zeros(profileVectorLength)):
        print("No favourite profile.")
    else:
        getFilmRecommendations("Based on your favourite films", allFilmDataUnseen, NUMBER_OF_RECOMMENDATIONS_PER_ROW, 
                               favouriteProfile['profile'], favouriteProfile['profileId'])
        # printStringifiedVector(favouriteProfile['profile'], cache['allGenres'], cache['allCountries'], "Favourite",
        #                        cachedNormalizedYearsKeys, cachedNormalizedRuntimesKeys, cachedNormalizedImdbRatingsKeys,
        #                        cache['minNumberOfVotes'], cache['diffNumberOfVotes'])

    if np.array_equal(recencyProfile['profile'], np.zeros(profileVectorLength)):
        print("No recency profile.")
    else:
        getFilmRecommendations("Based on what you watched recently", allFilmDataUnseen, NUMBER_OF_RECOMMENDATIONS_PER_ROW, 
                               recencyProfile['profile'], recencyProfile['profileId'])
        # printStringifiedVector(recencyProfile['profile'], cache['allGenres'], cache['allCountries'], "Recency",
        #                        cachedNormalizedYearsKeys, cachedNormalizedRuntimesKeys, cachedNormalizedImdbRatingsKeys,
        #                        cache['minNumberOfVotes'], cache['diffNumberOfVotes'])

    genreProfiles = sorted(genreProfiles, key=lambda x: x['weightedMeanRating'], reverse=True)

    for i in range(NUMBER_OF_GENRE_RECOMMENDATION_ROWS):
        if genreProfiles[i]['weightedMeanRating'] == 0.0:
            print("No genre profile.")
        else:
            countryText = getProfileMaxCountry(genreProfiles[i]['profile'], allGenresLength, cache['allCountries'])
            getFilmRecommendations(f"Because you like {countryText} {genreProfiles[i]['profileId']} films", 
                                   allFilmDataUnseen, NUMBER_OF_RECOMMENDATIONS_PER_ROW, genreProfiles[i]['profile'], 
                                   genreProfiles[i]['profileId'])
            # printStringifiedVector(genreProfiles[i]['profile'], cache['allGenres'], cache['allCountries'], 
            #                        genreProfiles[i]['profileId'], cachedNormalizedYearsKeys, 
            #                        cachedNormalizedRuntimesKeys, cachedNormalizedImdbRatingsKeys, 
            #                        cache['minNumberOfVotes'], cache['diffNumberOfVotes'])
        
    if np.array_equal(internationalProfile['profile'], np.zeros(profileVectorLength)):
        print("No international profile.")
    else:
        getFilmRecommendations("Try out some international films", allFilmDataUnseen, 
                                NUMBER_OF_RECOMMENDATIONS_PER_ROW, internationalProfile['profile'], 
                                internationalProfile['profileId'])
        # printStringifiedVector(internationalProfile['profile'], cache['allGenres'], cache['allCountries'], 
        #                        "International", cachedNormalizedYearsKeys, cachedNormalizedRuntimesKeys,
        #                        cachedNormalizedImdbRatingsKeys, cache['minNumberOfVotes'], cache['diffNumberOfVotes'])

    if np.array_equal(oldProfile['profile'], np.zeros(profileVectorLength)):
        print("No old profile.")
    else:
        getFilmRecommendations("Try out some older films", allFilmDataUnseen, NUMBER_OF_RECOMMENDATIONS_PER_ROW, 
                                oldProfile['profile'], oldProfile['profileId'])
        # printStringifiedVector(oldProfile['profile'], cache['allGenres'], cache['allCountries'], "Old",
        #                        cachedNormalizedYearsKeys, cachedNormalizedRuntimesKeys,
        #                        cachedNormalizedImdbRatingsKeys, cache['minNumberOfVotes'], cache['diffNumberOfVotes'])


def getFilmRecommendations(recommendedRowText, allFilmData, numberOfRecommendations, profileVector, 
                           profileId):
    global rowsOfRecommendations
    global allFilmDataVectorizedMagnitudes

    rowsOfRecommendations.append({"recommendedRowText": recommendedRowText, "recommendedFilms": [], 
                                  "profileId": profileId})
    profileVectorMagnitude = np.linalg.norm(profileVector)
    cosineSimilarities = {}

    for filmId in allFilmData:
        filmVectorMagnitude = allFilmDataVectorizedMagnitudes[filmId]
        cosineSimilarities[filmId] = cosineSimilarity(allFilmDataVectorized[filmId], profileVector,
                                                      filmVectorMagnitude, profileVectorMagnitude)

    cosineSimilarities = sorted(cosineSimilarities.items(), key=lambda x: x[1], reverse=True)

    i = 0
    while i < numberOfRecommendations:
        filmId = cosineSimilarities[i][0]
        
        if isFilmRecommendationUnique(filmId):
            film = allFilmDataUnseen[filmId]
            similarityScore = cosineSimilarities[i][1]
            film['id'] = filmId
            film['similarityScore'] = int(similarityScore * 100.0)

            rowsOfRecommendations[-1]['recommendedFilms'].append(film)
        else:
            numberOfRecommendations += 1

        i += 1


def isFilmRecommendationUnique(filmId):
    for rowOfRecommendations in rowsOfRecommendations:
        for recommendedFilm in rowOfRecommendations['recommendedFilms']:
            if recommendedFilm['id'] == filmId:
                return False
            
    return True


@app.route('/reviewRecommendation')
def reviewRecommendation():
    filmId = request.args.get('filmId')
    isThumbsUp = request.args.get('isThumbsUp').lower() == 'true'

    for row in rowsOfRecommendations:
        for film in row['recommendedFilms']:
            if film['id'] == filmId:
                profileId = row['profileId']

    profile = getProfile(profileId)

    # if the profile is a genre profile
    if profileId in cache['allGenres']:
        adjustment = profile['weightedMeanRating'] * RECOMMENDATION_REVIEW_FACTOR
        if isThumbsUp:
            profile['weightedMeanRating'] += adjustment
        else:
            profile['weightedMeanRating'] -= adjustment

    filmVector = allFilmDataVectorized[filmId]
    adjustment = (filmVector - profile['profile']) * RECOMMENDATION_REVIEW_FACTOR

    for i in range(len(adjustment)):
        if adjustment[i] == 0.0:
            adjustment[i] = RECOMMENDATION_REVIEW_FACTOR

    if isThumbsUp:
        profile['profile'] += adjustment
    else:
        profile['profile'] -= adjustment

    keepVectorBoundary(profile['profile'])

    return f"changed {profileId} profile due to after reviewing {filmId}", 200


def getProfile(profileId):
    if profileId == "favourite":
        return favouriteProfile
    elif profileId == "recency":
        return recencyProfile
    elif profileId == "old":
        return oldProfile
    elif profileId == "international":
        return internationalProfile
    else:
        for profile in genreProfiles:
            if profile['profileId'] == profileId:
                return profile

    print(f"Error: profile {profileId} not found. Returning zero vector.")
    return {'profile': np.zeros(profileVectorLength), 'profileId': profileId}


@app.route('/regenerateRecommendations')
def regenerateRecommendations():
    global rowsOfRecommendations
    global allFilmDataUnseen

    for row in rowsOfRecommendations:
        for film in row['recommendedFilms']:
            filmId = film['id']
            del allFilmDataUnseen[filmId]

    generateRecommendations()

    return jsonify(rowsOfRecommendations), 200


@app.route('/loadJsonFiles')
def loadJsonFiles():
    global haveJsonFilesAlreadyBeenLoaded

    if (haveJsonFilesAlreadyBeenLoaded):
        return JSON_FILES_ALREADY_LOADED_MESSAGE, 304
    
    global allFilmDataVectorized
    global allFilmDataVectorizedMagnitudes
    global cachedLetterboxdTitles
    global cache
    global cachedNormalizedYearsKeys
    global cachedNormalizedImdbRatingsKeys
    global cachedNormalizedRuntimesKeys

    try:
        allFilmDataVectorizedFile = open('../database/all-film-data-vectorized.json')
        allFilmDataVectorized = json.load(allFilmDataVectorizedFile)
        allFilmDataVectorizedMagnitudesFile = open('../database/all-film-data-vectorized-magnitudes.json')
        allFilmDataVectorizedMagnitudes = json.load(allFilmDataVectorizedMagnitudesFile)
        cachedLetterboxdTitlesFile = open('../database/cached-letterboxd-titles.json')
        cachedLetterboxdTitles = json.load(cachedLetterboxdTitlesFile)
        cacheFile = open('../database/cache.json')
        cache = json.load(cacheFile)
        cachedNormalizedYearsKeys = list(cache['normalizedYears'].keys())
        cachedNormalizedImdbRatingsKeys = list(cache['normalizedImdbRatings'].keys())
        cachedNormalizedRuntimesKeys = list(cache['normalizedRuntimes'].keys())

        haveJsonFilesAlreadyBeenLoaded = True

        return JSON_FILES_LOAD_SUCCESS_MESSAGE, 200
    except FileNotFoundError:
        return JSON_FILES_NOT_FOUND_ERROR_MESSAGE, 404
    except json.JSONDecodeError:
        return JSON_FILES_DECODE_ERROR_MESSAGE, 400


def deleteUserUploadedData():
    for fileOrDirectory in os.listdir(USER_UPLOADED_DATA_DIRECTORY_NAME):
        fileOrDirectoryPath = os.path.join(USER_UPLOADED_DATA_DIRECTORY_NAME, fileOrDirectory)
        if os.path.isdir(fileOrDirectoryPath):
            shutil.rmtree(fileOrDirectoryPath)
        elif fileOrDirectoryPath != ".gitignore":
            os.remove(fileOrDirectoryPath)


def isUnacceptableMediaType(filename):
    return not (filename.lower().endswith(".csv") or filename.lower().endswith(".zip"))


if __name__ == "__main__":
    app.run()

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

DATE_RATED_WEIGHT = 0.8
NUM_RECOMMENDATIONS_PER_ROW = 6
NUM_FILMS_WATCHED_IN_GENRE_THRESHOLD = 30
NUM_TOP_GENRE_PROFILES = 3
RECOMMENDATION_REVIEW_FACTOR = 0.1

profileVectorLength = 0
allFilmDataUnseen = {}
allFilmDataVectorized = {}
allFilmDataVectorizedMagnitudes = {}
cachedLetterboxdTitles = {}
cache = {}
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

app = Flask(__name__)


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
    cachedDateRatedAndUserRatingWeights = {}
    
    allGenresLength = len(cache['allGenres'])
    allCountriesLength = len(cache['allCountries'])

    # vectorize user-film-data
    for imdbFilmId in userFilmDataIds:
        vector = vectorizeFilm(userFilmData[imdbFilmId], cache['allGenres'], cache['allCountries'],
                               cache['normalizedYears'], cache['normalizedImdbRatings'], cache['minNumberOfVotes'],
                               cache['diffNumberOfVotes'], cache['normalizedRuntimes'])
        # normalize the dateRatedWeight as a float between DATE_RATED_WEIGHT and 1.0.
        dateRatedWeight = (((userFilmData[imdbFilmId]['dateRated'] - minDateRated) / diffDateRated) *
                           (1 - DATE_RATED_WEIGHT)) + DATE_RATED_WEIGHT

        # imdbRatings run from 1-10, we want values to run from 0.1 - 1.0
        userRatingWeight = round((userFilmData[imdbFilmId]['userRating'] / 10.0), 1)
        cachedDateRatedAndUserRatingWeights[imdbFilmId] = dateRatedWeight * userRatingWeight

        userFilmDataVectorized[imdbFilmId] = vector * cachedDateRatedAndUserRatingWeights[imdbFilmId]

    profileVectorLength = cache['profileVectorLength']

    favouriteProfile = initFavouriteProfile(userFilmDataIds, userFilmDataVectorized, profileVectorLength,
                                            cachedDateRatedAndUserRatingWeights, favouriteFilmIds,
                                            cache['allGenres'], cache['allCountries'])

    recencyProfile = initRecencyProfile(userFilmData, userFilmDataIds, userFilmDataVectorized, maxDateRated, 
                                        profileVectorLength, cachedDateRatedAndUserRatingWeights, cache['allGenres'],
                                        cache['allCountries'])

    genreProfiles = initGenreProfiles(userFilmDataIds, userFilmDataVectorized, cachedDateRatedAndUserRatingWeights,
                                      cache['allGenres'], profileVectorLength, NUM_FILMS_WATCHED_IN_GENRE_THRESHOLD, 
                                      cache['allCountries'])
    
    userProfile = initUserProfile(userFilmDataIds, userFilmDataVectorized, profileVectorLength,
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
    allFilmDataIds = list(allFilmDataUnseen.keys())

    if np.array_equal(favouriteProfile['profile'], np.zeros(profileVectorLength)):
        print("No favourite profile.")
    else:
        getFilmRecommendations("Based on your favourite films", allFilmDataIds, NUM_RECOMMENDATIONS_PER_ROW, 
                               favouriteProfile['profile'], favouriteProfile['profileId'])
        printStringifiedVector(favouriteProfile['profile'], cache['allGenres'], cache['allCountries'], "Favourite")

    if np.array_equal(recencyProfile['profile'], np.zeros(profileVectorLength)):
        print("No recency profile.")
    else:
        getFilmRecommendations("Based on what you watched recently", allFilmDataIds, NUM_RECOMMENDATIONS_PER_ROW, 
                               recencyProfile['profile'], recencyProfile['profileId'])
        printStringifiedVector(recencyProfile['profile'], cache['allGenres'], cache['allCountries'], "Recency")

    genreProfiles = sorted(genreProfiles, key=lambda x: x['weightedMeanRating'], reverse=True)

    max = NUM_TOP_GENRE_PROFILES
    i = 0
    while i < max:
        if genreProfiles[i]['weightedMeanRating'] == 0.0:
            print("No genre profile.")
        else:
            countryText = getProfileMaxCountry(genreProfiles[i]['profile'], allGenresLength, cache['allCountries'])
            getFilmRecommendations(f"Because you like {countryText} {genreProfiles[i]['profileId']} films", 
                                   allFilmDataIds, NUM_RECOMMENDATIONS_PER_ROW, genreProfiles[i]['profile'], 
                                   genreProfiles[i]['profileId'])
            printStringifiedVector(genreProfiles[i]['profile'], cache['allGenres'], cache['allCountries'], 
                                   genreProfiles[i]['profileId'])
        
        i += 1
        
    if np.array_equal(internationalProfile['profile'], np.zeros(profileVectorLength)):
        print("No international profile.")
    else:
        getFilmRecommendations("Try out some international films", allFilmDataIds, 
                                NUM_RECOMMENDATIONS_PER_ROW, internationalProfile['profile'], 
                                internationalProfile['profileId'])
        printStringifiedVector(internationalProfile['profile'], cache['allGenres'], cache['allCountries'], 
                               "International")

    if np.array_equal(oldProfile['profile'], np.zeros(profileVectorLength)):
        print("No old profile.")
    else:
        getFilmRecommendations("Try out some older films", allFilmDataIds, NUM_RECOMMENDATIONS_PER_ROW, 
                                oldProfile['profile'], oldProfile['profileId'])
        printStringifiedVector(oldProfile['profile'], cache['allGenres'], cache['allCountries'], "Old")


def getFilmRecommendations(recommendedRowText, allFilmDataIds, numberOfRecommendations, profileVector, 
                           profileId):
    global rowsOfRecommendations
    global allFilmDataVectorizedMagnitudes

    rowsOfRecommendations.append({"recommendedRowText": recommendedRowText, "recommendedFilms": [], 
                                  "profileId": profileId})
    profileVectorMagnitude = np.linalg.norm(profileVector)
    cosineSimilarities = {}

    for filmId in allFilmDataIds:
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
            film['similarityScore'] = round(similarityScore * 100.0, 2)
            film['wasFilmReviewed'] = False

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
                film['wasFilmReviewed'] = True

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

    keepVectorBoundary(profile['profile'], profileVectorLength)

    return f"changed {profileId} profile due to {("liking" if isThumbsUp else "disliking")} of {filmId}", 200


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
            if film['wasFilmReviewed']:
                filmId = film['id']
                del allFilmDataUnseen[filmId]

    generateRecommendations()

    return jsonify(rowsOfRecommendations), 200


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
    for file in glob.glob("../database/*.csv"):
        os.remove(file)


if __name__ == "__main__":
    app.run(host='localhost', port=60000)

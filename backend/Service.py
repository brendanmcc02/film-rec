import csv
from datetime import datetime
from flask import request, jsonify
import numpy as np
import json
import os
from LetterboxdConversionUtilities import *
from InitDocumentDatabase import *
from VectorizeUtilities import *

class Service:

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
    JSON_FILES_NOT_FOUND_ERROR_MESSAGE = "JSON files not found."
    JSON_FILES_DECODE_ERROR_MESSAGE = "JSON files decode error."
    INVALID_ZIP_FILE_ERROR_MESSAGE = "Zip file is invalid."

    def __init__(self, profileVectorLength=0, allFilmDataUnseen={}, allFilmDataVectorized={}, allFilmDataVectorizedMagnitudes={},
                 cachedLetterboxdTitles={}, cache={}, cachedNormalizedYearsKeys=[], cachedNormalizedImdbRatingsKeys=[],
                 cachedNormalizedRuntimesKeys = [], diffDateRated=datetime(1, 1, 1), minDateRated = datetime.now(), 
                 favouriteProfile = {'profile': np.zeros(0), 'profileId': 'favourite'},
                 genreProfiles = [], recencyProfile = {'profile': np.zeros(0), 'profileId': 'recency'}, 
                 internationalProfile = {'profile': np.zeros(0), 'profileId': 'international'}, 
                 oldProfile = {'profile': np.zeros(0), 'profileId': 'old'}, 
                 rowsOfRecommendations = [], isImdbFile = True, userFilmDataFilename = "", allGenresLength = 0, allCountriesLength = 0):
        self.profileVectorLength = 0
        self.allFilmDataUnseen = {}
        self.allFilmDataVectorized = {}
        self.allFilmDataVectorizedMagnitudes = {}
        self.cachedLetterboxdTitles = {}
        self.cache = {}
        self.cachedNormalizedYearsKeys = []
        self.cachedNormalizedImdbRatingsKeys = []
        self.cachedNormalizedRuntimesKeys = []
        self.diffDateRated = datetime(1, 1, 1)
        self.minDateRated = datetime.now()
        self.favouriteProfile = {'profile': np.zeros(self.profileVectorLength), 'profileId': 'favourite'}
        self.genreProfiles = []
        self.recencyProfile = {'profile': np.zeros(self.profileVectorLength), 'profileId': 'recency'}
        self.internationalProfile = {'profile': np.zeros(self.profileVectorLength), 'profileId': 'international'}
        self.oldProfile = {'profile': np.zeros(self.profileVectorLength), 'profileId': 'old'}
        self.rowsOfRecommendations = []
        self.isImdbFile = True
        self.userFilmDataFilename = ""
        self.allGenresLength = 0
        self.allCountriesLength = 0

    def verifyUserUploadedFile(self):
        _letterboxdConversionUtilities = LetterboxdConversionUtilities()

        self.deleteUserUploadedData()

        if 'file' not in request.files:
            return self.NO_FILE_IN_REQUEST_ERROR_MESSAGE, 400

        file = request.files['file']
        self.userFilmDataFilename = file.filename

        if self.isUnacceptableMediaType(self.userFilmDataFilename):
            return self.UNSUPPORTED_MEDIA_TYPE_ERROR_MESSAGE, 415

        try:
            userUploadedFileLocation = self.USER_UPLOADED_DATA_DIRECTORY_NAME + self.userFilmDataFilename
            file.save(userUploadedFileLocation)

            if userUploadedFileLocation.endswith(".zip"):
                if _letterboxdConversionUtilities.isLetterboxdZipFileInvalid(self.USER_UPLOADED_DATA_DIRECTORY_NAME, self.userFilmDataFilename):
                    return self.INVALID_ZIP_FILE_ERROR_MESSAGE, 400
                else:
                    self.userFilmDataFilename = "ratings.csv"
                    userUploadedFileLocation = self.USER_UPLOADED_DATA_DIRECTORY_NAME + self.userFilmDataFilename

            expectedImdbFileFilmAttributes = ["Const", "Your Rating", "Date Rated", "Title", "Original Title", "URL",
                                            "Title Type", "IMDb Rating", "Runtime (mins)", "Year", "Genres", "Num Votes",
                                            "Release Date", "Directors"]

            with open(userUploadedFileLocation, encoding='utf-8') as userFilmDataFile:
                reader = csv.DictReader(userFilmDataFile, delimiter=',', restkey='unexpectedData')

                for row in reader:
                    if 'unexpectedData' in row:
                        return self.FILE_MORE_DATA_THAN_ROW_HEADERS_ERROR_MESSAGE, 400

                    keys = list(row.keys())
                    for key in keys:
                        if key not in expectedImdbFileFilmAttributes:
                            self.isImdbFile = False
                            if key not in _letterboxdConversionUtilities.EXPECTED_LETTERBOXD_FILE_FILM_ATTRIBUTES:
                                return self.FILE_ROW_HEADERS_UNEXPECTED_FORMAT_ERROR_MESSAGE, 400

            return self.FILE_UPLOAD_SUCCESS_MESSAGE, 200
        except Exception as e:
            self.deleteUserUploadedData()
            return f"Error occurred with reading {self.userFilmDataFilename}.\n{e}", 400

    def initRowsOfRecommendations(self):
        try:
            userFilmDataList = []
            userUploadedFileLocation = self.USER_UPLOADED_DATA_DIRECTORY_NAME + self.userFilmDataFilename
            with open(userUploadedFileLocation, encoding='utf8') as userFilmDataFile:
                reader = csv.DictReader(userFilmDataFile, delimiter=',', restkey='unexpectedData')

                for row in reader:
                    userFilmDataList.append(row)
        except Exception as e:
            self.deleteUserUploadedData()
            return f"Error occurred with reading {self.userFilmDataFilename}.\n" + str(e), 400

        self.deleteUserUploadedData()
        allFilmDataFile = open('../database/all-film-data.json')
        allFilmData = json.load(allFilmDataFile)

        _letterboxdConversionUtilities = LetterboxdConversionUtilities()

        if not self.isImdbFile:
            userFilmDataList = (_letterboxdConversionUtilities
                                .convertLetterboxdFormatToImdbFormat(userFilmDataList, allFilmData, self.cachedLetterboxdTitles))

        userFilmData = {}
        favouriteFilmIds = []
        self.minDateRated = datetime.now()
        maxDateRated = self.minDateRated

        _initDocumentDatabase = InitDocumentDatabase()

        for film in userFilmDataList:
            if (film['Title Type'] == "Movie" and 
                    int(film['Runtime (mins)']) >= _initDocumentDatabase.RUNTIME_THRESHOLD and film['Genres'] != ""\
                    and int(film['Num Votes']) >= _initDocumentDatabase.NUMBER_OF_VOTES_THRESHOLD):
                if self.isImdbFile:
                    genres = film['Genres'].replace("\"", "").split(", ")
                else:
                    genres = film['Genres']
                try:
                    filmId = film['Const']
                    if filmId in allFilmData:
                        dateRated = datetime.strptime(film['Date Rated'], "%Y-%m-%d")
                        self.minDateRated = min(self.minDateRated, dateRated)

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
                    self.deleteUserUploadedData()
                    return f"value error with film: {film['Const']}", 400

        self.diffDateRated = maxDateRated - self.minDateRated
        isDiffDateRatedZero = False
        if self.diffDateRated == 0.0:
            isDiffDateRatedZero = True

        for imdbFilmId in allFilmData:
            if imdbFilmId not in userFilmData:
                self.allFilmDataUnseen[imdbFilmId] = allFilmData[imdbFilmId]

        userFilmDataVectorized = {}

        # init a dict with pre-computed scalar values
        cachedDateRatedAndUserRatingWeights = {}
        
        self.allGenresLength = len(self.cache['allGenres'])
        self.allCountriesLength = len(self.cache['allCountries'])

        _vectorizeUtilities = VectorizeUtilities()

        # vectorize user-film-data
        for imdbFilmId in userFilmData:
            vector = _vectorizeUtilities.vectorizeFilm(userFilmData[imdbFilmId], self.cache['allGenres'], self.cache['allCountries'],
                                                       self.cache['normalizedYears'], self.cache['normalizedImdbRatings'], self.cache['minNumberOfVotes'],
                                                       self.cache['diffNumberOfVotes'], self.cache['normalizedRuntimes'])
            if isDiffDateRatedZero:
                dateRatedWeight = 1.0
            else:
                # normalize the dateRatedWeight as a float between DATE_RATED_WEIGHT and 1.0.
                dateRatedWeight = (((userFilmData[imdbFilmId]['dateRated'] - self.minDateRated) / self.diffDateRated) *
                                    (1 - self.DATE_RATED_WEIGHT)) + self.DATE_RATED_WEIGHT

            # imdbRatings run from 1-10, we want values to run from 0.1 - 1.0
            userRatingWeight = round((userFilmData[imdbFilmId]['userRating'] / 10.0), 1)
            cachedDateRatedAndUserRatingWeights[imdbFilmId] = dateRatedWeight * userRatingWeight

            userFilmDataVectorized[imdbFilmId] = vector * cachedDateRatedAndUserRatingWeights[imdbFilmId]

        self.profileVectorLength = self.cache['profileVectorLength']

        self.favouriteProfile = _vectorizeUtilities.initFavouriteProfile(userFilmData, userFilmDataVectorized, 
                                                                         self.profileVectorLength,
                                                                         cachedDateRatedAndUserRatingWeights, favouriteFilmIds,
                                                                         self.cache['allGenres'], self.cache['allCountries'])

        self.recencyProfile = _vectorizeUtilities.initRecencyProfile(userFilmData, userFilmDataVectorized, maxDateRated, 
                                            self.profileVectorLength, cachedDateRatedAndUserRatingWeights, self.cache['allGenres'],
                                            self.cache['allCountries'])

        self.genreProfiles = _vectorizeUtilities.initGenreProfiles(userFilmData, userFilmDataVectorized, cachedDateRatedAndUserRatingWeights,
                                                                   self.cache['allGenres'], self.profileVectorLength, self.NUMBER_OF_FILMS_WATCHED_IN_GENRE_THRESHOLD, 
                                                                   self.cache['allCountries'])

        userProfile = _vectorizeUtilities.initUserProfile(userFilmData, userFilmDataVectorized, self.profileVectorLength,
                                    cachedDateRatedAndUserRatingWeights, self.cache['allGenres'], self.cache['allCountries'])

        self.internationalProfile = _vectorizeUtilities.initInternationalProfile(userProfile['profile'], self.cache['allCountries'], self.allGenresLength,
                                                                                 self.profileVectorLength)

        self.oldProfile = _vectorizeUtilities.initOldProfile(userProfile['profile'])

        self.generateRecommendations()

        return jsonify(self.rowsOfRecommendations), 200

    def generateRecommendations(self):
        self.rowsOfRecommendations = []

        if np.array_equal(self.favouriteProfile['profile'], np.zeros(self.profileVectorLength)):
            print("No favourite profile.")
        else:
            self.getFilmRecommendations("Based on your favourite films", self.allFilmDataUnseen, self.NUMBER_OF_RECOMMENDATIONS_PER_ROW, 
                                        self.favouriteProfile['profile'], self.favouriteProfile['profileId'])
            # printStringifiedVector(favouriteProfile['profile'], cache['allGenres'], cache['allCountries'], "Favourite",
            #                        cachedNormalizedYearsKeys, cachedNormalizedRuntimesKeys, cachedNormalizedImdbRatingsKeys,
            #                        cache['minNumberOfVotes'], cache['diffNumberOfVotes'])

        if np.array_equal(self.recencyProfile['profile'], np.zeros(self.profileVectorLength)):
            print("No recency profile.")
        else:
            self.getFilmRecommendations("Based on what you watched recently", self.allFilmDataUnseen, self.NUMBER_OF_RECOMMENDATIONS_PER_ROW, 
                                        self.recencyProfile['profile'], self.recencyProfile['profileId'])
            # printStringifiedVector(recencyProfile['profile'], cache['allGenres'], cache['allCountries'], "Recency",
            #                        cachedNormalizedYearsKeys, cachedNormalizedRuntimesKeys, cachedNormalizedImdbRatingsKeys,
            #                        cache['minNumberOfVotes'], cache['diffNumberOfVotes'])

        self.genreProfiles = sorted(self.genreProfiles, key=lambda x: x['weightedMeanRating'], reverse=True)

        _vectorizeUtilities = VectorizeUtilities()

        for i in range(self.NUMBER_OF_GENRE_RECOMMENDATION_ROWS):
            if self.genreProfiles[i]['weightedMeanRating'] == 0.0:
                print("No genre profile.")
            else:
                countryText = _vectorizeUtilities.getProfileMaxCountry(self.genreProfiles[i]['profile'], self.allGenresLength, self.cache['allCountries'])
                self.getFilmRecommendations(f"Because you like {countryText} {self.genreProfiles[i]['profileId']} films", 
                                            self.allFilmDataUnseen, self.NUMBER_OF_RECOMMENDATIONS_PER_ROW, self.genreProfiles[i]['profile'], 
                                            self.genreProfiles[i]['profileId'])
                # printStringifiedVector(genreProfiles[i]['profile'], cache['allGenres'], cache['allCountries'], 
                #                        genreProfiles[i]['profileId'], cachedNormalizedYearsKeys, 
                #                        cachedNormalizedRuntimesKeys, cachedNormalizedImdbRatingsKeys, 
                #                        cache['minNumberOfVotes'], cache['diffNumberOfVotes'])
            
        if np.array_equal(self.internationalProfile['profile'], np.zeros(self.profileVectorLength)):
            print("No international profile.")
        else:
            self.getFilmRecommendations("Try out some international films", self.allFilmDataUnseen, 
                                    self.NUMBER_OF_RECOMMENDATIONS_PER_ROW, self.internationalProfile['profile'], 
                                    self.internationalProfile['profileId'])
            # printStringifiedVector(internationalProfile['profile'], cache['allGenres'], cache['allCountries'], 
            #                        "International", cachedNormalizedYearsKeys, cachedNormalizedRuntimesKeys,
            #                        cachedNormalizedImdbRatingsKeys, cache['minNumberOfVotes'], cache['diffNumberOfVotes'])

        if np.array_equal(self.oldProfile['profile'], np.zeros(self.profileVectorLength)):
            print("No old profile.")
        else:
            self.getFilmRecommendations("Try out some older films", self.allFilmDataUnseen, self.NUMBER_OF_RECOMMENDATIONS_PER_ROW, 
                                    self.oldProfile['profile'], self.oldProfile['profileId'])
            # printStringifiedVector(oldProfile['profile'], cache['allGenres'], cache['allCountries'], "Old",
            #                        cachedNormalizedYearsKeys, cachedNormalizedRuntimesKeys,
            #                        cachedNormalizedImdbRatingsKeys, cache['minNumberOfVotes'], cache['diffNumberOfVotes'])


    def getFilmRecommendations(self, recommendedRowText, allFilmData, numberOfRecommendations, profileVector, 
                               profileId):
        self.rowsOfRecommendations.append({"recommendedRowText": recommendedRowText, "recommendedFilms": [], 
                                    "profileId": profileId})
        profileVectorMagnitude = np.linalg.norm(profileVector)
        cosineSimilarities = {}

        _vectorizeUtilities = VectorizeUtilities()

        for filmId in allFilmData:
            filmVectorMagnitude = self.allFilmDataVectorizedMagnitudes[filmId]
            cosineSimilarities[filmId] = _vectorizeUtilities.cosineSimilarity(self.allFilmDataVectorized[filmId], profileVector,
                                                        filmVectorMagnitude, profileVectorMagnitude)

        cosineSimilarities = sorted(cosineSimilarities.items(), key=lambda x: x[1], reverse=True)

        i = 0
        while i < numberOfRecommendations:
            filmId = cosineSimilarities[i][0]
            
            if self.isFilmRecommendationUnique(filmId):
                film = self.allFilmDataUnseen[filmId]
                similarityScore = cosineSimilarities[i][1]
                film['id'] = filmId
                film['similarityScore'] = int(similarityScore * 100.0)

                self.rowsOfRecommendations[-1]['recommendedFilms'].append(film)
            else:
                numberOfRecommendations += 1

            i += 1


    def isFilmRecommendationUnique(self, filmId):
        for rowOfRecommendations in self.rowsOfRecommendations:
            for recommendedFilm in rowOfRecommendations['recommendedFilms']:
                if recommendedFilm['id'] == filmId:
                    return False
                
        return True


    def reviewRecommendation(self):
        filmId = request.args.get('filmId')
        isThumbsUp = request.args.get('isThumbsUp').lower() == 'true'

        _vectorizeUtilities = VectorizeUtilities()

        for row in self.rowsOfRecommendations:
            for film in row['recommendedFilms']:
                if film['id'] == filmId:
                    profileId = row['profileId']

        profile = self.getProfile(profileId)

        # if the profile is a genre profile
        if profileId in self.cache['allGenres']:
            adjustment = profile['weightedMeanRating'] * self.RECOMMENDATION_REVIEW_FACTOR
            if isThumbsUp:
                profile['weightedMeanRating'] += adjustment
            else:
                profile['weightedMeanRating'] -= adjustment

        filmVector = self.allFilmDataVectorized[filmId]
        adjustment = (filmVector - profile['profile']) * self.RECOMMENDATION_REVIEW_FACTOR

        for i in range(len(adjustment)):
            if adjustment[i] == 0.0:
                adjustment[i] = self.RECOMMENDATION_REVIEW_FACTOR

        if isThumbsUp:
            profile['profile'] += adjustment
        else:
            profile['profile'] -= adjustment

        _vectorizeUtilities.keepVectorBoundary(profile['profile'])

        return f"changed {profileId} profile due to after reviewing {filmId}", 200


    def deleteUserUploadedData(self):
        for fileOrDirectory in os.listdir(self.USER_UPLOADED_DATA_DIRECTORY_NAME):
            fileOrDirectoryPath = os.path.join(self.USER_UPLOADED_DATA_DIRECTORY_NAME, fileOrDirectory)
            if os.path.isdir(fileOrDirectoryPath):
                shutil.rmtree(fileOrDirectoryPath)
            elif os.path.basename(fileOrDirectoryPath) != ".gitignore":
                os.remove(fileOrDirectoryPath)


    def isUnacceptableMediaType(self, filename):
        return not (filename.lower().endswith(".csv") or filename.lower().endswith(".zip"))
    
    def getProfile(self, profileId):
        if profileId == "favourite":
            return self.favouriteProfile
        elif profileId == "recency":
            return self.recencyProfile
        elif profileId == "old":
            return self.oldProfile
        elif profileId == "international":
            return self.internationalProfile
        else:
            for profile in self.genreProfiles:
                if profile['profileId'] == profileId:
                    return profile

        print(f"Error: profile {profileId} not found. Returning zero vector.")
        return {'profile': np.zeros(self.profileVectorLength), 'profileId': profileId}

    def regenerateRecommendations(self):
        for row in self.rowsOfRecommendations:
            for film in row['recommendedFilms']:
                filmId = film['id']
                del self.allFilmDataUnseen[filmId]

        self.generateRecommendations()

        return jsonify(self.rowsOfRecommendations), 200
    
    def loadJsonFiles(self):
        try:
            allFilmDataVectorizedFile = open('../database/all-film-data-vectorized.json')
            self.allFilmDataVectorized = json.load(allFilmDataVectorizedFile)
            allFilmDataVectorizedMagnitudesFile = open('../database/all-film-data-vectorized-magnitudes.json')
            self.allFilmDataVectorizedMagnitudes = json.load(allFilmDataVectorizedMagnitudesFile)
            cachedLetterboxdTitlesFile = open('../database/cached-letterboxd-titles.json')
            self.cachedLetterboxdTitles = json.load(cachedLetterboxdTitlesFile)
            cacheFile = open('../database/cache.json')
            self.cache = json.load(cacheFile)
            self.cachedNormalizedYearsKeys = list(self.cache['normalizedYears'].keys())
            self.cachedNormalizedImdbRatingsKeys = list(self.cache['normalizedImdbRatings'].keys())
            self.cachedNormalizedRuntimesKeys = list(self.cache['normalizedRuntimes'].keys())

            return self.JSON_FILES_LOAD_SUCCESS_MESSAGE, 200
        except FileNotFoundError:
            return self.JSON_FILES_NOT_FOUND_ERROR_MESSAGE, 404
        except json.JSONDecodeError:
            return self.JSON_FILES_DECODE_ERROR_MESSAGE, 400

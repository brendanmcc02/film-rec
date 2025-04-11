import csv
from datetime import datetime
from flask import request, jsonify
import numpy as np
from VectorProfile import *

class Service:

    def __init__(self, _database, _serviceUtilities, _vectorizeUtilities, _letterboxdConversionUtilities,
                 _initDatabase):
        self.database = _database
        self.serviceUtilities = _serviceUtilities
        self.vectorizeUtilities = _vectorizeUtilities
        self.letterboxdConversionUtilities = _letterboxdConversionUtilities
        self.initDatabase = _initDatabase
        self.allFilmDataUnseen = {}
        self.allFilmDataVectorized = _database.read("allFilmDataVectorized")
        self.allFilmDataVectorizedMagnitudes = _database.read("allFilmDataVectorizedMagnitudes")
        self.cachedLetterboxdTitles = _database.read("cachedLetterboxdTitles")
        self.allGenres = _database.read("allGenres")
        self.allGenresLength = len(self.allGenres)
        self.allCountries = _database.read("allCountries")
        self.allCountriesLength = len(self.allCountries)
        self.profileVectorLength = _database.read("profileVectorLength")
        self.minNumberOfVotes = _database.read("minNumberOfVotes")
        self.diffNumberOfVotes = _database.read("diffNumberOfVotes")
        self.normalizedYears = _database.read("normalizedYears")
        self.normalizedYearsKeys = list(self.normalizedYears.keys())
        self.normalizedImdbRatings = _database.read("normalizedImdbRatings")
        self.normalizedImdbRatingsKeys = list(self.normalizedImdbRatings.keys())
        self.normalizedRuntimes = _database.read("normalizedRuntimes")
        self.normalizedRuntimesKeys = list(self.normalizedRuntimes.keys())
        self.diffDateRated = datetime(1, 1, 1)
        self.minDateRated = datetime.now()
        self.favouriteProfile = VectorProfile('favourite', self.profileVectorLength)
        self.genreProfiles = []
        self.recencyProfile = VectorProfile('recency', self.profileVectorLength)
        self.internationalProfile = VectorProfile('international', self.profileVectorLength)
        self.oldProfile = VectorProfile('old', self.profileVectorLength)
        self.rowsOfRecommendations = []
        self.isImdbFile = True
        self.userFilmDataFilename = ""
        self.userFilmDataOriginal = []


    def verifyAndLoadUserUploadedFile(self):
        self.isImdbFile = True

        self.serviceUtilities.deleteUserUploadedData()

        if 'file' not in request.files:
            return self.serviceUtilities.NO_FILE_IN_REQUEST_ERROR_MESSAGE, 400

        file = request.files['file']
        self.userFilmDataFilename = file.filename

        if self.serviceUtilities.isUnacceptableMediaType(self.userFilmDataFilename):
            return self.serviceUtilities.UNSUPPORTED_MEDIA_TYPE_ERROR_MESSAGE, 415

        try:
            self.userFilmDataOriginal = []
            userUploadedFileLocation = self.serviceUtilities.USER_UPLOADED_DATA_DIRECTORY_NAME + self.userFilmDataFilename
            file.save(userUploadedFileLocation)

            if userUploadedFileLocation.endswith(".zip"):
                if self.letterboxdConversionUtilities.isLetterboxdZipFileInvalid(self.serviceUtilities.USER_UPLOADED_DATA_DIRECTORY_NAME, self.userFilmDataFilename):
                    return self.serviceUtilities.INVALID_ZIP_FILE_ERROR_MESSAGE, 400
                else:
                    self.userFilmDataFilename = "ratings.csv"
                    userUploadedFileLocation = self.serviceUtilities.USER_UPLOADED_DATA_DIRECTORY_NAME + self.userFilmDataFilename

            with open(userUploadedFileLocation, encoding='utf-8') as userFilmDataFile:
                reader = csv.DictReader(userFilmDataFile, delimiter=',', restkey='unexpectedData')

                for row in reader:
                    if 'unexpectedData' in row:
                        return self.serviceUtilities.FILE_MORE_DATA_THAN_ROW_HEADERS_ERROR_MESSAGE, 400

                    keys = list(row.keys())
                    for key in keys:
                        if key not in self.serviceUtilities.EXPECTED_IMDB_FILM_ATTRIBUTES:
                            self.isImdbFile = False
                            if key not in self.letterboxdConversionUtilities.EXPECTED_LETTERBOXD_FILE_FILM_ATTRIBUTES:
                                return self.serviceUtilities.FILE_ROW_HEADERS_UNEXPECTED_FORMAT_ERROR_MESSAGE, 400

                    self.userFilmDataOriginal.append(row)

            self.serviceUtilities.deleteUserUploadedData()
            return self.serviceUtilities.FILE_UPLOAD_SUCCESS_MESSAGE, 200
        except Exception as e:
            self.serviceUtilities.deleteUserUploadedData()
            return f"Error occurred with reading {self.userFilmDataFilename}.\n{e}", 400

    def getInitialRowsOfRecommendations(self):
        allFilmData = self.database.read("allFilmData")

        if not self.isImdbFile:
            self.userFilmDataOriginal = (self.letterboxdConversionUtilities.convertLetterboxdFormatToImdbFormat(self.userFilmDataOriginal,
                                                                                                                allFilmData, self.cachedLetterboxdTitles))

        userFilmData = {}
        favouriteFilmIds = []
        self.minDateRated = datetime.now()
        maxDateRated = self.minDateRated

        for film in self.userFilmDataOriginal:
            if (film['Title Type'] == "Movie" and 
                    int(film['Runtime (mins)']) >= self.initDatabase.RUNTIME_THRESHOLD and film['Genres'] != ""\
                    and int(film['Num Votes']) >= self.initDatabase.NUMBER_OF_VOTES_THRESHOLD):
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
                    self.serviceUtilities.deleteUserUploadedData()
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

        # vectorize user-film-data
        for imdbFilmId in userFilmData:
            vector = self.vectorizeUtilities.vectorizeFilm(userFilmData[imdbFilmId], self.allGenres, self.allCountries,
                                                           self.normalizedYears, self.normalizedImdbRatings, self.minNumberOfVotes,
                                                           self.diffNumberOfVotes, self.normalizedRuntimes)
            if isDiffDateRatedZero:
                dateRatedWeight = 1.0
            else:
                # normalize the dateRatedWeight as a float between DATE_RATED_WEIGHT and 1.0.
                dateRatedWeight = (((userFilmData[imdbFilmId]['dateRated'] - self.minDateRated) / self.diffDateRated) *
                                    (1 - self.serviceUtilities.DATE_RATED_WEIGHT)) + self.serviceUtilities.DATE_RATED_WEIGHT

            # imdbRatings run from 1-10, we want values to run from 0.1 - 1.0
            userRatingWeight = round((userFilmData[imdbFilmId]['userRating'] / 10.0), 1)
            cachedDateRatedAndUserRatingWeights[imdbFilmId] = dateRatedWeight * userRatingWeight

            userFilmDataVectorized[imdbFilmId] = vector * cachedDateRatedAndUserRatingWeights[imdbFilmId]

        self.favouriteProfile = self.vectorizeUtilities.initFavouriteProfile(userFilmData, userFilmDataVectorized, 
                                                                         self.profileVectorLength,
                                                                         cachedDateRatedAndUserRatingWeights, favouriteFilmIds,
                                                                         self.allGenres, self.allCountries)

        self.recencyProfile = self.vectorizeUtilities.initRecencyProfile(userFilmData, userFilmDataVectorized, maxDateRated, 
                                                                         self.profileVectorLength, cachedDateRatedAndUserRatingWeights, 
                                                                         self.allGenres, self.allCountries)

        self.genreProfiles = self.vectorizeUtilities.initGenreProfiles(userFilmData, userFilmDataVectorized, cachedDateRatedAndUserRatingWeights,
                                                                       self.allGenres, self.profileVectorLength, 
                                                                       self.serviceUtilities.NUMBER_OF_FILMS_WATCHED_IN_GENRE_THRESHOLD, 
                                                                       self.allCountries)

        userProfile = self.vectorizeUtilities.initUserProfile(userFilmData, userFilmDataVectorized, self.profileVectorLength,
                                                              cachedDateRatedAndUserRatingWeights, self.allGenres, self.allCountries)

        self.internationalProfile = self.vectorizeUtilities.initInternationalProfile(userProfile.profile, self.allCountries, self.allGenresLength,
                                                                                     self.profileVectorLength)

        self.oldProfile = self.vectorizeUtilities.initOldProfile(userProfile.profile)

        self.generateRecommendations()

        return jsonify(self.rowsOfRecommendations), 200

    def generateRecommendations(self):
        
        self.rowsOfRecommendations = []

        if np.array_equal(self.favouriteProfile.profile, np.zeros(self.profileVectorLength)):
            print("No favourite profile.")
        else:
            self.getFilmRecommendations("Based on your favourite films", self.favouriteProfile.profile, self.favouriteProfile.profileId)
            # self.vectorizeUtilities.printStringifiedVector(self.favouriteProfile.profile, self.allGenres, self.allCountries, "Favourite",
            #                        self.normalizedYearsKeys, self.normalizedRuntimesKeys, self.normalizedImdbRatingsKeys,
            #                        self.minNumberOfVotes, self.diffNumberOfVotes)

        if np.array_equal(self.recencyProfile.profile, np.zeros(self.profileVectorLength)):
            print("No recency profile.")
        else:
            self.getFilmRecommendations("Based on what you watched recently", self.recencyProfile.profile, self.recencyProfile.profileId)
            # self.vectorizeUtilities.printStringifiedVector(self.recencyProfile.profile, self.allGenres, self.allCountries, "Recency",
            #                                                self.normalizedYearsKeys, self.normalizedRuntimesKeys, self.normalizedImdbRatingsKeys,
            #                                                self.minNumberOfVotes, self.diffNumberOfVotes)

        self.genreProfiles = sorted(self.genreProfiles, key=lambda x: x.weightedMeanRating, reverse=True)

        for i in range(self.serviceUtilities.NUMBER_OF_GENRE_RECOMMENDATION_ROWS):
            if self.genreProfiles[i].weightedMeanRating == 0.0:
                print("No genre profile.")
            else:
                countryText = self.vectorizeUtilities.getProfileMaxCountry(self.genreProfiles[i].profile, self.allGenresLength, self.allCountries)
                self.getFilmRecommendations(f"Because you like {countryText} {self.genreProfiles[i].profileId} films", self.genreProfiles[i].profile, 
                                            self.genreProfiles[i].profileId)
                # self.vectorizeUtilities.printStringifiedVector(self.genreProfiles[i].profile, self.allGenres, self.allCountries, 
                #                        self.genreProfiles[i].profileId, self.normalizedYearsKeys, 
                #                        self.normalizedRuntimesKeys, self.normalizedImdbRatingsKeys, 
                #                        self.minNumberOfVotes, self.diffNumberOfVotes)
            
        if np.array_equal(self.internationalProfile.profile, np.zeros(self.profileVectorLength)):
            print("No international profile.")
        else:
            self.getFilmRecommendations("Try out some international films", self.internationalProfile.profile, self.internationalProfile.profileId)
            # self.vectorizeUtilities.printStringifiedVector(self.internationalProfile.profile, self.allGenres, self.allCountries, 
            #                        "International", self.normalizedYearsKeys, self.normalizedRuntimesKeys,
            #                        self.normalizedImdbRatingsKeys, self.minNumberOfVotes, self.diffNumberOfVotes)

        if np.array_equal(self.oldProfile.profile, np.zeros(self.profileVectorLength)):
            print("No old profile.")
        else:
            self.getFilmRecommendations("Try out some older films", self.oldProfile.profile, self.oldProfile.profileId)
            # self.vectorizeUtilities.printStringifiedVector(self.oldProfile.profile, self.allGenres, self.allCountries, "Old",
            #                        self.normalizedYearsKeys, self.normalizedRuntimesKeys,
            #                        self.normalizedImdbRatingsKeys, self.minNumberOfVotes, self.diffNumberOfVotes)


    def getFilmRecommendations(self, recommendedRowText, profileVector, profileId):
        self.rowsOfRecommendations.append({"recommendedRowText": recommendedRowText, "recommendedFilms": [], 
                                           "profileId": profileId})
        profileVectorMagnitude = np.linalg.norm(profileVector)
        cosineSimilarities = {}

        for filmId in self.allFilmDataUnseen:
            filmVectorMagnitude = self.allFilmDataVectorizedMagnitudes[filmId]
            cosineSimilarities[filmId] = self.vectorizeUtilities.cosineSimilarity(self.allFilmDataVectorized[filmId], profileVector,
                                                                                  filmVectorMagnitude, profileVectorMagnitude)

        cosineSimilarities = sorted(cosineSimilarities.items(), key=lambda x: x[1], reverse=True)

        numberOfRecommendations = self.serviceUtilities.NUMBER_OF_RECOMMENDATIONS_PER_ROW
        i = 0
        while i < numberOfRecommendations:
            filmId = cosineSimilarities[i][0]
            
            if self.serviceUtilities.isFilmRecommendationUnique(filmId, self.rowsOfRecommendations):
                film = self.allFilmDataUnseen[filmId]
                similarityScore = cosineSimilarities[i][1]
                film['id'] = filmId
                film['similarityScore'] = int(similarityScore * 100.0)

                self.rowsOfRecommendations[-1]['recommendedFilms'].append(film)
            else:
                numberOfRecommendations += 1

            i += 1


    def reviewRecommendation(self):
        filmId = request.args.get('filmId')
        isThumbsUp = request.args.get('isThumbsUp').lower() == 'true'

        for row in self.rowsOfRecommendations:
            for film in row['recommendedFilms']:
                if film['id'] == filmId:
                    profileId = row.profileId

        profile = self.getProfile(profileId)

        # if the profile is a genre profile
        if profileId in self.allGenres:
            adjustment = profile.weightedMeanRating * self.serviceUtilities.RECOMMENDATION_REVIEW_FACTOR
            if isThumbsUp:
                profile.weightedMeanRating += adjustment
            else:
                profile.weightedMeanRating -= adjustment

        filmVector = self.allFilmDataVectorized[filmId]
        adjustment = (filmVector - profile.profile) * self.serviceUtilities.RECOMMENDATION_REVIEW_FACTOR

        for i in range(len(adjustment)):
            if adjustment[i] == 0.0:
                adjustment[i] = self.serviceUtilities.RECOMMENDATION_REVIEW_FACTOR

        if isThumbsUp:
            profile.profile += adjustment
        else:
            profile.profile -= adjustment

        self.vectorizeUtilities.keepVectorBoundary(profile.profile)

        return f"changed {profileId} profile due to after reviewing {filmId}", 200
    

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
                if profile.profileId == profileId:
                    return profile

        print(f"Error: profile {profileId} not found. Returning zero vector.")
        return VectorProfile(profileId, self.profileVectorLength)


    def regenerateRecommendations(self):
        for row in self.rowsOfRecommendations:
            for film in row['recommendedFilms']:
                filmId = film['id']
                del self.allFilmDataUnseen[filmId]

        self.generateRecommendations()

        return jsonify(self.rowsOfRecommendations), 200

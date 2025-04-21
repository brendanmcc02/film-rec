import csv
from datetime import datetime
from flask import request
import numpy as np
from VectorProfile import *

class ServiceInstance:

    def __init__(self, cachedDatabase, serviceUtilities, vectorizeUtilities, letterboxdConversionUtilities,
                 initDatabase, guid):
        self.cachedDatabase = cachedDatabase
        self.serviceUtilities = serviceUtilities
        self.vectorizeUtilities = vectorizeUtilities
        self.letterboxdConversionUtilities = letterboxdConversionUtilities
        self.initDatabase = initDatabase
        self.allFilmDataUnseen = {}
        self.vectorProfiles = self.vectorizeUtilities.initVectorProfiles(self.cachedDatabase["ProfileVectorLength"])
        self.rowsOfRecommendations = []
        self.guid = guid

    def getInitialRowsOfRecommendations(self):
        isImdbFile = True

        self.serviceUtilities.deleteUserUploadedData()

        if 'file' not in request.files:
            return self.serviceUtilities.getFormattedResponse({}, self.serviceUtilities.NO_FILE_IN_REQUEST_ERROR_MESSAGE, self.guid, 400)

        file = request.files['file']
        userFilmDataFilename = file.filename

        if self.serviceUtilities.isUnacceptableMediaType(userFilmDataFilename):
            return self.serviceUtilities.getFormattedResponse({}, self.serviceUtilities.UNSUPPORTED_MEDIA_TYPE_ERROR_MESSAGE, self.guid, 415)

        try:
            userFilmDataOriginal = []
            userUploadedFileLocation = self.serviceUtilities.USER_UPLOADED_DATA_DIRECTORY_NAME + userFilmDataFilename
            file.save(userUploadedFileLocation)

            if userUploadedFileLocation.endswith(".zip"):
                if self.letterboxdConversionUtilities.isLetterboxdZipFileInvalid(self.serviceUtilities.USER_UPLOADED_DATA_DIRECTORY_NAME, userFilmDataFilename):
                    return self.serviceUtilities.getFormattedResponse({}, self.serviceUtilities.INVALID_ZIP_FILE_ERROR_MESSAGE, self.guid, 400)
                else:
                    userFilmDataFilename = "ratings.csv"
                    userUploadedFileLocation = self.serviceUtilities.USER_UPLOADED_DATA_DIRECTORY_NAME + userFilmDataFilename

            with open(userUploadedFileLocation, encoding='utf-8') as userFilmDataFile:
                reader = csv.DictReader(userFilmDataFile, delimiter=',', restkey='unexpectedData')

                for row in reader:
                    if 'unexpectedData' in row:
                        return self.serviceUtilities.getFormattedResponse({}, self.serviceUtilities.FILE_MORE_DATA_THAN_ROW_HEADERS_ERROR_MESSAGE, self.guid, 400)

                    keys = list(row.keys())
                    for key in keys:
                        if key not in self.serviceUtilities.EXPECTED_IMDB_FILM_ATTRIBUTES:
                            isImdbFile = False
                            if key not in self.letterboxdConversionUtilities.EXPECTED_LETTERBOXD_FILE_FILM_ATTRIBUTES:
                                return self.serviceUtilities.getFormattedResponse({}, self.serviceUtilities.FILE_ROW_HEADERS_UNEXPECTED_FORMAT_ERROR_MESSAGE, self.guid, 400)

                    userFilmDataOriginal.append(row)
        except Exception as e:
            return self.serviceUtilities.getFormattedResponse({}, f"Error occurred with reading {userFilmDataFilename}.\n{e}", self.guid, 400)
        finally:
            self.serviceUtilities.deleteUserUploadedData()
        
        # store in a local variable because dictionaries in python are pass by reference
        allFilmData = self.cachedDatabase["AllFilmData"]

        if not isImdbFile:
            userFilmDataOriginal = (self.letterboxdConversionUtilities.convertLetterboxdFormatToImdbFormat(userFilmDataOriginal,
                                                                                                           allFilmData, self.cachedDatabase["CachedLetterboxdTitles"]))

        userFilmData = {}
        favouriteFilmIds = []
        minDateRated = datetime.now()
        maxDateRated = minDateRated

        for film in userFilmDataOriginal:
            if (film['Title Type'] == "Movie" and 
                    int(film['Runtime (mins)']) >= self.initDatabase.RUNTIME_THRESHOLD and film['Genres'] != ""\
                    and int(film['Num Votes']) >= self.initDatabase.NUMBER_OF_VOTES_THRESHOLD):
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
                    self.serviceUtilities.deleteUserUploadedData()
                    return self.serviceUtilities.getFormattedResponse({}, f"value error with film: {film['Const']}", self.guid, 400)

        diffDateRated = maxDateRated - minDateRated
        isDiffDateRatedZero = False
        if diffDateRated == 0.0:
            isDiffDateRatedZero = True

        for imdbFilmId in allFilmData:
            if imdbFilmId not in userFilmData:
                self.allFilmDataUnseen[imdbFilmId] = allFilmData[imdbFilmId]

        userFilmDataVectorized = {}

        # init a dict with pre-computed scalar values
        cachedDateRatedAndUserRatingWeights = {}        

        # vectorize user-film-data
        for imdbFilmId in userFilmData:
            vector = self.vectorizeUtilities.vectorizeFilm(userFilmData[imdbFilmId], self.cachedDatabase["AllGenres"], self.cachedDatabase["AllCountries"],
                                                           self.cachedDatabase["NormalizedYears"], self.cachedDatabase["NormalizedImdbRatings"], self.cachedDatabase["MinNumberOfVotes"],
                                                           self.cachedDatabase["DiffNumberOfVotes"], self.cachedDatabase["NormalizedRuntimes"])
            if isDiffDateRatedZero:
                dateRatedWeight = 1.0
            else:
                # normalize the dateRatedWeight as a float between DATE_RATED_WEIGHT and 1.0.
                dateRatedWeight = (((userFilmData[imdbFilmId]['dateRated'] - minDateRated) / diffDateRated) *
                                    (1 - self.serviceUtilities.DATE_RATED_WEIGHT)) + self.serviceUtilities.DATE_RATED_WEIGHT

            # imdbRatings run from 1-10, we want values to run from 0.1 - 1.0
            userRatingWeight = round((userFilmData[imdbFilmId]['userRating'] / 10.0), 1)
            cachedDateRatedAndUserRatingWeights[imdbFilmId] = dateRatedWeight * userRatingWeight

            userFilmDataVectorized[imdbFilmId] = vector * cachedDateRatedAndUserRatingWeights[imdbFilmId]

        self.vectorProfiles["favouriteProfile"] = self.vectorizeUtilities.initFavouriteProfile(userFilmData, userFilmDataVectorized, 
                                                                             self.cachedDatabase["ProfileVectorLength"],
                                                                             cachedDateRatedAndUserRatingWeights, favouriteFilmIds,
                                                                             self.cachedDatabase["AllGenres"], self.cachedDatabase["AllCountries"])

        self.vectorProfiles["recencyProfile"] = self.vectorizeUtilities.initRecencyProfile(userFilmData, userFilmDataVectorized, maxDateRated, 
                                                                         self.cachedDatabase["ProfileVectorLength"], cachedDateRatedAndUserRatingWeights, 
                                                                         self.cachedDatabase["AllGenres"], self.cachedDatabase["AllCountries"])

        self.vectorProfiles["genreProfiles"] = self.vectorizeUtilities.initGenreProfiles(userFilmData, userFilmDataVectorized, cachedDateRatedAndUserRatingWeights,
                                                                       self.cachedDatabase["AllGenres"], self.cachedDatabase["ProfileVectorLength"], 
                                                                       self.serviceUtilities.NUMBER_OF_FILMS_WATCHED_IN_GENRE_THRESHOLD, 
                                                                       self.cachedDatabase["AllCountries"])

        userProfile = self.vectorizeUtilities.initUserProfile(userFilmData, userFilmDataVectorized, self.cachedDatabase["ProfileVectorLength"],
                                                              cachedDateRatedAndUserRatingWeights, self.cachedDatabase["AllGenres"], self.cachedDatabase["AllCountries"])

        self.vectorProfiles["internationalProfile"] = self.vectorizeUtilities.initInternationalProfile(userProfile.profile, self.cachedDatabase["AllCountries"], self.cachedDatabase["AllGenresLength"],
                                                                                     self.cachedDatabase["ProfileVectorLength"])

        self.vectorProfiles["oldProfile"] = self.vectorizeUtilities.initOldProfile(userProfile.profile)

        self.generateRecommendations()

        return self.serviceUtilities.getFormattedResponse(self.rowsOfRecommendations, "", self.guid, 200)

    def generateRecommendations(self):
        
        self.rowsOfRecommendations = []

        if np.array_equal(self.vectorProfiles["favouriteProfile"].profile, np.zeros(self.cachedDatabase["ProfileVectorLength"])):
            print("No favourite profile.")
        else:
            self.getFilmRecommendations("Based on your favourite films", self.vectorProfiles["favouriteProfile"].profile, self.vectorProfiles["favouriteProfile"].profileId)
            # self.vectorizeUtilities.printStringifiedVector(self.vectorProfiles["favouriteProfile"].profile, self.cachedDatabase["AllGenres"], self.cachedDatabase["AllCountries"], "Favourite",
            #                        self.cachedDatabase["NormalizedYearsKeys"], self.cachedDatabase["NormalizedRuntimesKeys"], self.cachedDatabase["NormalizedImdbRatingsKeys"],
            #                        self.cachedDatabase["MinNumberOfVotes"], self.cachedDatabase["DiffNumberOfVotes"])

        if np.array_equal(self.vectorProfiles["recencyProfile"].profile, np.zeros(self.cachedDatabase["ProfileVectorLength"])):
            print("No recency profile.")
        else:
            self.getFilmRecommendations("Based on what you watched recently", self.vectorProfiles["recencyProfile"].profile, self.vectorProfiles["recencyProfile"].profileId)
            # self.vectorizeUtilities.printStringifiedVector(self.vectorProfiles["recencyProfile"].profile, self.cachedDatabase["AllGenres"], self.cachedDatabase["AllCountries"], "Recency",
            #                                                self.cachedDatabase["NormalizedYearsKeys"], self.cachedDatabase["NormalizedRuntimesKeys"], self.cachedDatabase["NormalizedImdbRatingsKeys"],
            #                                                self.cachedDatabase["MinNumberOfVotes"], self.cachedDatabase["DiffNumberOfVotes"])

        self.vectorProfiles["genreProfiles"] = sorted(self.vectorProfiles["genreProfiles"], key=lambda x: x.weightedMeanRating, reverse=True)

        for i in range(self.serviceUtilities.NUMBER_OF_GENRE_RECOMMENDATION_ROWS):
            if self.vectorProfiles["genreProfiles"][i].weightedMeanRating == 0.0:
                print("No genre profile.")
            else:
                countryText = self.vectorizeUtilities.getProfileMaxCountry(self.vectorProfiles["genreProfiles"][i].profile, self.cachedDatabase["AllGenresLength"], self.cachedDatabase["AllCountries"])
                self.getFilmRecommendations(f"Because you like {countryText} {self.vectorProfiles["genreProfiles"][i].profileId} films", self.vectorProfiles["genreProfiles"][i].profile, 
                                            self.vectorProfiles["genreProfiles"][i].profileId)
                # self.vectorizeUtilities.printStringifiedVector(self.vectorProfiles["genreProfiles"][i].profile, self.cachedDatabase["AllGenres"], self.cachedDatabase["AllCountries"], 
                #                        self.vectorProfiles["genreProfiles"][i].profileId, self.cachedDatabase["NormalizedYearsKeys"], 
                #                        self.cachedDatabase["NormalizedRuntimesKeys"], self.cachedDatabase["NormalizedImdbRatingsKeys"], 
                #                        self.cachedDatabase["MinNumberOfVotes"], self.cachedDatabase["DiffNumberOfVotes"])
            
        if np.array_equal(self.vectorProfiles["internationalProfile"].profile, np.zeros(self.cachedDatabase["ProfileVectorLength"])):
            print("No international profile.")
        else:
            self.getFilmRecommendations("Try out some international films", self.vectorProfiles["internationalProfile"].profile, self.vectorProfiles["internationalProfile"].profileId)
            # self.vectorizeUtilities.printStringifiedVector(self.vectorProfiles["internationalProfile"].profile, self.cachedDatabase["AllGenres"], self.cachedDatabase["AllCountries"], 
            #                        "International", self.cachedDatabase["NormalizedYearsKeys"], self.cachedDatabase["NormalizedRuntimesKeys"],
            #                        self.cachedDatabase["NormalizedImdbRatingsKeys"], self.cachedDatabase["MinNumberOfVotes"], self.cachedDatabase["DiffNumberOfVotes"])

        if np.array_equal(self.vectorProfiles["oldProfile"].profile, np.zeros(self.cachedDatabase["ProfileVectorLength"])):
            print("No old profile.")
        else:
            self.getFilmRecommendations("Try out some older films", self.vectorProfiles["oldProfile"].profile, self.vectorProfiles["oldProfile"].profileId)
            # self.vectorizeUtilities.printStringifiedVector(self.vectorProfiles["oldProfile"].profile, self.cachedDatabase["AllGenres"], self.cachedDatabase["AllCountries"], "Old",
            #                        self.cachedDatabase["NormalizedYearsKeys"], self.cachedDatabase["NormalizedRuntimesKeys"],
            #                        self.cachedDatabase["NormalizedImdbRatingsKeys"], self.cachedDatabase["MinNumberOfVotes"], self.cachedDatabase["DiffNumberOfVotes"])


    def getFilmRecommendations(self, recommendedRowText, profileVector, profileId):
        self.rowsOfRecommendations.append({"recommendedRowText": recommendedRowText, "recommendedFilms": [], 
                                           "profileId": profileId})
        profileVectorMagnitude = np.linalg.norm(profileVector)
        cosineSimilarities = {}

        for filmId in self.allFilmDataUnseen:
            filmVectorMagnitude = self.cachedDatabase["AllFilmDataVectorizedMagnitudes"][filmId]
            cosineSimilarities[filmId] = self.vectorizeUtilities.cosineSimilarity(self.cachedDatabase["AllFilmDataVectorized"][filmId], profileVector,
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
        if profileId in self.cachedDatabase["AllGenres"]:
            adjustment = profile.weightedMeanRating * self.serviceUtilities.RECOMMENDATION_REVIEW_FACTOR
            if isThumbsUp:
                profile.weightedMeanRating += adjustment
            else:
                profile.weightedMeanRating -= adjustment

        filmVector = self.cachedDatabase["AllFilmDataVectorized"][filmId]
        adjustment = (filmVector - profile.profile) * self.serviceUtilities.RECOMMENDATION_REVIEW_FACTOR

        for i in range(len(adjustment)):
            if adjustment[i] == 0.0:
                adjustment[i] = self.serviceUtilities.RECOMMENDATION_REVIEW_FACTOR

        if isThumbsUp:
            profile.profile += adjustment
        else:
            profile.profile -= adjustment

        self.vectorizeUtilities.keepVectorBoundary(profile.profile)

        return self.serviceUtilities.getFormattedResponse(f"changed {profileId} profile due to after reviewing {filmId}", "", self.guid, 200)
    

    def getProfile(self, profileId):
        if profileId == "favourite":
            return self.vectorProfiles["favouriteProfile"]
        elif profileId == "recency":
            return self.vectorProfiles["recencyProfile"]
        elif profileId == "old":
            return self.vectorProfiles["oldProfile"]
        elif profileId == "international":
            return self.vectorProfiles["internationalProfile"]
        else:
            for profile in self.vectorProfiles["genreProfiles"]:
                if profile.profileId == profileId:
                    return profile

        print(f"Error: profile {profileId} not found. Returning zero vector.")

        return VectorProfile(profileId, self.cachedDatabase["ProfileVectorLength"])


    def regenerateRecommendations(self):
        for row in self.rowsOfRecommendations:
            for film in row['recommendedFilms']:
                filmId = film['id']
                del self.allFilmDataUnseen[filmId]

        self.generateRecommendations()

        return self.serviceUtilities.getFormattedResponse(self.rowsOfRecommendations, "", self.guid, 200)

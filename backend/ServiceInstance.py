from datetime import datetime
from flask import request
import numpy as np
from VectorProfile import *

class ServiceInstance:

    def __init__(self, cachedDatabase, serviceUtilities, vectorizeUtilities, letterboxdConversionUtilities,
                 initDatabase, fileUtilities, guid):
        self.cachedDatabase = cachedDatabase
        self.serviceUtilities = serviceUtilities
        self.vectorizeUtilities = vectorizeUtilities
        self.letterboxdConversionUtilities = letterboxdConversionUtilities
        self.initDatabase = initDatabase
        self.fileUtilities = fileUtilities
        self.allFilmDataUnseen = {}
        self.vectorProfiles = self.vectorizeUtilities.initVectorProfiles(self.cachedDatabase["ProfileVectorLength"])
        self.rowsOfRecommendations = []
        self.guid = guid

    def getInitialRowsOfRecommendations(self):
        fileWriteResponse = self.fileUtilities.getUserFilmDataOriginalFromFile(request.files, self.guid)

        if fileWriteResponse[1] != 200:
            return fileWriteResponse

        fileWriteResponseContent = fileWriteResponse[0].get_json()
        userFilmDataOriginal = fileWriteResponseContent["body"]["userFilmDataOriginal"]
        isImdbFile = fileWriteResponseContent["body"]["isImdbFile"]
        
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
            if (self.serviceUtilities.isFilmValid(film, self.initDatabase.RUNTIME_THRESHOLD, self.initDatabase.NUMBER_OF_VOTES_THRESHOLD)):
                genres = self.serviceUtilities.getFilmGenresCorrectFormat(film['Genres'], isImdbFile)
                
                try:
                    filmId = film['Const']
                    if filmId in allFilmData:
                        dateRated = datetime.strptime(film['Date Rated'], "%Y-%m-%d")
                        minDateRated = min(minDateRated, dateRated)

                        userFilmData[film['Const']] = self.serviceUtilities.getFormattedFilm(film, dateRated, genres, allFilmData[filmId]['countries'])

                        if userFilmData[filmId]['userRating'] >= self.serviceUtilities.FAVOURITE_FILM_RATING_THRESHOLD:
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

        self.allFilmDataUnseen = self.serviceUtilities.getAllFilmDataUnseen(allFilmData, userFilmData)

        userFilmDataVectorized = {}

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

        self.vectorProfiles["recentProfile"] = self.vectorizeUtilities.initRecentProfile(userFilmData, userFilmDataVectorized, maxDateRated, 
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

        if self.vectorizeUtilities.isZeroVector(self.vectorProfiles["favouriteProfile"].profile, self.cachedDatabase["ProfileVectorLength"]):
            print("No favourite profile.")
        else:
            self.getFilmRecommendations("Based on your favourite films", self.vectorProfiles["favouriteProfile"].profile, self.vectorProfiles["favouriteProfile"].profileId)

        if self.vectorizeUtilities.isZeroVector(self.vectorProfiles["recentProfile"].profile, self.cachedDatabase["ProfileVectorLength"]):
            print("No recent profile.")
        else:
            self.getFilmRecommendations("Based on what you watched recently", self.vectorProfiles["recentProfile"].profile, self.vectorProfiles["recentProfile"].profileId)

        self.vectorProfiles["genreProfiles"] = sorted(self.vectorProfiles["genreProfiles"], key=lambda x: x.weightedMeanRating, reverse=True)

        for i in range(self.serviceUtilities.NUMBER_OF_GENRE_RECOMMENDATION_ROWS):
            if self.vectorProfiles["genreProfiles"][i].weightedMeanRating == 0.0:
                print("No genre profile.")
            else:
                countryText = self.vectorizeUtilities.getProfileMaxCountry(self.vectorProfiles["genreProfiles"][i].profile, self.cachedDatabase["AllGenresLength"], self.cachedDatabase["AllCountries"])
                self.getFilmRecommendations(f"Because you like {countryText} {self.vectorProfiles["genreProfiles"][i].profileId} films", self.vectorProfiles["genreProfiles"][i].profile, 
                                            self.vectorProfiles["genreProfiles"][i].profileId)
            
        if self.vectorizeUtilities.isZeroVector(self.vectorProfiles["internationalProfile"].profile, self.cachedDatabase["ProfileVectorLength"]):
            print("No international profile.")
        else:
            self.getFilmRecommendations("Try out some international films", self.vectorProfiles["internationalProfile"].profile, self.vectorProfiles["internationalProfile"].profileId)

        if self.vectorizeUtilities.isZeroVector(self.vectorProfiles["oldProfile"].profile, self.cachedDatabase["ProfileVectorLength"]):
            print("No old profile.")
        else:
            self.getFilmRecommendations("Try out some older films", self.vectorProfiles["oldProfile"].profile, self.vectorProfiles["oldProfile"].profileId)


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
                film['imdbId'] = filmId
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
                if film['imdbId'] == filmId:
                    profileId = row["profileId"]

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

        return self.serviceUtilities.getFormattedResponse(f"Gave Thumbs {"Up" if isThumbsUp else "Down"} for film {filmId}.", "", self.guid, 200)
    

    def getProfile(self, profileId):
        if profileId == "favourite":
            return self.vectorProfiles["favouriteProfile"]
        elif profileId == "recent":
            return self.vectorProfiles["recentProfile"]
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
                filmId = film['imdbId']
                del self.allFilmDataUnseen[filmId]

        self.generateRecommendations()

        return self.serviceUtilities.getFormattedResponse(self.rowsOfRecommendations, "", self.guid, 200)

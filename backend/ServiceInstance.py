from datetime import datetime
from flask import request
from VectorProfile import *
from LetterboxdConversionUtilities import *
from ServiceUtilities import *
from VectorizeUtilities import *

class ServiceInstance:

    def __init__(self, cachedDatabase, guid):
        self.cachedDatabase = cachedDatabase
        self.allFilmDataUnseen = {}
        self.vectorProfiles = initVectorProfiles(self.cachedDatabase["ProfileVectorLength"])
        self.rowsOfRecommendations = []
        self.guid = guid

    def getInitialRowsOfRecommendations(self):
        getUserFilmDataOriginalFromFileResponse = getUserFilmDataOriginalFromFile(request.files, self.guid)

        if getUserFilmDataOriginalFromFileResponse[1] != 200:
            return getUserFilmDataOriginalFromFileResponse

        getUserFilmDataOriginalFromFileResponseContent = getUserFilmDataOriginalFromFileResponse[0].get_json()
        userFilmDataOriginal = getUserFilmDataOriginalFromFileResponseContent["body"]["userFilmDataOriginal"]
        isImdbFile = getUserFilmDataOriginalFromFileResponseContent["body"]["isImdbFile"]

        if not isImdbFile:
            userFilmDataOriginal = (convertLetterboxdFormatToImdbFormat(userFilmDataOriginal,
                                                                        self.cachedDatabase["AllFilmData"], 
                                                                        self.cachedDatabase["CachedLetterboxdTitles"]))

        userFilmData = {}
        favouriteFilmIds = []
        minDateRated = datetime.now()
        maxDateRated = minDateRated

        for film in userFilmDataOriginal:
            if (isFilmValid(film)):
                genres = getFilmGenresCorrectFormat(film['Genres'], isImdbFile)
                
                try:
                    imdbFilmId = film['Const']
                    if imdbFilmId in self.cachedDatabase["AllFilmData"]:
                        dateRated = datetime.strptime(film['Date Rated'], "%Y-%m-%d")
                        minDateRated = min(minDateRated, dateRated)

                        userFilmData[film['Const']] = getFormattedFilm(film, dateRated, genres, self.cachedDatabase["AllFilmData"][imdbFilmId]['countries'])

                        if userFilmData[imdbFilmId]['userRating'] >= FAVOURITE_FILM_RATING_THRESHOLD:
                            favouriteFilmIds.append(imdbFilmId)
                    else:
                        print(f"Film in userFilmData not found in allFilmData, {imdbFilmId}\n")
                except ValueError:
                    deleteUserUploadedData()
                    return getFormattedResponse({}, f"value error with film: {film['Const']}", self.guid, 400)

        diffDateRated = maxDateRated - minDateRated
        isDiffDateRatedZero = False
        if diffDateRated == 0.0:
            isDiffDateRatedZero = True

        self.allFilmDataUnseen = getAllFilmDataUnseen(self.cachedDatabase["AllFilmData"], userFilmData)

        self.initVectorProfiles(userFilmData, isDiffDateRatedZero, minDateRated, maxDateRated, diffDateRated, favouriteFilmIds)

        self.rowsOfRecommendations = self.getRowsOfRecommendations()

        return getFormattedResponse(self.rowsOfRecommendations, "", self.guid, 200)

    def initVectorProfiles(self, userFilmData, isDiffDateRatedZero, minDateRated, maxDateRated, diffDateRated, favouriteFilmIds):
        userFilmDataVectorized = {}
        cachedDateRatedAndUserRatingWeights = {}        

        for imdbFilmId in userFilmData:
            vector = vectorizeFilm(userFilmData[imdbFilmId], self.cachedDatabase["AllGenres"], self.cachedDatabase["AllCountries"],
                                                           self.cachedDatabase["NormalizedYears"], self.cachedDatabase["NormalizedImdbRatings"], self.cachedDatabase["MinNumberOfVotes"],
                                                           self.cachedDatabase["DiffNumberOfVotes"], self.cachedDatabase["NormalizedRuntimes"])
            if isDiffDateRatedZero:
                dateRatedWeight = 1.0
            else:
                dateRatedWeight = getNormalizedDateRatedWeight(userFilmData[imdbFilmId]['dateRated'], minDateRated, diffDateRated)

            # imdbRatings run from 1-10, we want values to run from 0.1 - 1.0
            userRatingWeight = round((userFilmData[imdbFilmId]['userRating'] / 10.0), 1)
            cachedDateRatedAndUserRatingWeights[imdbFilmId] = dateRatedWeight * userRatingWeight
            userFilmDataVectorized[imdbFilmId] = vector * cachedDateRatedAndUserRatingWeights[imdbFilmId]

        self.vectorProfiles["favouriteProfile"] = initFavouriteProfile(userFilmData, userFilmDataVectorized, 
                                                                             self.cachedDatabase["ProfileVectorLength"],
                                                                             cachedDateRatedAndUserRatingWeights, favouriteFilmIds,
                                                                             self.cachedDatabase["AllGenres"], self.cachedDatabase["AllCountries"])

        self.vectorProfiles["recentProfile"] = initRecentProfile(userFilmData, userFilmDataVectorized, maxDateRated, 
                                                                         self.cachedDatabase["ProfileVectorLength"], cachedDateRatedAndUserRatingWeights, 
                                                                         self.cachedDatabase["AllGenres"], self.cachedDatabase["AllCountries"])

        self.vectorProfiles["genreProfiles"] = initGenreProfiles(userFilmData, userFilmDataVectorized, cachedDateRatedAndUserRatingWeights,
                                                                       self.cachedDatabase["AllGenres"], self.cachedDatabase["ProfileVectorLength"], 
                                                                       NUMBER_OF_FILMS_WATCHED_IN_GENRE_THRESHOLD, 
                                                                       self.cachedDatabase["AllCountries"])

        userProfile = initUserProfile(userFilmData, userFilmDataVectorized, self.cachedDatabase["ProfileVectorLength"],
                                                              cachedDateRatedAndUserRatingWeights, self.cachedDatabase["AllGenres"], self.cachedDatabase["AllCountries"])

        self.vectorProfiles["internationalProfile"] = initInternationalProfile(userProfile.vector, self.cachedDatabase["AllCountries"], self.cachedDatabase["AllGenresLength"],
                                                                                     self.cachedDatabase["ProfileVectorLength"])

        self.vectorProfiles["oldProfile"] = initOldProfile(userProfile.vector)

    def getRowsOfRecommendations(self):
        self.rowsOfRecommendations = []

        if isZeroVector(self.vectorProfiles["favouriteProfile"].vector, self.cachedDatabase["ProfileVectorLength"]):
            print("No favourite profile.")
        else:
            self.rowsOfRecommendations.append(self.getRowOfRecommendations("Based on your favourite films", 
                                                                           self.vectorProfiles["favouriteProfile"].vector, 
                                                                           self.vectorProfiles["favouriteProfile"].profileId))
            

        if isZeroVector(self.vectorProfiles["recentProfile"].vector, self.cachedDatabase["ProfileVectorLength"]):
            print("No recent profile.")
        else:
            self.rowsOfRecommendations.append(self.getRowOfRecommendations("Based on what you watched recently", 
                                                                           self.vectorProfiles["recentProfile"].vector, 
                                                                           self.vectorProfiles["recentProfile"].profileId))

        self.vectorProfiles["genreProfiles"] = sorted(self.vectorProfiles["genreProfiles"], key=lambda x: x.weightedMeanRating, reverse=True)

        for i in range(NUMBER_OF_GENRE_RECOMMENDATION_ROWS):
            if self.vectorProfiles["genreProfiles"][i].weightedMeanRating == 0.0:
                print("No genre profile.")
            else:
                countryText = getProfileMaxCountry(self.vectorProfiles["genreProfiles"][i].vector, 
                                                                           self.cachedDatabase["AllGenresLength"], 
                                                                           self.cachedDatabase["AllCountries"])
                genreText = self.vectorProfiles["genreProfiles"][i].profileId
                self.rowsOfRecommendations.append(self.getRowOfRecommendations(f"Because you like {countryText} {genreText} films", 
                                                                               self.vectorProfiles["genreProfiles"][i].vector, 
                                                                               self.vectorProfiles["genreProfiles"][i].profileId))
            
        if isZeroVector(self.vectorProfiles["internationalProfile"].vector, self.cachedDatabase["ProfileVectorLength"]):
            print("No international profile.")
        else:
            self.rowsOfRecommendations.append(self.getRowOfRecommendations("Try out some international films", 
                                                                           self.vectorProfiles["internationalProfile"].vector, 
                                                                           self.vectorProfiles["internationalProfile"].profileId))
            

        if isZeroVector(self.vectorProfiles["oldProfile"].vector, self.cachedDatabase["ProfileVectorLength"]):
            print("No old profile.")
        else:
            self.rowsOfRecommendations.append(self.getRowOfRecommendations("Try out some older films", 
                                                                           self.vectorProfiles["oldProfile"].vector, 
                                                                           self.vectorProfiles["oldProfile"].profileId))

        return self.rowsOfRecommendations

    def getRowOfRecommendations(self, recommendedRowText, profileVector, profileId):
        rowOfRecommendations = {"recommendedRowText": recommendedRowText, "recommendedFilms": [], "profileId": profileId}

        cosineSimilarities = getSortedCosineSimilaritiesOfAllFilms(self.allFilmDataUnseen, 
                                                                                           profileVector, 
                                                                                           self.cachedDatabase["AllFilmDataVectorized"], 
                                                                                           self.cachedDatabase["AllFilmDataVectorizedMagnitudes"])

        maxNumberOfRecommendations = MAX_NUMBER_OF_RECOMMENDATIONS_PER_ROW
        i = 0
        while i < maxNumberOfRecommendations:
            imdbFilmId = cosineSimilarities[i][0]
            
            if isFilmRecommendationUnique(imdbFilmId, self.rowsOfRecommendations):
                film = self.allFilmDataUnseen[imdbFilmId]
                similarityScore = cosineSimilarities[i][1]
                film['imdbId'] = imdbFilmId
                film['similarityScore'] = int(similarityScore * 100.0)

                rowOfRecommendations['recommendedFilms'].append(film)
            else:
                maxNumberOfRecommendations += 1

            i += 1
        
        return rowOfRecommendations

    def reviewRecommendation(self):
        imdbFilmId = request.args.get('imdbFilmId')
        isThumbsUp = request.args.get('isThumbsUp').lower() == 'true'

        profileId = getProfileIdAssociatedWithFilmId(self.rowsOfRecommendations, imdbFilmId)
        profile = self.getProfileFromProfileId(profileId)

        if isProfileIdGenreProfile(profileId, self.cachedDatabase["AllGenres"]):
            self.adjustGenreProfileWeightedMeanRating(profile, isThumbsUp)

        self.adjustProfileVector(profile, imdbFilmId, isThumbsUp)

        keepVectorBoundary(profile.vector)

        return getFormattedResponse(f"Gave Thumbs {"Up" if isThumbsUp else "Down"} for film {imdbFilmId}.", "", self.guid, 200)

    def getProfileFromProfileId(self, profileId):
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

    def adjustGenreProfileWeightedMeanRating(self, genreProfile, isThumbsUp):
        adjustment = genreProfile.weightedMeanRating * RECOMMENDATION_REVIEW_FACTOR
        
        if isThumbsUp:
            genreProfile.weightedMeanRating += adjustment
        else:
            genreProfile.weightedMeanRating -= adjustment

    def adjustProfileVector(self, profile, imdbFilmId, isThumbsUp):
        filmVector = self.cachedDatabase["AllFilmDataVectorized"][imdbFilmId]
        adjustmentVector = (filmVector - profile.vector) * RECOMMENDATION_REVIEW_FACTOR

        for i in range(len(adjustmentVector)):
            if adjustmentVector[i] == 0.0:
                adjustmentVector[i] = RECOMMENDATION_REVIEW_FACTOR

        if isThumbsUp:
            profile.vector += adjustmentVector
        else:
            profile.vector -= adjustmentVector

    def regenerateRecommendations(self):
        self.allFilmDataUnseen = self.removePreviouslyRecommendedFilms(self.allFilmDataUnseen)

        self.rowsOfRecommendations = self.getRowsOfRecommendations()

        return getFormattedResponse(self.rowsOfRecommendations, "", self.guid, 200)

    def removePreviouslyRecommendedFilms(self, allFilmDataUnseen):
        allFilmDataUnseenRemoved = {}

        for imdbFilmId in allFilmDataUnseen:
            if isFilmRecommendationUnique(imdbFilmId, self.rowsOfRecommendations):
                allFilmDataUnseenRemoved[imdbFilmId] = allFilmDataUnseen[imdbFilmId]

        return allFilmDataUnseenRemoved
        

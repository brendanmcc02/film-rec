import numpy as np
from GenreVectorProfile import *
from VectorProfile import *

class VectorizeUtilities:

    YEAR_WEIGHT = 0.5
    IMDB_RATING_WEIGHT = 1.0
    NUMBER_OF_VOTES_WEIGHT = 1.0
    RUNTIME_WEIGHT = 0.3
    GENRE_WEIGHT = 0.7
    COUNTRY_WEIGHT = 1.0
    PROFILE_YEAR_INDEX = 0
    PROFILE_IMDB_RATING_INDEX = 1
    PROFILE_NUMBER_OF_VOTES_INDEX = 2
    PROFILE_RUNTIME_INDEX = 3
    PROFILE_GENRE_START_INDEX = 4
    RECENCY_PROFILE_DAYS_THRESHOLD = 30

    def vectorizeFilm(self, film, allGenres, allCountries, cachedNormalizedYears, cachedNormalizedImdbRatings,
                      minNumberOfVotes, diffNumberOfVotes, cachedNormalizedRuntimes):
        vector = []

        if self.isFilmInvalid(film):
            raise KeyError

        if str(film['year']) in cachedNormalizedYears:
            normalizedYear = cachedNormalizedYears[str(film['year'])]
            vector.append(normalizedYear)
        else:
            print(f"Error. Film year not in cached normalized years: {film['year']}")
            raise KeyError

        if str(film['imdbRating']) in cachedNormalizedImdbRatings:
            imdbRatingNorm = cachedNormalizedImdbRatings[str(film['imdbRating'])]
            vector.append(imdbRatingNorm)
        else:
            print(f"Error. Film imdb rating not in cached normalized imdb ratings. {str(film['imdbRating'])}")
            raise KeyError

        if diffNumberOfVotes == 0:
            print("diffNumberOfVotes = 0.")
            raise ZeroDivisionError

        numberOfVotesNorm = ((film['numberOfVotes'] - minNumberOfVotes) / diffNumberOfVotes) * self.NUMBER_OF_VOTES_WEIGHT
        vector.append(numberOfVotesNorm)

        if str(film['runtime']) in cachedNormalizedRuntimes:
            runtimeNorm = cachedNormalizedRuntimes[str(film['runtime'])]
            vector.append(runtimeNorm)
        else:
            print(f"Error. Film runtime not in cached normalized runtimes. {str(film['runtime'])}")
            raise KeyError

        self.oneHotEncode(vector, film['genres'], allGenres, self.GENRE_WEIGHT)
        self.oneHotEncode(vector, film['countries'], allCountries, self.COUNTRY_WEIGHT)

        return np.array(vector)

    def isFilmInvalid(self, film):
        expectedFilmKeys = ['year', 'imdbRating', 'numberOfVotes', 'runtime', 'genres', 'countries']

        for key in expectedFilmKeys:
            if key not in film:
                print(f"Error. Key {key} not in {film['title']}.")
                return True

        return False

    # used to one-hot encode genres or countries
    def oneHotEncode(self, vector, filmList, allList, weight):
        for element in allList:
            if element in filmList:
                vector.append(weight)
            else:
                vector.append(0.0)

        return vector

    def getCosineSimilarity(self, a, b, aMagnitude, bMagnitude):
        if aMagnitude == 0.0 or bMagnitude == 0.0:
            return 0.0

        return np.dot(a, b) / (aMagnitude * bMagnitude)

    def keepVectorBoundary(self, vector):
        profileVectorLength = len(vector)
        for i in range(0, profileVectorLength):
            if vector[i] < 0.0:
                vector[i] = 0.0
            elif vector[i] > 1.0:
                vector[i] = 1.0

    def printStringifiedVector(self, vector, allGenres, allCountries, text, cachedNormalizedYearsKeys,
                               cachedNormalizedRuntimesKeys, cachedNormalizedImdbRatingsKeys,
                               minNumberOfVotes, diffNumberOfVotes):
        print("\n" + text)
        print(f"YEAR_WEIGHT: {self.YEAR_WEIGHT}, NUMBER_OF_VOTES_WEIGHT: {self.NUMBER_OF_VOTES_WEIGHT}, "
            f"IMDB_RATING_WEIGHT: {self.IMDB_RATING_WEIGHT},\n"
            f"RUNTIME_WEIGHT: {self.RUNTIME_WEIGHT}, GENRE_WEIGHT: {self.GENRE_WEIGHT}, COUNTRY_WEIGHT: {self.COUNTRY_WEIGHT}")
        
        minYear = int(cachedNormalizedYearsKeys[0])
        diffYear = int(cachedNormalizedYearsKeys[-1]) - minYear
        if diffYear > 0:
            stringifiedYear = int(((vector[self.PROFILE_YEAR_INDEX] / self.YEAR_WEIGHT) * diffYear) + minYear)
        else:
            print("Error. diffYear = 0.")
            raise ZeroDivisionError

        minImdbRating = float(cachedNormalizedImdbRatingsKeys[0])
        diffImdbRating = float(cachedNormalizedImdbRatingsKeys[-1]) - minImdbRating
        if diffImdbRating > 0:
            stringifiedImdbRating = float(((vector[self.PROFILE_IMDB_RATING_INDEX] / self.IMDB_RATING_WEIGHT)
                                            * diffImdbRating) + minImdbRating)
            stringifiedImdbRating = round(stringifiedImdbRating, 1)
        else:
            print("Error. diffImdbRating = 0.")
            raise ZeroDivisionError

        minNumberOfVotes = int(minNumberOfVotes)
        diffNumberOfVotes = int(diffNumberOfVotes)
        if diffNumberOfVotes > 0:
            stringifiedNumberOfVotes = int(((vector[self.PROFILE_NUMBER_OF_VOTES_INDEX] / self.NUMBER_OF_VOTES_WEIGHT)
                                            * diffNumberOfVotes) + minNumberOfVotes)
        else:
            print("Error. diffNumberOfVotes = 0.")
            raise ZeroDivisionError

        minRuntime = int(cachedNormalizedRuntimesKeys[0])
        diffRuntime = int(cachedNormalizedRuntimesKeys[-1]) - minRuntime
        if diffRuntime > 0:
            stringifiedRuntime = int(((vector[self.PROFILE_RUNTIME_INDEX] / self.RUNTIME_WEIGHT) * diffRuntime)
                                    + minRuntime)
        else:
            print("Error. diffRuntime = 0.")
            raise ZeroDivisionError

        stringifiedVector = (f"Year: {stringifiedYear}\n"
                            f"IMDb Rating: {stringifiedImdbRating}\n"
                            f"NumOfVotes: {stringifiedNumberOfVotes}\n"
                            f"Runtime: {stringifiedRuntime} mins\n###############\n")

        i = self.PROFILE_GENRE_START_INDEX
        for genre in allGenres:
            stringifiedVector += f"{genre}: {round(vector[i], 3)}\n"
            i = i + 1

        stringifiedVector += "###############\n"
        for country in allCountries:
            stringifiedVector += f"{country}: {round(vector[i], 3)}\n"
            i = i + 1

        print(f"\n{stringifiedVector}\n")

    def initFavouriteProfile(self, userFilmDataIds, userFilmDataVectorized, profileVectorLength, 
                            cachedDateRatedAndUserRatingWeights, favouriteFilmIds, allGenres,
                            allCountries):
        favouriteProfile = VectorProfile('favourite', profileVectorLength)
        sumOfWeights = 0.0

        for imdbFilmId in userFilmDataIds:
            if imdbFilmId in favouriteFilmIds:
                favouriteProfile.profile += userFilmDataVectorized[imdbFilmId]
                sumOfWeights += cachedDateRatedAndUserRatingWeights[imdbFilmId]

        if sumOfWeights > 0.0:
            favouriteProfile.profile = np.divide(favouriteProfile.profile, sumOfWeights)
            # curve genres
            self.curveAccordingToMax(favouriteProfile.profile, allGenres, self.GENRE_WEIGHT, self.PROFILE_GENRE_START_INDEX)
            # curve countries
            self.curveAccordingToMax(favouriteProfile.profile, allCountries, self.COUNTRY_WEIGHT, 
                                     self.PROFILE_GENRE_START_INDEX + len(allGenres))
            return favouriteProfile
        else:
            favouriteProfile.profile = np.zeros(profileVectorLength)
            return favouriteProfile

    def initGenreProfiles(self, userFilmDataIds, userFilmDataVectorized, cachedDateRatedAndUserRatingWeights, 
                        allGenres, profileVectorLength, numFilmsWatchedInGenreThreshold, allCountries):
        genreProfiles = {}

        for genre in allGenres:
            genreProfiles[genre] = GenreVectorProfile(genre, profileVectorLength)

        for imdbFilmId in userFilmDataIds:
            filmGenres = self.getFilmGenres(userFilmDataVectorized[imdbFilmId], allGenres)
            for genre in filmGenres:
                genreProfiles[genre].profile += userFilmDataVectorized[imdbFilmId]
                genreProfiles[genre].sumOfWeights += cachedDateRatedAndUserRatingWeights[imdbFilmId]
                genreProfiles[genre].quantityFilmsWatched += 1

        for genre in allGenres:
            if genreProfiles[genre].quantityFilmsWatched == 0:
                continue
            
            genreProfiles[genre].profile = np.divide(genreProfiles[genre].profile, 
                                                     genreProfiles[genre].sumOfWeights)
            # curve countries
            self.curveAccordingToMax(genreProfiles[genre].profile, allCountries, self.COUNTRY_WEIGHT, 
                                self.PROFILE_GENRE_START_INDEX + len(allGenres))
            genreProfiles[genre].weightedMeanRating = (genreProfiles[genre].sumOfWeights / 
                                                       genreProfiles[genre].quantityFilmsWatched)
            if numFilmsWatchedInGenreThreshold > 0:
                numFilmsWatchedInGenreFactor = min(1.0, (genreProfiles[genre].quantityFilmsWatched /
                                                        numFilmsWatchedInGenreThreshold))
            else:
                numFilmsWatchedInGenreFactor = 1.0

            genreProfiles[genre].weightedMeanRating *= numFilmsWatchedInGenreFactor

        # return as a list of GenreProfileVector objects
        return [value for _, value in genreProfiles.items()]

    def getFilmGenres(self, vectorizedFilm, allGenres):
        filmGenreIndexes = []
        profileGenreEndIndex = self.PROFILE_GENRE_START_INDEX + len(allGenres)

        for i in range(self.PROFILE_GENRE_START_INDEX, profileGenreEndIndex):
            if vectorizedFilm[i] > 0.0:
                filmGenreIndexes.append(i - self.PROFILE_GENRE_START_INDEX)

        filmGenres = []

        for genreIndex in filmGenreIndexes:
            filmGenres.append(allGenres[genreIndex])

        return filmGenres

    def initRecentProfile(self, userFilmData, userFilmDataVectorized, maxDateRated, 
                           profileVectorLength, cachedDateRatedAndUserRatingWeights, allGenres,
                           allCountries):
        recentProfile = VectorProfile('recent', profileVectorLength)
        sumOfWeights = 0.0

        for imdbFilmId in userFilmData:
            timeDifference = maxDateRated - userFilmData[imdbFilmId]['dateRated']
            if timeDifference.days <= self.RECENCY_PROFILE_DAYS_THRESHOLD:
                recentProfile.profile += userFilmDataVectorized[imdbFilmId]
                sumOfWeights += cachedDateRatedAndUserRatingWeights[imdbFilmId]
            else:
                # file is sorted by date, no need to look further
                break

        if sumOfWeights > 0.0:
            recentProfile.profile = np.divide(recentProfile.profile, sumOfWeights)
            # curve genres
            self.curveAccordingToMax(recentProfile.profile, allGenres, self.GENRE_WEIGHT, self.PROFILE_GENRE_START_INDEX)
            # curve countries
            self.curveAccordingToMax(recentProfile.profile, allCountries, self.COUNTRY_WEIGHT, 
                                self.PROFILE_GENRE_START_INDEX + len(allGenres))
            return recentProfile
        else:
            recentProfile.profile = np.zeros(profileVectorLength)
            return recentProfile

    def initUserProfile(self, userFilmDataIds, userFilmDataVectorized, profileVectorLength, 
                        cachedDateRatedAndUserRatingWeights, allGenres, allCountries):
        userProfile = VectorProfile('user', profileVectorLength)
        sumOfWeights = 0.0

        for imdbFilmId in userFilmDataIds:
            userProfile.profile += userFilmDataVectorized[imdbFilmId]
            sumOfWeights += cachedDateRatedAndUserRatingWeights[imdbFilmId]

        if sumOfWeights > 0.0:
            userProfile.profile = np.divide(userProfile.profile, sumOfWeights)
            # curve genres
            self.curveAccordingToMax(userProfile.profile, allGenres, self.GENRE_WEIGHT, self.PROFILE_GENRE_START_INDEX)
            # curve countries
            self.curveAccordingToMax(userProfile.profile, allCountries, self.COUNTRY_WEIGHT, 
                                     self.PROFILE_GENRE_START_INDEX + len(allGenres))
            
        return userProfile

    def initOldProfile(self, userProfile):
        # note: userProfile already has curved genres and countries
        oldProfile = VectorProfile('old')
        oldProfile.profile = np.copy(userProfile)
        oldProfile.profile[self.PROFILE_YEAR_INDEX] = 0.0
        
        return oldProfile

    def initInternationalProfile(self, userProfile, allCountries, allGenresLength, profileVectorLength):
        internationalProfile = VectorProfile('international')
        internationalProfile.profile = np.copy(userProfile)

        countryStartIndex = self.PROFILE_GENRE_START_INDEX + allGenresLength
        maxCountryIndex = countryStartIndex
        maxCountryValue = internationalProfile.profile[countryStartIndex]

        hasUserOnlyWatchedAmericanOrBritishFilms = True

        for index in range(countryStartIndex, (countryStartIndex + len(allCountries))):
                if internationalProfile.profile[index] > maxCountryValue:
                    maxCountryValue = internationalProfile.profile[index]
                    maxCountryIndex = index

                if self.isNonZeroIndexValueNotAmericanOrBritish(index, allCountries, countryStartIndex, 
                                                                internationalProfile.profile[index]):
                    hasUserOnlyWatchedAmericanOrBritishFilms = False

        if hasUserOnlyWatchedAmericanOrBritishFilms:
            internationalProfile.profile = np.zeros(profileVectorLength)
            return internationalProfile

        americanIndex = allCountries.index("American") + countryStartIndex
        britishIndex = allCountries.index("British") + countryStartIndex
        
        if maxCountryIndex == americanIndex or maxCountryIndex == britishIndex:
            internationalProfile.profile[americanIndex] = 0.0
            internationalProfile.profile[britishIndex] = 0.0
        else:        
            internationalProfile.profile[maxCountryIndex] = 0.0

        # curve countries
        self.curveAccordingToMax(internationalProfile.profile, allCountries, self.COUNTRY_WEIGHT, 
                                 countryStartIndex)

        return internationalProfile

    def isNonZeroIndexValueNotAmericanOrBritish(self, index, allCountries, countryStartIndex, valueAtIndex):
        return (valueAtIndex > 0.0 and allCountries[index - countryStartIndex] != "American" and
                allCountries[index - countryStartIndex] != "British")

    # used to curve genre/country values according to max genre/country value
    def curveAccordingToMax(self, profileVector, list, weight, startIndex):
        endIndex = startIndex + len(list)
        minValue = profileVector[startIndex]
        maxValue = profileVector[startIndex]

        for index in range(startIndex, endIndex):
            minValue = min(minValue, profileVector[index])
            maxValue = max(maxValue, profileVector[index])

        diffValue = maxValue - minValue

        for index in range(startIndex, endIndex):
            if diffValue > 0.0:
                profileVector[index] = (profileVector[index] - minValue) / diffValue
            elif minValue > 0.0:
                profileVector[index] = 1.0

            profileVector[index] *= weight

    def getProfileMaxCountry(self, profile, allGenresLength, allCountries):
        countryStartIndex = self.PROFILE_GENRE_START_INDEX + allGenresLength
        maxCountryIndex = countryStartIndex
        maxCountryValue = profile[countryStartIndex]

        for i in range(countryStartIndex, (countryStartIndex + len(allCountries))):
                if profile[i] > maxCountryValue:
                    maxCountryValue = profile[i]
                    maxCountryIndex = i

        return allCountries[maxCountryIndex - countryStartIndex]
    
    def initVectorProfiles(self, profileVectorLength):
        vectorProfiles = {}

        vectorProfiles["favouriteProfile"] = VectorProfile('favourite', profileVectorLength)
        vectorProfiles["genreProfiles"] = []
        vectorProfiles["recentProfile"] = VectorProfile('recent', profileVectorLength)
        vectorProfiles["internationalProfile"] = VectorProfile('international', profileVectorLength)
        vectorProfiles["oldProfile"] = VectorProfile('old', profileVectorLength)

        return vectorProfiles

    def isZeroVector(self, vectorProfile, profileVectorLength):
        return np.array_equal(vectorProfile, np.zeros(profileVectorLength))

import numpy as np
from GenreVectorProfile import *
from VectorProfile import *

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
VECTORIZED_MAGNITUDE_NUMBER_OF_ROUNDED_DECIMAL_POINTS = 5

def vectorizeFilm(film, allGenres, allCountries, cachedNormalizedYears, cachedNormalizedImdbRatings,
                    minNumberOfVotes, diffNumberOfVotes, cachedNormalizedRuntimes):
    vector = []

    if isFilmInvalid(film):
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

    numberOfVotesNorm = ((film['numberOfVotes'] - minNumberOfVotes) / diffNumberOfVotes) * NUMBER_OF_VOTES_WEIGHT
    vector.append(numberOfVotesNorm)

    if str(film['runtime']) in cachedNormalizedRuntimes:
        runtimeNorm = cachedNormalizedRuntimes[str(film['runtime'])]
        vector.append(runtimeNorm)
    else:
        print(f"Error. Film runtime not in cached normalized runtimes. {str(film['runtime'])}")
        raise KeyError

    oneHotEncode(vector, film['genres'], allGenres, GENRE_WEIGHT)
    oneHotEncode(vector, film['countries'], allCountries, COUNTRY_WEIGHT)

    return np.array(vector)

def isFilmInvalid(film):
    expectedFilmKeys = ['year', 'imdbRating', 'numberOfVotes', 'runtime', 'genres', 'countries']

    for key in expectedFilmKeys:
        if key not in film:
            print(f"Error. Key {key} not in {film['title']}.")
            return True

    return False

# used to one-hot encode genres or countries
def oneHotEncode(vector, filmList, allList, weight):
    for element in allList:
        if element in filmList:
            vector.append(weight)
        else:
            vector.append(0.0)

    return vector

def getCosineSimilarity(a, b, aMagnitude, bMagnitude):
    if aMagnitude == 0.0 or bMagnitude == 0.0:
        return 0.0

    return np.dot(a, b) / (aMagnitude * bMagnitude)

def keepVectorBoundary(vector):
    profileVectorLength = len(vector)
    for i in range(0, profileVectorLength):
        if vector[i] < 0.0:
            vector[i] = 0.0
        elif vector[i] > 1.0:
            vector[i] = 1.0

def printStringifiedVector(vector, allGenres, allCountries, text, cachedNormalizedYearsKeys,
                            cachedNormalizedRuntimesKeys, cachedNormalizedImdbRatingsKeys,
                            minNumberOfVotes, diffNumberOfVotes):
    print("\n" + text)
    print(f"YEAR_WEIGHT: {YEAR_WEIGHT}, NUMBER_OF_VOTES_WEIGHT: {NUMBER_OF_VOTES_WEIGHT}, "
        f"IMDB_RATING_WEIGHT: {IMDB_RATING_WEIGHT},\n"
        f"RUNTIME_WEIGHT: {RUNTIME_WEIGHT}, GENRE_WEIGHT: {GENRE_WEIGHT}, COUNTRY_WEIGHT: {COUNTRY_WEIGHT}")
    
    minYear = int(cachedNormalizedYearsKeys[0])
    diffYear = int(cachedNormalizedYearsKeys[-1]) - minYear
    if diffYear > 0:
        stringifiedYear = int(((vector[PROFILE_YEAR_INDEX] / YEAR_WEIGHT) * diffYear) + minYear)
    else:
        print("Error. diffYear = 0.")
        raise ZeroDivisionError

    minImdbRating = float(cachedNormalizedImdbRatingsKeys[0])
    diffImdbRating = float(cachedNormalizedImdbRatingsKeys[-1]) - minImdbRating
    if diffImdbRating > 0:
        stringifiedImdbRating = float(((vector[PROFILE_IMDB_RATING_INDEX] / IMDB_RATING_WEIGHT)
                                        * diffImdbRating) + minImdbRating)
        stringifiedImdbRating = round(stringifiedImdbRating, 1)
    else:
        print("Error. diffImdbRating = 0.")
        raise ZeroDivisionError

    minNumberOfVotes = int(minNumberOfVotes)
    diffNumberOfVotes = int(diffNumberOfVotes)
    if diffNumberOfVotes > 0:
        stringifiedNumberOfVotes = int(((vector[PROFILE_NUMBER_OF_VOTES_INDEX] / NUMBER_OF_VOTES_WEIGHT)
                                        * diffNumberOfVotes) + minNumberOfVotes)
    else:
        print("Error. diffNumberOfVotes = 0.")
        raise ZeroDivisionError

    minRuntime = int(cachedNormalizedRuntimesKeys[0])
    diffRuntime = int(cachedNormalizedRuntimesKeys[-1]) - minRuntime
    if diffRuntime > 0:
        stringifiedRuntime = int(((vector[PROFILE_RUNTIME_INDEX] / RUNTIME_WEIGHT) * diffRuntime)
                                + minRuntime)
    else:
        print("Error. diffRuntime = 0.")
        raise ZeroDivisionError

    stringifiedVector = (f"Year: {stringifiedYear}\n"
                        f"IMDb Rating: {stringifiedImdbRating}\n"
                        f"NumOfVotes: {stringifiedNumberOfVotes}\n"
                        f"Runtime: {stringifiedRuntime} mins\n###############\n")

    i = PROFILE_GENRE_START_INDEX
    for genre in allGenres:
        stringifiedVector += f"{genre}: {round(vector[i], 3)}\n"
        i = i + 1

    stringifiedVector += "###############\n"
    for country in allCountries:
        stringifiedVector += f"{country}: {round(vector[i], 3)}\n"
        i = i + 1

    print(f"\n{stringifiedVector}\n")

def initFavouriteProfile(userFilmDataIds, userFilmDataVectorized, profileVectorLength, 
                        cachedDateRatedAndUserRatingWeights, favouriteFilmIds, allGenres,
                        allCountries):
    favouriteProfile = VectorProfile('favourite', profileVectorLength)
    sumOfWeights = 0.0

    for imdbFilmId in userFilmDataIds:
        if imdbFilmId in favouriteFilmIds:
            favouriteProfile.vector += userFilmDataVectorized[imdbFilmId]
            sumOfWeights += cachedDateRatedAndUserRatingWeights[imdbFilmId]

    if sumOfWeights > 0.0:
        favouriteProfile.vector = np.divide(favouriteProfile.vector, sumOfWeights)
        # curve genres
        curveAccordingToMax(favouriteProfile.vector, allGenres, GENRE_WEIGHT, PROFILE_GENRE_START_INDEX)
        # curve countries
        curveAccordingToMax(favouriteProfile.vector, allCountries, COUNTRY_WEIGHT, 
                                    PROFILE_GENRE_START_INDEX + len(allGenres))
        return favouriteProfile
    else:
        favouriteProfile.vector = np.zeros(profileVectorLength)
        return favouriteProfile

def initGenreProfiles(userFilmDataIds, userFilmDataVectorized, cachedDateRatedAndUserRatingWeights, 
                    allGenres, profileVectorLength, numFilmsWatchedInGenreThreshold, allCountries):
    genreProfiles = {}

    for genre in allGenres:
        genreProfiles[genre] = GenreVectorProfile(genre, profileVectorLength)

    for imdbFilmId in userFilmDataIds:
        filmGenres = getFilmGenres(userFilmDataVectorized[imdbFilmId], allGenres)
        for genre in filmGenres:
            genreProfiles[genre].vector += userFilmDataVectorized[imdbFilmId]
            genreProfiles[genre].sumOfWeights += cachedDateRatedAndUserRatingWeights[imdbFilmId]
            genreProfiles[genre].quantityFilmsWatched += 1

    for genre in allGenres:
        if genreProfiles[genre].quantityFilmsWatched == 0:
            continue
        
        genreProfiles[genre].vector = np.divide(genreProfiles[genre].vector, 
                                                    genreProfiles[genre].sumOfWeights)
        # curve countries
        curveAccordingToMax(genreProfiles[genre].vector, allCountries, COUNTRY_WEIGHT, 
                            PROFILE_GENRE_START_INDEX + len(allGenres))
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

def getFilmGenres(vectorizedFilm, allGenres):
    filmGenreIndexes = []
    profileGenreEndIndex = PROFILE_GENRE_START_INDEX + len(allGenres)

    for i in range(PROFILE_GENRE_START_INDEX, profileGenreEndIndex):
        if vectorizedFilm[i] > 0.0:
            filmGenreIndexes.append(i - PROFILE_GENRE_START_INDEX)

    filmGenres = []

    for genreIndex in filmGenreIndexes:
        filmGenres.append(allGenres[genreIndex])

    return filmGenres

def initRecentProfile(userFilmData, userFilmDataVectorized, maxDateRated, 
                        profileVectorLength, cachedDateRatedAndUserRatingWeights, allGenres,
                        allCountries):
    recentProfile = VectorProfile('recent', profileVectorLength)
    sumOfWeights = 0.0

    for imdbFilmId in userFilmData:
        timeDifference = maxDateRated - userFilmData[imdbFilmId]['dateRated']
        if timeDifference.days <= RECENCY_PROFILE_DAYS_THRESHOLD:
            recentProfile.vector += userFilmDataVectorized[imdbFilmId]
            sumOfWeights += cachedDateRatedAndUserRatingWeights[imdbFilmId]
        else:
            # file is sorted by date, no need to look further
            break

    if sumOfWeights > 0.0:
        recentProfile.vector = np.divide(recentProfile.vector, sumOfWeights)
        # curve genres
        curveAccordingToMax(recentProfile.vector, allGenres, GENRE_WEIGHT, PROFILE_GENRE_START_INDEX)
        # curve countries
        curveAccordingToMax(recentProfile.vector, allCountries, COUNTRY_WEIGHT, 
                            PROFILE_GENRE_START_INDEX + len(allGenres))
        return recentProfile
    else:
        recentProfile.vector = np.zeros(profileVectorLength)
        return recentProfile

def initUserProfile(userFilmDataIds, userFilmDataVectorized, profileVectorLength, 
                    cachedDateRatedAndUserRatingWeights, allGenres, allCountries):
    userProfile = VectorProfile('user', profileVectorLength)
    sumOfWeights = 0.0

    for imdbFilmId in userFilmDataIds:
        userProfile.vector += userFilmDataVectorized[imdbFilmId]
        sumOfWeights += cachedDateRatedAndUserRatingWeights[imdbFilmId]

    if sumOfWeights > 0.0:
        userProfile.vector = np.divide(userProfile.vector, sumOfWeights)
        # curve genres
        curveAccordingToMax(userProfile.vector, allGenres, GENRE_WEIGHT, PROFILE_GENRE_START_INDEX)
        # curve countries
        curveAccordingToMax(userProfile.vector, allCountries, COUNTRY_WEIGHT, 
                                    PROFILE_GENRE_START_INDEX + len(allGenres))
        
    return userProfile

def initOldProfile(userProfile):
    # note: userProfile already has curved genres and countries
    oldProfile = VectorProfile('old')
    oldProfile.vector = np.copy(userProfile)
    oldProfile.vector[PROFILE_YEAR_INDEX] = 0.0
    
    return oldProfile

def initInternationalProfile(userProfile, allCountries, allGenresLength, profileVectorLength):
    internationalProfile = VectorProfile('international')
    internationalProfile.vector = np.copy(userProfile)

    countryStartIndex = PROFILE_GENRE_START_INDEX + allGenresLength
    maxCountryIndex = countryStartIndex
    maxCountryValue = internationalProfile.vector[countryStartIndex]

    hasUserOnlyWatchedAmericanOrBritishFilms = True

    for index in range(countryStartIndex, (countryStartIndex + len(allCountries))):
            if internationalProfile.vector[index] > maxCountryValue:
                maxCountryValue = internationalProfile.vector[index]
                maxCountryIndex = index

            if isNonZeroIndexValueNotAmericanOrBritish(index, allCountries, countryStartIndex, 
                                                            internationalProfile.vector[index]):
                hasUserOnlyWatchedAmericanOrBritishFilms = False

    if hasUserOnlyWatchedAmericanOrBritishFilms:
        internationalProfile.vector = np.zeros(profileVectorLength)
        return internationalProfile

    americanIndex = allCountries.index("American") + countryStartIndex
    britishIndex = allCountries.index("British") + countryStartIndex
    
    if maxCountryIndex == americanIndex or maxCountryIndex == britishIndex:
        internationalProfile.vector[americanIndex] = 0.0
        internationalProfile.vector[britishIndex] = 0.0
    else:        
        internationalProfile.vector[maxCountryIndex] = 0.0

    # curve countries
    curveAccordingToMax(internationalProfile.vector, allCountries, COUNTRY_WEIGHT, 
                                countryStartIndex)

    return internationalProfile

def isNonZeroIndexValueNotAmericanOrBritish(index, allCountries, countryStartIndex, valueAtIndex):
    return (valueAtIndex > 0.0 and allCountries[index - countryStartIndex] != "American" and
            allCountries[index - countryStartIndex] != "British")

# used to curve genre/country values according to max genre/country value
def curveAccordingToMax(profileVector, list, weight, startIndex):
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

def getProfileMaxCountry(profile, allGenresLength, allCountries):
    countryStartIndex = PROFILE_GENRE_START_INDEX + allGenresLength
    maxCountryIndex = countryStartIndex
    maxCountryValue = profile[countryStartIndex]

    for i in range(countryStartIndex, (countryStartIndex + len(allCountries))):
            if profile[i] > maxCountryValue:
                maxCountryValue = profile[i]
                maxCountryIndex = i

    return allCountries[maxCountryIndex - countryStartIndex]

def initVectorProfiles(profileVectorLength):
    vectorProfiles = {}

    vectorProfiles["favouriteProfile"] = VectorProfile('favourite', profileVectorLength)
    vectorProfiles["genreProfiles"] = []
    vectorProfiles["recentProfile"] = VectorProfile('recent', profileVectorLength)
    vectorProfiles["internationalProfile"] = VectorProfile('international', profileVectorLength)
    vectorProfiles["oldProfile"] = VectorProfile('old', profileVectorLength)

    return vectorProfiles

def isZeroVector(vectorProfile, profileVectorLength):
    return np.array_equal(vectorProfile, np.zeros(profileVectorLength))

def getSortedCosineSimilaritiesOfAllFilms(allFilmDataUnseen, profileVector, allFilmDataVectorized, allFilmDataVectorizedMagnitudes):
    cosineSimilarities = {}
    profileVectorMagnitude = np.linalg.norm(profileVector)
    
    for imdbFilmId in allFilmDataUnseen:
        filmVectorMagnitude = allFilmDataVectorizedMagnitudes[imdbFilmId]
        cosineSimilarities[imdbFilmId] = getCosineSimilarity(allFilmDataVectorized[imdbFilmId], profileVector,
                                                                filmVectorMagnitude, profileVectorMagnitude)

    return sorted(cosineSimilarities.items(), key=lambda x: x[1], reverse=True)

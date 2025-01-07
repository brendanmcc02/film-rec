import numpy as np

YEAR_WEIGHT = 1.0
IMDB_RATING_WEIGHT = 1.0
NUM_OF_VOTES_WEIGHT = 1.0
RUNTIME_WEIGHT = 0.3
GENRE_WEIGHT = 1.0
COUNTRY_WEIGHT = 1.0
PROFILE_YEAR_INDEX = 0
PROFILE_IMDB_RATING_INDEX = 1
PROFILE_NUM_OF_VOTES_INDEX = 2
PROFILE_RUNTIME_INDEX = 3
PROFILE_GENRE_START_INDEX = 4
RECENCY_PROFILE_DAYS_THRESHOLD = 30


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

    numberOfVotesNorm = ((film['numberOfVotes'] - minNumberOfVotes) / diffNumberOfVotes) * NUM_OF_VOTES_WEIGHT
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
            vector.append(0)

    return vector


def cosineSimilarity(a, b, aMagnitude, bMagnitude):
    if aMagnitude == 0.0 or bMagnitude == 0.0:
        return 0.0

    return np.dot(a, b) / (aMagnitude * bMagnitude)


def keepVectorBoundary(vector, profileVectorLength):
    for i in range(0, profileVectorLength):
        if vector[i] < 0.0:
            vector[i] = 0.0
        elif vector[i] > 1.0:
            vector[i] = 1.0


def printStringifiedVector(vector, allGenres, allCountries, text):
    print(text)
    print(f"YEAR_WEIGHT: {YEAR_WEIGHT}, NUM_OF_VOTES_WEIGHT: {NUM_OF_VOTES_WEIGHT}, IMDB_RATING_WEIGHT: {IMDB_RATING_WEIGHT}\n"
          f"RUNTIME_WEIGHT: {RUNTIME_WEIGHT}, GENRE_WEIGHT: {GENRE_WEIGHT}, COUNTRY_WEIGHT: {COUNTRY_WEIGHT}")
    stringifiedVector = (f"Year: {round(vector[PROFILE_YEAR_INDEX], 3)}\n"
                         f"IMDb Rating: {round(vector[PROFILE_IMDB_RATING_INDEX], 3)}\n"
                         f"NumOfVotes: {round(vector[PROFILE_NUM_OF_VOTES_INDEX], 3)}\n"
                         f"Runtime: {round(vector[PROFILE_RUNTIME_INDEX], 3)}\n")

    i = PROFILE_GENRE_START_INDEX
    for genre in allGenres:
        stringifiedVector += f"{genre}: {round(vector[i], 3)}\n"
        i = i + 1

    for country in allCountries:
        stringifiedVector += f"{country}: {round(vector[i], 3)}\n"
        i = i + 1

    print(f"\n{stringifiedVector}\n")


def initFavouriteProfile(userFilmDataIds, userFilmDataVectorized, profileVectorLength, 
                         cachedDateRatedAndUserRatingWeights, favouriteFilmIds):
    favouriteProfile = np.zeros(profileVectorLength)
    sumOfWeights = 0.0

    for imdbFilmId in userFilmDataIds:
        if imdbFilmId in favouriteFilmIds:
            favouriteProfile += userFilmDataVectorized[imdbFilmId]
            sumOfWeights += cachedDateRatedAndUserRatingWeights[imdbFilmId]

    if sumOfWeights > 0.0:
        favouriteProfile = np.divide(favouriteProfile, sumOfWeights)
        return {'profile': favouriteProfile, 'profileId': 'favourite'}
    else:
        return {'profile': np.zeros(profileVectorLength), 'profileId': 'favourite'}


def initGenreProfiles(userFilmDataIds, userFilmDataVectorized, cachedDateRatedAndUserRatingWeights, 
                      allGenres, profileVectorLength, numFilmsWatchedInGenreThreshold):
    genreProfiles = {}

    for genre in allGenres:
        genreProfiles[genre] = {"profileId": genre, "profile": np.zeros(profileVectorLength),
                                "sumOfWeights": 0.0, "quantityFilmsWatched": 0,
                                "weightedMeanRating": 0.0}

    for imdbFilmId in userFilmDataIds:
        filmGenres = getFilmGenres(userFilmDataVectorized[imdbFilmId], allGenres)
        for genre in filmGenres:
            genreProfiles[genre]['profile'] += userFilmDataVectorized[imdbFilmId]
            genreProfiles[genre]['sumOfWeights'] += cachedDateRatedAndUserRatingWeights[imdbFilmId]
            genreProfiles[genre]['quantityFilmsWatched'] += 1

    for genre in allGenres:
        if genreProfiles[genre]['quantityFilmsWatched'] == 0:
            continue
        
        numFilmsWatchedInGenreFactor = min(1.0, (genreProfiles[genre]['quantityFilmsWatched'] /
                                                 numFilmsWatchedInGenreThreshold))
        genreProfiles[genre]['profile'] = np.divide(genreProfiles[genre]['profile'], 
                                                    genreProfiles[genre]['sumOfWeights'])
        genreProfiles[genre]['profile'] *= numFilmsWatchedInGenreFactor
        genreProfiles[genre]['weightedMeanRating'] = (genreProfiles[genre]['sumOfWeights'] / 
                                                      genreProfiles[genre]['quantityFilmsWatched'])
        genreProfiles[genre]['weightedMeanRating'] *= numFilmsWatchedInGenreFactor

    # return as a list of tuples, where each tuple has the values (genre, profile, weightedMeanRating, 
    # sumOfWeights, quantityFilmsWatched)
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


def initRecencyProfile(userFilmData, userFilmDataIds, userFilmDataVectorized, maxDateRated, 
                       profileVectorLength, cachedDateRatedAndUserRatingWeights):
    recencyProfile = np.zeros(profileVectorLength)
    sumOfWeights = 0.0

    for imdbFilmId in userFilmDataIds:
        timeDifference = maxDateRated - userFilmData[imdbFilmId]['dateRated']
        if timeDifference.days <= RECENCY_PROFILE_DAYS_THRESHOLD:
            recencyProfile += userFilmDataVectorized[imdbFilmId]
            sumOfWeights += cachedDateRatedAndUserRatingWeights[imdbFilmId]
        else:
            # file is sorted by date, no need to look further
            break

    if sumOfWeights > 0.0:
        recencyProfile = np.divide(recencyProfile, sumOfWeights)
        return {'profile': recencyProfile, 'profileId': 'recency'}
    else:
        return {'profile': np.zeros(profileVectorLength), 'profileId': 'recency'}


def initUserProfile(userFilmDataIds, userFilmDataVectorized, profileVectorLength, 
                    cachedDateRatedAndUserRatingWeights):
    userProfile = np.zeros(profileVectorLength)
    sumOfWeights = 0.0

    for imdbFilmId in userFilmDataIds:
        userProfile += userFilmDataVectorized[imdbFilmId]
        sumOfWeights += cachedDateRatedAndUserRatingWeights[imdbFilmId]

    if sumOfWeights > 0.0:
        userProfile = np.divide(userProfile, sumOfWeights)
        
    return {'profile': userProfile, 'profileId': 'user'}


def initOldProfile(userProfile):
    oldProfile = {'profile': np.copy(userProfile), 'profileId': 'old'}
    oldProfile['profile'][PROFILE_YEAR_INDEX] = 0.0
    return oldProfile


def initObscureProfile(userProfile):
    obscureProfile = {'profile': np.copy(userProfile), 'profileId': 'obscure'}
    obscureProfile['profile'][PROFILE_NUM_OF_VOTES_INDEX] = 0.0
    return obscureProfile


def initInternationalProfile(userProfile, allCountries, allGenresLength):
    internationalProfile = {'profile': np.copy(userProfile), 'profileId': 'international'}

    countryStartIndex = PROFILE_GENRE_START_INDEX + allGenresLength
    maxCountryIndex = countryStartIndex
    maxCountryValue = internationalProfile['profile'][countryStartIndex]

    for i in range(countryStartIndex, (countryStartIndex + len(allCountries))):
            if internationalProfile['profile'][i] > maxCountryValue:
                maxCountryValue = internationalProfile['profile'][i]
                maxCountryIndex = i

    americanIndex = allCountries.index("American") + countryStartIndex
    britishIndex = allCountries.index("British") + countryStartIndex
    if maxCountryIndex == americanIndex or maxCountryIndex == britishIndex:
        internationalProfile['profile'][americanIndex] = 0.0
        internationalProfile['profile'][britishIndex] = 0.0
    else:        
        internationalProfile['profile'][maxCountryIndex] = 0.0

    curveAccordingToMax(internationalProfile['profile'], allCountries, COUNTRY_WEIGHT, 
                        countryStartIndex)

    return internationalProfile


# used to curve genre/country values according to max genre/country value
def curveAccordingToMax(profileVector, list, weight, startIndex):
    userProfileGenreEndIndex = startIndex + len(list)
    minValue = profileVector[startIndex]
    maxValue = profileVector[startIndex]

    for index in range(startIndex, userProfileGenreEndIndex):
        minValue = min(minValue, profileVector[index])
        maxValue = max(maxValue, profileVector[index])

    diffValue = maxValue - minValue

    for index in range(startIndex, userProfileGenreEndIndex):
        if diffValue > 0.0:
            profileVector[index] = (profileVector[index] - minValue) / diffValue
        else:
            profileVector[index] = 0.0

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

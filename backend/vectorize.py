import numpy as np
YEAR_WEIGHT = 0.3
NUM_VOTES_WEIGHT = 0.3
RUNTIME_WEIGHT = 0.3
GENRE_WEIGHT = 0.75
COUNTRY_WEIGHT = 0.5
LANGUAGE_WEIGHT = 0.5
PROFILE_YEAR_INDEX = 0
PROFILE_IMDB_RATING_INDEX = 1
PROFILE_NUM_OF_VOTES_INDEX = 2
PROFILE_RUNTIME_INDEX = 3
PROFILE_GENRE_START_INDEX = 4
RECENCY_PROFILE_DAYS_THRESHOLD = 30


def vectorizeFilm(film, allGenres, allLanguages, allCountries, cachedNormalizedYears, cachedNormalizedImdbRatings,
                  minNumberOfVotes, diffNumberOfVotes, cachedNormalizedRuntimes):
    vector = []

    if isFilmInvalid(film):
        print("Film is invalid")
        return np.zeros(1)

    if str(film['year']) in cachedNormalizedYears:
        normalizedYear = cachedNormalizedYears[str(film['year'])]
        vector.append(normalizedYear)
    else:
        print(f"Error. Film year not in cached normalized years: {film['year']}")

    if str(film['imdbRating']) in cachedNormalizedImdbRatings:
        imdbRatingNorm = cachedNormalizedImdbRatings[str(film['imdbRating'])]
        vector.append(imdbRatingNorm)
    else:
        print(f"Error. Film imdb rating not in cached normalized imdb ratings. {str(film['imdbRating'])}")

    if diffNumberOfVotes == 0:
        print("diffNumberOfVotes = 0.")
        raise ZeroDivisionError

    numberOfVotesNorm = ((film['numberOfVotes'] - minNumberOfVotes) / diffNumberOfVotes) * NUM_VOTES_WEIGHT
    vector.append(numberOfVotesNorm)

    if str(film['runtime']) in cachedNormalizedRuntimes:
        runtimeNorm = cachedNormalizedRuntimes[str(film['runtime'])]
        vector.append(runtimeNorm)
    else:
        print(f"Error. Film runtime not in cached normalized runtimes. {str(film['runtime'])}")

    oneHotEncode(vector, film['genres'], allGenres)
    oneHotEncode(vector, film['languages'], allLanguages)
    oneHotEncode(vector, film['countries'], allCountries)

    return np.array(vector)


def isFilmInvalid(film):
    expectedFilmKeys = ['year', 'imdbRating', 'numberOfVotes', 'runtime', 'genres', 'languages', 'countries']

    for key in expectedFilmKeys:
        if key not in film:
            print(f"Error. Key {key} not in {film['title']}.")
            return True

    return False


# used to one-hot encode genres, countries, languages
def oneHotEncode(vector, filmList, allList):
    for element in allList:
        if element in filmList:
            vector.append(1)
        else:
            vector.append(0)

    return vector


def cosineSimilarity(a, b, aMagnitude, bMagnitude):
    if aMagnitude == 0.0 or bMagnitude == 0.0:
        return 0.0

    return np.dot(a, b) / (aMagnitude * bMagnitude)


def keepVectorBoundary(vector, PROFILE_VECTOR_LENGTH):
    for i in range(0, PROFILE_VECTOR_LENGTH):
        if vector[i] < 0.0:
            vector[i] = 0.0
        elif vector[i] > 1.0:
            vector[i] = 1.0


def printStringifiedVector(vector, allGenres, allCountries, allLanguages):
    print(f"YEAR_WEIGHT: {YEAR_WEIGHT}, NUM_OF_VOTES_WEIGHT: {NUM_VOTES_WEIGHT}, RUNTIME_WEIGHT: {RUNTIME_WEIGHT}, "
          f"LANGUAGE_WEIGHT: {LANGUAGE_WEIGHT}, COUNTRY_WEIGHT: {COUNTRY_WEIGHT}\n")
    stringifiedVector = (f"Year: {round(vector[PROFILE_YEAR_INDEX], 3)}\n"
                         f"IMDb Rating: {round(vector[PROFILE_IMDB_RATING_INDEX], 3)}\n"
                         f"NumOfVotes: {round(vector[PROFILE_NUM_OF_VOTES_INDEX], 3)}\n"
                         f"Runtime: {round(vector[PROFILE_RUNTIME_INDEX], 3)}\n")

    i = PROFILE_GENRE_START_INDEX
    for genre in allGenres:
        stringifiedVector += f"{genre}: {round(vector[i], 3)}\n"
        i = i + 1

    for language in allLanguages:
        stringifiedVector += f"{language}: {round(vector[i], 3)}\n"
        i = i + 1

    for country in allCountries:
        stringifiedVector += f"{country}: {round(vector[i], 3)}\n"
        i = i + 1

    print(f"\n{stringifiedVector}\n")


# films with multiple genres, languages & countries have higher magnitudes due to the nature of calculating vector
# magnitudes. this calculates the magnitude of a vector in an unbiased way.
def calculateUnbiasedVectorMagnitude(vector, allGenresLength, allLanguagesLength, allCountriesLength):
    unbiasedVectorMagnitude = 0.0

    for i in range(PROFILE_YEAR_INDEX, PROFILE_GENRE_START_INDEX):
        unbiasedVectorMagnitude += vector[i] * vector[i]

    profileGenreEndIndex = PROFILE_GENRE_START_INDEX + allGenresLength
    meanGenreVectorSum = 0.0
    meanGenreVectorQuantity = 0
    for i in range(PROFILE_GENRE_START_INDEX, profileGenreEndIndex):
        if vector[i] > 0.0:
            meanGenreVectorSum += vector[i]
            meanGenreVectorQuantity += 1

    if meanGenreVectorQuantity > 0:
        meanGenreVectorValue = meanGenreVectorSum / meanGenreVectorQuantity
    else:
        meanGenreVectorValue = 0
    unbiasedVectorMagnitude += meanGenreVectorValue * meanGenreVectorValue

    profileLanguageEndIndex = profileGenreEndIndex + allLanguagesLength
    meanLanguageVectorSum = 0.0
    meanLanguageVectorQuantity = 0
    for i in range(profileGenreEndIndex, profileLanguageEndIndex):
        if vector[i] > 0.0:
            meanLanguageVectorSum += vector[i]
            meanLanguageVectorQuantity += 1

    if meanLanguageVectorQuantity > 0:
        meanLanguageVectorValue = meanLanguageVectorSum / meanLanguageVectorQuantity
    else:
        meanLanguageVectorValue = 0
    unbiasedVectorMagnitude += meanLanguageVectorValue * meanLanguageVectorValue

    vectorCountryEndIndex = profileLanguageEndIndex + allCountriesLength
    meanCountryVectorSum = 0.0
    meanCountryVectorQuantity = 0
    for i in range(profileLanguageEndIndex, vectorCountryEndIndex):
        if vector[i] > 0.0:
            meanCountryVectorSum += vector[i]
            meanCountryVectorQuantity += 1

    if meanCountryVectorQuantity > 0:
        meanCountryVectorValue = meanCountryVectorSum / meanCountryVectorQuantity
    else:
        meanCountryVectorValue = 0
    unbiasedVectorMagnitude += meanCountryVectorValue * meanCountryVectorValue

    return np.sqrt(unbiasedVectorMagnitude)


def initGenreProfiles(userFilmDataIds, userFilmDataVectorized, cachedUserRatingScalars, cachedDateRatedScalars,
                      allGenres, profileVectorLength, allLanguagesLength, allCountriesLength,
                      numFilmsWatchedInGenreThreshold):
    genreProfiles = {}

    allGenresLength = len(allGenres)

    for genre in allGenres:
        genreProfiles[genre] = {"profile": np.zeros(profileVectorLength), "magnitude": 0.0, 
                                "weightedAverageSum": 0.0, "quantityFilmsWatched": 0}

    for imdbFilmId in userFilmDataIds:
        filmGenres = getFilmGenres(userFilmDataVectorized[imdbFilmId], allGenres)
        for genre in filmGenres:
            genreProfiles[genre]['profile'] += userFilmDataVectorized[imdbFilmId]
            genreProfiles[genre]['weightedAverageSum'] += (cachedUserRatingScalars[imdbFilmId] *
                                                           cachedDateRatedScalars[imdbFilmId])
            genreProfiles[genre]['quantityFilmsWatched'] += 1

    for genre in allGenres:
        if genreProfiles[genre]['weightedAverageSum'] == 0.0:
            continue
        
        genreProfiles[genre]['profile'] = np.divide(genreProfiles[genre]['profile'], 
                                                    genreProfiles[genre]['weightedAverageSum'])
        genreProfiles[genre]['profile'] *= min(1.0, genreProfiles[genre]['quantityFilmsWatched'] /
                                               numFilmsWatchedInGenreThreshold)
        genreProfiles[genre]['magnitude'] = calculateUnbiasedVectorMagnitude(genreProfiles[genre]['profile'],
                                                                             allGenresLength, allLanguagesLength,
                                                                             allCountriesLength)

    # TODO curve country and language vectors according to max value

    # return sorted (descending) list
    return sorted(genreProfiles.items(), key=lambda item: item[1]['magnitude'], reverse=True)


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


def initRecencyProfile(userFilmData, userFilmDataIds, userFilmDataVectorized, maxDateRated, profileVectorLength, 
                       cachedUserRatingScalars, cachedDateRatedScalars, allGenresLength, allCountries, 
                       allLanguages, allGenres):
    recencyProfile = np.zeros(profileVectorLength)
    weightedAverageSum = 0.0

    for imdbFilmId in userFilmDataIds:
        timeDifference = maxDateRated - userFilmData[imdbFilmId]['dateRated']
        if timeDifference.days <= RECENCY_PROFILE_DAYS_THRESHOLD:
            recencyProfile += userFilmDataVectorized[imdbFilmId]
            weightedAverageSum += (cachedUserRatingScalars[imdbFilmId] * cachedDateRatedScalars[imdbFilmId])
        else:
            # file is sorted by date, no need to look further
            break

    if weightedAverageSum > 0.0:
        recencyProfile = np.divide(recencyProfile, weightedAverageSum)
        # curve genres
        curveAccordingToMax(recencyProfile, allGenres, GENRE_WEIGHT, PROFILE_GENRE_START_INDEX)
        # curve languages
        languagesStartIndex = PROFILE_GENRE_START_INDEX + allGenresLength
        curveAccordingToMax(recencyProfile, allLanguages, LANGUAGE_WEIGHT, languagesStartIndex)
        # curve countries
        countriesStartIndex = languagesStartIndex + len(allLanguages)
        curveAccordingToMax(recencyProfile, allCountries, COUNTRY_WEIGHT, countriesStartIndex)
        return recencyProfile
    else:
        return np.zeros(profileVectorLength)
    
# used to curve country or languages vectors according to max value
def curveAccordingToMax(userProfile, list, weight, startIndex):
    userProfileGenreEndIndex = startIndex + len(list)
    minValue = userProfile[startIndex]
    maxValue = userProfile[startIndex]

    for i in range(startIndex, userProfileGenreEndIndex):
        minValue = min(minValue, userProfile[i])
        maxValue = max(maxValue, userProfile[i])

    diffValue = maxValue - minValue

    if diffValue == 0.0:
        print("Error. diffValue is 0.")
        raise ZeroDivisionError

    for i in range(startIndex, userProfileGenreEndIndex):
        userProfile[i] = (userProfile[i] - minValue) / diffValue
        userProfile[i] *= weight

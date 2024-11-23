import numpy as np
from init_all_film_data import YEAR_WEIGHT
RUNTIME_WEIGHT = 0.3
# from experimenting (yearNorm weight was fixed at 0.3), ~0.75 was a good sweet spot in the sense that
# it picked both single- and multi-genre films. The algorithm still heavily favoured the 4 genres that had the
# highest weighing, but this is expected and good behaviour.
GENRE_WEIGHT = 0.75
PROFILE_YEAR_INDEX = 0
PROFILE_IMDB_RATING_INDEX = 1
PROFILE_NUM_OF_VOTES_INDEX = 2
PROFILE_RUNTIME_INDEX = 3
PROFILE_GENRE_START_INDEX = 4


def vectorizeFilm(film, allGenres, allLanguages, allCountries, cachedNormalizedYears, cachedNormalizedImdbRatings,
                  minNumberOfVotes, diffNumberOfVotes, minRuntime, diffRuntime):
    vector = []

    normalizedYear = cachedNormalizedYears[film['year']]
    vector.append(normalizedYear)

    imdbRatingNorm = cachedNormalizedImdbRatings[str(film['imdbRating'])]
    vector.append(imdbRatingNorm)

    numberOfVotesNorm = (film['numberOfVotes'] - minNumberOfVotes) / diffNumberOfVotes
    vector.append(numberOfVotesNorm)

    runtimeNorm = ((film['runtime'] - minRuntime) / diffRuntime) * RUNTIME_WEIGHT
    vector.append(runtimeNorm)

    oneHotEncode(vector, film['genres'], allGenres)
    oneHotEncode(vector, film['languages'], allLanguages)
    oneHotEncode(vector, film['countries'], allCountries)

    return np.array(vector)


# used to one-hot encode genres, countries, languages
def oneHotEncode(vector, filmList, allList):
    for element in allList:
        if element in filmList:
            vector.append(1)
        else:
            vector.append(0)

    return vector


def cosineSimilarity(a, b, aMagnitude, bMagnitude):
    return np.dot(a, b) / (aMagnitude * bMagnitude)


# ensures that all vector features are >= 0.0 && <= 1.0
def keepVectorBoundary(vector, PROFILE_VECTOR_LENGTH):
    for i in range(0, PROFILE_VECTOR_LENGTH):
        if vector[i] < 0.0:
            vector[i] = 0.0
        elif vector[i] > 1.0:
            vector[i] = 1.0


# given a user profile vector, curve the genres
# for example, if drama is the highest rated genre with a score of 0.4, fix this as 1.0 and curve the other
# genre values relative to this max value.
# after the genres are normalised, I apply a weight of GENRE_WEIGHT to all genres.
def curveGenres(userProfile, allGenres):
    userProfileGenreEndIndex = PROFILE_GENRE_START_INDEX + len(allGenres)
    minGenreValue = userProfile[PROFILE_GENRE_START_INDEX]
    maxGenreValue = userProfile[PROFILE_GENRE_START_INDEX]

    for i in range(PROFILE_GENRE_START_INDEX, userProfileGenreEndIndex):
        minGenreValue = min(minGenreValue, userProfile[i])
        maxGenreValue = max(maxGenreValue, userProfile[i])

    print(f"min:{minGenreValue}, max:{maxGenreValue}")

    diffGenreValue = maxGenreValue - minGenreValue

    for i in range(PROFILE_GENRE_START_INDEX, userProfileGenreEndIndex):
        userProfile[i] = (userProfile[i] - minGenreValue) / diffGenreValue
        userProfile[i] *= GENRE_WEIGHT


def stringifyVector(vector, allGenres, allCountries, allLanguages):
    print(f"All values rounded to 3 decimal places\nYEAR_WEIGHT: {YEAR_WEIGHT}, RUNTIME_WEIGHT: {RUNTIME_WEIGHT}, "
          f"GENRE_WEIGHT: {GENRE_WEIGHT}")
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

    if meanGenreVectorQuantity != 0:
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

    if meanLanguageVectorQuantity != 0:
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

    if meanCountryVectorQuantity != 0:
        meanCountryVectorValue = meanCountryVectorSum / meanCountryVectorQuantity
    else:
        meanCountryVectorValue = 0
    unbiasedVectorMagnitude += meanCountryVectorValue * meanCountryVectorValue

    return np.sqrt(unbiasedVectorMagnitude)

import numpy as np
RUNTIME_WEIGHT = 0.3


def vectorizeFilm(film, allGenres, allLanguages, allCountries, cachedNormalizedYears, cachedNormalizedImdbRatings,
                  minNumberOfVotes, diffNumberOfVotes, minRuntime, diffRuntime):
    vector = []

    normalizedYear = cachedNormalizedYears[str(film['year'])]
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

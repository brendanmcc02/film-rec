import numpy as np
from app import GENRE_WEIGHT, RUNTIME_WEIGHT


def vectorizeFilm(film, allGenres, allLanguages, allCountries, cachedNormalizedYears, cachedNormalizedImdbRatings,
                  minNumberOfVotes, DIFF_NUMBER_OF_VOTES, minRuntime, DIFF_RUNTIME):
    vector = []

    normalizedYear = cachedNormalizedYears[film['year']]
    vector.append(normalizedYear)

    imdbRatingNorm = cachedNormalizedImdbRatings[str(film['imdbRating'])]
    vector.append(imdbRatingNorm)

    numberOfVotesNorm = (film['numberOfVotes'] - minNumberOfVotes) / DIFF_NUMBER_OF_VOTES
    vector.append(numberOfVotesNorm)

    runtimeNorm = ((film['runtime'] - minRuntime) / DIFF_RUNTIME) * RUNTIME_WEIGHT
    vector.append(runtimeNorm)

    oneHotEncode(vector, film['genres'], allGenres)
    oneHotEncode(vector, film['language'], allLanguages)
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


def cosineSimilarity(a, b, bMagnitude):
    return np.dot(a, b) / (np.linalg.norm(a) * bMagnitude)


# given a user profile vector, curve the genres
# for example, if drama is the highest rated genre with a score of 0.4, make the value = 1.0 and then scale
# the other genres relative to this max value (1.0 in this case).
# after the genres are normalised, I apply a weight of GENRE_WEIGHT to all genres.
def curveGenres(userProfile):
    # normalise the genres in the user profile
    MIN_GENRE_VALUE = userProfile[4]
    MAX_GENRE_VALUE = userProfile[4]

    for i in range(4, 27):
        MIN_GENRE_VALUE = min(MIN_GENRE_VALUE, userProfile[i])
        MAX_GENRE_VALUE = max(MAX_GENRE_VALUE, userProfile[i])

    DIFF_GENRE = MAX_GENRE_VALUE - MIN_GENRE_VALUE

    for i in range(4, 27):
        userProfile[i] = (userProfile[i] - MIN_GENRE_VALUE) / DIFF_GENRE  # normalise the genres
        userProfile[i] = userProfile[i] * GENRE_WEIGHT


# ensures that all vector features are >= 0.0 && <= 1.0
def keepVectorBoundary(vector, PROFILE_VECTOR_LENGTH):
    for i in range(0, PROFILE_VECTOR_LENGTH):
        if vector[i] < 0.0:
            vector[i] = 0.0
        elif vector[i] > 1.0:
            vector[i] = 1.0

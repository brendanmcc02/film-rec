import numpy as np
from init_all_film_data import YEAR_WEIGHT
RUNTIME_WEIGHT = 0.3
# from experimenting (yearNorm weight was fixed at 0.3), ~0.75 was a good sweet spot in the sense that
# it picked both single- and multi-genre films. The algorithm still heavily favoured the 4 genres that had the
# highest weighing, but this is expected and good behaviour.
GENRE_WEIGHT = 0.75


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


# given a user profile vector, curve the genres
# for example, if drama is the highest rated genre with a score of 0.4, fix this as 1.0 and curve the other
# genre values relative to this max value.
# after the genres are normalised, I apply a weight of GENRE_WEIGHT to all genres.
def curveGenres(userProfile, allGenres):
    userProfileGenreStartIndex = 4
    userProfileGenreEndIndex = userProfileGenreStartIndex + len(allGenres)
    minGenreValue = userProfile[userProfileGenreStartIndex]
    maxGenreValue = userProfile[userProfileGenreStartIndex]

    for i in range(userProfileGenreStartIndex, userProfileGenreEndIndex):
        minGenreValue = min(minGenreValue, userProfile[i])
        maxGenreValue = max(maxGenreValue, userProfile[i])

    print(f"min:{minGenreValue}, max:{maxGenreValue}")

    diffGenreValue = maxGenreValue - minGenreValue

    for i in range(userProfileGenreStartIndex, userProfileGenreEndIndex):
        userProfile[i] = (userProfile[i] - minGenreValue) / diffGenreValue
        userProfile[i] *= GENRE_WEIGHT


def stringifyVector(vector, allGenres, allCountries, allLanguages):
    print(f"All values rounded to 3 decimal places\nYEAR_WEIGHT: {YEAR_WEIGHT}, RUNTIME_WEIGHT: {RUNTIME_WEIGHT}, "
          f"GENRE_WEIGHT: {GENRE_WEIGHT}")
    stringifiedVector = (f"Year: {round(vector[0], 3)}\nIMDb Rating: {round(vector[1], 3)}\n"
                         f"NumOfVotes: {round(vector[2], 3)}\nRuntime: {round(vector[3], 3)}\n")

    i = 4
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

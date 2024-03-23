import json
import numpy as np


VECTOR_LENGTH = 27


def main():
    global VECTOR_LENGTH
    # read in all-film-data-vectorized.json & my-film-data-vectorized.json as dictionaries
    allFilmDataVecFile = open('../data/all-film-data-vectorized.json')
    allFilmDataVec = json.load(allFilmDataVecFile)
    myFilmDataVecFile = open('../data/my-film-data-vectorized.json')
    myFilmDataVec = json.load(myFilmDataVecFile)

    myFilmDataKeys = list(myFilmDataVec.keys())  # get list of keys of my-film-data-vectorized

    VECTOR_LENGTH = len(myFilmDataVec[myFilmDataKeys[0]])  # length of each vector

    # create user profile based on my-film-data-vectorized
    userProfileList = [0.0] * VECTOR_LENGTH  # initialise the list to have 0 in each entry
    userProfile = np.array(userProfileList)  # convert from list to vector
    for key in myFilmDataKeys:
        # sum the (already weighted) vectors together
        userProfile = userProfile + myFilmDataVec[key]

    # read in my-film-data.json
    myFilmDataFile = open('../data/my-film-data.json')
    myFilmData = json.load(myFilmDataFile)
    myFilmDataKeys = list(myFilmData.keys())
    # read in all-film-data.json
    allFilmDataFile = open('../data/all-film-data.json')
    allFilmData = json.load(allFilmDataFile)

    # calculate the weighted averages of the userProfile:

    # find the min & max myRating in my-film-data
    MIN_MY_RATING = myFilmData[myFilmDataKeys[0]]['myRating']
    MAX_MY_RATING = myFilmData[myFilmDataKeys[0]]['myRating']
    for key in myFilmDataKeys:
        MIN_MY_RATING = min(MIN_MY_RATING, myFilmData[key]['myRating'])
        MAX_MY_RATING = max(MAX_MY_RATING, myFilmData[key]['myRating'])

    # pre-compute the myRating differences for higher efficiency
    DIFF_MY_RATING = MAX_MY_RATING - MIN_MY_RATING

    # find the sum of the weighted averages
    weightedAverageSum = 0.0
    for key in myFilmDataKeys:
        myRating_norm = (myFilmData[key]['myRating'] - MIN_MY_RATING) / DIFF_MY_RATING
        # increment the weighted average
        weightedAverageSum = weightedAverageSum + myRating_norm

    # divide the userProfile vector by the weighted average
    userProfile = np.divide(userProfile, weightedAverageSum)

    normaliseGenres(userProfile)

    # fix imdbRating to 1.0, intuitively we want to recommend films that have higher imdbRatings, even if the
    # weighting says otherwise
    userProfile[1] = 1.0

    print("User Profile: \n" + str(userProfile))

    # dict: key = filmId, value = similarity to userProfile
    similarities = {}

    # get list of keys of my-film-data-vectorized
    allFilmDataKeys = list(allFilmDataVec.keys())
    # for each film in all-film-data-vectorized
    for filmId in allFilmDataKeys:
        # calculate similarity to userProfile
        similarities[filmId] = cosineSimilarity(allFilmDataVec[filmId], userProfile)

    # sort similarities in descending order.
    similarities = sorted(similarities.items(), key=lambda x: x[1], reverse=True)

    print("\nWe think you'll enjoy these 20 films:")
    for i in range(0, 20):
        filmId = similarities[i][0]
        film = allFilmData[filmId]
        similarity = similarities[i][1]
        vector = allFilmDataVec[filmId]
        print(stringifyFilm(film, similarity, vector))

    print("\n")


def stringifyFilm(film, similarity, vector):
    return (film['title'] + " (" + str(film['year']) + "). " + str(film['imdbRating']) + " Genres: " +
            str(film['genres']) + " (" + str(round(similarity * 100.0, 2)) + "% match)\n" + str(vector) + "\n")


# gets the cosine similarity between two vectors
def cosineSimilarity(A, B):
    return np.dot(A, B) / (np.linalg.norm(A) * np.linalg.norm(B))


def normaliseGenres(userProfile):
    # normalise the genres in the user profile
    MIN_GENRE_VALUE = userProfile[4]
    MAX_GENRE_VALUE = userProfile[4]

    for i in range(4, VECTOR_LENGTH):
        MIN_GENRE_VALUE = min(MIN_GENRE_VALUE, userProfile[i])
        MAX_GENRE_VALUE = max(MAX_GENRE_VALUE, userProfile[i])

    DIFF_GENRE = MAX_GENRE_VALUE - MIN_GENRE_VALUE

    for i in range(4, VECTOR_LENGTH):
        userProfile[i] = (userProfile[i] - MIN_GENRE_VALUE) / DIFF_GENRE  # normalise the genres
        # from experimenting (year_norm weight was fixed at 0.3), 0.68 was a good sweet spot in the sense that
        # it picked both single- and multi-genre films. The algorithm still heavily favoured the 4 genres that had the
        # highest weighing, but this is expected and good behaviour.
        userProfile[i] = userProfile[i] * 0.68


if __name__ == "__main__":
    main()

import json
import numpy as np


def main():
    # read in all-film-data-vectorized.json & my-film-data-vectorized.json as dictionaries
    allFilmDataVecFile = open('../data/all-film-data-vectorized.json')
    allFilmDataVec = json.load(allFilmDataVecFile)
    myFilmDataVecFile = open('../data/my-film-data-vectorized.json')
    myFilmDataVec = json.load(myFilmDataVecFile)

    # get list of keys of my-film-data-vectorized
    myFilmDataKeys = list(myFilmDataVec.keys())

    VECTOR_LENGTH = len(myFilmDataVec[myFilmDataKeys[0]])  # length of each vector

    # create user profile based on my-film-data-vectorized
    userProfileList = [0.0] * VECTOR_LENGTH  # initialise the list to have 0 in each entry
    userProfile = np.array(userProfileList)  # convert from list to vector
    for key in myFilmDataKeys:
        # sum the (already weighted) vectors together
        userProfile = userProfile + myFilmDataVec[key]

    # read in my-film-data.json as a dictionary
    myFilmDataFile = open('../data/my-film-data.json')
    myFilmData = json.load(myFilmDataFile)

    # calculate the weighted averages of the userProfile:

    # find the min & max myRating in my-film-data
    MIN_MY_RATING = myFilmData[0]['myRating']
    MAX_MY_RATING = myFilmData[0]['myRating']
    for film in myFilmData:
        MIN_MY_RATING = min(MIN_MY_RATING, film['myRating'])
        MAX_MY_RATING = max(MAX_MY_RATING, film['myRating'])

    # pre-compute the myRating differences for higher efficiency
    DIFF_MY_RATING = MAX_MY_RATING - MIN_MY_RATING

    # find the sum of the weighted averages
    weightedAverageSum = 0.0
    for film in myFilmData:
        myRating_norm = (film['myRating'] - MIN_MY_RATING) / DIFF_MY_RATING
        # increment the weighted average
        weightedAverageSum = weightedAverageSum + myRating_norm

    # divide the userProfile vector by the weighted average
    userProfile = np.divide(userProfile, weightedAverageSum)

    # dict: key = filmId, value = similarity to userProfile
    similarities = {}

    # get list of keys of my-film-data-vectorized
    allFilmDataKeys = list(allFilmDataVec.keys())
    # for each film in all-film-data-vectorized
    for filmId in allFilmDataKeys:
        # calculate similarity to userProfile
        similarities[filmId] = cosineSimilarity(allFilmDataVec[filmId], userProfile)

    # sort similarities in descending order
    similarities = sorted(similarities.items(), key=lambda x: x[1], reverse=True)

    print("We recommend these 25 films:")
    for i in range(0, 25):
        print(similarities[i][0])


# gets the cosine similarity between two vectors
def cosineSimilarity(A, B):
    return np.dot(A, B) / (np.linalg.norm(A) * np.linalg.norm(B))


if __name__ == "__main__":
    main()

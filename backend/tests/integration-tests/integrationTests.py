import os
import requests
import sys
absolutePathOfCurrentFile = os.path.dirname(os.path.abspath(__file__))
testRootDirectory = os.path.dirname(absolutePathOfCurrentFile)
backendRootDirectory = os.path.dirname(testRootDirectory)
sys.path.append(testRootDirectory)
sys.path.append(backendRootDirectory)
from ServiceUtilities import *
from TestUtilities import *

testUploadFilesDirectory = "test-upload-files/"

testUtilities = TestUtilities("../../../")

def test_getInitialRowsOfRecommendations_guidExists(backendUrl):
    filesToSend = testUtilities.getFilesToSend("imdb-no-recent-films.csv")
    
    getInitialRowsOfRecommendationsResponse = requests.post(backendUrl + "/getInitialRowsOfRecommendations", files=filesToSend)
    assert getInitialRowsOfRecommendationsResponse.status_code == 200

    getInitialRowsOfRecommendationsResponseContent = getInitialRowsOfRecommendationsResponse.json()
    assert 'guid' in getInitialRowsOfRecommendationsResponseContent

def test_regenerateRowsOfRecommendations_guidExists(backendUrl):
    filesToSend = testUtilities.getFilesToSend("imdb-no-recent-films.csv")
    
    getInitialRowsOfRecommendationsResponse = requests.post(backendUrl + "/getInitialRowsOfRecommendations", files=filesToSend)
    assert getInitialRowsOfRecommendationsResponse.status_code == 200

    getInitialRowsOfRecommendationsResponseContent = getInitialRowsOfRecommendationsResponse.json()
    guid = getInitialRowsOfRecommendationsResponseContent["guid"]

    regenerateRecommendationsResponse = requests.get(backendUrl + "/regenerateRecommendations?guid=" + guid)
    assert regenerateRecommendationsResponse.status_code == 200

    responseContent = regenerateRecommendationsResponse.json()
    assert 'guid' in responseContent

def test_getInitialRowsOfRecommendations_errorMessageExists(backendUrl):
    filesToSend = testUtilities.getFilesToSend("imdb-no-recent-films.csv")
    
    getInitialRowsOfRecommendationsResponse = requests.post(backendUrl + "/getInitialRowsOfRecommendations", files=filesToSend)
    assert getInitialRowsOfRecommendationsResponse.status_code == 200

    getInitialRowsOfRecommendationsResponseContent = getInitialRowsOfRecommendationsResponse.json()
    assert 'errorMessage' in getInitialRowsOfRecommendationsResponseContent

def test_regenerateRowsOfRecommendations_errorMessageExists(backendUrl):
    filesToSend = testUtilities.getFilesToSend("imdb-no-recent-films.csv")
    
    getInitialRowsOfRecommendationsResponse = requests.post(backendUrl + "/getInitialRowsOfRecommendations", files=filesToSend)
    assert getInitialRowsOfRecommendationsResponse.status_code == 200

    getInitialRowsOfRecommendationsResponseContent = getInitialRowsOfRecommendationsResponse.json()
    guid = getInitialRowsOfRecommendationsResponseContent["guid"]

    regenerateRecommendationsResponse = requests.get(backendUrl + "/regenerateRecommendations?guid=" + guid)
    assert regenerateRecommendationsResponse.status_code == 200

    responseContent = regenerateRecommendationsResponse.json()
    assert 'errorMessage' in responseContent

def test_getInitialRowsOfRecommendations_bodyExists(backendUrl):
    filesToSend = testUtilities.getFilesToSend("imdb-no-recent-films.csv")
    
    getInitialRowsOfRecommendationsResponse = requests.post(backendUrl + "/getInitialRowsOfRecommendations", files=filesToSend)
    assert getInitialRowsOfRecommendationsResponse.status_code == 200

    getInitialRowsOfRecommendationsResponseContent = getInitialRowsOfRecommendationsResponse.json()
    assert 'body' in getInitialRowsOfRecommendationsResponseContent

def test_regenerateRowsOfRecommendations_bodyExists(backendUrl):
    filesToSend = testUtilities.getFilesToSend("imdb-no-recent-films.csv")
    
    getInitialRowsOfRecommendationsResponse = requests.post(backendUrl + "/getInitialRowsOfRecommendations", files=filesToSend)
    assert getInitialRowsOfRecommendationsResponse.status_code == 200

    getInitialRowsOfRecommendationsResponseContent = getInitialRowsOfRecommendationsResponse.json()
    guid = getInitialRowsOfRecommendationsResponseContent["guid"]

    regenerateRecommendationsResponse = requests.get(backendUrl + "/regenerateRecommendations?guid=" + guid)
    assert regenerateRecommendationsResponse.status_code == 200

    regenerateRecommendationsResponseContent = regenerateRecommendationsResponse.json()
    assert 'body' in regenerateRecommendationsResponseContent

def test_getInitialRowsOfRecommendations_noFile(backendUrl):
    filesToSend = {'file': ("", None)}
    response = requests.post(backendUrl + "/getInitialRowsOfRecommendations", files=filesToSend)

    assert response.status_code == 400
    responseContent = response.json()
    assert responseContent["errorMessage"] == ServiceUtilities.NO_FILE_IN_REQUEST_ERROR_MESSAGE

def test_getInitialRowsOfRecommendations_unacceptedFileType(backendUrl):
    filesToSend = testUtilities.getFilesToSend("test.txt")
    response = requests.post(backendUrl + "/getInitialRowsOfRecommendations", files=filesToSend)

    assert response.status_code == 415
    responseContent = response.json()
    assert responseContent["errorMessage"] == ServiceUtilities.UNSUPPORTED_MEDIA_TYPE_ERROR_MESSAGE

def test_getInitialRowsOfRecommendations_imdbIncorrectHeader(backendUrl):
    filesToSend = testUtilities.getFilesToSend("imdb-incorrect-header.csv")
    response = requests.post(backendUrl + "/getInitialRowsOfRecommendations", files=filesToSend)

    assert response.status_code == 400
    responseContent = response.json()
    assert responseContent["errorMessage"] == ServiceUtilities.FILE_ROW_HEADERS_UNEXPECTED_FORMAT_ERROR_MESSAGE

def test_getInitialRowsOfRecommendations_imdbMissingHeader(backendUrl):
    filesToSend = testUtilities.getFilesToSend("imdb-missing-header.csv")
    response = requests.post(backendUrl + "/getInitialRowsOfRecommendations", files=filesToSend)

    assert response.status_code == 400
    responseContent = response.json()
    assert responseContent["errorMessage"] == ServiceUtilities.FILE_MORE_DATA_THAN_ROW_HEADERS_ERROR_MESSAGE

def test_getInitialRowsOfRecommendations_letterboxdIncorrectHeaderCsv(backendUrl):
    filesToSend = testUtilities.getFilesToSend("letterboxd-incorrect-header.csv")
    response = requests.post(backendUrl + "/getInitialRowsOfRecommendations", files=filesToSend)

    assert response.status_code == 400
    responseContent = response.json()
    assert responseContent["errorMessage"] == ServiceUtilities.FILE_ROW_HEADERS_UNEXPECTED_FORMAT_ERROR_MESSAGE

def test_getInitialRowsOfRecommendations_letterboxdMissingHeaderCsv(backendUrl):
    filesToSend = testUtilities.getFilesToSend("letterboxd-missing-header.csv")
    response = requests.post(backendUrl + "/getInitialRowsOfRecommendations", files=filesToSend)

    assert response.status_code == 400
    responseContent = response.json()
    assert responseContent["errorMessage"] == ServiceUtilities.FILE_MORE_DATA_THAN_ROW_HEADERS_ERROR_MESSAGE

def test_getInitialRowsOfRecommendations_letterboxdIncorrectZip(backendUrl):
    filesToSend = testUtilities.getFilesToSend("letterboxd-incorrect.zip")
    
    response = requests.post(backendUrl + "/getInitialRowsOfRecommendations", files=filesToSend)

    assert response.status_code == 400
    responseContent = response.json()
    assert responseContent["errorMessage"] == ServiceUtilities.INVALID_ZIP_FILE_ERROR_MESSAGE

def test_getInitialRowsOfRecommendations_imdbNoRecentFilms(backendUrl):
    filesToSend = testUtilities.getFilesToSend("imdb-no-recent-films.csv")
    
    getInitialRowsOfRecommendationsResponse = requests.post(backendUrl + "/getInitialRowsOfRecommendations", files=filesToSend)
    assert getInitialRowsOfRecommendationsResponse.status_code == 200

    ## wrap this in a function?
    responseContent = getInitialRowsOfRecommendationsResponse.json()
    rowsOfRecommendations = responseContent["body"]

    numberOfFavouriteRows = 1
    numberOfRecentRows = 0
    numberOfGenreRows = ServiceUtilities.NUMBER_OF_GENRE_RECOMMENDATION_ROWS
    numberOfInternationalRows = 1
    numberOfOldRows = 1
    totalNumberOfRows = (numberOfFavouriteRows + numberOfRecentRows + numberOfGenreRows + 
                         numberOfInternationalRows + numberOfOldRows)
    
    testUtilities.verifyRowsOfRecommendations(rowsOfRecommendations, totalNumberOfRows)

    for row in rowsOfRecommendations:
        assert row['profileId'] != "recency"

def test_getInitialRowsOfRecommendations_letterboxdNoRecentFilms(backendUrl):
    filesToSend = testUtilities.getFilesToSend("letterboxd-no-recent-films.csv")
    
    getInitialRowsOfRecommendationsResponse = requests.post(backendUrl + "/getInitialRowsOfRecommendations", files=filesToSend)
    assert getInitialRowsOfRecommendationsResponse.status_code == 200

    responseContent = getInitialRowsOfRecommendationsResponse.json()
    rowsOfRecommendations = responseContent["body"]

    numberOfFavouriteRows = 1
    numberOfRecentRows = 0
    numberOfGenreRows = ServiceUtilities.NUMBER_OF_GENRE_RECOMMENDATION_ROWS
    numberOfInternationalRows = 1
    numberOfOldRows = 1
    totalNumberOfRows = (numberOfFavouriteRows + numberOfRecentRows + numberOfGenreRows + 
                         numberOfInternationalRows + numberOfOldRows)
    
    testUtilities.verifyRowsOfRecommendations(rowsOfRecommendations, totalNumberOfRows)

    for row in rowsOfRecommendations:
        assert row['profileId'] != "recency"

def test_getInitialRowsOfRecommendations_imdbNoRecentAndFavouriteFilms(backendUrl):
    filesToSend = testUtilities.getFilesToSend("imdb-no-recent-and-favourite-films.csv")
    
    getInitialRowsOfRecommendationsResponse = requests.post(backendUrl + "/getInitialRowsOfRecommendations", files=filesToSend)
    assert getInitialRowsOfRecommendationsResponse.status_code == 200

    responseContent = getInitialRowsOfRecommendationsResponse.json()
    rowsOfRecommendations = responseContent["body"]

    numberOfFavouriteRows = 0
    numberOfRecentRows = 0
    numberOfGenreRows = ServiceUtilities.NUMBER_OF_GENRE_RECOMMENDATION_ROWS
    numberOfInternationalRows = 1
    numberOfOldRows = 1
    totalNumberOfRows = (numberOfFavouriteRows + numberOfRecentRows + numberOfGenreRows + 
                         numberOfInternationalRows + numberOfOldRows)
    
    testUtilities.verifyRowsOfRecommendations(rowsOfRecommendations, totalNumberOfRows)

    for row in rowsOfRecommendations:
        assert row['profileId'] != "recency"
        assert row['profileId'] != "favourite"

def test_getInitialRowsOfRecommendations_letterboxdNoRecentAndFavouriteFilms(backendUrl):
    filesToSend = testUtilities.getFilesToSend("letterboxd-no-recent-and-favourite-films.csv")
    
    getInitialRowsOfRecommendationsResponse = requests.post(backendUrl + "/getInitialRowsOfRecommendations", files=filesToSend)
    assert getInitialRowsOfRecommendationsResponse.status_code == 200

    responseContent = getInitialRowsOfRecommendationsResponse.json()
    rowsOfRecommendations = responseContent["body"]

    numberOfFavouriteRows = 0
    numberOfRecentRows = 0
    numberOfGenreRows = ServiceUtilities.NUMBER_OF_GENRE_RECOMMENDATION_ROWS
    numberOfInternationalRows = 1
    numberOfOldRows = 1
    totalNumberOfRows = (numberOfFavouriteRows + numberOfRecentRows + numberOfGenreRows + 
                         numberOfInternationalRows + numberOfOldRows)
    
    testUtilities.verifyRowsOfRecommendations(rowsOfRecommendations, totalNumberOfRows)

    for row in rowsOfRecommendations:
        assert row['profileId'] != "recency"
        assert row['profileId'] != "favourite"

def test_getInitialRowsOfRecommendations_imdbNoRecentAndInternationalFilms(backendUrl):
    filesToSend = testUtilities.getFilesToSend("imdb-no-recent-and-international-films.csv")
    
    getInitialRowsOfRecommendationsResponse = requests.post(backendUrl + "/getInitialRowsOfRecommendations", files=filesToSend)
    assert getInitialRowsOfRecommendationsResponse.status_code == 200

    responseContent = getInitialRowsOfRecommendationsResponse.json()
    rowsOfRecommendations = responseContent["body"]

    numberOfFavouriteRows = 1
    numberOfRecentRows = 0
    numberOfGenreRows = ServiceUtilities.NUMBER_OF_GENRE_RECOMMENDATION_ROWS
    numberOfInternationalRows = 0
    numberOfOldRows = 1
    totalNumberOfRows = (numberOfFavouriteRows + numberOfRecentRows + numberOfGenreRows + 
                         numberOfInternationalRows + numberOfOldRows)
    
    testUtilities.verifyRowsOfRecommendations(rowsOfRecommendations, totalNumberOfRows)

    for row in rowsOfRecommendations:
        assert row['profileId'] != "recency"
        assert row['profileId'] != "international"

def test_getInitialRowsOfRecommendations_letterboxdNoRecentAndInternationalFilms(backendUrl):
    filesToSend = testUtilities.getFilesToSend("letterboxd-no-recent-and-international-films.csv")
    
    getInitialRowsOfRecommendationsResponse = requests.post(backendUrl + "/getInitialRowsOfRecommendations", files=filesToSend)
    assert getInitialRowsOfRecommendationsResponse.status_code == 200

    responseContent = getInitialRowsOfRecommendationsResponse.json()
    rowsOfRecommendations = responseContent["body"]

    numberOfFavouriteRows = 1
    numberOfRecentRows = 0
    numberOfGenreRows = ServiceUtilities.NUMBER_OF_GENRE_RECOMMENDATION_ROWS
    numberOfInternationalRows = 0
    numberOfOldRows = 1
    totalNumberOfRows = (numberOfFavouriteRows + numberOfRecentRows + numberOfGenreRows + 
                         numberOfInternationalRows + numberOfOldRows)
    
    testUtilities.verifyRowsOfRecommendations(rowsOfRecommendations, totalNumberOfRows)

    for row in rowsOfRecommendations:
        assert row['profileId'] != "recency"
        assert row['profileId'] != "international"

# tests for cases when the user has rated films with only two genres
def test_getInitialRowsOfRecommendations_imdbNoRecentAndTwoGenres_ensuresTwoGenreRows(backendUrl):
    filesToSend = testUtilities.getFilesToSend("imdb-no-recent-films-and-two-genres.csv")
    
    getInitialRowsOfRecommendationsResponse = requests.post(backendUrl + "/getInitialRowsOfRecommendations", files=filesToSend)
    assert getInitialRowsOfRecommendationsResponse.status_code == 200

    responseContent = getInitialRowsOfRecommendationsResponse.json()
    rowsOfRecommendations = responseContent["body"]

    numberOfFavouriteRows = 1
    numberOfRecentRows = 0
    numberOfGenreRows = 2
    numberOfInternationalRows = 1
    numberOfOldRows = 1
    totalNumberOfRows = (numberOfFavouriteRows + numberOfRecentRows + numberOfGenreRows + 
                         numberOfInternationalRows + numberOfOldRows)
    
    testUtilities.verifyRowsOfRecommendations(rowsOfRecommendations, totalNumberOfRows)

    for row in rowsOfRecommendations:
        assert row['profileId'] != "recency"

# tests for cases when the user has rated films with only two genres
def test_getInitialRowsOfRecommendations_letterboxdNoRecentAndTwoGenres_ensuresTwoGenreRows(backendUrl):
    filesToSend = testUtilities.getFilesToSend("letterboxd-no-recent-films-and-two-genres.csv")
    
    getInitialRowsOfRecommendationsResponse = requests.post(backendUrl + "/getInitialRowsOfRecommendations", files=filesToSend)
    assert getInitialRowsOfRecommendationsResponse.status_code == 200

    responseContent = getInitialRowsOfRecommendationsResponse.json()
    rowsOfRecommendations = responseContent["body"]

    numberOfFavouriteRows = 1
    numberOfRecentRows = 0
    numberOfGenreRows = 2
    numberOfInternationalRows = 1
    numberOfOldRows = 1
    totalNumberOfRows = (numberOfFavouriteRows + numberOfRecentRows + numberOfGenreRows + 
                         numberOfInternationalRows + numberOfOldRows)
    
    testUtilities.verifyRowsOfRecommendations(rowsOfRecommendations, totalNumberOfRows)

    for row in rowsOfRecommendations:
        assert row['profileId'] != "recency"

# tests for cases when the user has rated films with only one genre
def test_getInitialRowsOfRecommendations_imdbInternationalFilmAndNoRecentFilmsAndOneGenres_ensuresOneGenreRows(backendUrl):
    filesToSend = testUtilities.getFilesToSend("imdb-international-film-no-recent-films-and-one-genre.csv")
    
    getInitialRowsOfRecommendationsResponse = requests.post(backendUrl + "/getInitialRowsOfRecommendations", files=filesToSend)
    assert getInitialRowsOfRecommendationsResponse.status_code == 200

    responseContent = getInitialRowsOfRecommendationsResponse.json()
    rowsOfRecommendations = responseContent["body"]

    numberOfFavouriteRows = 1
    numberOfRecentRows = 0
    numberOfGenreRows = 1
    numberOfInternationalRows = 1
    numberOfOldRows = 1
    totalNumberOfRows = (numberOfFavouriteRows + numberOfRecentRows + numberOfGenreRows + 
                         numberOfInternationalRows + numberOfOldRows)
    
    testUtilities.verifyRowsOfRecommendations(rowsOfRecommendations, totalNumberOfRows)

    for row in rowsOfRecommendations:
        assert row['profileId'] != "recency"

# tests for cases when the user has rated films with only one genre
def test_getInitialRowsOfRecommendations_letterboxdInternationalFilmAndNoRecentFilmsAndOneGenres_ensuresOneGenreRows(backendUrl):
    filesToSend = testUtilities.getFilesToSend("letterboxd-international-film-no-recent-films-and-one-genre.csv")
    
    getInitialRowsOfRecommendationsResponse = requests.post(backendUrl + "/getInitialRowsOfRecommendations", files=filesToSend)
    assert getInitialRowsOfRecommendationsResponse.status_code == 200

    responseContent = getInitialRowsOfRecommendationsResponse.json()
    rowsOfRecommendations = responseContent["body"]

    numberOfFavouriteRows = 1
    numberOfRecentRows = 0
    numberOfGenreRows = 1
    numberOfInternationalRows = 1
    numberOfOldRows = 1
    totalNumberOfRows = (numberOfFavouriteRows + numberOfRecentRows + numberOfGenreRows + 
                         numberOfInternationalRows + numberOfOldRows)
    
    testUtilities.verifyRowsOfRecommendations(rowsOfRecommendations, totalNumberOfRows)

    for row in rowsOfRecommendations:
        assert row['profileId'] != "recency"

# tests for cases when the user has rated films with only one genre
def test_getInitialRowsOfRecommendations_imdbNoInternationalFilmsAndNoRecentFilmsAndOneGenres_ensuresOneGenreRows(backendUrl):
    filesToSend = testUtilities.getFilesToSend("imdb-american-film-no-recent-films-and-one-genre.csv")
    
    getInitialRowsOfRecommendationsResponse = requests.post(backendUrl + "/getInitialRowsOfRecommendations", files=filesToSend)
    assert getInitialRowsOfRecommendationsResponse.status_code == 200

    responseContent = getInitialRowsOfRecommendationsResponse.json()
    rowsOfRecommendations = responseContent["body"]

    numberOfFavouriteRows = 1
    numberOfRecentRows = 0
    numberOfGenreRows = 1
    numberOfInternationalRows = 0
    numberOfOldRows = 1
    totalNumberOfRows = (numberOfFavouriteRows + numberOfRecentRows + numberOfGenreRows + 
                         numberOfInternationalRows + numberOfOldRows)
    
    testUtilities.verifyRowsOfRecommendations(rowsOfRecommendations, totalNumberOfRows)

    for row in rowsOfRecommendations:
        assert row['profileId'] != "recency"
        assert row['profileId'] != "international"

# tests for cases when the user has rated films with only one genre
def test_getInitialRowsOfRecommendations_letterboxdNoInternationalFilmsAndNoRecentFilmsAndOneGenres_ensuresOneGenreRows(backendUrl):
    filesToSend = testUtilities.getFilesToSend("letterboxd-american-film-no-recent-films-and-one-genre.csv")
    
    getInitialRowsOfRecommendationsResponse = requests.post(backendUrl + "/getInitialRowsOfRecommendations", files=filesToSend)
    assert getInitialRowsOfRecommendationsResponse.status_code == 200

    responseContent = getInitialRowsOfRecommendationsResponse.json()
    rowsOfRecommendations = responseContent["body"]

    numberOfFavouriteRows = 1
    numberOfRecentRows = 0
    numberOfGenreRows = 1
    numberOfInternationalRows = 0
    numberOfOldRows = 1
    totalNumberOfRows = (numberOfFavouriteRows + numberOfRecentRows + numberOfGenreRows + 
                         numberOfInternationalRows + numberOfOldRows)
    
    testUtilities.verifyRowsOfRecommendations(rowsOfRecommendations, totalNumberOfRows)

    for row in rowsOfRecommendations:
        assert row['profileId'] != "recency"
        assert row['profileId'] != "international"

def test_getInitialRowsOfRecommendations_letterboxdZipNoRecentFilms(backendUrl):
    filesToSend = testUtilities.getFilesToSend("letterboxd-no-recent.zip")
    
    getInitialRowsOfRecommendationsResponse = requests.post(backendUrl + "/getInitialRowsOfRecommendations", files=filesToSend)
    assert getInitialRowsOfRecommendationsResponse.status_code == 200

    responseContent = getInitialRowsOfRecommendationsResponse.json()
    rowsOfRecommendations = responseContent["body"]

    numberOfFavouriteRows = 1
    numberOfRecentRows = 0
    numberOfGenreRows = ServiceUtilities.NUMBER_OF_GENRE_RECOMMENDATION_ROWS
    numberOfInternationalRows = 1
    numberOfOldRows = 1
    totalNumberOfRows = (numberOfFavouriteRows + numberOfRecentRows + numberOfGenreRows + 
                         numberOfInternationalRows + numberOfOldRows)
    
    testUtilities.verifyRowsOfRecommendations(rowsOfRecommendations, totalNumberOfRows)

    for row in rowsOfRecommendations:
        assert row['profileId'] != "recency"

def test_getInitialRowsOfRecommendations_imdbNoRecognisedFilms(backendUrl):
    filesToSend = testUtilities.getFilesToSend("imdb-no-recognised-films.csv")
    
    getInitialRowsOfRecommendationsResponse = requests.post(backendUrl + "/getInitialRowsOfRecommendations", files=filesToSend)
    assert getInitialRowsOfRecommendationsResponse.status_code == 200

    responseContent = getInitialRowsOfRecommendationsResponse.json()
    rowsOfRecommendations = responseContent["body"]

    numberOfFavouriteRows = 0
    numberOfRecentRows = 0
    numberOfGenreRows = 0
    numberOfInternationalRows = 0
    numberOfOldRows = 0
    totalNumberOfRows = (numberOfFavouriteRows + numberOfRecentRows + numberOfGenreRows + 
                         numberOfInternationalRows + numberOfOldRows)
    
    testUtilities.verifyRowsOfRecommendations(rowsOfRecommendations, totalNumberOfRows)

def test_getInitialRowsOfRecommendations_letterboxdNoRecognisedFilms(backendUrl):
    filesToSend = testUtilities.getFilesToSend("letterboxd-no-recognised-films.csv")

    getInitialRowsOfRecommendationsResponse = requests.post(backendUrl + "/getInitialRowsOfRecommendations", files=filesToSend)
    assert getInitialRowsOfRecommendationsResponse.status_code == 200

    responseContent = getInitialRowsOfRecommendationsResponse.json()
    rowsOfRecommendations = responseContent["body"]

    numberOfFavouriteRows = 0
    numberOfRecentRows = 0
    numberOfGenreRows = 0
    numberOfInternationalRows = 0
    numberOfOldRows = 0
    totalNumberOfRows = (numberOfFavouriteRows + numberOfRecentRows + numberOfGenreRows + 
                         numberOfInternationalRows + numberOfOldRows)
    
    testUtilities.verifyRowsOfRecommendations(rowsOfRecommendations, totalNumberOfRows)

def test_regenerateRowsOfRecommendations_imdb(backendUrl):
    filesToSend = testUtilities.getFilesToSend("imdb-no-recent-films.csv")
    
    getInitialRowsOfRecommendationsResponse = requests.post(backendUrl + "/getInitialRowsOfRecommendations", files=filesToSend)
    assert getInitialRowsOfRecommendationsResponse.status_code == 200

    getInitialRowsOfRecommendationsResponseContent = getInitialRowsOfRecommendationsResponse.json()
    guid = getInitialRowsOfRecommendationsResponseContent["guid"]

    regenerateRecommendationsResponse = requests.get(backendUrl + "/regenerateRecommendations?guid=" + guid)
    assert regenerateRecommendationsResponse.status_code == 200

    # verify the newly recommended films are valid
    # TODO move this to a method to make more readable?
    numberOfFavouriteRows = 1
    numberOfRecentRows = 0
    numberOfGenreRows = ServiceUtilities.NUMBER_OF_GENRE_RECOMMENDATION_ROWS
    numberOfInternationalRows = 1
    numberOfOldRows = 1
    totalNumberOfRows = (numberOfFavouriteRows + numberOfRecentRows + numberOfGenreRows + 
                         numberOfInternationalRows + numberOfOldRows)
    
    responseContent = regenerateRecommendationsResponse.json()
    regeneratedRecommendations = responseContent["body"]
    testUtilities.verifyRowsOfRecommendations(regeneratedRecommendations, totalNumberOfRows)

    # ensure all newly recommended films are unique
    # TODO move this to a method to make more readable?
    initialRecommendationFilmIds = []
    getInitialRowsOfRecommendationsResponseContent = getInitialRowsOfRecommendationsResponse.json()
    initialRecommendations = getInitialRowsOfRecommendationsResponseContent["body"]
    for row in initialRecommendations:
        for film in row['recommendedFilms']:
            initialRecommendationFilmIds.append(film['id'])

    for row in regeneratedRecommendations:
        for film in row['recommendedFilms']:
            assert film['id'] not in initialRecommendationFilmIds

def test_regenerateRowsOfRecommendations_letterboxd(backendUrl):
    filesToSend = testUtilities.getFilesToSend("letterboxd-no-recent-films.csv")
    
    getInitialRowsOfRecommendationsResponse = requests.post(backendUrl + "/getInitialRowsOfRecommendations", files=filesToSend)
    assert getInitialRowsOfRecommendationsResponse.status_code == 200

    getInitialRowsOfRecommendationsResponseContent = getInitialRowsOfRecommendationsResponse.json()
    guid = getInitialRowsOfRecommendationsResponseContent["guid"]

    regenerateRecommendationsResponse = requests.get(backendUrl + "/regenerateRecommendations?guid=" + guid)
    assert regenerateRecommendationsResponse.status_code == 200

    # verify the newly recommended films are valid
    numberOfFavouriteRows = 1
    numberOfRecentRows = 0
    numberOfGenreRows = ServiceUtilities.NUMBER_OF_GENRE_RECOMMENDATION_ROWS
    numberOfInternationalRows = 1
    numberOfOldRows = 1
    totalNumberOfRows = (numberOfFavouriteRows + numberOfRecentRows + numberOfGenreRows + 
                         numberOfInternationalRows + numberOfOldRows)
    
    responseContent = regenerateRecommendationsResponse.json()
    regeneratedRecommendations = responseContent["body"]
    testUtilities.verifyRowsOfRecommendations(regeneratedRecommendations, totalNumberOfRows)

    # ensure all newly recommended films are unique
    # TODO move this to a method to make more readable?
    initialRecommendationFilmIds = []
    getInitialRowsOfRecommendationsResponseContent = getInitialRowsOfRecommendationsResponse.json()
    initialRecommendations = getInitialRowsOfRecommendationsResponseContent["body"]
    for row in initialRecommendations:
        for film in row['recommendedFilms']:
            initialRecommendationFilmIds.append(film['id'])

    for row in regeneratedRecommendations:
        for film in row['recommendedFilms']:
            assert film['id'] not in initialRecommendationFilmIds

def test_getInitialRowsOfRecommendations_successfulResponse_shouldHaveEmptyErrorMessage(backendUrl):
    filesToSend = testUtilities.getFilesToSend("letterboxd-no-recent-films.csv")

    getInitialRowsOfRecommendationsResponse = requests.post(backendUrl + "/getInitialRowsOfRecommendations", files=filesToSend)
    assert getInitialRowsOfRecommendationsResponse.status_code == 200

    getInitialRowsOfRecommendationsResponseContent = getInitialRowsOfRecommendationsResponse.json()

    assert getInitialRowsOfRecommendationsResponseContent["errorMessage"] == ""

def test_regenerateRecommendations_successfulResponse_shouldHaveEmptyErrorMessage(backendUrl):
    filesToSend = testUtilities.getFilesToSend("letterboxd-no-recent-films.csv")

    getInitialRowsOfRecommendationsResponse = requests.post(backendUrl + "/getInitialRowsOfRecommendations", files=filesToSend)
    assert getInitialRowsOfRecommendationsResponse.status_code == 200

    getInitialRowsOfRecommendationsResponseContent = getInitialRowsOfRecommendationsResponse.json()
    guid = getInitialRowsOfRecommendationsResponseContent["guid"]

    regenerateRecommendationsResponse = requests.get(backendUrl + "/regenerateRecommendations?guid=" + guid)
    assert regenerateRecommendationsResponse.status_code == 200

    regenerateRecommendationsResponseContent = regenerateRecommendationsResponse.json()

    assert regenerateRecommendationsResponseContent["errorMessage"] == ""

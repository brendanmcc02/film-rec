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

def test_getInitialRowsOfRecommendations_guidExists(backendUrl):
    fileName = "imdb-no-recent-films.csv"
    file = open(testUploadFilesDirectory + fileName)
    filesToSend = {'file': (fileName, file)}
    
    response = requests.post(backendUrl + "/getInitialRowsOfRecommendations", files=filesToSend)
    assert response.status_code == 200

    responseContent = response.json()
    assert 'guid' in responseContent

def test_regenerateRowsOfRecommendations_guidExists(backendUrl):
    fileName = "imdb-no-recent-films.csv"
    file = open(testUploadFilesDirectory + fileName)
    filesToSend = {'file': (fileName, file)}
    
    getInitialRowsOfRecommendationsResponse = requests.post(backendUrl + "/getInitialRowsOfRecommendations", files=filesToSend)
    assert getInitialRowsOfRecommendationsResponse.status_code == 200

    getInitialRowsOfRecommendationsResponseContent = getInitialRowsOfRecommendationsResponse.json()
    guid = getInitialRowsOfRecommendationsResponseContent["guid"]

    regenerateRecommendationsResponse = requests.get(backendUrl + "/regenerateRecommendations?guid=" + guid)
    assert regenerateRecommendationsResponse.status_code == 200

    responseContent = regenerateRecommendationsResponse.json()
    assert 'guid' in responseContent

def test_getInitialRowsOfRecommendations_errorMessageExists(backendUrl):
    fileName = "imdb-no-recent-films.csv"
    file = open(testUploadFilesDirectory + fileName)
    filesToSend = {'file': (fileName, file)}
    
    response = requests.post(backendUrl + "/getInitialRowsOfRecommendations", files=filesToSend)
    assert response.status_code == 200
    # todo for 200 codes assert empty errorMessage

    responseContent = response.json()
    assert 'errorMessage' in responseContent

def test_regenerateRowsOfRecommendations_errorMessageExists(backendUrl):
    fileName = "imdb-no-recent-films.csv"
    file = open(testUploadFilesDirectory + fileName)
    filesToSend = {'file': (fileName, file)}
    
    getInitialRowsOfRecommendationsResponse = requests.post(backendUrl + "/getInitialRowsOfRecommendations", files=filesToSend)
    assert getInitialRowsOfRecommendationsResponse.status_code == 200

    getInitialRowsOfRecommendationsResponseContent = getInitialRowsOfRecommendationsResponse.json()
    guid = getInitialRowsOfRecommendationsResponseContent["guid"]

    regenerateRecommendationsResponse = requests.get(backendUrl + "/regenerateRecommendations?guid=" + guid)
    assert regenerateRecommendationsResponse.status_code == 200

    responseContent = regenerateRecommendationsResponse.json()
    assert 'errorMessage' in responseContent

def test_getInitialRowsOfRecommendations_bodyExists(backendUrl):
    fileName = "imdb-no-recent-films.csv"
    file = open(testUploadFilesDirectory + fileName)
    filesToSend = {'file': (fileName, file)}
    
    response = requests.post(backendUrl + "/getInitialRowsOfRecommendations", files=filesToSend)
    assert response.status_code == 200

    responseContent = response.json()
    assert 'body' in responseContent

def test_regenerateRowsOfRecommendations_bodyExists(backendUrl):
    fileName = "imdb-no-recent-films.csv"
    file = open(testUploadFilesDirectory + fileName)
    filesToSend = {'file': (fileName, file)}
    
    getInitialRowsOfRecommendationsResponse = requests.post(backendUrl + "/getInitialRowsOfRecommendations", files=filesToSend)
    assert getInitialRowsOfRecommendationsResponse.status_code == 200

    getInitialRowsOfRecommendationsResponseContent = getInitialRowsOfRecommendationsResponse.json()
    guid = getInitialRowsOfRecommendationsResponseContent["guid"]

    regenerateRecommendationsResponse = requests.get(backendUrl + "/regenerateRecommendations?guid=" + guid)
    assert regenerateRecommendationsResponse.status_code == 200

    responseContent = regenerateRecommendationsResponse.json()
    assert 'body' in responseContent

def test_getInitialRowsOfRecommendations_noFile(backendUrl):
    filesToSend = {'file': ("", None)}
    response = requests.post(backendUrl + "/getInitialRowsOfRecommendations", files=filesToSend)

    assert response.status_code == 400
    responseContent = response.json()
    assert responseContent["errorMessage"] == ServiceUtilities.NO_FILE_IN_REQUEST_ERROR_MESSAGE

def test_getInitialRowsOfRecommendations_unacceptedFileType(backendUrl):
    fileName = "test.txt"
    file = open(testUploadFilesDirectory + fileName)
    filesToSend = {'file': (fileName, file)}
    response = requests.post(backendUrl + "/getInitialRowsOfRecommendations", files=filesToSend)

    assert response.status_code == 415
    responseContent = response.json()
    assert responseContent["errorMessage"] == ServiceUtilities.UNSUPPORTED_MEDIA_TYPE_ERROR_MESSAGE

def test_getInitialRowsOfRecommendations_imdbIncorrectHeader(backendUrl):
    fileName = "imdb-incorrect-header.csv"
    file = open(testUploadFilesDirectory + fileName)
    filesToSend = {'file': (fileName, file)}
    response = requests.post(backendUrl + "/getInitialRowsOfRecommendations", files=filesToSend)

    assert response.status_code == 400
    responseContent = response.json()
    assert responseContent["errorMessage"] == ServiceUtilities.FILE_ROW_HEADERS_UNEXPECTED_FORMAT_ERROR_MESSAGE

def test_getInitialRowsOfRecommendations_imdbMissingHeader(backendUrl):
    fileName = "imdb-missing-header.csv"
    file = open(testUploadFilesDirectory + fileName)
    filesToSend = {'file': (fileName, file)}
    response = requests.post(backendUrl + "/getInitialRowsOfRecommendations", files=filesToSend)

    assert response.status_code == 400
    responseContent = response.json()
    assert responseContent["errorMessage"] == ServiceUtilities.FILE_MORE_DATA_THAN_ROW_HEADERS_ERROR_MESSAGE

def test_getInitialRowsOfRecommendations_letterboxdIncorrectHeaderCsv(backendUrl):
    fileName = "letterboxd-incorrect-header.csv"
    file = open(testUploadFilesDirectory + fileName)
    filesToSend = {'file': (fileName, file)}
    response = requests.post(backendUrl + "/getInitialRowsOfRecommendations", files=filesToSend)

    assert response.status_code == 400
    responseContent = response.json()
    assert responseContent["errorMessage"] == ServiceUtilities.FILE_ROW_HEADERS_UNEXPECTED_FORMAT_ERROR_MESSAGE

def test_getInitialRowsOfRecommendations_letterboxdMissingHeaderCsv(backendUrl):
    fileName = "letterboxd-missing-header.csv"
    file = open(testUploadFilesDirectory + fileName)
    filesToSend = {'file': (fileName, file)}
    response = requests.post(backendUrl + "/getInitialRowsOfRecommendations", files=filesToSend)

    assert response.status_code == 400
    responseContent = response.json()
    assert responseContent["errorMessage"] == ServiceUtilities.FILE_MORE_DATA_THAN_ROW_HEADERS_ERROR_MESSAGE

def test_getInitialRowsOfRecommendations_letterboxdincorrectZip(backendUrl):
    fileName = "letterboxd-incorrect.zip"
    file = open(testUploadFilesDirectory + fileName, 'rb')
    filesToSend = {'file': (fileName, file)}
    response = requests.post(backendUrl + "/getInitialRowsOfRecommendations", files=filesToSend)

    assert response.status_code == 400
    responseContent = response.json()
    assert responseContent["errorMessage"] == ServiceUtilities.INVALID_ZIP_FILE_ERROR_MESSAGE

def test_getInitialRowsOfRecommendations_imdbNoRecentFilms(backendUrl):
    fileName = "imdb-no-recent-films.csv"
    file = open(testUploadFilesDirectory + fileName)
    filesToSend = {'file': (fileName, file)}
    
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
    
    testUtilities = TestUtilities("../../../")
    testUtilities.verifyRowsOfRecommendations(rowsOfRecommendations, totalNumberOfRows)

    for row in rowsOfRecommendations:
        assert row['profileId'] != "recency"

def test_getInitialRowsOfRecommendations_letterboxdNoRecentFilms(backendUrl):
    fileName = "letterboxd-no-recent-films.csv"
    file = open(testUploadFilesDirectory + fileName)
    filesToSend = {'file': (fileName, file)}
    
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
    
    testUtilities = TestUtilities("../../../")
    testUtilities.verifyRowsOfRecommendations(rowsOfRecommendations, totalNumberOfRows)

    for row in rowsOfRecommendations:
        assert row['profileId'] != "recency"

def test_getInitialRowsOfRecommendations_imdbNoRecentAndFavouriteFilms(backendUrl):
    fileName = "imdb-no-recent-and-favourite-films.csv"
    file = open(testUploadFilesDirectory + fileName)
    filesToSend = {'file': (fileName, file)}
    
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
    
    testUtilities = TestUtilities("../../../")
    testUtilities.verifyRowsOfRecommendations(rowsOfRecommendations, totalNumberOfRows)

    for row in rowsOfRecommendations:
        assert row['profileId'] != "recency"
        assert row['profileId'] != "favourite"

def test_getInitialRowsOfRecommendations_letterboxdNoRecentAndFavouriteFilms(backendUrl):
    fileName = "letterboxd-no-recent-and-favourite-films.csv"
    file = open(testUploadFilesDirectory + fileName)
    filesToSend = {'file': (fileName, file)}
    
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
    
    testUtilities = TestUtilities("../../../")
    testUtilities.verifyRowsOfRecommendations(rowsOfRecommendations, totalNumberOfRows)

    for row in rowsOfRecommendations:
        assert row['profileId'] != "recency"
        assert row['profileId'] != "favourite"

def test_getInitialRowsOfRecommendations_imdbNoRecentAndInternationalFilms(backendUrl):
    fileName = "imdb-no-recent-and-international-films.csv"
    file = open(testUploadFilesDirectory + fileName)
    filesToSend = {'file': (fileName, file)}
    
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
    
    testUtilities = TestUtilities("../../../")
    testUtilities.verifyRowsOfRecommendations(rowsOfRecommendations, totalNumberOfRows)

    for row in rowsOfRecommendations:
        assert row['profileId'] != "recency"
        assert row['profileId'] != "international"

def test_getInitialRowsOfRecommendations_letterboxdNoRecentAndInternationalFilms(backendUrl):
    fileName = "letterboxd-no-recent-and-international-films.csv"
    file = open(testUploadFilesDirectory + fileName)
    filesToSend = {'file': (fileName, file)}
    
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
    
    testUtilities = TestUtilities("../../../")
    testUtilities.verifyRowsOfRecommendations(rowsOfRecommendations, totalNumberOfRows)

    for row in rowsOfRecommendations:
        assert row['profileId'] != "recency"
        assert row['profileId'] != "international"

# tests for cases when the user has rated films with only two genres
def test_getInitialRowsOfRecommendations_imdbNoRecentAndTwoGenres_ensuresTwoGenreRows(backendUrl):
    fileName = "imdb-no-recent-films-and-two-genres.csv"
    file = open(testUploadFilesDirectory + fileName)
    filesToSend = {'file': (fileName, file)}
    
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
    
    testUtilities = TestUtilities("../../../")
    testUtilities.verifyRowsOfRecommendations(rowsOfRecommendations, totalNumberOfRows)

    for row in rowsOfRecommendations:
        assert row['profileId'] != "recency"

# tests for cases when the user has rated films with only two genres
def test_getInitialRowsOfRecommendations_letterboxdNoRecentAndTwoGenres_ensuresTwoGenreRows(backendUrl):
    fileName = "letterboxd-no-recent-films-and-two-genres.csv"
    file = open(testUploadFilesDirectory + fileName)
    filesToSend = {'file': (fileName, file)}
    
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
    
    testUtilities = TestUtilities("../../../")
    testUtilities.verifyRowsOfRecommendations(rowsOfRecommendations, totalNumberOfRows)

    for row in rowsOfRecommendations:
        assert row['profileId'] != "recency"

# tests for cases when the user has rated films with only one genre
def test_getInitialRowsOfRecommendations_imdbInternationalFilmAndNoRecentFilmsAndOneGenres_ensuresOneGenreRows(backendUrl):
    fileName = "imdb-international-film-no-recent-films-and-one-genre.csv"
    file = open(testUploadFilesDirectory + fileName)
    filesToSend = {'file': (fileName, file)}
    
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
    
    testUtilities = TestUtilities("../../../")
    testUtilities.verifyRowsOfRecommendations(rowsOfRecommendations, totalNumberOfRows)

    for row in rowsOfRecommendations:
        assert row['profileId'] != "recency"

# tests for cases when the user has rated films with only one genre
def test_getInitialRowsOfRecommendations_letterboxdInternationalFilmAndNoRecentFilmsAndOneGenres_ensuresOneGenreRows(backendUrl):
    fileName = "letterboxd-international-film-no-recent-films-and-one-genre.csv"
    file = open(testUploadFilesDirectory + fileName)
    filesToSend = {'file': (fileName, file)}
    
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
    
    testUtilities = TestUtilities("../../../")
    testUtilities.verifyRowsOfRecommendations(rowsOfRecommendations, totalNumberOfRows)

    for row in rowsOfRecommendations:
        assert row['profileId'] != "recency"

# tests for cases when the user has rated films with only one genre
def test_getInitialRowsOfRecommendations_imdbNoInternationalFilmsAndNoRecentFilmsAndOneGenres_ensuresOneGenreRows(backendUrl):
    fileName = "imdb-american-film-no-recent-films-and-one-genre.csv"
    file = open(testUploadFilesDirectory + fileName)
    filesToSend = {'file': (fileName, file)}
    
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
    
    testUtilities = TestUtilities("../../../")
    testUtilities.verifyRowsOfRecommendations(rowsOfRecommendations, totalNumberOfRows)

    for row in rowsOfRecommendations:
        assert row['profileId'] != "recency"
        assert row['profileId'] != "international"

# tests for cases when the user has rated films with only one genre
def test_getInitialRowsOfRecommendations_letterboxdNoInternationalFilmsAndNoRecentFilmsAndOneGenres_ensuresOneGenreRows(backendUrl):
    fileName = "letterboxd-american-film-no-recent-films-and-one-genre.csv"
    file = open(testUploadFilesDirectory + fileName)
    filesToSend = {'file': (fileName, file)}
    
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
    
    testUtilities = TestUtilities("../../../")
    testUtilities.verifyRowsOfRecommendations(rowsOfRecommendations, totalNumberOfRows)

    for row in rowsOfRecommendations:
        assert row['profileId'] != "recency"
        assert row['profileId'] != "international"

def test_getInitialRowsOfRecommendations_letterboxdZipNoRecentFilms(backendUrl):
    fileName = "letterboxd-no-recent.zip"
    file = open(testUploadFilesDirectory + fileName, 'rb')
    filesToSend = {'file': (fileName, file)}
    
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
    
    testUtilities = TestUtilities("../../../")
    testUtilities.verifyRowsOfRecommendations(rowsOfRecommendations, totalNumberOfRows)

    for row in rowsOfRecommendations:
        assert row['profileId'] != "recency"

def test_getInitialRowsOfRecommendations_imdbNoRecognisedFilms(backendUrl):
    fileName = "imdb-no-recognised-films.csv"
    file = open(testUploadFilesDirectory + fileName, 'rb')
    filesToSend = {'file': (fileName, file)}
    
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
    
    testUtilities = TestUtilities("../../../")
    testUtilities.verifyRowsOfRecommendations(rowsOfRecommendations, totalNumberOfRows)

def test_getInitialRowsOfRecommendations_letterboxdNoRecognisedFilms(backendUrl):
    fileName = "letterboxd-no-recognised-films.csv"
    file = open(testUploadFilesDirectory + fileName, 'rb')
    filesToSend = {'file': (fileName, file)}
    
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
    
    testUtilities = TestUtilities("../../../")
    testUtilities.verifyRowsOfRecommendations(rowsOfRecommendations, totalNumberOfRows)

def test_regenerateRowsOfRecommendations_imdb(backendUrl):
    fileName = "imdb-no-recent-films.csv"
    file = open(testUploadFilesDirectory + fileName)
    filesToSend = {'file': (fileName, file)}
    
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
    testUtilities = TestUtilities("../../../")
    testUtilities.verifyRowsOfRecommendations(regeneratedRecommendations, totalNumberOfRows)

    # ensure all newly recommended films are unique
    # TODO move this to a method to make more readable?
    initialRecommendationFilmIds = []
    initialRecommendations = getInitialRowsOfRecommendationsResponse.json()
    for row in initialRecommendations:
        for film in row['recommendedFilms']:
            initialRecommendationFilmIds.append(film['id'])

    for row in regeneratedRecommendations:
        for film in row['recommendedFilms']:
            assert film['id'] not in initialRecommendationFilmIds

def test_regenerateRowsOfRecommendations_letterboxd(backendUrl):
    fileName = "letterboxd-no-recent-films.csv"
    file = open(testUploadFilesDirectory + fileName)
    filesToSend = {'file': (fileName, file)}
    
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
    testUtilities = TestUtilities("../../../")
    testUtilities.verifyRowsOfRecommendations(regeneratedRecommendations, totalNumberOfRows)

    # ensure all newly recommended films are unique
    initialRecommendationFilmIds = []
    initialRecommendations = getInitialRowsOfRecommendationsResponse.json()
    for row in initialRecommendations:
        for film in row['recommendedFilms']:
            initialRecommendationFilmIds.append(film['id'])

    for row in regeneratedRecommendations:
        for film in row['recommendedFilms']:
            assert film['id'] not in initialRecommendationFilmIds

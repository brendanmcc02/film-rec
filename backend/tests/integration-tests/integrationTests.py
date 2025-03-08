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

def test_verifyUserUploadedFile_noFile(backendUrl):
    filesToSend = {'file': ("", None)}
    response = requests.post(backendUrl + "/verifyUserUploadedFile", files=filesToSend)

    assert response.status_code == 400
    assert response.content.decode(encoding='utf-8') == ServiceUtilities.NO_FILE_IN_REQUEST_ERROR_MESSAGE

def test_verifyUserUploadedFile_unacceptedFileType(backendUrl):
    fileName = "test.txt"
    file = open(testUploadFilesDirectory + fileName)
    filesToSend = {'file': (fileName, file)}
    response = requests.post(backendUrl + "/verifyUserUploadedFile", files=filesToSend)

    assert response.status_code == 415
    assert response.content.decode(encoding='utf-8') == ServiceUtilities.UNSUPPORTED_MEDIA_TYPE_ERROR_MESSAGE

def test_verifyUserUploadedFile_imdbCorrect(backendUrl):
    fileName = "imdb-no-recent-films.csv"
    file = open(testUploadFilesDirectory + fileName)
    filesToSend = {'file': (fileName, file)}
    response = requests.post(backendUrl + "/verifyUserUploadedFile", files=filesToSend)

    assert response.status_code == 200
    assert response.content.decode(encoding='utf-8') == ServiceUtilities.FILE_UPLOAD_SUCCESS_MESSAGE

def test_verifyUserUploadedFile_imdbIncorrectHeader(backendUrl):
    fileName = "imdb-incorrect-header.csv"
    file = open(testUploadFilesDirectory + fileName)
    filesToSend = {'file': (fileName, file)}
    response = requests.post(backendUrl + "/verifyUserUploadedFile", files=filesToSend)

    assert response.status_code == 400
    assert response.content.decode(encoding='utf-8') == ServiceUtilities.FILE_ROW_HEADERS_UNEXPECTED_FORMAT_ERROR_MESSAGE

def test_verifyUserUploadedFile_imdbMissingHeader(backendUrl):
    fileName = "imdb-missing-header.csv"
    file = open(testUploadFilesDirectory + fileName)
    filesToSend = {'file': (fileName, file)}
    response = requests.post(backendUrl + "/verifyUserUploadedFile", files=filesToSend)

    assert response.status_code == 400
    assert response.content.decode(encoding='utf-8') == ServiceUtilities.FILE_MORE_DATA_THAN_ROW_HEADERS_ERROR_MESSAGE

def test_verifyUserUploadedFile_letterboxdCorrectCsv(backendUrl):
    fileName = "letterboxd-no-recent-films.csv"
    file = open(testUploadFilesDirectory + fileName)
    filesToSend = {'file': (fileName, file)}
    response = requests.post(backendUrl + "/verifyUserUploadedFile", files=filesToSend)

    assert response.status_code == 200
    assert response.content.decode(encoding='utf-8') == ServiceUtilities.FILE_UPLOAD_SUCCESS_MESSAGE

def test_verifyUserUploadedFile_letterboxdIncorrectHeaderCsv(backendUrl):
    fileName = "letterboxd-incorrect-header.csv"
    file = open(testUploadFilesDirectory + fileName)
    filesToSend = {'file': (fileName, file)}
    response = requests.post(backendUrl + "/verifyUserUploadedFile", files=filesToSend)

    assert response.status_code == 400
    assert response.content.decode(encoding='utf-8') == ServiceUtilities.FILE_ROW_HEADERS_UNEXPECTED_FORMAT_ERROR_MESSAGE

def test_verifyUserUploadedFile_letterboxdMissingHeaderCsv(backendUrl):
    fileName = "letterboxd-missing-header.csv"
    file = open(testUploadFilesDirectory + fileName)
    filesToSend = {'file': (fileName, file)}
    response = requests.post(backendUrl + "/verifyUserUploadedFile", files=filesToSend)

    assert response.status_code == 400
    assert response.content.decode(encoding='utf-8') == ServiceUtilities.FILE_MORE_DATA_THAN_ROW_HEADERS_ERROR_MESSAGE

def test_verifyUserUploadedFile_letterboxdincorrectZip(backendUrl):
    fileName = "letterboxd-incorrect.zip"
    file = open(testUploadFilesDirectory + fileName, 'rb')
    filesToSend = {'file': (fileName, file)}
    response = requests.post(backendUrl + "/verifyUserUploadedFile", files=filesToSend)

    assert response.status_code == 400
    assert response.content.decode(encoding='utf-8') == ServiceUtilities.INVALID_ZIP_FILE_ERROR_MESSAGE

def test_verifyUserUploadedFile_letterboxdCorrectZip(backendUrl):
    fileName = "letterboxd-no-recent.zip"
    file = open(testUploadFilesDirectory + fileName, 'rb')
    filesToSend = {'file': (fileName, file)}
    response = requests.post(backendUrl + "/verifyUserUploadedFile", files=filesToSend)

    assert response.status_code == 200
    assert response.content.decode(encoding='utf-8') == ServiceUtilities.FILE_UPLOAD_SUCCESS_MESSAGE

def test_initRowsOfRecommendations_imdbNoRecentFilms(backendUrl):
    fileName = "imdb-no-recent-films.csv"
    file = open(testUploadFilesDirectory + fileName)
    filesToSend = {'file': (fileName, file)}
    verifyUserUploadedFileResponse = requests.post(backendUrl + "/verifyUserUploadedFile", files=filesToSend)

    assert verifyUserUploadedFileResponse.status_code == 200
    assert verifyUserUploadedFileResponse.content.decode(encoding='utf-8') == ServiceUtilities.FILE_UPLOAD_SUCCESS_MESSAGE

    initRowsOfRecommendationsResponse = requests.get(backendUrl + "/initRowsOfRecommendations")
    assert initRowsOfRecommendationsResponse.status_code == 200

    rowsOfRecommendations = initRowsOfRecommendationsResponse.json()

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

def test_initRowsOfRecommendations_letterboxdNoRecentFilms(backendUrl):
    fileName = "letterboxd-no-recent-films.csv"
    file = open(testUploadFilesDirectory + fileName)
    filesToSend = {'file': (fileName, file)}
    verifyUserUploadedFileResponse = requests.post(backendUrl + "/verifyUserUploadedFile", files=filesToSend)

    assert verifyUserUploadedFileResponse.status_code == 200
    assert verifyUserUploadedFileResponse.content.decode(encoding='utf-8') == ServiceUtilities.FILE_UPLOAD_SUCCESS_MESSAGE

    initRowsOfRecommendationsResponse = requests.get(backendUrl + "/initRowsOfRecommendations")
    assert initRowsOfRecommendationsResponse.status_code == 200

    rowsOfRecommendations = initRowsOfRecommendationsResponse.json()

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

def test_initRowsOfRecommendations_imdbNoRecentAndFavouriteFilms(backendUrl):
    fileName = "imdb-no-recent-and-favourite-films.csv"
    file = open(testUploadFilesDirectory + fileName)
    filesToSend = {'file': (fileName, file)}
    verifyUserUploadedFileResponse = requests.post(backendUrl + "/verifyUserUploadedFile", files=filesToSend)

    assert verifyUserUploadedFileResponse.status_code == 200
    assert verifyUserUploadedFileResponse.content.decode(encoding='utf-8') == ServiceUtilities.FILE_UPLOAD_SUCCESS_MESSAGE

    initRowsOfRecommendationsResponse = requests.get(backendUrl + "/initRowsOfRecommendations")
    assert initRowsOfRecommendationsResponse.status_code == 200

    rowsOfRecommendations = initRowsOfRecommendationsResponse.json()

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

def test_initRowsOfRecommendations_letterboxdNoRecentAndFavouriteFilms(backendUrl):
    fileName = "letterboxd-no-recent-and-favourite-films.csv"
    file = open(testUploadFilesDirectory + fileName)
    filesToSend = {'file': (fileName, file)}
    verifyUserUploadedFileResponse = requests.post(backendUrl + "/verifyUserUploadedFile", files=filesToSend)

    assert verifyUserUploadedFileResponse.status_code == 200
    assert verifyUserUploadedFileResponse.content.decode(encoding='utf-8') == ServiceUtilities.FILE_UPLOAD_SUCCESS_MESSAGE

    initRowsOfRecommendationsResponse = requests.get(backendUrl + "/initRowsOfRecommendations")
    assert initRowsOfRecommendationsResponse.status_code == 200

    rowsOfRecommendations = initRowsOfRecommendationsResponse.json()

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

def test_initRowsOfRecommendations_imdbNoRecentAndInternationalFilms(backendUrl):
    fileName = "imdb-no-recent-and-international-films.csv"
    file = open(testUploadFilesDirectory + fileName)
    filesToSend = {'file': (fileName, file)}
    verifyUserUploadedFileResponse = requests.post(backendUrl + "/verifyUserUploadedFile", files=filesToSend)

    assert verifyUserUploadedFileResponse.status_code == 200
    assert verifyUserUploadedFileResponse.content.decode(encoding='utf-8') == ServiceUtilities.FILE_UPLOAD_SUCCESS_MESSAGE

    initRowsOfRecommendationsResponse = requests.get(backendUrl + "/initRowsOfRecommendations")
    assert initRowsOfRecommendationsResponse.status_code == 200

    rowsOfRecommendations = initRowsOfRecommendationsResponse.json()

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

def test_initRowsOfRecommendations_letterboxdNoRecentAndInternationalFilms(backendUrl):
    fileName = "letterboxd-no-recent-and-international-films.csv"
    file = open(testUploadFilesDirectory + fileName)
    filesToSend = {'file': (fileName, file)}
    verifyUserUploadedFileResponse = requests.post(backendUrl + "/verifyUserUploadedFile", files=filesToSend)

    assert verifyUserUploadedFileResponse.status_code == 200
    assert verifyUserUploadedFileResponse.content.decode(encoding='utf-8') == ServiceUtilities.FILE_UPLOAD_SUCCESS_MESSAGE

    initRowsOfRecommendationsResponse = requests.get(backendUrl + "/initRowsOfRecommendations")
    assert initRowsOfRecommendationsResponse.status_code == 200

    rowsOfRecommendations = initRowsOfRecommendationsResponse.json()

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
def test_initRowsOfRecommendations_imdbNoRecentAndTwoGenres_ensuresTwoGenreRows(backendUrl):
    fileName = "imdb-no-recent-films-and-two-genres.csv"
    file = open(testUploadFilesDirectory + fileName)
    filesToSend = {'file': (fileName, file)}
    verifyUserUploadedFileResponse = requests.post(backendUrl + "/verifyUserUploadedFile", files=filesToSend)

    assert verifyUserUploadedFileResponse.status_code == 200
    assert verifyUserUploadedFileResponse.content.decode(encoding='utf-8') == ServiceUtilities.FILE_UPLOAD_SUCCESS_MESSAGE

    initRowsOfRecommendationsResponse = requests.get(backendUrl + "/initRowsOfRecommendations")
    assert initRowsOfRecommendationsResponse.status_code == 200

    rowsOfRecommendations = initRowsOfRecommendationsResponse.json()

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
def test_initRowsOfRecommendations_letterboxdNoRecentAndTwoGenres_ensuresTwoGenreRows(backendUrl):
    fileName = "letterboxd-no-recent-films-and-two-genres.csv"
    file = open(testUploadFilesDirectory + fileName)
    filesToSend = {'file': (fileName, file)}
    verifyUserUploadedFileResponse = requests.post(backendUrl + "/verifyUserUploadedFile", files=filesToSend)

    assert verifyUserUploadedFileResponse.status_code == 200
    assert verifyUserUploadedFileResponse.content.decode(encoding='utf-8') == ServiceUtilities.FILE_UPLOAD_SUCCESS_MESSAGE

    initRowsOfRecommendationsResponse = requests.get(backendUrl + "/initRowsOfRecommendations")
    assert initRowsOfRecommendationsResponse.status_code == 200

    rowsOfRecommendations = initRowsOfRecommendationsResponse.json()

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
def test_initRowsOfRecommendations_imdbInternationalFilmAndNoRecentFilmsAndOneGenres_ensuresOneGenreRows(backendUrl):
    fileName = "imdb-international-film-no-recent-films-and-one-genre.csv"
    file = open(testUploadFilesDirectory + fileName)
    filesToSend = {'file': (fileName, file)}
    verifyUserUploadedFileResponse = requests.post(backendUrl + "/verifyUserUploadedFile", files=filesToSend)

    assert verifyUserUploadedFileResponse.status_code == 200
    assert verifyUserUploadedFileResponse.content.decode(encoding='utf-8') == ServiceUtilities.FILE_UPLOAD_SUCCESS_MESSAGE

    initRowsOfRecommendationsResponse = requests.get(backendUrl + "/initRowsOfRecommendations")
    assert initRowsOfRecommendationsResponse.status_code == 200

    rowsOfRecommendations = initRowsOfRecommendationsResponse.json()

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
def test_initRowsOfRecommendations_letterboxdInternationalFilmAndNoRecentFilmsAndOneGenres_ensuresOneGenreRows(backendUrl):
    fileName = "letterboxd-international-film-no-recent-films-and-one-genre.csv"
    file = open(testUploadFilesDirectory + fileName)
    filesToSend = {'file': (fileName, file)}
    verifyUserUploadedFileResponse = requests.post(backendUrl + "/verifyUserUploadedFile", files=filesToSend)

    assert verifyUserUploadedFileResponse.status_code == 200
    assert verifyUserUploadedFileResponse.content.decode(encoding='utf-8') == ServiceUtilities.FILE_UPLOAD_SUCCESS_MESSAGE

    initRowsOfRecommendationsResponse = requests.get(backendUrl + "/initRowsOfRecommendations")
    assert initRowsOfRecommendationsResponse.status_code == 200

    rowsOfRecommendations = initRowsOfRecommendationsResponse.json()

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
def test_initRowsOfRecommendations_imdbNoInternationalFilmsAndNoRecentFilmsAndOneGenres_ensuresOneGenreRows(backendUrl):
    fileName = "imdb-american-film-no-recent-films-and-one-genre.csv"
    file = open(testUploadFilesDirectory + fileName)
    filesToSend = {'file': (fileName, file)}
    verifyUserUploadedFileResponse = requests.post(backendUrl + "/verifyUserUploadedFile", files=filesToSend)

    assert verifyUserUploadedFileResponse.status_code == 200
    assert verifyUserUploadedFileResponse.content.decode(encoding='utf-8') == ServiceUtilities.FILE_UPLOAD_SUCCESS_MESSAGE

    initRowsOfRecommendationsResponse = requests.get(backendUrl + "/initRowsOfRecommendations")
    assert initRowsOfRecommendationsResponse.status_code == 200

    rowsOfRecommendations = initRowsOfRecommendationsResponse.json()

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
def test_initRowsOfRecommendations_letterboxdNoInternationalFilmsAndNoRecentFilmsAndOneGenres_ensuresOneGenreRows(backendUrl):
    fileName = "letterboxd-american-film-no-recent-films-and-one-genre.csv"
    file = open(testUploadFilesDirectory + fileName)
    filesToSend = {'file': (fileName, file)}
    verifyUserUploadedFileResponse = requests.post(backendUrl + "/verifyUserUploadedFile", files=filesToSend)

    assert verifyUserUploadedFileResponse.status_code == 200
    assert verifyUserUploadedFileResponse.content.decode(encoding='utf-8') == ServiceUtilities.FILE_UPLOAD_SUCCESS_MESSAGE

    initRowsOfRecommendationsResponse = requests.get(backendUrl + "/initRowsOfRecommendations")
    assert initRowsOfRecommendationsResponse.status_code == 200

    rowsOfRecommendations = initRowsOfRecommendationsResponse.json()

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

def test_initRowsOfRecommendations_letterboxdZipNoRecentFilms(backendUrl):
    fileName = "letterboxd-no-recent.zip"
    file = open(testUploadFilesDirectory + fileName, 'rb')
    filesToSend = {'file': (fileName, file)}
    verifyUserUploadedFileResponse = requests.post(backendUrl + "/verifyUserUploadedFile", files=filesToSend)

    assert verifyUserUploadedFileResponse.status_code == 200
    assert verifyUserUploadedFileResponse.content.decode(encoding='utf-8') == ServiceUtilities.FILE_UPLOAD_SUCCESS_MESSAGE

    initRowsOfRecommendationsResponse = requests.get(backendUrl + "/initRowsOfRecommendations")
    assert initRowsOfRecommendationsResponse.status_code == 200

    rowsOfRecommendations = initRowsOfRecommendationsResponse.json()

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

def test_initRowsOfRecommendations_imdbNoRecognisedFilms(backendUrl):
    fileName = "imdb-no-recognised-films.csv"
    file = open(testUploadFilesDirectory + fileName, 'rb')
    filesToSend = {'file': (fileName, file)}
    verifyUserUploadedFileResponse = requests.post(backendUrl + "/verifyUserUploadedFile", files=filesToSend)

    assert verifyUserUploadedFileResponse.status_code == 200
    assert verifyUserUploadedFileResponse.content.decode(encoding='utf-8') == ServiceUtilities.FILE_UPLOAD_SUCCESS_MESSAGE

    initRowsOfRecommendationsResponse = requests.get(backendUrl + "/initRowsOfRecommendations")
    assert initRowsOfRecommendationsResponse.status_code == 200

    rowsOfRecommendations = initRowsOfRecommendationsResponse.json()

    numberOfFavouriteRows = 0
    numberOfRecentRows = 0
    numberOfGenreRows = 0
    numberOfInternationalRows = 0
    numberOfOldRows = 0
    totalNumberOfRows = (numberOfFavouriteRows + numberOfRecentRows + numberOfGenreRows + 
                         numberOfInternationalRows + numberOfOldRows)
    
    testUtilities = TestUtilities("../../../")
    testUtilities.verifyRowsOfRecommendations(rowsOfRecommendations, totalNumberOfRows)

def test_initRowsOfRecommendations_letterboxdNoRecognisedFilms(backendUrl):
    fileName = "letterboxd-no-recognised-films.csv"
    file = open(testUploadFilesDirectory + fileName, 'rb')
    filesToSend = {'file': (fileName, file)}
    verifyUserUploadedFileResponse = requests.post(backendUrl + "/verifyUserUploadedFile", files=filesToSend)

    assert verifyUserUploadedFileResponse.status_code == 200
    assert verifyUserUploadedFileResponse.content.decode(encoding='utf-8') == ServiceUtilities.FILE_UPLOAD_SUCCESS_MESSAGE

    initRowsOfRecommendationsResponse = requests.get(backendUrl + "/initRowsOfRecommendations")
    assert initRowsOfRecommendationsResponse.status_code == 200

    rowsOfRecommendations = initRowsOfRecommendationsResponse.json()

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
    verifyUserUploadedFileResponse = requests.post(backendUrl + "/verifyUserUploadedFile", files=filesToSend)

    assert verifyUserUploadedFileResponse.status_code == 200
    assert verifyUserUploadedFileResponse.content.decode(encoding='utf-8') == ServiceUtilities.FILE_UPLOAD_SUCCESS_MESSAGE

    initRowsOfRecommendationsResponse = requests.get(backendUrl + "/initRowsOfRecommendations")
    assert initRowsOfRecommendationsResponse.status_code == 200

    regenerateRecommendationsResponse = requests.get(backendUrl + "/regenerateRecommendations")
    assert regenerateRecommendationsResponse.status_code == 200

    # verify the newly recommended films are valid
    numberOfFavouriteRows = 1
    numberOfRecentRows = 0
    numberOfGenreRows = ServiceUtilities.NUMBER_OF_GENRE_RECOMMENDATION_ROWS
    numberOfInternationalRows = 1
    numberOfOldRows = 1
    totalNumberOfRows = (numberOfFavouriteRows + numberOfRecentRows + numberOfGenreRows + 
                         numberOfInternationalRows + numberOfOldRows)
    regeneratedRecommendations = regenerateRecommendationsResponse.json()
    testUtilities = TestUtilities("../../../")
    testUtilities.verifyRowsOfRecommendations(regeneratedRecommendations, totalNumberOfRows)

    # ensure all newly recommended films are unique
    initialRecommendationFilmIds = []
    initialRecommendations = initRowsOfRecommendationsResponse.json()
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
    verifyUserUploadedFileResponse = requests.post(backendUrl + "/verifyUserUploadedFile", files=filesToSend)

    assert verifyUserUploadedFileResponse.status_code == 200
    assert verifyUserUploadedFileResponse.content.decode(encoding='utf-8') == ServiceUtilities.FILE_UPLOAD_SUCCESS_MESSAGE

    initRowsOfRecommendationsResponse = requests.get(backendUrl + "/initRowsOfRecommendations")
    assert initRowsOfRecommendationsResponse.status_code == 200

    regenerateRecommendationsResponse = requests.get(backendUrl + "/regenerateRecommendations")
    assert regenerateRecommendationsResponse.status_code == 200

    # verify the newly recommended films are valid
    numberOfFavouriteRows = 1
    numberOfRecentRows = 0
    numberOfGenreRows = ServiceUtilities.NUMBER_OF_GENRE_RECOMMENDATION_ROWS
    numberOfInternationalRows = 1
    numberOfOldRows = 1
    totalNumberOfRows = (numberOfFavouriteRows + numberOfRecentRows + numberOfGenreRows + 
                         numberOfInternationalRows + numberOfOldRows)
    regeneratedRecommendations = regenerateRecommendationsResponse.json()
    testUtilities = TestUtilities("../../../")
    testUtilities.verifyRowsOfRecommendations(regeneratedRecommendations, totalNumberOfRows)

    # ensure all newly recommended films are unique
    initialRecommendationFilmIds = []
    initialRecommendations = initRowsOfRecommendationsResponse.json()
    for row in initialRecommendations:
        for film in row['recommendedFilms']:
            initialRecommendationFilmIds.append(film['id'])

    for row in regeneratedRecommendations:
        for film in row['recommendedFilms']:
            assert film['id'] not in initialRecommendationFilmIds

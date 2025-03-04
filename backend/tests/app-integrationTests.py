import json
import os
import requests
import sys
import testUtilities
# import the needed file from backend directory
# (this is ugly as hell, there's probably an easier way but it gets the job done)
absolutePathOfCurrentFile = os.path.dirname(os.path.abspath(__file__))
parentDirectoryOfCurrentFile = os.path.dirname(absolutePathOfCurrentFile)
sys.path.append(parentDirectoryOfCurrentFile)
import app
backendUrl = "http://127.0.0.1:5000"
testUploadFilesDirectory = "test-upload-files/"

def test_loadJsonFiles():
    response = requests.get(backendUrl + "/loadJsonFiles")

    assert response.status_code == 200
    assert response.content.decode(encoding='utf-8') == app.JSON_FILES_LOAD_SUCCESS_MESSAGE

    response = requests.get(backendUrl + "/loadJsonFiles")

    assert response.status_code == 304
    # 304 responses typically do not have content, so do not assert for response content

def test_verifyUserUploadedFile_noFile():
    filesToSend = {'file': ("", None)}
    response = requests.post(backendUrl + "/verifyUserUploadedFile", files=filesToSend)

    assert response.status_code == 400
    assert response.content.decode(encoding='utf-8') == app.NO_FILE_IN_REQUEST_ERROR_MESSAGE

def test_verifyUserUploadedFile_txtFile():
    fileName = "test.txt"
    file = open(testUploadFilesDirectory + fileName)
    filesToSend = {'file': (fileName, file)}
    response = requests.post(backendUrl + "/verifyUserUploadedFile", files=filesToSend)

    assert response.status_code == 415
    assert response.content.decode(encoding='utf-8') == app.IS_NOT_CSV_ERROR_MESSAGE 

def test_verifyUserUploadedFile_imdbCorrect():
    fileName = "imdb-no-recent-films.csv"
    file = open(testUploadFilesDirectory + fileName)
    filesToSend = {'file': (fileName, file)}
    response = requests.post(backendUrl + "/verifyUserUploadedFile", files=filesToSend)

    assert response.status_code == 200
    assert response.content.decode(encoding='utf-8') == app.FILE_UPLOAD_SUCCESS_MESSAGE

def test_verifyUserUploadedFile_imdbIncorrectHeader():
    fileName = "imdb-incorrect-header.csv"
    file = open(testUploadFilesDirectory + fileName)
    filesToSend = {'file': (fileName, file)}
    response = requests.post(backendUrl + "/verifyUserUploadedFile", files=filesToSend)

    assert response.status_code == 400
    assert response.content.decode(encoding='utf-8') == app.FILE_ROW_HEADERS_UNEXPECTED_FORMAT_ERROR_MESSAGE

def test_verifyUserUploadedFile_imdbMissingHeader():
    fileName = "imdb-missing-header.csv"
    file = open(testUploadFilesDirectory + fileName)
    filesToSend = {'file': (fileName, file)}
    response = requests.post(backendUrl + "/verifyUserUploadedFile", files=filesToSend)

    assert response.status_code == 400
    assert response.content.decode(encoding='utf-8') == app.FILE_MORE_DATA_THAN_ROW_HEADERS_ERROR_MESSAGE

def test_verifyUserUploadedFile_letterboxdCorrect():
    fileName = "letterboxd-no-recent-films.csv"
    file = open(testUploadFilesDirectory + fileName)
    filesToSend = {'file': (fileName, file)}
    response = requests.post(backendUrl + "/verifyUserUploadedFile", files=filesToSend)

    assert response.status_code == 200
    assert response.content.decode(encoding='utf-8') == app.FILE_UPLOAD_SUCCESS_MESSAGE

def test_verifyUserUploadedFile_letterboxdIncorrectHeader():
    fileName = "letterboxd-incorrect-header.csv"
    file = open(testUploadFilesDirectory + fileName)
    filesToSend = {'file': (fileName, file)}
    response = requests.post(backendUrl + "/verifyUserUploadedFile", files=filesToSend)

    assert response.status_code == 400
    assert response.content.decode(encoding='utf-8') == app.FILE_ROW_HEADERS_UNEXPECTED_FORMAT_ERROR_MESSAGE

def test_verifyUserUploadedFile_letterboxdMissingHeader():
    fileName = "letterboxd-missing-header.csv"
    file = open(testUploadFilesDirectory + fileName)
    filesToSend = {'file': (fileName, file)}
    response = requests.post(backendUrl + "/verifyUserUploadedFile", files=filesToSend)

    assert response.status_code == 400
    assert response.content.decode(encoding='utf-8') == app.FILE_MORE_DATA_THAN_ROW_HEADERS_ERROR_MESSAGE

def test_initRowsOfRecommendations_imdbNoRecentFilms():
    fileName = "imdb-no-recent-films.csv"
    file = open(testUploadFilesDirectory + fileName)
    filesToSend = {'file': (fileName, file)}
    postResponse = requests.post(backendUrl + "/verifyUserUploadedFile", files=filesToSend)

    assert postResponse.status_code == 200
    assert postResponse.content.decode(encoding='utf-8') == app.FILE_UPLOAD_SUCCESS_MESSAGE

    getResponse = requests.get(backendUrl + "/initRowsOfRecommendations")
    assert getResponse.status_code == 200

    rowsOfRecommendations = getResponse.json()

    numberOfFavouriteRows = 1
    numberOfRecentRows = 0
    numberOfInternationalRows = 1
    numberOfOldRows = 1
    totalNumberOfRows = (numberOfFavouriteRows + numberOfRecentRows + app.NUMBER_OF_GENRE_RECOMMENDATION_ROWS + 
                         numberOfInternationalRows + numberOfOldRows)
    
    testUtilities.verifyRowsOfRecommendations(rowsOfRecommendations, totalNumberOfRows)

    for row in rowsOfRecommendations:
        assert row['profileId'] != "recency"

def test_initRowsOfRecommendations_letterboxdNoRecentFilms():
    fileName = "letterboxd-no-recent-films.csv"
    file = open(testUploadFilesDirectory + fileName)
    filesToSend = {'file': (fileName, file)}
    postResponse = requests.post(backendUrl + "/verifyUserUploadedFile", files=filesToSend)

    assert postResponse.status_code == 200
    assert postResponse.content.decode(encoding='utf-8') == app.FILE_UPLOAD_SUCCESS_MESSAGE

    getResponse = requests.get(backendUrl + "/initRowsOfRecommendations")
    assert getResponse.status_code == 200

    rowsOfRecommendations = getResponse.json()

    numberOfFavouriteRows = 1
    numberOfRecentRows = 0
    numberOfInternationalRows = 1
    numberOfOldRows = 1
    totalNumberOfRows = (numberOfFavouriteRows + numberOfRecentRows + app.NUMBER_OF_GENRE_RECOMMENDATION_ROWS + 
                         numberOfInternationalRows + numberOfOldRows)
    
    testUtilities.verifyRowsOfRecommendations(rowsOfRecommendations, totalNumberOfRows)

    for row in rowsOfRecommendations:
        assert row['profileId'] != "recency"

def test_initRowsOfRecommendations_imdbNoRecentAndFavouriteFilms():
    fileName = "imdb-no-recent-and-favourite-films.csv"
    file = open(testUploadFilesDirectory + fileName)
    filesToSend = {'file': (fileName, file)}
    postResponse = requests.post(backendUrl + "/verifyUserUploadedFile", files=filesToSend)

    assert postResponse.status_code == 200
    assert postResponse.content.decode(encoding='utf-8') == app.FILE_UPLOAD_SUCCESS_MESSAGE

    getResponse = requests.get(backendUrl + "/initRowsOfRecommendations")
    assert getResponse.status_code == 200

    rowsOfRecommendations = getResponse.json()

    numberOfFavouriteRows = 0
    numberOfRecentRows = 0
    numberOfInternationalRows = 1
    numberOfOldRows = 1
    totalNumberOfRows = (numberOfFavouriteRows + numberOfRecentRows + app.NUMBER_OF_GENRE_RECOMMENDATION_ROWS + 
                         numberOfInternationalRows + numberOfOldRows)
    
    testUtilities.verifyRowsOfRecommendations(rowsOfRecommendations, totalNumberOfRows)

    for row in rowsOfRecommendations:
        assert row['profileId'] != "recency"
        assert row['profileId'] != "favourite"

def test_initRowsOfRecommendations_letterboxdNoRecentAndFavouriteFilms():
    fileName = "letterboxd-no-recent-and-favourite-films.csv"
    file = open(testUploadFilesDirectory + fileName)
    filesToSend = {'file': (fileName, file)}
    postResponse = requests.post(backendUrl + "/verifyUserUploadedFile", files=filesToSend)

    assert postResponse.status_code == 200
    assert postResponse.content.decode(encoding='utf-8') == app.FILE_UPLOAD_SUCCESS_MESSAGE

    getResponse = requests.get(backendUrl + "/initRowsOfRecommendations")
    assert getResponse.status_code == 200

    rowsOfRecommendations = getResponse.json()

    numberOfFavouriteRows = 0
    numberOfRecentRows = 0
    numberOfInternationalRows = 1
    numberOfOldRows = 1
    totalNumberOfRows = (numberOfFavouriteRows + numberOfRecentRows + app.NUMBER_OF_GENRE_RECOMMENDATION_ROWS + 
                         numberOfInternationalRows + numberOfOldRows)
    
    testUtilities.verifyRowsOfRecommendations(rowsOfRecommendations, totalNumberOfRows)

    for row in rowsOfRecommendations:
        assert row['profileId'] != "recency"
        assert row['profileId'] != "favourite"

def test_initRowsOfRecommendations_imdbNoRecentAndInternationalFilms():
    fileName = "imdb-no-recent-and-international-films.csv"
    file = open(testUploadFilesDirectory + fileName)
    filesToSend = {'file': (fileName, file)}
    postResponse = requests.post(backendUrl + "/verifyUserUploadedFile", files=filesToSend)

    assert postResponse.status_code == 200
    assert postResponse.content.decode(encoding='utf-8') == app.FILE_UPLOAD_SUCCESS_MESSAGE

    getResponse = requests.get(backendUrl + "/initRowsOfRecommendations")
    assert getResponse.status_code == 200

    rowsOfRecommendations = getResponse.json()

    numberOfFavouriteRows = 1
    numberOfRecentRows = 0
    numberOfInternationalRows = 0
    numberOfOldRows = 1
    totalNumberOfRows = (numberOfFavouriteRows + numberOfRecentRows + app.NUMBER_OF_GENRE_RECOMMENDATION_ROWS + 
                         numberOfInternationalRows + numberOfOldRows)
    
    testUtilities.verifyRowsOfRecommendations(rowsOfRecommendations, totalNumberOfRows)

    for row in rowsOfRecommendations:
        assert row['profileId'] != "recency"
        assert row['profileId'] != "international"

def test_initRowsOfRecommendations_letterboxdNoRecentAndInternationalFilms():
    fileName = "letterboxd-no-recent-and-international-films.csv"
    file = open(testUploadFilesDirectory + fileName)
    filesToSend = {'file': (fileName, file)}
    postResponse = requests.post(backendUrl + "/verifyUserUploadedFile", files=filesToSend)

    assert postResponse.status_code == 200
    assert postResponse.content.decode(encoding='utf-8') == app.FILE_UPLOAD_SUCCESS_MESSAGE

    getResponse = requests.get(backendUrl + "/initRowsOfRecommendations")
    assert getResponse.status_code == 200

    rowsOfRecommendations = getResponse.json()

    numberOfFavouriteRows = 1
    numberOfRecentRows = 0
    numberOfInternationalRows = 0
    numberOfOldRows = 1
    totalNumberOfRows = (numberOfFavouriteRows + numberOfRecentRows + app.NUMBER_OF_GENRE_RECOMMENDATION_ROWS + 
                         numberOfInternationalRows + numberOfOldRows)
    
    testUtilities.verifyRowsOfRecommendations(rowsOfRecommendations, totalNumberOfRows)

    for row in rowsOfRecommendations:
        assert row['profileId'] != "recency"
        assert row['profileId'] != "international"

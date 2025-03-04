import os
import requests
import sys
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
    fileName = "imdb-correct.csv"
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
    fileName = "letterboxd-correct.csv"
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

# def test_initRowsOfRecommendations_imdbNoRecentFilms():
#     fileName = "imdb-no-recent.csv"
#     file = open(testUploadFilesDirectory + fileName)
#     filesToSend = {'file': (fileName, file)}
#     postResponse = requests.post(backendUrl + "/verifyUserUploadedFile", files=filesToSend)

#     assert postResponse.status_code == 200
#     assert os.path.exists("../../../database/imdb-correct.csv")

#     getResponse = requests.get(backendUrl + "/initRowsOfRecommendations")
#     assert getResponse.status_code == 200

#     rowsOfRecommendations = getResponse.json()

#     numberOfFavouriteRows = 1
#     numberOfInternationalRows = 1
#     numberOfOldRows = 1
#     total = numberOfFavouriteRows + app.NUMBER_OF_TOP_GENRE_PROFILES + numberOfInternationalRows + numberOfOldRows
#     assert len(rowsOfRecommendations) == total

#     for row in rowsOfRecommendations:
#         assert 'recommendedRowText' in row
#         assert row['recommendedRowsText'] != ""
        
#         assert 'profileId' in row
#         assert row['profileId'] != ""

#         assert 'recommendedFilms' in row
#         assert len(row['recommendedFilms']) == app.NUMBER_OF_RECOMMENDATIONS_PER_ROW

#         for film in row['recommendedFilms']:
#             assert 'similarityScore' in film
#             assert film['similarityScore'] != None
#             assert film['similarityScore'] >= 0.0
#             assert film['similarityScore'] <= 100.0

test_loadJsonFiles()

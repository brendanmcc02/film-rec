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

def test_verifyUserUploadedFile_noFile():
    filesToSend = {'file': ("", None)}
    response = requests.post(backendUrl + "/verifyUserUploadedFile", files=filesToSend)

    assert response.status_code == 400
    assert response.content.decode(encoding='utf-8') == app.NO_FILE_IN_REQUEST_ERROR_MESSAGE

def test_verifyUserUploadedFile_txtFile():
    file = open(testUploadFilesDirectory + "test.txt")
    filesToSend = {'file': ("imdb-correct.csv", file)}
    response = requests.post(backendUrl + "/verifyUserUploadedFile", files=filesToSend)

    assert response.status_code == 400
    assert response.content.decode(encoding='utf-8') == app.IS_NOT_CSV_ERROR_MESSAGE 

def test_verifyUserUploadedFile_imdbCorrect():
    file = open(testUploadFilesDirectory + "imdb-correct.csv")
    filesToSend = {'file': ("imdb-correct.csv", file)}
    response = requests.post(backendUrl + "/verifyUserUploadedFile", files=filesToSend)

    assert response.status_code == 200

def test_verifyUserUploadedFile_imdbIncorrectHeader():
    file = open(testUploadFilesDirectory + "imdb-incorrect-header.csv")
    filesToSend = {'file': ("imdb-incorrect-header.csv", file)}
    response = requests.post(backendUrl + "/verifyUserUploadedFile", files=filesToSend)

    assert response.status_code == 400
    assert response.content.decode(encoding='utf-8') == app.FILE_ROW_HEADERS_UNEXPECTED_FORMAT_ERROR_MESSAGE

def test_verifyUserUploadedFile_imdbMissingHeader():
    file = open(testUploadFilesDirectory + "imdb-missing-header.csv")
    filesToSend = {'file': ("imdb-missing-header.csv", file)}
    response = requests.post(backendUrl + "/verifyUserUploadedFile", files=filesToSend)

    assert response.status_code == 400
    assert response.content.decode(encoding='utf-8') == app.FILE_MORE_DATA_THAN_ROW_HEADERS_ERROR_MESSAGE

def test_verifyUserUploadedFile_letterboxdCorrect():
    file = open(testUploadFilesDirectory + "letterboxd-correct.csv")
    filesToSend = {'file': ("letterboxd-correct.csv", file)}
    response = requests.post(backendUrl + "/verifyUserUploadedFile", files=filesToSend)

    assert response.status_code == 200

def test_verifyUserUploadedFile_letterboxdIncorrectHeader():
    file = open(testUploadFilesDirectory + "letterboxd-incorrect-header.csv")
    filesToSend = {'file': ("letterboxd-incorrect-header.csv", file)}
    response = requests.post(backendUrl + "/verifyUserUploadedFile", files=filesToSend)

    assert response.status_code == 400
    assert response.content.decode(encoding='utf-8') == app.FILE_ROW_HEADERS_UNEXPECTED_FORMAT_ERROR_MESSAGE

def test_verifyUserUploadedFile_letterboxdMissingHeader():
    file = open(testUploadFilesDirectory + "letterboxd-missing-header.csv")
    filesToSend = {'file': ("letterboxd-missing-header.csv", file)}
    response = requests.post(backendUrl + "/verifyUserUploadedFile", files=filesToSend)

    assert response.status_code == 400
    assert response.content.decode(encoding='utf-8') == app.FILE_MORE_DATA_THAN_ROW_HEADERS_ERROR_MESSAGE

# def test_initRowsOfRecommendations_imdbNoRecentFilms():
#     file = open(testUploadFilesDirectory + "imdb-no-recent.csv")
#     filesToSend = {'file': ("imdb-correct.csv", file)}
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


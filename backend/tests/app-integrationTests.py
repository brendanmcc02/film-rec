import os
import requests
import sys
absolutePath = os.path.dirname(os.path.abspath(__file__))
parentDirectoryOfAbsolutePath = os.path.dirname(absolutePath)
sys.path.append(parentDirectoryOfAbsolutePath)
import app
backendUrl = "http://127.0.0.1:5000"

def test_verifyUserUploadedFile_imdbCorrect():
    file = open("test-csv-files/imdb-correct.csv")
    filesToSend = {'file': ("imdb-correct.csv", file)}
    response = requests.post(backendUrl + "/verifyUserUploadedFile", files=filesToSend)

    assert response.status_code == 200
    assert os.path.exists("../../../database/imdb-correct.csv")
    os.remove("../../../database/imdb-correct.csv")

def test_verifyUserUploadedFile_imdbIncorrectHeader():
    file = open("test-csv-files/imdb-incorrect-header.csv")
    filesToSend = {'file': ("imdb-incorrect-header.csv", file)}
    response = requests.post(backendUrl + "/verifyUserUploadedFile", files=filesToSend)

    assert response.status_code == 400
    assert os.path.exists("../../../database/imdb-incorrect-header.csv")
    os.remove("../../../database/imdb-incorrect-header.csv")

def test_verifyUserUploadedFile_imdbMissingHeader():
    file = open("test-csv-files/imdb-missing-header.csv")
    filesToSend = {'file': ("imdb-missing-header.csv", file)}
    response = requests.post(backendUrl + "/verifyUserUploadedFile", files=filesToSend)

    assert response.status_code == 400
    assert os.path.exists("../../../database/imdb-missing-header.csv")
    os.remove("../../../database/imdb-missing-header.csv")

def test_verifyUserUploadedFile_letterboxdCorrect():
    file = open("test-csv-files/letterboxd-correct.csv")
    filesToSend = {'file': ("letterboxd-correct.csv", file)}
    response = requests.post(backendUrl + "/verifyUserUploadedFile", files=filesToSend)

    assert response.status_code == 200
    assert os.path.exists("../../../database/letterboxd-correct.csv")
    os.remove("../../../database/letterboxd-correct.csv")

def test_verifyUserUploadedFile_letterboxdIncorrectHeader():
    file = open("test-csv-files/letterboxd-incorrect-header.csv")
    filesToSend = {'file': ("letterboxd-incorrect-header.csv", file)}
    response = requests.post(backendUrl + "/verifyUserUploadedFile", files=filesToSend)

    assert response.status_code == 400
    assert os.path.exists("../../../database/letterboxd-incorrect-header.csv")
    os.remove("../../../database/letterboxd-incorrect-header.csv")

def test_verifyUserUploadedFile_letterboxdMissingHeader():
    file = open("test-csv-files/letterboxd-missing-header.csv")
    filesToSend = {'file': ("letterboxd-missing-header.csv", file)}
    response = requests.post(backendUrl + "/verifyUserUploadedFile", files=filesToSend)

    assert response.status_code == 400
    assert os.path.exists("../../../database/letterboxd-missing-header.csv")
    os.remove("../../../database/letterboxd-missing-header.csv")

def test_initRowsOfRecommendations_imdbNoRecentFilms():
    file = open("test-csv-files/imdb-no-recent.csv")
    filesToSend = {'file': ("imdb-correct.csv", file)}
    postResponse = requests.post(backendUrl + "/verifyUserUploadedFile", files=filesToSend)

    assert postResponse.status_code == 200
    assert os.path.exists("../../../database/imdb-correct.csv")

    getResponse = requests.get(backendUrl + "/initRowsOfRecommendations")
    assert getResponse.status_code == 200

    rowsOfRecommendations = getResponse.json()

    numberOfFavouriteRows = 1
    numberOfInternationalRows = 1
    numberOfOldRows = 1
    total = numberOfFavouriteRows + app.NUMBER_OF_TOP_GENRE_PROFILES + numberOfInternationalRows + numberOfOldRows
    assert len(rowsOfRecommendations) == total

    for row in rowsOfRecommendations:
        assert 'recommendedRowText' in row
        assert row['recommendedRowsText'] != ""
        
        assert 'profileId' in row
        assert row['profileId'] != ""

        assert 'recommendedFilms' in row
        assert len(row['recommendedFilms']) == app.NUMBER_OF_RECOMMENDATIONS_PER_ROW

        for film in row['recommendedFilms']:
            assert 'similarityScore' in film
            assert film['similarityScore'] != None
            assert film['similarityScore'] >= 0.0
            assert film['similarityScore'] <= 100.0


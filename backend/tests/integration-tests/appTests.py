import os
import requests

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

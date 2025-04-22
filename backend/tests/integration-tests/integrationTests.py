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

database = DocumentDatabase("../../../")
testUtilities = TestUtilities(database)

def test_getInitialRowsOfRecommendations_guidExists(backendUrl):
    filesToSend = testUtilities.getFilesToSend("imdb-no-recent-films.csv")
    
    getInitialRowsOfRecommendationsResponse = requests.post(backendUrl + "/getInitialRowsOfRecommendations", files=filesToSend)
    assert getInitialRowsOfRecommendationsResponse.status_code == 200

    testUtilities.verifyAttributeExists(getInitialRowsOfRecommendationsResponse, 'guid')

def test_regenerateRowsOfRecommendations_guidExists(backendUrl):
    filesToSend = testUtilities.getFilesToSend("imdb-no-recent-films.csv")
    
    getInitialRowsOfRecommendationsResponse = requests.post(backendUrl + "/getInitialRowsOfRecommendations", files=filesToSend)
    assert getInitialRowsOfRecommendationsResponse.status_code == 200

    guid = testUtilities.getGuidFromResponse(getInitialRowsOfRecommendationsResponse)

    regenerateRecommendationsResponse = requests.get(backendUrl + "/regenerateRecommendations?guid=" + guid)
    assert regenerateRecommendationsResponse.status_code == 200

    testUtilities.verifyAttributeExists(regenerateRecommendationsResponse, 'guid')

def test_getInitialRowsOfRecommendations_errorMessageExists(backendUrl):
    filesToSend = testUtilities.getFilesToSend("imdb-no-recent-films.csv")
    
    getInitialRowsOfRecommendationsResponse = requests.post(backendUrl + "/getInitialRowsOfRecommendations", files=filesToSend)
    assert getInitialRowsOfRecommendationsResponse.status_code == 200

    testUtilities.verifyAttributeExists(getInitialRowsOfRecommendationsResponse, 'errorMessage')

def test_regenerateRowsOfRecommendations_errorMessageExists(backendUrl):
    filesToSend = testUtilities.getFilesToSend("imdb-no-recent-films.csv")
    
    getInitialRowsOfRecommendationsResponse = requests.post(backendUrl + "/getInitialRowsOfRecommendations", files=filesToSend)
    assert getInitialRowsOfRecommendationsResponse.status_code == 200

    guid = testUtilities.getGuidFromResponse(getInitialRowsOfRecommendationsResponse)

    regenerateRecommendationsResponse = requests.get(backendUrl + "/regenerateRecommendations?guid=" + guid)
    assert regenerateRecommendationsResponse.status_code == 200

    testUtilities.verifyAttributeExists(regenerateRecommendationsResponse, 'errorMessage')

def test_getInitialRowsOfRecommendations_bodyExists(backendUrl):
    filesToSend = testUtilities.getFilesToSend("imdb-no-recent-films.csv")
    
    getInitialRowsOfRecommendationsResponse = requests.post(backendUrl + "/getInitialRowsOfRecommendations", files=filesToSend)
    assert getInitialRowsOfRecommendationsResponse.status_code == 200

    testUtilities.verifyAttributeExists(getInitialRowsOfRecommendationsResponse, 'body')

def test_regenerateRowsOfRecommendations_bodyExists(backendUrl):
    filesToSend = testUtilities.getFilesToSend("imdb-no-recent-films.csv")
    
    getInitialRowsOfRecommendationsResponse = requests.post(backendUrl + "/getInitialRowsOfRecommendations", files=filesToSend)
    assert getInitialRowsOfRecommendationsResponse.status_code == 200

    guid = testUtilities.getGuidFromResponse(getInitialRowsOfRecommendationsResponse)

    regenerateRecommendationsResponse = requests.get(backendUrl + "/regenerateRecommendations?guid=" + guid)
    assert regenerateRecommendationsResponse.status_code == 200

    testUtilities.verifyAttributeExists(regenerateRecommendationsResponse, 'body')

def test_getInitialRowsOfRecommendations_noFile(backendUrl):
    filesToSend = {'file': ("", None)}
    response = requests.post(backendUrl + "/getInitialRowsOfRecommendations", files=filesToSend)

    assert response.status_code == 400
    
    testUtilities.verifyErrorMessage(response, ServiceUtilities.NO_FILE_IN_REQUEST_ERROR_MESSAGE)

def test_getInitialRowsOfRecommendations_unacceptedFileType(backendUrl):
    filesToSend = testUtilities.getFilesToSend("test.txt")
    response = requests.post(backendUrl + "/getInitialRowsOfRecommendations", files=filesToSend)

    assert response.status_code == 415

    testUtilities.verifyErrorMessage(response, ServiceUtilities.UNSUPPORTED_MEDIA_TYPE_ERROR_MESSAGE)

def test_getInitialRowsOfRecommendations_imdbIncorrectHeader(backendUrl):
    filesToSend = testUtilities.getFilesToSend("imdb-incorrect-header.csv")
    response = requests.post(backendUrl + "/getInitialRowsOfRecommendations", files=filesToSend)

    assert response.status_code == 400

    testUtilities.verifyErrorMessage(response, ServiceUtilities.FILE_ROW_HEADERS_UNEXPECTED_FORMAT_ERROR_MESSAGE)

def test_getInitialRowsOfRecommendations_imdbMissingHeader(backendUrl):
    filesToSend = testUtilities.getFilesToSend("imdb-missing-header.csv")
    response = requests.post(backendUrl + "/getInitialRowsOfRecommendations", files=filesToSend)

    assert response.status_code == 400

    testUtilities.verifyErrorMessage(response, ServiceUtilities.FILE_MORE_DATA_THAN_ROW_HEADERS_ERROR_MESSAGE)

def test_getInitialRowsOfRecommendations_letterboxdIncorrectHeaderCsv(backendUrl):
    filesToSend = testUtilities.getFilesToSend("letterboxd-incorrect-header.csv")
    response = requests.post(backendUrl + "/getInitialRowsOfRecommendations", files=filesToSend)

    assert response.status_code == 400

    testUtilities.verifyErrorMessage(response, ServiceUtilities.FILE_ROW_HEADERS_UNEXPECTED_FORMAT_ERROR_MESSAGE)

def test_getInitialRowsOfRecommendations_letterboxdMissingHeaderCsv(backendUrl):
    filesToSend = testUtilities.getFilesToSend("letterboxd-missing-header.csv")
    response = requests.post(backendUrl + "/getInitialRowsOfRecommendations", files=filesToSend)

    assert response.status_code == 400

    testUtilities.verifyErrorMessage(response, ServiceUtilities.FILE_MORE_DATA_THAN_ROW_HEADERS_ERROR_MESSAGE)

def test_getInitialRowsOfRecommendations_letterboxdIncorrectZip(backendUrl):
    filesToSend = testUtilities.getFilesToSend("letterboxd-incorrect.zip")
    
    response = requests.post(backendUrl + "/getInitialRowsOfRecommendations", files=filesToSend)

    assert response.status_code == 400

    testUtilities.verifyErrorMessage(response, ServiceUtilities.INVALID_ZIP_FILE_ERROR_MESSAGE)

def test_getInitialRowsOfRecommendations_imdbNoRecentFilms(backendUrl):
    filesToSend = testUtilities.getFilesToSend("imdb-no-recent-films.csv")
    
    getInitialRowsOfRecommendationsResponse = requests.post(backendUrl + "/getInitialRowsOfRecommendations", files=filesToSend)
    assert getInitialRowsOfRecommendationsResponse.status_code == 200

    expectedNumberOfFavouriteRows = 1
    expectedNumberOfRecentRows = 0
    expectedNumberOfGenreRows = ServiceUtilities.NUMBER_OF_GENRE_RECOMMENDATION_ROWS
    expectedNumberOfInternationalRows = 1
    expectedNumberOfOldRows = 1
    
    testUtilities.verifyRowsOfRecommendations(getInitialRowsOfRecommendationsResponse, expectedNumberOfFavouriteRows, expectedNumberOfRecentRows, 
                                              expectedNumberOfGenreRows, expectedNumberOfInternationalRows, expectedNumberOfOldRows)

def test_getInitialRowsOfRecommendations_letterboxdNoRecentFilms(backendUrl):
    filesToSend = testUtilities.getFilesToSend("letterboxd-no-recent-films.csv")
    
    getInitialRowsOfRecommendationsResponse = requests.post(backendUrl + "/getInitialRowsOfRecommendations", files=filesToSend)
    assert getInitialRowsOfRecommendationsResponse.status_code == 200

    expectedNumberOfFavouriteRows = 1
    expectedNumberOfRecentRows = 0
    expectedNumberOfGenreRows = ServiceUtilities.NUMBER_OF_GENRE_RECOMMENDATION_ROWS
    expectedNumberOfInternationalRows = 1
    expectedNumberOfOldRows = 1
    
    testUtilities.verifyRowsOfRecommendations(getInitialRowsOfRecommendationsResponse, expectedNumberOfFavouriteRows, expectedNumberOfRecentRows, 
                                              expectedNumberOfGenreRows, expectedNumberOfInternationalRows, expectedNumberOfOldRows)

def test_getInitialRowsOfRecommendations_imdbNoRecentAndFavouriteFilms(backendUrl):
    filesToSend = testUtilities.getFilesToSend("imdb-no-recent-and-favourite-films.csv")
    
    getInitialRowsOfRecommendationsResponse = requests.post(backendUrl + "/getInitialRowsOfRecommendations", files=filesToSend)
    assert getInitialRowsOfRecommendationsResponse.status_code == 200

    expectedNumberOfFavouriteRows = 0
    expectedNumberOfRecentRows = 0
    expectedNumberOfGenreRows = ServiceUtilities.NUMBER_OF_GENRE_RECOMMENDATION_ROWS
    expectedNumberOfInternationalRows = 1
    expectedNumberOfOldRows = 1
    
    testUtilities.verifyRowsOfRecommendations(getInitialRowsOfRecommendationsResponse, expectedNumberOfFavouriteRows, expectedNumberOfRecentRows, 
                                              expectedNumberOfGenreRows, expectedNumberOfInternationalRows, expectedNumberOfOldRows)

def test_getInitialRowsOfRecommendations_letterboxdNoRecentAndFavouriteFilms(backendUrl):
    filesToSend = testUtilities.getFilesToSend("letterboxd-no-recent-and-favourite-films.csv")
    
    getInitialRowsOfRecommendationsResponse = requests.post(backendUrl + "/getInitialRowsOfRecommendations", files=filesToSend)
    assert getInitialRowsOfRecommendationsResponse.status_code == 200

    expectedNumberOfFavouriteRows = 0
    expectedNumberOfRecentRows = 0
    expectedNumberOfGenreRows = ServiceUtilities.NUMBER_OF_GENRE_RECOMMENDATION_ROWS
    expectedNumberOfInternationalRows = 1
    expectedNumberOfOldRows = 1
    
    testUtilities.verifyRowsOfRecommendations(getInitialRowsOfRecommendationsResponse, expectedNumberOfFavouriteRows, expectedNumberOfRecentRows, 
                                              expectedNumberOfGenreRows, expectedNumberOfInternationalRows, expectedNumberOfOldRows)

def test_getInitialRowsOfRecommendations_imdbNoRecentAndInternationalFilms(backendUrl):
    filesToSend = testUtilities.getFilesToSend("imdb-no-recent-and-international-films.csv")
    
    getInitialRowsOfRecommendationsResponse = requests.post(backendUrl + "/getInitialRowsOfRecommendations", files=filesToSend)
    assert getInitialRowsOfRecommendationsResponse.status_code == 200

    expectedNumberOfFavouriteRows = 1
    expectedNumberOfRecentRows = 0
    expectedNumberOfGenreRows = ServiceUtilities.NUMBER_OF_GENRE_RECOMMENDATION_ROWS
    expectedNumberOfInternationalRows = 0
    expectedNumberOfOldRows = 1
    
    testUtilities.verifyRowsOfRecommendations(getInitialRowsOfRecommendationsResponse, expectedNumberOfFavouriteRows, expectedNumberOfRecentRows, 
                                              expectedNumberOfGenreRows, expectedNumberOfInternationalRows, expectedNumberOfOldRows)

def test_getInitialRowsOfRecommendations_letterboxdNoRecentAndInternationalFilms(backendUrl):
    filesToSend = testUtilities.getFilesToSend("letterboxd-no-recent-and-international-films.csv")
    
    getInitialRowsOfRecommendationsResponse = requests.post(backendUrl + "/getInitialRowsOfRecommendations", files=filesToSend)
    assert getInitialRowsOfRecommendationsResponse.status_code == 200

    expectedNumberOfFavouriteRows = 1
    expectedNumberOfRecentRows = 0
    expectedNumberOfGenreRows = ServiceUtilities.NUMBER_OF_GENRE_RECOMMENDATION_ROWS
    expectedNumberOfInternationalRows = 0
    expectedNumberOfOldRows = 1
    
    testUtilities.verifyRowsOfRecommendations(getInitialRowsOfRecommendationsResponse, expectedNumberOfFavouriteRows, expectedNumberOfRecentRows, 
                                              expectedNumberOfGenreRows, expectedNumberOfInternationalRows, expectedNumberOfOldRows)

def test_getInitialRowsOfRecommendations_imdbNoRecentAndTwoGenres_ensuresTwoGenreRows(backendUrl):
    filesToSend = testUtilities.getFilesToSend("imdb-no-recent-films-and-two-genres.csv")
    
    getInitialRowsOfRecommendationsResponse = requests.post(backendUrl + "/getInitialRowsOfRecommendations", files=filesToSend)
    assert getInitialRowsOfRecommendationsResponse.status_code == 200

    expectedNumberOfFavouriteRows = 1
    expectedNumberOfRecentRows = 0
    expectedNumberOfGenreRows = 2
    expectedNumberOfInternationalRows = 1
    expectedNumberOfOldRows = 1
    
    testUtilities.verifyRowsOfRecommendations(getInitialRowsOfRecommendationsResponse, expectedNumberOfFavouriteRows, expectedNumberOfRecentRows, 
                                              expectedNumberOfGenreRows, expectedNumberOfInternationalRows, expectedNumberOfOldRows)

def test_getInitialRowsOfRecommendations_letterboxdNoRecentAndTwoGenres_ensuresTwoGenreRows(backendUrl):
    filesToSend = testUtilities.getFilesToSend("letterboxd-no-recent-films-and-two-genres.csv")
    
    getInitialRowsOfRecommendationsResponse = requests.post(backendUrl + "/getInitialRowsOfRecommendations", files=filesToSend)
    assert getInitialRowsOfRecommendationsResponse.status_code == 200

    expectedNumberOfFavouriteRows = 1
    expectedNumberOfRecentRows = 0
    expectedNumberOfGenreRows = 2
    expectedNumberOfInternationalRows = 1
    expectedNumberOfOldRows = 1
    
    testUtilities.verifyRowsOfRecommendations(getInitialRowsOfRecommendationsResponse, expectedNumberOfFavouriteRows, expectedNumberOfRecentRows, 
                                              expectedNumberOfGenreRows, expectedNumberOfInternationalRows, expectedNumberOfOldRows)

def test_getInitialRowsOfRecommendations_imdbInternationalFilmAndNoRecentFilmsAndOneGenres_ensuresOneGenreRows(backendUrl):
    filesToSend = testUtilities.getFilesToSend("imdb-international-film-no-recent-films-and-one-genre.csv")
    
    getInitialRowsOfRecommendationsResponse = requests.post(backendUrl + "/getInitialRowsOfRecommendations", files=filesToSend)
    assert getInitialRowsOfRecommendationsResponse.status_code == 200

    expectedNumberOfFavouriteRows = 1
    expectedNumberOfRecentRows = 0
    expectedNumberOfGenreRows = 1
    expectedNumberOfInternationalRows = 1
    expectedNumberOfOldRows = 1
    
    testUtilities.verifyRowsOfRecommendations(getInitialRowsOfRecommendationsResponse, expectedNumberOfFavouriteRows, expectedNumberOfRecentRows, 
                                              expectedNumberOfGenreRows, expectedNumberOfInternationalRows, expectedNumberOfOldRows)

def test_getInitialRowsOfRecommendations_letterboxdInternationalFilmAndNoRecentFilmsAndOneGenres_ensuresOneGenreRows(backendUrl):
    filesToSend = testUtilities.getFilesToSend("letterboxd-international-film-no-recent-films-and-one-genre.csv")
    
    getInitialRowsOfRecommendationsResponse = requests.post(backendUrl + "/getInitialRowsOfRecommendations", files=filesToSend)
    assert getInitialRowsOfRecommendationsResponse.status_code == 200

    expectedNumberOfFavouriteRows = 1
    expectedNumberOfRecentRows = 0
    expectedNumberOfGenreRows = 1
    expectedNumberOfInternationalRows = 1
    expectedNumberOfOldRows = 1
    
    testUtilities.verifyRowsOfRecommendations(getInitialRowsOfRecommendationsResponse, expectedNumberOfFavouriteRows, expectedNumberOfRecentRows, 
                                              expectedNumberOfGenreRows, expectedNumberOfInternationalRows, expectedNumberOfOldRows)

def test_getInitialRowsOfRecommendations_imdbNoInternationalFilmsAndNoRecentFilmsAndOneGenres_ensuresOneGenreRows(backendUrl):
    filesToSend = testUtilities.getFilesToSend("imdb-american-film-no-recent-films-and-one-genre.csv")
    
    getInitialRowsOfRecommendationsResponse = requests.post(backendUrl + "/getInitialRowsOfRecommendations", files=filesToSend)
    assert getInitialRowsOfRecommendationsResponse.status_code == 200

    expectedNumberOfFavouriteRows = 1
    expectedNumberOfRecentRows = 0
    expectedNumberOfGenreRows = 1
    expectedNumberOfInternationalRows = 0
    expectedNumberOfOldRows = 1
    
    testUtilities.verifyRowsOfRecommendations(getInitialRowsOfRecommendationsResponse, expectedNumberOfFavouriteRows, expectedNumberOfRecentRows, 
                                              expectedNumberOfGenreRows, expectedNumberOfInternationalRows, expectedNumberOfOldRows)

def test_getInitialRowsOfRecommendations_letterboxdNoInternationalFilmsAndNoRecentFilmsAndOneGenres_ensuresOneGenreRows(backendUrl):
    filesToSend = testUtilities.getFilesToSend("letterboxd-american-film-no-recent-films-and-one-genre.csv")
    
    getInitialRowsOfRecommendationsResponse = requests.post(backendUrl + "/getInitialRowsOfRecommendations", files=filesToSend)
    assert getInitialRowsOfRecommendationsResponse.status_code == 200

    expectedNumberOfFavouriteRows = 1
    expectedNumberOfRecentRows = 0
    expectedNumberOfGenreRows = 1
    expectedNumberOfInternationalRows = 0
    expectedNumberOfOldRows = 1
    
    testUtilities.verifyRowsOfRecommendations(getInitialRowsOfRecommendationsResponse, expectedNumberOfFavouriteRows, expectedNumberOfRecentRows, 
                                              expectedNumberOfGenreRows, expectedNumberOfInternationalRows, expectedNumberOfOldRows)

def test_getInitialRowsOfRecommendations_letterboxdZipNoRecentFilms(backendUrl):
    filesToSend = testUtilities.getFilesToSend("letterboxd-no-recent.zip")
    
    getInitialRowsOfRecommendationsResponse = requests.post(backendUrl + "/getInitialRowsOfRecommendations", files=filesToSend)
    assert getInitialRowsOfRecommendationsResponse.status_code == 200

    expectedNumberOfFavouriteRows = 1
    expectedNumberOfRecentRows = 0
    expectedNumberOfGenreRows = ServiceUtilities.NUMBER_OF_GENRE_RECOMMENDATION_ROWS
    expectedNumberOfInternationalRows = 1
    expectedNumberOfOldRows = 1
    
    testUtilities.verifyRowsOfRecommendations(getInitialRowsOfRecommendationsResponse, expectedNumberOfFavouriteRows, expectedNumberOfRecentRows, 
                                              expectedNumberOfGenreRows, expectedNumberOfInternationalRows, expectedNumberOfOldRows)

def test_getInitialRowsOfRecommendations_imdbNoRecognisedFilms(backendUrl):
    filesToSend = testUtilities.getFilesToSend("imdb-no-recognised-films.csv")
    
    getInitialRowsOfRecommendationsResponse = requests.post(backendUrl + "/getInitialRowsOfRecommendations", files=filesToSend)
    assert getInitialRowsOfRecommendationsResponse.status_code == 200

    expectedNumberOfFavouriteRows = 0
    expectedNumberOfRecentRows = 0
    expectedNumberOfGenreRows = 0
    expectedNumberOfInternationalRows = 0
    expectedNumberOfOldRows = 0
    
    testUtilities.verifyRowsOfRecommendations(getInitialRowsOfRecommendationsResponse, expectedNumberOfFavouriteRows, expectedNumberOfRecentRows, 
                                              expectedNumberOfGenreRows, expectedNumberOfInternationalRows, expectedNumberOfOldRows)

def test_getInitialRowsOfRecommendations_letterboxdNoRecognisedFilms(backendUrl):
    filesToSend = testUtilities.getFilesToSend("letterboxd-no-recognised-films.csv")

    getInitialRowsOfRecommendationsResponse = requests.post(backendUrl + "/getInitialRowsOfRecommendations", files=filesToSend)
    assert getInitialRowsOfRecommendationsResponse.status_code == 200

    expectedNumberOfFavouriteRows = 0
    expectedNumberOfRecentRows = 0
    expectedNumberOfGenreRows = 0
    expectedNumberOfInternationalRows = 0
    expectedNumberOfOldRows = 0
    
    testUtilities.verifyRowsOfRecommendations(getInitialRowsOfRecommendationsResponse, expectedNumberOfFavouriteRows, expectedNumberOfRecentRows, 
                                              expectedNumberOfGenreRows, expectedNumberOfInternationalRows, expectedNumberOfOldRows)

def test_regenerateRowsOfRecommendations_imdb(backendUrl):
    filesToSend = testUtilities.getFilesToSend("imdb-no-recent-films.csv")
    
    getInitialRowsOfRecommendationsResponse = requests.post(backendUrl + "/getInitialRowsOfRecommendations", files=filesToSend)
    assert getInitialRowsOfRecommendationsResponse.status_code == 200

    guid = testUtilities.getGuidFromResponse(getInitialRowsOfRecommendationsResponse)

    regenerateRecommendationsResponse = requests.get(backendUrl + "/regenerateRecommendations?guid=" + guid)
    assert regenerateRecommendationsResponse.status_code == 200

    expectedNumberOfFavouriteRows = 1
    expectedNumberOfRecentRows = 0
    expectedNumberOfGenreRows = ServiceUtilities.NUMBER_OF_GENRE_RECOMMENDATION_ROWS
    expectedNumberOfInternationalRows = 1
    expectedNumberOfOldRows = 1
    
    testUtilities.verifyRowsOfRecommendations(regenerateRecommendationsResponse, expectedNumberOfFavouriteRows, expectedNumberOfRecentRows,
                                              expectedNumberOfGenreRows, expectedNumberOfInternationalRows, expectedNumberOfOldRows)

    testUtilities.verifyRegeneratedFilmsAreDifferentToInitialFilms(getInitialRowsOfRecommendationsResponse, regenerateRecommendationsResponse)

def test_regenerateRowsOfRecommendations_letterboxd(backendUrl):
    filesToSend = testUtilities.getFilesToSend("letterboxd-no-recent-films.csv")
    
    getInitialRowsOfRecommendationsResponse = requests.post(backendUrl + "/getInitialRowsOfRecommendations", files=filesToSend)
    assert getInitialRowsOfRecommendationsResponse.status_code == 200

    guid = testUtilities.getGuidFromResponse(getInitialRowsOfRecommendationsResponse)

    regenerateRecommendationsResponse = requests.get(backendUrl + "/regenerateRecommendations?guid=" + guid)
    assert regenerateRecommendationsResponse.status_code == 200

    expectedNumberOfFavouriteRows = 1
    expectedNumberOfRecentRows = 0
    expectedNumberOfGenreRows = ServiceUtilities.NUMBER_OF_GENRE_RECOMMENDATION_ROWS
    expectedNumberOfInternationalRows = 1
    expectedNumberOfOldRows = 1
    
    testUtilities.verifyRowsOfRecommendations(regenerateRecommendationsResponse, expectedNumberOfFavouriteRows, expectedNumberOfRecentRows,
                                              expectedNumberOfGenreRows, expectedNumberOfInternationalRows, expectedNumberOfOldRows)

    testUtilities.verifyRegeneratedFilmsAreDifferentToInitialFilms(getInitialRowsOfRecommendationsResponse, regenerateRecommendationsResponse)

def test_getInitialRowsOfRecommendations_successfulResponse_shouldHaveEmptyErrorMessage(backendUrl):
    filesToSend = testUtilities.getFilesToSend("letterboxd-no-recent-films.csv")

    getInitialRowsOfRecommendationsResponse = requests.post(backendUrl + "/getInitialRowsOfRecommendations", files=filesToSend)
    assert getInitialRowsOfRecommendationsResponse.status_code == 200

    testUtilities.verifyErrorMessage(getInitialRowsOfRecommendationsResponse, "")

def test_regenerateRecommendations_successfulResponse_shouldHaveEmptyErrorMessage(backendUrl):
    filesToSend = testUtilities.getFilesToSend("letterboxd-no-recent-films.csv")

    getInitialRowsOfRecommendationsResponse = requests.post(backendUrl + "/getInitialRowsOfRecommendations", files=filesToSend)
    assert getInitialRowsOfRecommendationsResponse.status_code == 200

    guid = testUtilities.getGuidFromResponse(getInitialRowsOfRecommendationsResponse)

    regenerateRecommendationsResponse = requests.get(backendUrl + "/regenerateRecommendations?guid=" + guid)
    assert regenerateRecommendationsResponse.status_code == 200

    testUtilities.verifyErrorMessage(regenerateRecommendationsResponse, "")

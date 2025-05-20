import os
import requests
import sys
absolutePathOfCurrentFile = os.path.dirname(os.path.abspath(__file__))
backendDirectory = os.path.dirname(absolutePathOfCurrentFile)
sys.path.append(backendDirectory)
from DocumentDatabase import *
from ServiceUtilities import *

class TestUtilities:

    LOCAL_DEPLOYMENT_URL = "http://localhost:60000"
    PROD_DEPLOYMENT_URL = "http://localhost:60000"
    TEST_UPLOAD_FILES_DIRECTORY = "test-upload-files/"

    def __init__(self, database):
        self.database = database


    def verifyFilm(self, film, imdbFilmId, allGenres, allCountries):
        assert 'title' in film
        assert film['title'] != ""

        assert 'letterboxdTitle' in film
        assert film['letterboxdTitle'] != ""

        assert 'year' in film
        assert film['year'] != None
        assert film['year'] != 0

        assert 'letterboxdYear' in film
        assert film['letterboxdYear'] != None
        assert film['letterboxdYear'] != 0

        assert 'imdbRating' in film
        assert film['imdbRating'] != None
        assert film['imdbRating'] >= 1.0
        assert film['imdbRating'] <= 10.0

        assert 'numberOfVotes' in film
        assert film['numberOfVotes'] != None
        assert film['numberOfVotes'] >= NUMBER_OF_VOTES_THRESHOLD

        assert 'runtime' in film
        assert film['runtime'] != None
        assert film['runtime'] >= RUNTIME_THRESHOLD

        assert 'runtimeHoursMinutes' in film
        assert film['runtime'] != ""

        assert 'genres' in film
        assert len(film['genres']) > 0

        for genre in film['genres']:
            assert genre in allGenres

        assert 'imdbUrl' in film
        assert film['imdbUrl'] == BASE_IMDB_URL + imdbFilmId

        assert 'countries' in film

        for country in film['countries']:
            assert country in allCountries

        assert 'poster' in film
        assert film['poster'] != ""

        assert 'summary' in film
        assert film['summary'] != ""

    def verifyRowsOfRecommendations(self, response, expectedNumberOfFavouriteRows, expectedNumberOfRecentRows, 
                                    expectedNumberOfGenreRows, expectedNumberOfInternationalRows, expectedNumberOfOldRows):
        responseContent = response.json()
        rowsOfRecommendations = responseContent["body"]

        allGenres = self.database.read("AllGenres")
        allCountries = self.database.read("AllCountries")

        assert len(rowsOfRecommendations) == (expectedNumberOfFavouriteRows + expectedNumberOfRecentRows + expectedNumberOfGenreRows + 
                                              expectedNumberOfInternationalRows + expectedNumberOfOldRows)

        for row in rowsOfRecommendations:
            assert 'recommendedRowText' in row
            assert row['recommendedRowText'] != ""
            
            assert 'profileId' in row
            assert row['profileId'] != ""

            assert 'recommendedFilms' in row
            assert len(row['recommendedFilms']) == MAX_NUMBER_OF_RECOMMENDATIONS_PER_ROW

            for film in row['recommendedFilms']:
                assert 'imdbFilmId' in film
                assert film['imdbFilmId'] != ""
                self.verifyFilm(film, film['imdbFilmId'], allGenres, allCountries)
                assert 'similarityScore' in film
                assert film['similarityScore'] != None
                assert film['similarityScore'] >= 0.0
                assert film['similarityScore'] <= 100.0

        self.verifyExpectedNumberOfRows(rowsOfRecommendations, expectedNumberOfFavouriteRows, ["favourite"])
        self.verifyExpectedNumberOfRows(rowsOfRecommendations, expectedNumberOfRecentRows, ["recent"])
        self.verifyExpectedNumberOfRows(rowsOfRecommendations, expectedNumberOfGenreRows, allGenres)
        self.verifyExpectedNumberOfRows(rowsOfRecommendations, expectedNumberOfInternationalRows, ["international"])
        self.verifyExpectedNumberOfRows(rowsOfRecommendations, expectedNumberOfOldRows, ["old"])

    def getFilesToSend(self, fileName):
        file = open(self.TEST_UPLOAD_FILES_DIRECTORY + fileName, 'rb')
        return {'file': (fileName, file)}

    def getGuidFromResponse(self, response):
        responseContent = response.json()
        return responseContent["guid"]

    def verifyRegeneratedFilmsAreDifferentToInitialFilms(self, getInitialRowsOfRecommendationsResponse, regenerateRecommendationsResponse):
        initialRecommendationFilmIds = []

        getInitialRowsOfRecommendationsResponseContent = getInitialRowsOfRecommendationsResponse.json()
        initialRecommendations = getInitialRowsOfRecommendationsResponseContent["body"]

        for rowOfFilms in initialRecommendations:
            for recommendedFilm in rowOfFilms['recommendedFilms']:
                initialRecommendationFilmIds.append(recommendedFilm['imdbFilmId'])

        regenerateRecommendationsResponseContent = regenerateRecommendationsResponse.json()
        regeneratedRecommendations = regenerateRecommendationsResponseContent["body"]

        for rowOfFilms in regeneratedRecommendations:
            for recommendedFilm in rowOfFilms['recommendedFilms']:
                assert recommendedFilm['imdbFilmId'] not in initialRecommendationFilmIds

    def verifyExpectedNumberOfRows(self, rowsOfRecommendations, expectedNumberOfRows, profileIds):
        actualNumberOfRows = 0

        for row in rowsOfRecommendations:
            if row['profileId'] in profileIds:
                actualNumberOfRows += 1

        assert expectedNumberOfRows == actualNumberOfRows

    def verifyErrorMessage(self, response, expectedErrorMessage):
        responseContent = response.json()
        assert responseContent["errorMessage"] == expectedErrorMessage

    def verifyAttributeExists(self, response, attribute):
        responseContent = response.json()
        assert attribute in responseContent

    def verifyReviewsOfAllRecommendations(self, response, isThumbsUp, backendUrl):
        responseContent = response.json()
        rowsOfRecommendations = responseContent["body"]

        guid = self.getGuidFromResponse(response)

        for row in rowsOfRecommendations:
            for recommendedFilm in row['recommendedFilms']:
                imdbFilmId = recommendedFilm['imdbFilmId']
                reviewRecommendationResponse = requests.get(backendUrl + "/reviewRecommendation?guid=" + guid + "&imdbFilmId=" + imdbFilmId + "&isThumbsUp=" + str(isThumbsUp))
                self.verifyReviewRecommendationResponse(reviewRecommendationResponse, imdbFilmId, isThumbsUp)

    def verifyReviewRecommendationResponse(self, reviewRecommendationsResponse, imdbFilmId, isThumbsUp):
        responseContent = reviewRecommendationsResponse.json()
        responseBody = responseContent["body"]

        assert imdbFilmId in responseBody
        
        if isThumbsUp:
            assert "Up" in responseBody
        else:
            assert "Down" in responseBody

import os
import sys
absolutePathOfCurrentFile = os.path.dirname(os.path.abspath(__file__))
backendDirectory = os.path.dirname(absolutePathOfCurrentFile)
sys.path.append(backendDirectory)
from DocumentDatabase import *
from ServiceUtilities import *
from InitDatabase import *

class TestUtilities:

    LOCAL_DEPLOYMENT_URL = "http://localhost:60000"
    PROD_DEPLOYMENT_URL = "https://film-rec-backend.onrender.com"
    TEST_UPLOAD_FILES_DIRECTORY = "test-upload-files/"

    def __init__(self, _repositoryRoot):
        self.repositoryRoot = _repositoryRoot


    def verifyFilm(self, film, filmId, allGenres, allCountries):
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
        assert film['numberOfVotes'] >= InitDatabase.NUMBER_OF_VOTES_THRESHOLD

        assert 'runtime' in film
        assert film['runtime'] != None
        assert film['runtime'] >= InitDatabase.RUNTIME_THRESHOLD

        assert 'runtimeHoursMinutes' in film
        assert film['runtime'] != ""

        assert 'genres' in film
        assert len(film['genres']) > 0

        for genre in film['genres']:
            assert genre in allGenres

        assert 'imdbUrl' in film
        assert film['imdbUrl'] == InitDatabase.BASE_IMDB_URL + filmId

        assert 'countries' in film

        for country in film['countries']:
            assert country in allCountries

        assert 'poster' in film
        assert film['poster'] != ""

        assert 'summary' in film
        assert film['summary'] != ""

    def verifyRowsOfRecommendations(self, rowsOfRecommendations, totalNumberOfRows):
        database = DocumentDatabase(self.repositoryRoot)
        allGenres = database.read("AllGenres")
        allCountries = database.read("AllCountries")

        assert len(rowsOfRecommendations) == totalNumberOfRows

        for row in rowsOfRecommendations:
            assert 'recommendedRowText' in row
            assert row['recommendedRowText'] != ""
            
            assert 'profileId' in row
            assert row['profileId'] != ""

            assert 'recommendedFilms' in row
            assert len(row['recommendedFilms']) == ServiceUtilities.NUMBER_OF_RECOMMENDATIONS_PER_ROW

            for film in row['recommendedFilms']:
                assert 'id' in film
                assert film['id'] != ""
                self.verifyFilm(film, film['id'], allGenres, allCountries)
                assert 'similarityScore' in film
                assert film['similarityScore'] != None
                assert film['similarityScore'] >= 0.0
                assert film['similarityScore'] <= 100.0

    def getFilesToSend(self, fileName):
        file = open(self.TEST_UPLOAD_FILES_DIRECTORY + fileName, 'rb')
        return {'file': (fileName, file)}

import json
import os
import sys
absolutePathOfCurrentFile = os.path.dirname(os.path.abspath(__file__))
backendDirectory = os.path.dirname(absolutePathOfCurrentFile)
sys.path.append(backendDirectory)
import app
import initDatabase

cacheFileLocation = "../../../database/cache.json"
LOCAL_DEPLOYMENT_URL = "http://localhost:60000"
PROD_DEPLOYMENT_URL = "https://film-rec-backend.onrender.com"

def verifyFilm(film, filmId, allGenres, allCountries):
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
    assert film['numberOfVotes'] >= initDatabase.NUMBER_OF_VOTES_THRESHOLD

    assert 'runtime' in film
    assert film['runtime'] != None
    assert film['runtime'] >= initDatabase.RUNTIME_THRESHOLD

    assert 'runtimeHoursMinutes' in film
    assert film['runtime'] != ""

    assert 'genres' in film
    assert len(film['genres']) > 0

    for genre in film['genres']:
        assert genre in allGenres

    assert 'imdbUrl' in film
    assert film['imdbUrl'] == initDatabase.BASE_IMDB_URL + filmId

    assert 'countries' in film

    for country in film['countries']:
        assert country in allCountries

    assert 'poster' in film
    assert film['poster'] != ""

    assert 'summary' in film
    assert film['summary'] != ""

def verifyRowsOfRecommendations(rowsOfRecommendations, totalNumberOfRows):
    cacheFile = open(cacheFileLocation)
    cache = json.load(cacheFile)

    assert len(rowsOfRecommendations) == totalNumberOfRows

    for row in rowsOfRecommendations:
        assert 'recommendedRowText' in row
        assert row['recommendedRowText'] != ""
        
        assert 'profileId' in row
        assert row['profileId'] != ""

        assert 'recommendedFilms' in row
        assert len(row['recommendedFilms']) == app.NUMBER_OF_RECOMMENDATIONS_PER_ROW

        for film in row['recommendedFilms']:
            assert 'id' in film
            assert film['id'] != ""
            verifyFilm(film, film['id'], cache['allGenres'], cache['allCountries'])
            assert 'similarityScore' in film
            assert film['similarityScore'] != None
            assert film['similarityScore'] >= 0.0
            assert film['similarityScore'] <= 100.0

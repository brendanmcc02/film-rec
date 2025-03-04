import os
import sys
# import the needed file from backend directory
# (this is ugly as hell, there's probably an easier way but it gets the job done)
absolutePathOfCurrentFile = os.path.dirname(os.path.abspath(__file__))
parentDirectoryOfCurrentFile = os.path.dirname(absolutePathOfCurrentFile)
sys.path.append(parentDirectoryOfCurrentFile)
import initAllFilmData

cacheFileLocation = "../../database/cache.json"

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
    assert film['numberOfVotes'] >= initAllFilmData.NUMBER_OF_VOTES_THRESHOLD

    assert 'runtime' in film
    assert film['runtime'] != None
    assert film['runtime'] >= initAllFilmData.RUNTIME_THRESHOLD

    assert 'runtimeHoursMinutes' in film
    assert film['runtime'] != ""

    assert 'genres' in film
    assert len(film['genres']) > 0

    for genre in film['genres']:
        assert genre in allGenres

    assert 'imdbUrl' in film
    assert film['imdbUrl'] == initAllFilmData.BASE_IMDB_URL + filmId

    assert 'countries' in film

    for country in film['countries']:
        assert country in allCountries

    assert 'poster' in film
    assert film['poster'] != ""

    assert 'summary' in film
    assert film['summary'] != ""

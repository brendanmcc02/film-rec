import pytest
import json

allFilmDataFileLocation = "../../database/all-film-data.json"
cachedTmdbFilmDataLocation = "../../database/cached-tmdb-film-data.json"
cachedLetterboxdTitlesLocation = "../../database/cached-letterboxd-titles.json"

def test_allFilmDataFileExists():
    try:
        with open(allFilmDataFileLocation, encoding='utf-8') as allFilmDataFile:
            json.load(allFilmDataFile)

    except FileNotFoundError:
        pytest.fail("File not found.")
    except json.JSONDecodeError:
        pytest.fail("JSON decode error.")
    except Exception as e:
        pytest.fail("File open error.")


def test_allFilmsHaveValidTitles():
    allFilmDataFile = open(allFilmDataFileLocation)
    allFilmData = json.load(allFilmDataFile)

    for filmId in allFilmData:
        assert 'title' in allFilmData[filmId]
        assert allFilmData[filmId]['title'] != ""

def test_allFilmsHaveValidLetterboxdTitles():
    allFilmDataFile = open(allFilmDataFileLocation)
    allFilmData = json.load(allFilmDataFile)

    for filmId in allFilmData:
        assert 'letterboxdTitle' in allFilmData[filmId]
        assert allFilmData[filmId]['letterboxdTitle'] != ""

def test_allFilmsHaveValidYear():
    allFilmDataFile = open(allFilmDataFileLocation)
    allFilmData = json.load(allFilmDataFile)

    for filmId in allFilmData:
        assert 'year' in allFilmData[filmId]
        assert allFilmData[filmId]['year'] != None

def test_allFilmsHaveValidLetterboxdYear():
    allFilmDataFile = open(allFilmDataFileLocation)
    allFilmData = json.load(allFilmDataFile)

    for filmId in allFilmData:
        assert 'letterboxdYear' in allFilmData[filmId]
        assert allFilmData[filmId]['letterboxdYear'] != 0
        assert allFilmData[filmId]['letterboxdYear'] != None

def test_allFilmsHaveValidImdbRating():
    allFilmDataFile = open(allFilmDataFileLocation)
    allFilmData = json.load(allFilmDataFile)

    for filmId in allFilmData:
        assert 'imdbRating' in allFilmData[filmId]
        assert allFilmData[filmId]['imdbRating'] != None

def test_allFilmsHaveValidNumberOfVotes():
    allFilmDataFile = open(allFilmDataFileLocation)
    allFilmData = json.load(allFilmDataFile)

    for filmId in allFilmData:
        assert 'numberOfVotes' in allFilmData[filmId]
        assert allFilmData[filmId]['numberOfVotes'] != None
        assert allFilmData[filmId]['numberOfVotes'] != 0

def test_allFilmsHaveValidRuntime():
    allFilmDataFile = open(allFilmDataFileLocation)
    allFilmData = json.load(allFilmDataFile)

    for filmId in allFilmData:
        assert 'runtime' in allFilmData[filmId]
        assert allFilmData[filmId]['runtime'] != None
        assert allFilmData[filmId]['runtime'] != 0

def test_allFilmsHaveValidRuntimeHoursMinutes():
    allFilmDataFile = open(allFilmDataFileLocation)
    allFilmData = json.load(allFilmDataFile)

    for filmId in allFilmData:
        assert 'runtimeHoursMinutes' in allFilmData[filmId]
        assert allFilmData[filmId]['runtime'] != ""

def test_allFilmsHaveValidGenres():
    allFilmDataFile = open(allFilmDataFileLocation)
    allFilmData = json.load(allFilmDataFile)

    for filmId in allFilmData:
        assert 'genres' in allFilmData[filmId]
        assert len(allFilmData[filmId]['genres']) > 0

        for genre in allFilmData[filmId]['genres']:
            assert genre != ""

def test_allFilmsHaveValidImdbUrls():
    allFilmDataFile = open(allFilmDataFileLocation)
    allFilmData = json.load(allFilmDataFile)

    for filmId in allFilmData:
        assert 'imdbUrl' in allFilmData[filmId]
        assert allFilmData[filmId]['imdbUrl'] != ""

def test_allFilmsHaveValidCountries():
    allFilmDataFile = open(allFilmDataFileLocation)
    allFilmData = json.load(allFilmDataFile)

    for filmId in allFilmData:
        assert 'countries' in allFilmData[filmId]

        for country in allFilmData[filmId]['countries']:
            assert country != ""

def test_allFilmsHaveValidPosters():
    allFilmDataFile = open(allFilmDataFileLocation)
    allFilmData = json.load(allFilmDataFile)

    for filmId in allFilmData:
        assert 'poster' in allFilmData[filmId]
        assert allFilmData[filmId]['poster'] != ""

def test_allFilmsHaveValidSummaries():
    allFilmDataFile = open(allFilmDataFileLocation)
    allFilmData = json.load(allFilmDataFile)

    for filmId in allFilmData:
        assert 'summary' in allFilmData[filmId]
        assert allFilmData[filmId]['summary'] != ""

def test_allCachedTmdbFilmsHaveValidLetterboxdTitles():
    cachedTmdbFilmDataFile = open(cachedTmdbFilmDataLocation)
    cachedTmdbFilmData = json.load(cachedTmdbFilmDataFile)

    for filmId in cachedTmdbFilmData:
        assert 'letterboxdTitle' in cachedTmdbFilmData[filmId]
        assert cachedTmdbFilmData[filmId]['letterboxdTitle'] != ""

def test_allCachedTmdbFilmsHaveValidLetterboxdYears():
    cachedTmdbFilmDataFile = open(cachedTmdbFilmDataLocation)
    cachedTmdbFilmData = json.load(cachedTmdbFilmDataFile)

    for filmId in cachedTmdbFilmData:
        assert 'letterboxdYear' in cachedTmdbFilmData[filmId]
        assert cachedTmdbFilmData[filmId]['letterboxdYear'] != None

def test_allCachedTmdbFilmsHaveValidCountries():
    cachedTmdbFilmDataFile = open(cachedTmdbFilmDataLocation)
    cachedTmdbFilmData = json.load(cachedTmdbFilmDataFile)

    for filmId in cachedTmdbFilmData:
        assert 'countries' in cachedTmdbFilmData[filmId]

        for country in cachedTmdbFilmData[filmId]['countries']:
            assert country != ""

def test_allCachedTmdbFilmsHaveValidLetterboxdPosters():
    cachedTmdbFilmDataFile = open(cachedTmdbFilmDataLocation)
    cachedTmdbFilmData = json.load(cachedTmdbFilmDataFile)

    for filmId in cachedTmdbFilmData:
        assert 'poster' in cachedTmdbFilmData[filmId]
        assert cachedTmdbFilmData[filmId]['poster'] != ""

def test_allCachedTmdbFilmsHaveValidLetterboxdSummaries():
    cachedTmdbFilmDataFile = open(cachedTmdbFilmDataLocation)
    cachedTmdbFilmData = json.load(cachedTmdbFilmDataFile)

    for filmId in cachedTmdbFilmData:
        assert 'summary' in cachedTmdbFilmData[filmId]
        assert cachedTmdbFilmData[filmId]['summary'] != ""

def test_cachedLetterboxdTitles():
    cachedLetterboxdTitlesFile = open(cachedLetterboxdTitlesLocation)
    cachedLetterboxdTitles = json.load(cachedLetterboxdTitlesFile)

    for letterboxdTitle in cachedLetterboxdTitles:
        assert len(cachedLetterboxdTitles[letterboxdTitle]) > 0

        for film in cachedLetterboxdTitles[letterboxdTitle]:
            assert 'imdbFilmId' in film
            assert film['imdbFilmId'] != ""
            
            for year in film['years']:
                assert year != None
                assert year > 0

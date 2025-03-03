import pytest
import json

allFilmDataFileLocation = "../../database/all-film-data.json"
cachedTmdbFilmDataLocation = "../../database/cached-tmdb-film-data.json"
cachedLetterboxdTitlesLocation = "../../database/cached-letterboxd-titles.json"
allFilmDataVectorizedLocation = "../../database/all-film-data-vectorized.json"
allFilmDataVectorizedMagnitudesLocation = "../../database/all-film-data-vectorized-magnitudes.json"
cacheLocation = "../../database/cache.json"

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


def test_allFilmData():
    allFilmDataFile = open(allFilmDataFileLocation)
    allFilmData = json.load(allFilmDataFile)

    for filmId in allFilmData:
        assert 'title' in allFilmData[filmId]
        assert allFilmData[filmId]['title'] != ""

        assert 'letterboxdTitle' in allFilmData[filmId]
        assert allFilmData[filmId]['letterboxdTitle'] != ""

        assert 'year' in allFilmData[filmId]
        assert allFilmData[filmId]['year'] != None

        assert 'letterboxdYear' in allFilmData[filmId]
        assert allFilmData[filmId]['letterboxdYear'] != 0
        assert allFilmData[filmId]['letterboxdYear'] != None

        assert 'imdbRating' in allFilmData[filmId]
        assert allFilmData[filmId]['imdbRating'] != None

        assert 'numberOfVotes' in allFilmData[filmId]
        assert allFilmData[filmId]['numberOfVotes'] != None
        assert allFilmData[filmId]['numberOfVotes'] != 0

        assert 'runtime' in allFilmData[filmId]
        assert allFilmData[filmId]['runtime'] != None
        assert allFilmData[filmId]['runtime'] != 0

        assert 'runtimeHoursMinutes' in allFilmData[filmId]
        assert allFilmData[filmId]['runtime'] != ""

        assert 'genres' in allFilmData[filmId]
        assert len(allFilmData[filmId]['genres']) > 0

        for genre in allFilmData[filmId]['genres']:
            assert genre != ""
    
        assert 'imdbUrl' in allFilmData[filmId]
        assert allFilmData[filmId]['imdbUrl'] != ""

        assert 'countries' in allFilmData[filmId]

        for country in allFilmData[filmId]['countries']:
            assert country != ""

        assert 'poster' in allFilmData[filmId]
        assert allFilmData[filmId]['poster'] != ""

        assert 'summary' in allFilmData[filmId]
        assert allFilmData[filmId]['summary'] != ""

def test_cachedTmdbFilmData():
    cachedTmdbFilmDataFile = open(cachedTmdbFilmDataLocation)
    cachedTmdbFilmData = json.load(cachedTmdbFilmDataFile)

    for filmId in cachedTmdbFilmData:
        assert 'letterboxdTitle' in cachedTmdbFilmData[filmId]
        assert cachedTmdbFilmData[filmId]['letterboxdTitle'] != ""

        assert 'letterboxdYear' in cachedTmdbFilmData[filmId]
        assert cachedTmdbFilmData[filmId]['letterboxdYear'] != None

        assert 'countries' in cachedTmdbFilmData[filmId]

        for country in cachedTmdbFilmData[filmId]['countries']:
            assert country != ""

        assert 'poster' in cachedTmdbFilmData[filmId]
        assert cachedTmdbFilmData[filmId]['poster'] != ""

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

def test_allFilmDataVectorized():
    allFilmDataVectorizedFile = open(allFilmDataVectorizedLocation)
    allFilmDataVectorized = json.load(allFilmDataVectorizedFile)

    for filmId in allFilmDataVectorized:
        assert len(allFilmDataVectorized[filmId]) > 0
        
        for dimension in allFilmDataVectorized[filmId]:
            assert dimension >= 0.0 and dimension <= 1.0

def test_allFilmDataVectorizedMagnitudes():
    allFilmDataVectorizedMagnitudesFile = open(allFilmDataVectorizedMagnitudesLocation)
    allFilmDataVectorizedMagnitudes = json.load(allFilmDataVectorizedMagnitudesFile)

    for filmId in allFilmDataVectorizedMagnitudes:
        assert allFilmDataVectorizedMagnitudes[filmId] != None

def test_cache():
    cacheFile = open(cacheLocation)
    cache = json.load(cacheFile)

    assert 'allGenres' in cache

    for genre in cache['allGenres']:
        assert genre != ""

    assert 'allCountries' in cache

    for country in cache['allCountries']:
        assert country != ""

    assert 'normalizedYears' in cache

    for normalizedYear in cache['normalizedYears']:
        assert (cache['normalizedYears'][normalizedYear] >= 0.0  
                and cache['normalizedYears'][normalizedYear] <= 1.0)

    assert 'normalizedImdbRatings' in cache

    for normalizedImdbRating in cache['normalizedImdbRatings']:
        assert (cache['normalizedImdbRatings'][normalizedImdbRating] >= 0.0 
                and cache['normalizedImdbRatings'][normalizedImdbRating] <= 1.0)

    assert 'normalizedRuntimes' in cache

    for normalizedRuntime in cache['normalizedRuntimes']:
        assert (cache['normalizedRuntimes'][normalizedRuntime] >= 0.0 
                and cache['normalizedRuntimes'][normalizedRuntime] <= 1.0)

    assert 'minNumberOfVotes' in cache
    assert cache['minNumberOfVotes'] != None
    assert cache['minNumberOfVotes'] > 0

    assert 'diffNumberOfVotes' in cache
    assert cache['diffNumberOfVotes'] != None
    assert cache['diffNumberOfVotes'] >= 0

    assert 'profileVectorLength' in cache
    assert cache['profileVectorLength'] != None
    assert cache['profileVectorLength'] > 0

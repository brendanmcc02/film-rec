import json
import numpy as np
import os
import pytest
import sys
absolutePathOfCurrentFile = os.path.dirname(os.path.abspath(__file__))
testRootDirectory = os.path.dirname(absolutePathOfCurrentFile)
backendRootDirectory = os.path.dirname(testRootDirectory)
sys.path.append(testRootDirectory)
sys.path.append(backendRootDirectory)
import initDocumentDatabase
import testUtilities

allFilmDataFileLocation = "../../../database/all-film-data.json"
cachedTmdbFilmDataFileLocation = "../../../database/cached-tmdb-film-data.json"
cachedLetterboxdTitlesFileLocation = "../../../database/cached-letterboxd-titles.json"
allFilmDataVectorizedFileLocation = "../../../database/all-film-data-vectorized.json"
allFilmDataVectorizedMagnitudesFileLocation = "../../../database/all-film-data-vectorized-magnitudes.json"

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

def test_cachedTmdbFilmDataFileExists():
    try:
        with open(cachedTmdbFilmDataFileLocation, encoding='utf-8') as cachedTmdbFilmDataFile:
            json.load(cachedTmdbFilmDataFile)

    except FileNotFoundError:
        pytest.fail("File not found.")
    except json.JSONDecodeError:
        pytest.fail("JSON decode error.")
    except Exception as e:
        pytest.fail("File open error.")

def test_cachedLetterboxdTitlesFileExists():
    try:
        with open(cachedLetterboxdTitlesFileLocation, encoding='utf-8') as cachedLetterboxdTitlesFile:
            json.load(cachedLetterboxdTitlesFile)

    except FileNotFoundError:
        pytest.fail("File not found.")
    except json.JSONDecodeError:
        pytest.fail("JSON decode error.")
    except Exception as e:
        pytest.fail("File open error.")

def test_allFilmDataVectorizedFileExists():
    try:
        with open(allFilmDataVectorizedFileLocation, encoding='utf-8') as allFilmDataVectorizedFile:
            json.load(allFilmDataVectorizedFile)

    except FileNotFoundError:
        pytest.fail("File not found.")
    except json.JSONDecodeError:
        pytest.fail("JSON decode error.")
    except Exception as e:
        pytest.fail("File open error.")

def test_allFilmDataVectorizedMagnitudesFileExists():
    try:
        with open(allFilmDataVectorizedMagnitudesFileLocation, encoding='utf-8') as allFilmDataVectorizedMagnitudesFile:
            json.load(allFilmDataVectorizedMagnitudesFile)

    except FileNotFoundError:
        pytest.fail("File not found.")
    except json.JSONDecodeError:
        pytest.fail("JSON decode error.")
    except Exception as e:
        pytest.fail("File open error.")

def test_cacheFileExists():
    try:
        with open(testUtilities.cacheFileLocation, encoding='utf-8') as cacheFile:
            json.load(cacheFile)

    except FileNotFoundError:
        pytest.fail("File not found.")
    except json.JSONDecodeError:
        pytest.fail("JSON decode error.")
    except Exception as e:
        pytest.fail("File open error.")

def test_allFilmData():
    allFilmDataFile = open(allFilmDataFileLocation)
    allFilmData = json.load(allFilmDataFile)
    cacheFile = open(testUtilities.cacheFileLocation)
    cache = json.load(cacheFile)

    for filmId in allFilmData:
        testUtilities.verifyFilm(allFilmData[filmId], filmId, cache['allGenres'], cache['allCountries'])

def test_cachedTmdbFilmData():
    cachedTmdbFilmDataFile = open(cachedTmdbFilmDataFileLocation)
    cachedTmdbFilmData = json.load(cachedTmdbFilmDataFile)
    cacheFile = open(testUtilities.cacheFileLocation)
    cache = json.load(cacheFile)

    for filmId in cachedTmdbFilmData:
        assert 'letterboxdTitle' in cachedTmdbFilmData[filmId]
        assert cachedTmdbFilmData[filmId]['letterboxdTitle'] != ""

        assert 'letterboxdYear' in cachedTmdbFilmData[filmId]
        assert cachedTmdbFilmData[filmId]['letterboxdYear'] != None

        assert 'countries' in cachedTmdbFilmData[filmId]

        for country in cachedTmdbFilmData[filmId]['countries']:
            assert country in cache['allCountries']

        assert 'poster' in cachedTmdbFilmData[filmId]
        assert cachedTmdbFilmData[filmId]['poster'] != ""

        assert 'summary' in cachedTmdbFilmData[filmId]
        assert cachedTmdbFilmData[filmId]['summary'] != ""

def test_cachedLetterboxdTitles():
    cachedLetterboxdTitlesFile = open(cachedLetterboxdTitlesFileLocation)
    cachedLetterboxdTitles = json.load(cachedLetterboxdTitlesFile)

    for letterboxdTitle in cachedLetterboxdTitles:
        assert letterboxdTitle != ""
        assert len(cachedLetterboxdTitles[letterboxdTitle]) > 0

        for film in cachedLetterboxdTitles[letterboxdTitle]:
            assert 'imdbFilmId' in film
            assert film['imdbFilmId'] != ""
            
            # should only be 1 year (if the years match between IMDb & Letterboxd),
            # or 2 years (one for IMDb, one for Letterboxd). No more.
            assert len(film['years']) == 1 or len(film['years']) == 2
            for year in film['years']:
                assert year != None
                assert year > 0

def test_allFilmDataVectorized():
    allFilmDataFile = open(allFilmDataFileLocation)
    allFilmData = json.load(allFilmDataFile)
    allFilmDataVectorizedFile = open(allFilmDataVectorizedFileLocation)
    allFilmDataVectorized = json.load(allFilmDataVectorizedFile)
    cacheFile = open(testUtilities.cacheFileLocation)
    cache = json.load(cacheFile)

    assert len(allFilmData) == len(allFilmDataVectorized)

    for filmId in allFilmDataVectorized:
        assert len(allFilmDataVectorized[filmId]) == cache['profileVectorLength']

        assert allFilmDataVectorized[filmId][initDocumentDatabase.PROFILE_YEAR_INDEX] <= initDocumentDatabase.YEAR_WEIGHT
        assert allFilmDataVectorized[filmId][initDocumentDatabase.PROFILE_YEAR_INDEX] >= 0.0
        assert allFilmDataVectorized[filmId][initDocumentDatabase.PROFILE_NUMBER_OF_VOTES_INDEX] <= initDocumentDatabase.NUMBER_OF_VOTES_WEIGHT
        assert allFilmDataVectorized[filmId][initDocumentDatabase.PROFILE_NUMBER_OF_VOTES_INDEX] >= 0.0
        assert allFilmDataVectorized[filmId][initDocumentDatabase.PROFILE_IMDB_RATING_INDEX] <= initDocumentDatabase.IMDB_RATING_WEIGHT
        assert allFilmDataVectorized[filmId][initDocumentDatabase.PROFILE_IMDB_RATING_INDEX] >= 0.0
        assert allFilmDataVectorized[filmId][initDocumentDatabase.PROFILE_RUNTIME_INDEX] <= initDocumentDatabase.RUNTIME_WEIGHT
        assert allFilmDataVectorized[filmId][initDocumentDatabase.PROFILE_RUNTIME_INDEX] >= 0.0
        
        profileCountryStartIndex = initDocumentDatabase.PROFILE_GENRE_START_INDEX + len(cache['allGenres'])
        for i in range(initDocumentDatabase.PROFILE_GENRE_START_INDEX, profileCountryStartIndex):
            assert allFilmDataVectorized[filmId][i] <= initDocumentDatabase.GENRE_WEIGHT
            assert allFilmDataVectorized[filmId][i] >= 0.0

        for i in range(profileCountryStartIndex, cache['profileVectorLength']):
            assert allFilmDataVectorized[filmId][i] <= initDocumentDatabase.COUNTRY_WEIGHT
            assert allFilmDataVectorized[filmId][i] >= 0.0

def test_allFilmDataVectorizedMagnitudes():
    allFilmDataFile = open(allFilmDataFileLocation)
    allFilmData = json.load(allFilmDataFile)
    allFilmDataVectorizedMagnitudesFile = open(allFilmDataVectorizedMagnitudesFileLocation)
    allFilmDataVectorizedMagnitudes = json.load(allFilmDataVectorizedMagnitudesFile)
    allFilmDataVectorizedFile = open(allFilmDataVectorizedFileLocation)
    allFilmDataVectorized = json.load(allFilmDataVectorizedFile)

    assert len(allFilmData) == len(allFilmDataVectorized)

    for filmId in allFilmDataVectorizedMagnitudes:
        assert allFilmDataVectorizedMagnitudes[filmId] != None
        expectedMagnitude = np.linalg.norm(allFilmDataVectorized[filmId])
        expectedMagnitudeFloat = expectedMagnitude.item()
        assert allFilmDataVectorizedMagnitudes[filmId] == round(expectedMagnitudeFloat,
                                                                initDocumentDatabase.VECTORIZED_MAGNITUDE_NUMBER_OF_ROUNDED_DECIMAL_POINTS)

def test_cache():
    cacheFile = open(testUtilities.cacheFileLocation)
    cache = json.load(cacheFile)

    assert 'allGenres' in cache

    for genre in cache['allGenres']:
        assert genre != ""

    assert 'allCountries' in cache

    for country in cache['allCountries']:
        assert country != ""

    assert 'normalizedYears' in cache

    for normalizedYear in cache['normalizedYears']:
        assert cache['normalizedYears'][normalizedYear] >= 0.0  
        assert cache['normalizedYears'][normalizedYear] <= initDocumentDatabase.YEAR_WEIGHT

    assert 'normalizedImdbRatings' in cache

    for normalizedImdbRating in cache['normalizedImdbRatings']:
        assert cache['normalizedImdbRatings'][normalizedImdbRating] >= 0.0 
        assert cache['normalizedImdbRatings'][normalizedImdbRating] <= initDocumentDatabase.IMDB_RATING_WEIGHT

    assert 'normalizedRuntimes' in cache

    for normalizedRuntime in cache['normalizedRuntimes']:
        assert int(normalizedRuntime) >= initDocumentDatabase.RUNTIME_THRESHOLD
        assert cache['normalizedRuntimes'][normalizedRuntime] >= 0.0 
        assert cache['normalizedRuntimes'][normalizedRuntime] <= initDocumentDatabase.RUNTIME_WEIGHT

    assert 'minNumberOfVotes' in cache
    assert cache['minNumberOfVotes'] != None
    assert cache['minNumberOfVotes'] >= initDocumentDatabase.NUMBER_OF_VOTES_THRESHOLD

    assert 'diffNumberOfVotes' in cache
    assert cache['diffNumberOfVotes'] != None
    assert cache['diffNumberOfVotes'] > 0

    assert 'profileVectorLength' in cache
    assert cache['profileVectorLength'] != None

def test_convertRuntimeToHoursMinutes():
    assert initDocumentDatabase.convertRuntimeToHoursMinutes(60) == "1h"
    assert initDocumentDatabase.convertRuntimeToHoursMinutes(120) == "2h"
    
    assert initDocumentDatabase.convertRuntimeToHoursMinutes(40) == "40m"
    assert initDocumentDatabase.convertRuntimeToHoursMinutes(100) == "1h40m"

def test_allFilmData_correspondsWith_cachedTmdbFilmData():
    allFilmDataFile = open(allFilmDataFileLocation)
    allFilmData = json.load(allFilmDataFile)
    cachedTmdbFilmDataFile = open(cachedTmdbFilmDataFileLocation)
    cachedTmdbFilmData = json.load(cachedTmdbFilmDataFile)

    assert len(allFilmData) == len(cachedTmdbFilmData)

    for filmId in allFilmData:
        assert filmId in cachedTmdbFilmData
        assert allFilmData[filmId]['letterboxdTitle'] == cachedTmdbFilmData[filmId]['letterboxdTitle']
        assert allFilmData[filmId]['letterboxdYear'] == cachedTmdbFilmData[filmId]['letterboxdYear']
        assert allFilmData[filmId]['poster'] == cachedTmdbFilmData[filmId]['poster']
        assert allFilmData[filmId]['summary'] == cachedTmdbFilmData[filmId]['summary']

        for country in allFilmData[filmId]['countries']:
            assert country in cachedTmdbFilmData[filmId]['countries']

def test_allFilmData_correspondsWith_cachedLetterboxdTitles():
    allFilmDataFile = open(allFilmDataFileLocation)
    allFilmData = json.load(allFilmDataFile)
    cachedLetterboxdTitlesFile = open(cachedLetterboxdTitlesFileLocation)
    cachedLetterboxdTitles = json.load(cachedLetterboxdTitlesFile)

    for letterboxdTitle in cachedLetterboxdTitles:
        for film in cachedLetterboxdTitles[letterboxdTitle]:
            filmId = film['imdbFilmId']
            assert filmId in allFilmData
            assert allFilmData[filmId]['letterboxdTitle'] == letterboxdTitle

            for year in film['years']:
                assert year == allFilmData[filmId]['year'] or year == allFilmData[filmId]['letterboxdYear']


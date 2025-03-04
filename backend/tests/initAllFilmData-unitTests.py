import pytest
import json
import os
import sys

absolutePath = os.path.dirname(os.path.abspath(__file__))
parentDirectoryOfAbsolutePath = os.path.dirname(absolutePath)
sys.path.append(parentDirectoryOfAbsolutePath)
import initAllFilmData

allFilmDataFileLocation = "../../database/all-film-data.json"
cachedTmdbFilmDataFileLocation = "../../database/cached-tmdb-film-data.json"
cachedLetterboxdTitlesFileLocation = "../../database/cached-letterboxd-titles.json"
allFilmDataVectorizedFileLocation = "../../database/all-film-data-vectorized.json"
allFilmDataVectorizedMagnitudesFileLocation = "../../database/all-film-data-vectorized-magnitudes.json"
cacheFileLocation = "../../database/cache.json"
allGenres = ["Action","Adventure","Animation","Biography","Comedy","Crime","Documentary","Drama","Family","Fantasy","Film-Noir","History","Horror","Music","Musical","Mystery","News","Romance","Sci-Fi","Sport","Thriller","War","Western"]
allCountries = ["Algerian","American","Angolan","Argentinian","Australian","Austrian","Azerbaijani","Bangladeshi","Belgian","Bosnian & Herzegovinian","Botswanan","Brazilian","British","Bulgarian","Canadian","Cantonese","Chilean","Chinese","Colombian","Cypriot","Czech","Danish","Dominican","Dutch","Egyptian","Emirati","Estonian","Filipino","Finnish","French","German","Greek","Hungarian","Icelandic","Indian","Indonesian","Iranian","Irish","Israeli","Italian","Japanese","Jordanian","Kazakhstani","Latvian","Lebanese","Lithuanian","Luxembourgish","Malawian","Malian","Mexican","Myanma","New Zealand","Norwegian","Peruvian","Polish","Romanian","Russian","Saudi","Serbian","Serbian and Montenegrin","Singaporean","Slovenian","South African","South Korean","Soviet Union","Spanish","Swedish","Swiss","Taiwanese","Thai","Turkish","Venezuelan","Yugoslavian"]

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
        with open(cachedTmdbFilmDataFileLocation, encoding='utf-8') as cachedTmdbDataFile:
            json.load(cachedTmdbDataFile)

    except FileNotFoundError:
        pytest.fail("File not found.")
    except json.JSONDecodeError:
        pytest.fail("JSON decode error.")
    except Exception as e:
        pytest.fail("File open error.")

def test_cachedLetterboxdTitlesFileExists():
    try:
        with open(cachedTmdbFilmDataFileLocation, encoding='utf-8') as cachedTmdbDataFile:
            json.load(cachedTmdbDataFile)

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
        assert allFilmData[filmId]['imdbRating'] >= 1.0
        assert allFilmData[filmId]['imdbRating'] <= 10.0

        assert 'numberOfVotes' in allFilmData[filmId]
        assert allFilmData[filmId]['numberOfVotes'] != None
        assert allFilmData[filmId]['numberOfVotes'] != 0
        assert allFilmData[filmId]['numberOfVotes'] >= initAllFilmData.NUMBER_OF_VOTES_THRESHOLD

        assert 'runtime' in allFilmData[filmId]
        assert allFilmData[filmId]['runtime'] != None
        assert allFilmData[filmId]['runtime'] != 0
        assert allFilmData[filmId]['runtime'] >= initAllFilmData.RUNTIME_THRESHOLD

        assert 'runtimeHoursMinutes' in allFilmData[filmId]
        assert allFilmData[filmId]['runtime'] != ""

        assert 'genres' in allFilmData[filmId]
        assert len(allFilmData[filmId]['genres']) > 0

        for genre in allFilmData[filmId]['genres']:
            assert genre in allGenres
    
        assert 'imdbUrl' in allFilmData[filmId]
        assert allFilmData[filmId]['imdbUrl'] == initAllFilmData.BASE_IMDB_URL + filmId

        assert 'countries' in allFilmData[filmId]

        for country in allFilmData[filmId]['countries']:
            assert country in allCountries

        assert 'poster' in allFilmData[filmId]
        assert allFilmData[filmId]['poster'] != ""

        assert 'summary' in allFilmData[filmId]
        assert allFilmData[filmId]['summary'] != ""

def test_cachedTmdbFilmData():
    cachedTmdbFilmDataFile = open(cachedTmdbFilmDataFileLocation)
    cachedTmdbFilmData = json.load(cachedTmdbFilmDataFile)

    for filmId in cachedTmdbFilmData:
        assert 'letterboxdTitle' in cachedTmdbFilmData[filmId]
        assert cachedTmdbFilmData[filmId]['letterboxdTitle'] != ""

        assert 'letterboxdYear' in cachedTmdbFilmData[filmId]
        assert cachedTmdbFilmData[filmId]['letterboxdYear'] != None

        assert 'countries' in cachedTmdbFilmData[filmId]

        for country in cachedTmdbFilmData[filmId]['countries']:
            assert country in allCountries

        assert 'poster' in cachedTmdbFilmData[filmId]
        assert cachedTmdbFilmData[filmId]['poster'] != ""

        assert 'summary' in cachedTmdbFilmData[filmId]
        assert cachedTmdbFilmData[filmId]['summary'] != ""

def test_cachedLetterboxdTitles():
    cachedLetterboxdTitlesFile = open(cachedLetterboxdTitlesFileLocation)
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
    allFilmDataVectorizedFile = open(allFilmDataVectorizedFileLocation)
    allFilmDataVectorized = json.load(allFilmDataVectorizedFile)

    for filmId in allFilmDataVectorized:
        assert len(allFilmDataVectorized[filmId]) > 0
        
        for dimension in allFilmDataVectorized[filmId]:
            assert dimension >= 0.0 and dimension <= 1.0

def test_allFilmDataVectorizedMagnitudes():
    allFilmDataVectorizedMagnitudesFile = open(allFilmDataVectorizedMagnitudesFileLocation)
    allFilmDataVectorizedMagnitudes = json.load(allFilmDataVectorizedMagnitudesFile)

    for filmId in allFilmDataVectorizedMagnitudes:
        assert allFilmDataVectorizedMagnitudes[filmId] != None

def test_cache():
    cacheFile = open(cacheFileLocation)
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
        assert cache['normalizedYears'][normalizedYear] <= 1.0

    assert 'normalizedImdbRatings' in cache

    for normalizedImdbRating in cache['normalizedImdbRatings']:
        assert cache['normalizedImdbRatings'][normalizedImdbRating] >= 0.0 
        assert cache['normalizedImdbRatings'][normalizedImdbRating] <= 1.0

    assert 'normalizedRuntimes' in cache

    for normalizedRuntime in cache['normalizedRuntimes']:
        assert cache['normalizedRuntimes'][normalizedRuntime] >= 0.0 
        assert cache['normalizedRuntimes'][normalizedRuntime] <= 1.0

    assert 'minNumberOfVotes' in cache
    assert cache['minNumberOfVotes'] != None
    assert cache['minNumberOfVotes'] > 0

    assert 'diffNumberOfVotes' in cache
    assert cache['diffNumberOfVotes'] != None
    assert cache['diffNumberOfVotes'] >= 0

    assert 'profileVectorLength' in cache
    assert cache['profileVectorLength'] != None
    assert cache['profileVectorLength'] > 0

def test_convertRuntimeToHoursMinutes():
    assert initAllFilmData.convertRuntimeToHoursMinutes(60) == "1h"
    assert initAllFilmData.convertRuntimeToHoursMinutes(120) == "2h"
    
    assert initAllFilmData.convertRuntimeToHoursMinutes(40) == "40m"
    assert initAllFilmData.convertRuntimeToHoursMinutes(100) == "1h40m"

# TODO test that files correspond with eachother, e.g. every id in allFIlmData has entry in cache-*

import numpy as np
import os
import sys
absolutePathOfCurrentFile = os.path.dirname(os.path.abspath(__file__))
testRootDirectory = os.path.dirname(absolutePathOfCurrentFile)
backendRootDirectory = os.path.dirname(testRootDirectory)
sys.path.append(testRootDirectory)
sys.path.append(backendRootDirectory)
from DocumentDatabase import *
from InitDatabase import *
from TestUtilities import *
from VectorizeUtilities import *

REPOSITORY_ROOT = "../../../"

def test_allFilmDataExists():
    database = DocumentDatabase(REPOSITORY_ROOT)
    assert database.read("AllFilmData") != None

def test_cachedTmdbFilmDataExists():
    database = DocumentDatabase(REPOSITORY_ROOT)
    assert database.read("CachedTmdbFilmData") != None

def test_cachedLetterboxdTitlesExists():
    database = DocumentDatabase(REPOSITORY_ROOT)
    assert database.read("CachedLetterboxdTitles") != None

def test_allFilmDataVectorizedExists():
    database = DocumentDatabase(REPOSITORY_ROOT)
    assert database.read("AllFilmDataVectorized") != None

def test_allFilmDataVectorizedMagnitudesExists():
    database = DocumentDatabase(REPOSITORY_ROOT)
    assert database.read("AllFilmDataVectorizedMagnitudes") != None

def test_allCountriesExists():
    database = DocumentDatabase(REPOSITORY_ROOT)
    assert database.read("AllCountries") != None

def test_allGenresExists():
    database = DocumentDatabase(REPOSITORY_ROOT)
    assert database.read("AllGenres") != None

def test_cachedCountriesExists():
    database = DocumentDatabase(REPOSITORY_ROOT)
    assert database.read("CachedCountries") != None

def test_diffNumberOfVotesExists():
    database = DocumentDatabase(REPOSITORY_ROOT)
    assert database.read("DiffNumberOfVotes") != None

def test_minNumberOfVotesExists():
    database = DocumentDatabase(REPOSITORY_ROOT)
    assert database.read("MinNumberOfVotes") != None

def test_normalizedImdbRatingsExists():
    database = DocumentDatabase(REPOSITORY_ROOT)
    assert database.read("NormalizedImdbRatings") != None

def test_normalizedRuntimesExists():
    database = DocumentDatabase(REPOSITORY_ROOT)
    assert database.read("NormalizedRuntimes") != None

def test_normalizedYearsExists():
    database = DocumentDatabase(REPOSITORY_ROOT)
    assert database.read("NormalizedYears") != None

def test_profileVectorLengthExists():
    database = DocumentDatabase(REPOSITORY_ROOT)
    assert database.read("ProfileVectorLength") != None

def test_allFilmData():
    database = DocumentDatabase(REPOSITORY_ROOT)
    allFilmData = database.read("AllFilmData")
    allGenres = database.read("AllGenres")
    allCountries = database.read("AllCountries")

    testUtilities = TestUtilities("../../../")

    for filmId in allFilmData:
        testUtilities.verifyFilm(allFilmData[filmId], filmId, allGenres, allCountries)

def test_cachedTmdbFilmData():
    database = DocumentDatabase(REPOSITORY_ROOT)
    cachedTmdbFilmData = database.read("CachedTmdbFilmData")
    allCountries = database.read("AllCountries")

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
    database = DocumentDatabase(REPOSITORY_ROOT)
    cachedLetterboxdTitles = database.read("CachedLetterboxdTitles")

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
    database = DocumentDatabase(REPOSITORY_ROOT)
    allFilmData = database.read("AllFilmData")
    allFilmDataVectorized = database.read("AllFilmDataVectorized")
    profileVectorLength = database.read("ProfileVectorLength")
    allGenres = database.read("AllGenres")

    assert len(allFilmData) == len(allFilmDataVectorized)

    for filmId in allFilmDataVectorized:
        assert len(allFilmDataVectorized[filmId]) == profileVectorLength

        assert allFilmDataVectorized[filmId][VectorizeUtilities.PROFILE_YEAR_INDEX] <= VectorizeUtilities.YEAR_WEIGHT
        assert allFilmDataVectorized[filmId][VectorizeUtilities.PROFILE_YEAR_INDEX] >= 0.0
        assert allFilmDataVectorized[filmId][VectorizeUtilities.PROFILE_NUMBER_OF_VOTES_INDEX] <= VectorizeUtilities.NUMBER_OF_VOTES_WEIGHT
        assert allFilmDataVectorized[filmId][VectorizeUtilities.PROFILE_NUMBER_OF_VOTES_INDEX] >= 0.0
        assert allFilmDataVectorized[filmId][VectorizeUtilities.PROFILE_IMDB_RATING_INDEX] <= VectorizeUtilities.IMDB_RATING_WEIGHT
        assert allFilmDataVectorized[filmId][VectorizeUtilities.PROFILE_IMDB_RATING_INDEX] >= 0.0
        assert allFilmDataVectorized[filmId][VectorizeUtilities.PROFILE_RUNTIME_INDEX] <= VectorizeUtilities.RUNTIME_WEIGHT
        assert allFilmDataVectorized[filmId][VectorizeUtilities.PROFILE_RUNTIME_INDEX] >= 0.0
        
        profileCountryStartIndex = VectorizeUtilities.PROFILE_GENRE_START_INDEX + len(allGenres)
        for i in range(VectorizeUtilities.PROFILE_GENRE_START_INDEX, profileCountryStartIndex):
            assert allFilmDataVectorized[filmId][i] <= VectorizeUtilities.GENRE_WEIGHT
            assert allFilmDataVectorized[filmId][i] >= 0.0

        for i in range(profileCountryStartIndex, profileVectorLength):
            assert allFilmDataVectorized[filmId][i] <= VectorizeUtilities.COUNTRY_WEIGHT
            assert allFilmDataVectorized[filmId][i] >= 0.0

def test_allFilmDataVectorizedMagnitudes():
    database = DocumentDatabase(REPOSITORY_ROOT)
    allFilmData = database.read("AllFilmData")
    allFilmDataVectorizedMagnitudes = database.read("AllFilmDataVectorizedMagnitudes")
    allFilmDataVectorized = database.read("AllFilmDataVectorized")

    assert len(allFilmData) == len(allFilmDataVectorized)

    for filmId in allFilmDataVectorizedMagnitudes:
        assert allFilmDataVectorizedMagnitudes[filmId] != None
        expectedMagnitude = np.linalg.norm(allFilmDataVectorized[filmId])
        expectedMagnitudeFloat = expectedMagnitude.item()
        assert allFilmDataVectorizedMagnitudes[filmId] == round(expectedMagnitudeFloat,
                                                                InitDatabase.VECTORIZED_MAGNITUDE_NUMBER_OF_ROUNDED_DECIMAL_POINTS)

def test_allGenres():
    database = DocumentDatabase(REPOSITORY_ROOT)
    allGenres = database.read("AllGenres")

    assert len(allGenres) > 0

    for genre in allGenres:
        assert genre != ""

def test_allCountries():
    database = DocumentDatabase(REPOSITORY_ROOT)
    allCountries = database.read("AllGenres")

    assert len(allCountries) > 0

    for country in allCountries:
        assert country != ""

def test_normalizedYears():
    database = DocumentDatabase(REPOSITORY_ROOT)
    normalizedYears = database.read("NormalizedYears")

    for normalizedYear in normalizedYears:
        assert normalizedYears[normalizedYear] >= 0.0  
        assert normalizedYears[normalizedYear] <= VectorizeUtilities.YEAR_WEIGHT

def test_normalizedImdbRatings():
    database = DocumentDatabase(REPOSITORY_ROOT)
    normalizedImdbRatings = database.read("NormalizedImdbRatings")

    for normalizedImdbRating in normalizedImdbRatings:
        assert normalizedImdbRatings[normalizedImdbRating] >= 0.0 
        assert normalizedImdbRatings[normalizedImdbRating] <= VectorizeUtilities.IMDB_RATING_WEIGHT

def test_normalizedRuntimes():
    database = DocumentDatabase(REPOSITORY_ROOT)
    normalizedRuntimes = database.read("NormalizedRuntimes")

    for normalizedRuntime in normalizedRuntimes:
        assert int(normalizedRuntime) >= InitDatabase.RUNTIME_THRESHOLD
        assert normalizedRuntimes[normalizedRuntime] >= 0.0 
        assert normalizedRuntimes[normalizedRuntime] <= VectorizeUtilities.RUNTIME_WEIGHT

def test_minNumberOfVotes():
    database = DocumentDatabase(REPOSITORY_ROOT)
    minNumberOfVotes = database.read("MinNumberOfVotes")

    assert minNumberOfVotes != None
    assert minNumberOfVotes >= InitDatabase.NUMBER_OF_VOTES_THRESHOLD

def test_diffNumberOfVotes():
    database = DocumentDatabase(REPOSITORY_ROOT)
    diffNumberOfVotes = database.read("DiffNumberOfVotes")

    assert diffNumberOfVotes != None
    assert diffNumberOfVotes > 0

def test_profileVectorLength():
    database = DocumentDatabase(REPOSITORY_ROOT)
    profileVectorLength = database.read("ProfileVectorLength")
    
    assert profileVectorLength != None
    assert profileVectorLength > 0

def test_convertRuntimeToHoursMinutes():
    database = DocumentDatabase(REPOSITORY_ROOT)
    initDatabase = InitDatabase(database)
    assert initDatabase.convertRuntimeToHoursMinutes(60) == "1h"
    assert initDatabase.convertRuntimeToHoursMinutes(120) == "2h"
    
    assert initDatabase.convertRuntimeToHoursMinutes(40) == "40m"
    assert initDatabase.convertRuntimeToHoursMinutes(100) == "1h40m"

def test_allFilmData_correspondsWith_cachedTmdbFilmData():
    database = DocumentDatabase(REPOSITORY_ROOT)
    allFilmData = database.read("AllFilmData")
    cachedTmdbFilmData = database.read("CachedTmdbFilmData")

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
    database = DocumentDatabase(REPOSITORY_ROOT)
    allFilmData = database.read("AllFilmData")
    cachedLetterboxdTitles = database.read("CachedLetterboxdTitles")

    for letterboxdTitle in cachedLetterboxdTitles:
        for film in cachedLetterboxdTitles[letterboxdTitle]:
            filmId = film['imdbFilmId']
            assert filmId in allFilmData
            assert allFilmData[filmId]['letterboxdTitle'] == letterboxdTitle

            for year in film['years']:
                assert year == allFilmData[filmId]['year'] or year == allFilmData[filmId]['letterboxdYear']

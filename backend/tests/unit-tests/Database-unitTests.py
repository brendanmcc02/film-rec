import numpy as np
import os
import sys
absolutePathOfCurrentFile = os.path.dirname(os.path.abspath(__file__))
testRootDirectory = os.path.dirname(absolutePathOfCurrentFile)
backendRootDirectory = os.path.dirname(testRootDirectory)
sys.path.append(testRootDirectory)
sys.path.append(backendRootDirectory)
from DocumentDatabase import *
from InitDocumentDatabase import *
from TestUtilities import *
from VectorizeUtilities import *

REPOSITORY_ROOT = "../../../"

def test_allFilmDataExists():
    documentDatabase = DocumentDatabase(REPOSITORY_ROOT)
    assert documentDatabase.read("allFilmData") != None

def test_cachedTmdbFilmDataExists():
    documentDatabase = DocumentDatabase(REPOSITORY_ROOT)
    assert documentDatabase.read("cachedTmdbFilmData") != None

def test_cachedLetterboxdTitlesExists():
    documentDatabase = DocumentDatabase(REPOSITORY_ROOT)
    assert documentDatabase.read("cachedLetterboxdTitles") != None

def test_allFilmDataVectorizedExists():
    documentDatabase = DocumentDatabase(REPOSITORY_ROOT)
    assert documentDatabase.read("allFilmDataVectorized") != None

def test_allFilmDataVectorizedMagnitudesExists():
    documentDatabase = DocumentDatabase(REPOSITORY_ROOT)
    assert documentDatabase.read("allFilmDataVectorizedMagnitudes") != None

def test_allCountriesExists():
    documentDatabase = DocumentDatabase(REPOSITORY_ROOT)
    assert documentDatabase.read("allCountries") != None

def test_allGenresExists():
    documentDatabase = DocumentDatabase(REPOSITORY_ROOT)
    assert documentDatabase.read("allGenres") != None

def test_cachedCountriesExists():
    documentDatabase = DocumentDatabase(REPOSITORY_ROOT)
    assert documentDatabase.read("cachedCountries") != None

def test_diffNumberOfVotesExists():
    documentDatabase = DocumentDatabase(REPOSITORY_ROOT)
    assert documentDatabase.read("diffNumberOfVotes") != None

def test_minNumberOfVotesExists():
    documentDatabase = DocumentDatabase(REPOSITORY_ROOT)
    assert documentDatabase.read("minNumberOfVotes") != None

def test_normalizedImdbRatingsExists():
    documentDatabase = DocumentDatabase(REPOSITORY_ROOT)
    assert documentDatabase.read("normalizedImdbRatings") != None

def test_normalizedRuntimesExists():
    documentDatabase = DocumentDatabase(REPOSITORY_ROOT)
    assert documentDatabase.read("normalizedRuntimes") != None

def test_normalizedYearsExists():
    documentDatabase = DocumentDatabase(REPOSITORY_ROOT)
    assert documentDatabase.read("normalizedYears") != None

def test_profileVectorLengthExists():
    documentDatabase = DocumentDatabase(REPOSITORY_ROOT)
    assert documentDatabase.read("profileVectorLength") != None

def test_allFilmData():
    documentDatabase = DocumentDatabase(REPOSITORY_ROOT)
    allFilmData = documentDatabase.read("allFilmData")
    allGenres = documentDatabase.read("allGenres")
    allCountries = documentDatabase.read("allCountries")

    testUtilities = TestUtilities("../../../")

    for filmId in allFilmData:
        testUtilities.verifyFilm(allFilmData[filmId], filmId, allGenres, allCountries)

def test_cachedTmdbFilmData():
    documentDatabase = DocumentDatabase(REPOSITORY_ROOT)
    cachedTmdbFilmData = documentDatabase.read("cachedTmdbFilmData")
    allCountries = documentDatabase.read("allCountries")

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
    documentDatabase = DocumentDatabase(REPOSITORY_ROOT)
    cachedLetterboxdTitles = documentDatabase.read("cachedLetterboxdTitles")

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
    documentDatabase = DocumentDatabase(REPOSITORY_ROOT)
    allFilmData = documentDatabase.read("allFilmData")
    allFilmDataVectorized = documentDatabase.read("allFilmDataVectorized")
    profileVectorLength = documentDatabase.read("profileVectorLength")
    allGenres = documentDatabase.read("allGenres")

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
    documentDatabase = DocumentDatabase(REPOSITORY_ROOT)
    allFilmData = documentDatabase.read("allFilmData")
    allFilmDataVectorizedMagnitudes = documentDatabase.read("allFilmDataVectorizedMagnitudes")
    allFilmDataVectorized = documentDatabase.read("allFilmDataVectorized")

    assert len(allFilmData) == len(allFilmDataVectorized)

    for filmId in allFilmDataVectorizedMagnitudes:
        assert allFilmDataVectorizedMagnitudes[filmId] != None
        expectedMagnitude = np.linalg.norm(allFilmDataVectorized[filmId])
        expectedMagnitudeFloat = expectedMagnitude.item()
        assert allFilmDataVectorizedMagnitudes[filmId] == round(expectedMagnitudeFloat,
                                                                InitDocumentDatabase.VECTORIZED_MAGNITUDE_NUMBER_OF_ROUNDED_DECIMAL_POINTS)

def test_allGenres():
    documentDatabase = DocumentDatabase(REPOSITORY_ROOT)
    allGenres = documentDatabase.read("allGenres")

    assert len(allGenres) > 0

    for genre in allGenres:
        assert genre != ""

def test_allCountries():
    documentDatabase = DocumentDatabase(REPOSITORY_ROOT)
    allCountries = documentDatabase.read("allGenres")

    assert len(allCountries) > 0

    for country in allCountries:
        assert country != ""

def test_normalizedYears():
    documentDatabase = DocumentDatabase(REPOSITORY_ROOT)
    normalizedYears = documentDatabase.read("normalizedYears")

    for normalizedYear in normalizedYears:
        assert normalizedYears[normalizedYear] >= 0.0  
        assert normalizedYears[normalizedYear] <= VectorizeUtilities.YEAR_WEIGHT

def test_normalizedImdbRatings():
    documentDatabase = DocumentDatabase(REPOSITORY_ROOT)
    normalizedImdbRatings = documentDatabase.read("normalizedImdbRatings")

    for normalizedImdbRating in normalizedImdbRatings:
        assert normalizedImdbRatings[normalizedImdbRating] >= 0.0 
        assert normalizedImdbRatings[normalizedImdbRating] <= VectorizeUtilities.IMDB_RATING_WEIGHT

def test_normalizedRuntimes():
    documentDatabase = DocumentDatabase(REPOSITORY_ROOT)
    normalizedRuntimes = documentDatabase.read("normalizedRuntimes")

    for normalizedRuntime in normalizedRuntimes:
        assert int(normalizedRuntime) >= InitDocumentDatabase.RUNTIME_THRESHOLD
        assert normalizedRuntimes[normalizedRuntime] >= 0.0 
        assert normalizedRuntimes[normalizedRuntime] <= VectorizeUtilities.RUNTIME_WEIGHT

def test_minNumberOfVotes():
    documentDatabase = DocumentDatabase(REPOSITORY_ROOT)
    minNumberOfVotes = documentDatabase.read("minNumberOfVotes")

    assert minNumberOfVotes != None
    assert minNumberOfVotes >= InitDocumentDatabase.NUMBER_OF_VOTES_THRESHOLD

def test_diffNumberOfVotes():
    documentDatabase = DocumentDatabase(REPOSITORY_ROOT)
    diffNumberOfVotes = documentDatabase.read("diffNumberOfVotes")

    assert diffNumberOfVotes != None
    assert diffNumberOfVotes > 0

def test_profileVectorLength():
    documentDatabase = DocumentDatabase(REPOSITORY_ROOT)
    profileVectorLength = documentDatabase.read("profileVectorLength")
    
    assert profileVectorLength != None
    assert profileVectorLength > 0

def test_convertRuntimeToHoursMinutes():
    documentDatbase = DocumentDatabase(REPOSITORY_ROOT)
    initDocumentDatabase = InitDocumentDatabase(documentDatbase)
    assert initDocumentDatabase.convertRuntimeToHoursMinutes(60) == "1h"
    assert initDocumentDatabase.convertRuntimeToHoursMinutes(120) == "2h"
    
    assert initDocumentDatabase.convertRuntimeToHoursMinutes(40) == "40m"
    assert initDocumentDatabase.convertRuntimeToHoursMinutes(100) == "1h40m"

def test_allFilmData_correspondsWith_cachedTmdbFilmData():
    documentDatabase = DocumentDatabase(REPOSITORY_ROOT)
    allFilmData = documentDatabase.read("allFilmData")
    cachedTmdbFilmData = documentDatabase.read("cachedTmdbFilmData")

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
    documentDatabase = DocumentDatabase(REPOSITORY_ROOT)
    allFilmData = documentDatabase.read("allFilmData")
    cachedLetterboxdTitles = documentDatabase.read("cachedLetterboxdTitles")

    for letterboxdTitle in cachedLetterboxdTitles:
        for film in cachedLetterboxdTitles[letterboxdTitle]:
            filmId = film['imdbFilmId']
            assert filmId in allFilmData
            assert allFilmData[filmId]['letterboxdTitle'] == letterboxdTitle

            for year in film['years']:
                assert year == allFilmData[filmId]['year'] or year == allFilmData[filmId]['letterboxdYear']

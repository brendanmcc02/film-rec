import os
import sys
import testUtilities
# import the needed file from backend directory
# (this is ugly as hell, there's probably an easier way but it gets the job done)
absolutePathOfCurrentFile = os.path.dirname(os.path.abspath(__file__))
parentDirectoryOfCurrentFile = os.path.dirname(absolutePathOfCurrentFile)
sys.path.append(parentDirectoryOfCurrentFile)
import vectorizeUtilities

def test_keepVectorBoundary():
    vector = [1.1, -0.1, 0.0]
    vectorizeUtilities.keepVectorBoundary(vector)

    for dimension in vector:
        assert dimension >= 0.0 and dimension <= 1.0

    vector = [0.9, 0.1, 0.0]
    vectorizeUtilities.keepVectorBoundary(vector)

    for dimension in vector:
        assert dimension >= 0.0 and dimension <= 1.0

def test_getFilmGenres():
    cacheFile = open(testUtilities.cacheFileLocation)
    cache = json.load(cacheFile)
    filmVectorWithActionComedyRomance = [0.0, 0.0, 0.0, 0.0, 0.7, 0.0, 0.0, 0.0, 0.7, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.7, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    assert (vectorizeUtilities.getFilmGenres(filmVectorWithActionComedyRomance, cache['allGenres']) == 
            ["Action", "Comedy", "Romance"])

    filmVectorWithAdventureDramaWestern = [0.0, 0.0, 0.0, 0.0, 0.0, 0.7, 0.0, 0.0, 0.0, 0.0, 0.0, 0.7, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.7, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    assert (vectorizeUtilities.getFilmGenres(filmVectorWithAdventureDramaWestern, cache['allGenres']) == 
            ["Adventure", "Drama", "Western"])

    filmVectorWithDrama = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.7, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    assert (vectorizeUtilities.getFilmGenres(filmVectorWithDrama, cache['allGenres']) == 
            ["Drama"])

def test_curveAccordingToMax_ZeroVector():
    allZeroTestVector = [0.0, 0.0, 0.0]
    testWeight = 0.5
    testStartIndex = 0
    vectorizeUtilities.curveAccordingToMax(allZeroTestVector, allZeroTestVector, testWeight, testStartIndex)
    assert allZeroTestVector == [0.0, 0.0, 0.0]

    allZeroTestVector = [0.0, 0.0, 0.0]
    testWeight = 1.0
    testStartIndex = 0
    vectorizeUtilities.curveAccordingToMax(allZeroTestVector, allZeroTestVector, testWeight, testStartIndex)
    assert allZeroTestVector == [0.0, 0.0, 0.0]

def test_curveAccordingToMax_SingleOneVector():
    containsSingleOneTestVector = [1.0, 0.0, 0.0]
    testWeight = 1.0
    testStartIndex = 0
    vectorizeUtilities.curveAccordingToMax(containsSingleOneTestVector, containsSingleOneTestVector, 
                                           testWeight, testStartIndex)
    assert containsSingleOneTestVector == [1.0, 0.0, 0.0]

    containsSingleOneTestVector = [1.0, 0.0, 0.0]
    testWeight = 0.5
    testStartIndex = 0
    vectorizeUtilities.curveAccordingToMax(containsSingleOneTestVector, containsSingleOneTestVector, 
                                           testWeight, testStartIndex)
    assert containsSingleOneTestVector == [0.5, 0.0, 0.0]

def test_curveAccordingToMax_multiVariableVector():
    multiVariableTestVector = [1.0, 0.5, 0.0]
    testWeight = 0.5
    testStartIndex = 0
    vectorizeUtilities.curveAccordingToMax(multiVariableTestVector, multiVariableTestVector, 
                                           testWeight, testStartIndex)
    assert multiVariableTestVector == [0.5, 0.25, 0.0]

    multiVariableTestVector = [0.8, 0.4, 0.0]
    testWeight = 0.5
    testStartIndex = 0
    vectorizeUtilities.curveAccordingToMax(multiVariableTestVector, multiVariableTestVector, 
                                           testWeight, testStartIndex)
    assert multiVariableTestVector == [0.5, 0.25, 0.0]

    multiVariableTestVector = [0.8, 0.4, 0.0]
    testWeight = 1.0
    testStartIndex = 0
    vectorizeUtilities.curveAccordingToMax(multiVariableTestVector, multiVariableTestVector, 
                                           testWeight, testStartIndex)
    assert multiVariableTestVector == [1.0, 0.5, 0.0]

def test_getProfileMaxCountry_filmHasOnlyOneMaxCountry():
    cacheFile = open(testUtilities.cacheFileLocation)
    cache = json.load(cacheFile)
    allGenresLength = len(cache['allGenres'])

    filmVectorWithAmerican = [0.0, 0.0, 0.0, 0.0, 0.7, 0.0, 0.0, 0.0, 0.0, 0.7, 0.0, 0.7, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

    assert (vectorizeUtilities.getProfileMaxCountry(filmVectorWithAmerican, allGenresLength, cache['allCountries']) 
            == "American")

def test_getProfileMaxCountry_filmHasMultipleMaxCountries_EnsuresOnlyOneIsReturned():
    cacheFile = open(testUtilities.cacheFileLocation)
    cache = json.load(cacheFile)
    allGenresLength = len(cache['allGenres'])

    filmVectorWithAmericanAndBritish = [0.0, 0.0, 0.0, 0.0, 0.0, 0.7, 0.0, 0.0, 0.0, 0.0, 0.0, 0.7, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.7, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

    assert (vectorizeUtilities.getProfileMaxCountry(filmVectorWithAmericanAndBritish, allGenresLength, cache['allCountries']) 
            == "American")


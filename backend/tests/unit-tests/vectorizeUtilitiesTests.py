import os
import sys
import json
absolutePath = os.path.dirname(os.path.abspath(__file__))
parentDirectoryOfAbsolutePath = os.path.dirname(os.path.dirname(absolutePath))
sys.path.append(parentDirectoryOfAbsolutePath)
import vectorizeUtilities

def test_keepVectorBoundary():
    vector = [1.1, -0.1, 0.0]
    vectorizeUtilities.keepVectorBoundary(vector)

    for dimension in vector:
        assert dimension >= 0.0 and dimension <= 1.0

def test_getFilmGenres():
    cacheFile = open("../../../database/cache.json")
    cache = json.load(cacheFile)
    allGenres = cache['allGenres']

    filmVectorWithActionComedyRomance = [0.0, 0.0, 0.0, 0.0, 0.7, 0.0, 0.0, 0.0, 0.7, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.7, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    assert (vectorizeUtilities.getFilmGenres(filmVectorWithActionComedyRomance, allGenres) == 
            ["Action", "Comedy", "Romance"])

    filmVectorWithAdventureDramaWestern = [0.0, 0.0, 0.0, 0.0, 0.0, 0.7, 0.0, 0.0, 0.0, 0.0, 0.0, 0.7, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.7, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    assert (vectorizeUtilities.getFilmGenres(filmVectorWithAdventureDramaWestern, allGenres) == 
            ["Adventure", "Drama", "Western"])

    filmVectorWithDrama = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.7, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    assert (vectorizeUtilities.getFilmGenres(filmVectorWithDrama, allGenres) == 
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

def test_getProfileMaxCountry_filmHasOnlyOneCountry():
    cacheFile = open("../../../database/cache.json")
    cache = json.load(cacheFile)

    allGenresLength = len(cache['allGenres'])

    filmVectorWithAmerican = [0.42272727272727273, 0.9638554216867469, 0.9922394797260969, 0.09756838905775077, 0.7, 0.0, 0.0, 0.0, 0.0, 0.7, 0.0, 0.7, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

    assert (vectorizeUtilities.getProfileMaxCountry(filmVectorWithAmerican, allGenresLength, cache['allCountries']) 
            == "American")

def test_getProfileMaxCountry_filmHasMultipleCountries_EnsuresOnlyOneIsReturned():
    cacheFile = open("../../../database/cache.json")
    cache = json.load(cacheFile)

    allGenresLength = len(cache['allGenres'])

    filmVectorWithAmericanAndBritish = [0.16363636363636364, 0.8072289156626505, 0.020540722226202377, 0.0547112462006079, 0.0, 0.7, 0.0, 0.0, 0.0, 0.0, 0.0, 0.7, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.7, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

    assert (vectorizeUtilities.getProfileMaxCountry(filmVectorWithAmericanAndBritish, allGenresLength, cache['allCountries']) 
            == "American")


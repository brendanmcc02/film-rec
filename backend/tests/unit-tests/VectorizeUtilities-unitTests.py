import os
import sys
absolutePathOfCurrentFile = os.path.dirname(os.path.abspath(__file__))
testRootDirectory = os.path.dirname(absolutePathOfCurrentFile)
backendRootDirectory = os.path.dirname(testRootDirectory)
sys.path.append(testRootDirectory)
sys.path.append(backendRootDirectory)
from DocumentDatabase import *
from VectorizeUtilities import *

REPOSITORY_ROOT = "../../../"

def test_keepVectorBoundary():
    vector = [1.1, -0.1, 0.0]
    keepVectorBoundary(vector)

    for dimension in vector:
        assert dimension >= 0.0
        assert dimension <= 1.0

    vector = [0.9, 0.1, 0.0]
    keepVectorBoundary(vector)

    for dimension in vector:
        assert dimension >= 0.0
        assert dimension <= 1.0

def test_getFilmGenres():
    database = DocumentDatabase(REPOSITORY_ROOT)
    allGenres = database.read("AllGenres")

    filmVectorWithActionComedyRomance = [0.0, 0.0, 0.0, 0.0, 0.7, 0.0, 0.0, 0.0, 0.7, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.7, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    assert (getFilmGenres(filmVectorWithActionComedyRomance, allGenres) == 
            ["Action", "Comedy", "Romance"])

    filmVectorWithAdventureDramaWestern = [0.0, 0.0, 0.0, 0.0, 0.0, 0.7, 0.0, 0.0, 0.0, 0.0, 0.0, 0.7, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.7, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    assert (getFilmGenres(filmVectorWithAdventureDramaWestern, allGenres) == 
            ["Adventure", "Drama", "Western"])

    filmVectorWithDrama = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.7, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    assert (getFilmGenres(filmVectorWithDrama, allGenres) == 
            ["Drama"])

def test_curveAccordingToMax_ZeroVector():
    allZeroTestVector = [0.0, 0.0, 0.0]
    testWeight = 0.5
    testStartIndex = 0
    curveAccordingToMax(allZeroTestVector, allZeroTestVector, testWeight, testStartIndex)
    assert allZeroTestVector == [0.0, 0.0, 0.0]

    allZeroTestVector = [0.0, 0.0, 0.0]
    testWeight = 1.0
    testStartIndex = 0
    curveAccordingToMax(allZeroTestVector, allZeroTestVector, testWeight, testStartIndex)
    assert allZeroTestVector == [0.0, 0.0, 0.0]

def test_curveAccordingToMax_SingleOneVector():
    containsSingleOneTestVector = [1.0, 0.0, 0.0]
    testWeight = 1.0
    testStartIndex = 0
    curveAccordingToMax(containsSingleOneTestVector, containsSingleOneTestVector, 
                                           testWeight, testStartIndex)
    assert containsSingleOneTestVector == [1.0, 0.0, 0.0]

    containsSingleOneTestVector = [1.0, 0.0, 0.0]
    testWeight = 0.5
    testStartIndex = 0
    curveAccordingToMax(containsSingleOneTestVector, containsSingleOneTestVector, 
                                           testWeight, testStartIndex)
    assert containsSingleOneTestVector == [0.5, 0.0, 0.0]

def test_curveAccordingToMax_multiVariableVector():
    multiVariableTestVector = [1.0, 0.5, 0.0]
    testWeight = 0.5
    testStartIndex = 0
    curveAccordingToMax(multiVariableTestVector, multiVariableTestVector, 
                                           testWeight, testStartIndex)
    assert multiVariableTestVector == [0.5, 0.25, 0.0]

    multiVariableTestVector = [0.8, 0.4, 0.0]
    testWeight = 0.5
    testStartIndex = 0
    curveAccordingToMax(multiVariableTestVector, multiVariableTestVector, 
                                           testWeight, testStartIndex)
    assert multiVariableTestVector == [0.5, 0.25, 0.0]

    multiVariableTestVector = [0.8, 0.4, 0.0]
    testWeight = 1.0
    testStartIndex = 0
    curveAccordingToMax(multiVariableTestVector, multiVariableTestVector, 
                                           testWeight, testStartIndex)
    assert multiVariableTestVector == [1.0, 0.5, 0.0]

def test_getProfileMaxCountry_filmHasOnlyOneMaxCountry():
    database = DocumentDatabase(REPOSITORY_ROOT)
    allGenres = database.read("AllGenres")
    allCountries = database.read("AllCountries")
    allGenresLength = len(allGenres)

    filmVectorWithAmerican = [0.0, 0.0, 0.0, 0.0, 0.7, 0.0, 0.0, 0.0, 0.0, 0.7, 0.0, 0.7, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

    assert (getProfileMaxCountry(filmVectorWithAmerican, allGenresLength, allCountries) 
            == "American")

def test_getProfileMaxCountry_filmHasMultipleMaxCountries_EnsuresOnlyOneIsReturned():
    database = DocumentDatabase(REPOSITORY_ROOT)
    allGenres = database.read("AllGenres")
    allCountries = database.read("AllCountries")
    allGenresLength = len(allGenres)

    filmVectorWithAmericanAndBritish = [0.0, 0.0, 0.0, 0.0, 0.0, 0.7, 0.0, 0.0, 0.0, 0.0, 0.0, 0.7, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.7, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

    assert (getProfileMaxCountry(filmVectorWithAmericanAndBritish, allGenresLength, allCountries) 
            == "American")


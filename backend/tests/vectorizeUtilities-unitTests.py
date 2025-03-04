import os
import sys
import json
absolutePath = os.path.dirname(os.path.abspath(__file__))
parentDirectoryOfAbsolutePath = os.path.dirname(absolutePath)
sys.path.append(parentDirectoryOfAbsolutePath)
import vectorizeUtilities

mockGenres = ["Action","Adventure","Animation","Biography","Comedy","Crime","Documentary","Drama","Family","Fantasy","Film-Noir","History","Horror","Music","Musical","Mystery","News","Romance","Sci-Fi","Sport","Thriller","War","Western"]
mockCountries = ["Algerian","American","Angolan","Argentinian","Australian","Austrian","Azerbaijani","Bangladeshi","Belgian","Bosnian & Herzegovinian","Botswanan","Brazilian","British","Bulgarian","Canadian","Cantonese","Chilean","Chinese","Colombian","Cypriot","Czech","Danish","Dominican","Dutch","Egyptian","Emirati","Estonian","Filipino","Finnish","French","German","Greek","Hungarian","Icelandic","Indian","Indonesian","Iranian","Irish","Israeli","Italian","Japanese","Jordanian","Kazakhstani","Latvian","Lebanese","Lithuanian","Luxembourgish","Malawian","Malian","Mexican","Myanma","New Zealand","Norwegian","Peruvian","Polish","Romanian","Russian","Saudi","Serbian","Serbian and Montenegrin","Singaporean","Slovenian","South African","South Korean","Soviet Union","Spanish","Swedish","Swiss","Taiwanese","Thai","Turkish","Venezuelan","Yugoslavian"]

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
    filmVectorWithActionComedyRomance = [0.0, 0.0, 0.0, 0.0, 0.7, 0.0, 0.0, 0.0, 0.7, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.7, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    assert (vectorizeUtilities.getFilmGenres(filmVectorWithActionComedyRomance, mockGenres) == 
            ["Action", "Comedy", "Romance"])

    filmVectorWithAdventureDramaWestern = [0.0, 0.0, 0.0, 0.0, 0.0, 0.7, 0.0, 0.0, 0.0, 0.0, 0.0, 0.7, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.7, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    assert (vectorizeUtilities.getFilmGenres(filmVectorWithAdventureDramaWestern, mockGenres) == 
            ["Adventure", "Drama", "Western"])

    filmVectorWithDrama = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.7, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    assert (vectorizeUtilities.getFilmGenres(filmVectorWithDrama, mockGenres) == 
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
    allGenresLength = len(mockGenres)

    filmVectorWithAmerican = [0.0, 0.0, 0.0, 0.0, 0.7, 0.0, 0.0, 0.0, 0.0, 0.7, 0.0, 0.7, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

    assert (vectorizeUtilities.getProfileMaxCountry(filmVectorWithAmerican, allGenresLength, mockCountries) 
            == "American")

def test_getProfileMaxCountry_filmHasMultipleCountries_EnsuresOnlyOneIsReturned():
    allGenresLength = len(mockGenres)

    filmVectorWithAmericanAndBritish = [0.0, 0.0, 0.0, 0.0, 0.0, 0.7, 0.0, 0.0, 0.0, 0.0, 0.0, 0.7, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.7, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

    assert (vectorizeUtilities.getProfileMaxCountry(filmVectorWithAmericanAndBritish, allGenresLength, mockCountries) 
            == "American")


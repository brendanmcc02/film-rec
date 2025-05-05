from flask import jsonify
import os
import shutil

class ServiceUtilities:

    DATE_RATED_WEIGHT = 0.8
    NUMBER_OF_RECOMMENDATIONS_PER_ROW = 6
    NUMBER_OF_FILMS_WATCHED_IN_GENRE_THRESHOLD = 30
    NUMBER_OF_GENRE_RECOMMENDATION_ROWS = 3
    RECOMMENDATION_REVIEW_FACTOR = 0.2
    USER_UPLOADED_DATA_DIRECTORY_NAME = "user-uploaded-data/"
    UNSUPPORTED_MEDIA_TYPE_ERROR_MESSAGE = "File must be .csv or .zip."
    NO_FILE_IN_REQUEST_ERROR_MESSAGE = "No file found in the request"
    FILE_MORE_DATA_THAN_ROW_HEADERS_ERROR_MESSAGE = "File has more data than row headers."
    FILE_ROW_HEADERS_UNEXPECTED_FORMAT_ERROR_MESSAGE = "Row headers do not conform to expected format."
    INVALID_ZIP_FILE_ERROR_MESSAGE = "Zip file is invalid."
    EXPECTED_IMDB_FILM_ATTRIBUTES = ["Const", "Your Rating", "Date Rated", "Title", "Original Title", "URL",
                                     "Title Type", "IMDb Rating", "Runtime (mins)", "Year", "Genres", "Num Votes",
                                     "Release Date", "Directors"]
    FAVOURITE_FILM_RATING_THRESHOLD = 9

    def isFilmRecommendationUnique(self, filmId, rowsOfRecommendations):
        for rowOfRecommendations in rowsOfRecommendations:
            for recommendedFilm in rowOfRecommendations['recommendedFilms']:
                if recommendedFilm['imdbId'] == filmId:
                    return False
                
        return True
    
    def deleteUserUploadedData(self):
        for fileOrDirectory in os.listdir(self.USER_UPLOADED_DATA_DIRECTORY_NAME):
            fileOrDirectoryPath = os.path.join(self.USER_UPLOADED_DATA_DIRECTORY_NAME, fileOrDirectory)
            if os.path.isdir(fileOrDirectoryPath):
                shutil.rmtree(fileOrDirectoryPath)
            elif os.path.basename(fileOrDirectoryPath) != ".gitignore":
                os.remove(fileOrDirectoryPath)

    def getFormattedResponse(self, body, errorMessage, guid, statusCode):
        return jsonify({"body": body,
                        "errorMessage": errorMessage, 
                        "guid": guid}), statusCode

    def initCachedDatabase(self, database):
        cachedDatabase = {}

        cachedDatabase["AllFilmData"] = database.read("AllFilmData")
        cachedDatabase["AllFilmDataVectorized"] = database.read("AllFilmDataVectorized")
        cachedDatabase["AllFilmDataVectorizedMagnitudes"] = database.read("AllFilmDataVectorizedMagnitudes")
        cachedDatabase["CachedLetterboxdTitles"] = database.read("CachedLetterboxdTitles")
        cachedDatabase["AllGenres"] = database.read("AllGenres")
        cachedDatabase["AllGenresLength"] = len(cachedDatabase["AllGenres"])
        cachedDatabase["AllCountries"] = database.read("AllCountries")
        cachedDatabase["AllCountriesLength"] = len(cachedDatabase["AllCountries"])
        cachedDatabase["ProfileVectorLength"] = database.read("ProfileVectorLength")
        cachedDatabase["MinNumberOfVotes"] = database.read("MinNumberOfVotes")
        cachedDatabase["DiffNumberOfVotes"] = database.read("DiffNumberOfVotes")
        cachedDatabase["NormalizedYears"] = database.read("NormalizedYears")
        cachedDatabase["NormalizedYearsKeys"] = list(cachedDatabase["NormalizedYears"].keys())
        cachedDatabase["NormalizedImdbRatings"] = database.read("NormalizedImdbRatings")
        cachedDatabase["NormalizedImdbRatingsKeys"]  = list(cachedDatabase["NormalizedImdbRatings"].keys())
        cachedDatabase["NormalizedRuntimes"] = database.read("NormalizedRuntimes")
        cachedDatabase["NormalizedRuntimesKeys"] = list(cachedDatabase["NormalizedRuntimes"].keys())

        return cachedDatabase

    def getAllFilmDataUnseen(self, allFilmData, userFilmData):
        allFilmDataUnseen = {}

        for imdbFilmId in allFilmData:
            if imdbFilmId not in userFilmData:
                allFilmDataUnseen[imdbFilmId] = allFilmData[imdbFilmId]

        return allFilmDataUnseen
    
    def getFormattedFilm(self, film, dateRated, genres, countries):
        return {
            "title": film['Title'],
            "year": int(film['Year']),
            "userRating": int(film['Your Rating']),
            "dateRated": dateRated,
            "imdbRating": float(film['IMDb Rating']),
            "numberOfVotes": int(film['Num Votes']),
            "runtime": int(film['Runtime (mins)']),
            "genres": genres,
            "countries": countries
        }
    
    def isFilmValid(self, film, runtimeThreshold, numberOfVotesThreshold):
        return (film['Title Type'] == "Movie" and 
                film['Genres'] != "" and 
                int(film['Runtime (mins)']) >= runtimeThreshold and 
                int(film['Num Votes']) >= numberOfVotesThreshold)
import csv
from flask import jsonify
import os
import shutil

class ServiceUtilities:

    DATE_RATED_WEIGHT = 0.8
    MAX_NUMBER_OF_RECOMMENDATIONS_PER_ROW = 6
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
        for row in rowsOfRecommendations:
            for recommendedFilm in row['recommendedFilms']:
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
    
    def getFilmGenresCorrectFormat(self, filmGenres, isImdbFile):
        if isImdbFile:
            return filmGenres.replace("\"", "").split(", ")
        else:
            return filmGenres
        
    def getNormalizedDateRatedWeight(self, dateRated, minDateRated, diffDateRated):
        return (((dateRated - minDateRated) / diffDateRated) *
                                    (1 - self.DATE_RATED_WEIGHT)) + self.DATE_RATED_WEIGHT

    def getProfileIdAssociatedWithFilmId(self, rowsOfRecommendations, filmId):
        for row in rowsOfRecommendations:
            for film in row['recommendedFilms']:
                if film['imdbId'] == filmId:
                    return row["profileId"]

    def isProfileIdGenreProfile(self, profileId, allGenres):
        return profileId in allGenres

    def getUserFilmDataOriginalFromFile(self, requestFiles, guid, letterboxdConversionUtilities):
        isImdbFile = True

        self.deleteUserUploadedData()

        if 'file' not in requestFiles:
            return self.getFormattedResponse({}, self.NO_FILE_IN_REQUEST_ERROR_MESSAGE, guid, 400)

        file = requestFiles['file']
        userFilmDataFilename = (guid + "-" + file.filename)

        if self.isUnacceptableMediaType(userFilmDataFilename):
            return self.getFormattedResponse({}, self.UNSUPPORTED_MEDIA_TYPE_ERROR_MESSAGE, guid, 415)

        try:
            userFilmDataOriginal = []
            userUploadedFileLocation = self.USER_UPLOADED_DATA_DIRECTORY_NAME + userFilmDataFilename
            file.save(userUploadedFileLocation)

            if userUploadedFileLocation.endswith(".zip"):
                if letterboxdConversionUtilities.isLetterboxdZipFileInvalid(self.USER_UPLOADED_DATA_DIRECTORY_NAME, userFilmDataFilename):
                    return self.getFormattedResponse({}, self.INVALID_ZIP_FILE_ERROR_MESSAGE, guid, 400)
                else:
                    userFilmDataFilename = "ratings.csv"
                    userUploadedFileLocation = self.USER_UPLOADED_DATA_DIRECTORY_NAME + userFilmDataFilename

            with open(userUploadedFileLocation, encoding='utf-8') as userFilmDataFile:
                reader = csv.DictReader(userFilmDataFile, delimiter=',', restkey='unexpectedData')

                for row in reader:
                    if 'unexpectedData' in row:
                        return self.getFormattedResponse({}, self.FILE_MORE_DATA_THAN_ROW_HEADERS_ERROR_MESSAGE, guid, 400)

                    keys = list(row.keys())
                    for key in keys:
                        if key not in self.EXPECTED_IMDB_FILM_ATTRIBUTES:
                            isImdbFile = False
                            if key not in letterboxdConversionUtilities.EXPECTED_LETTERBOXD_FILE_FILM_ATTRIBUTES:
                                return self.getFormattedResponse({}, self.FILE_ROW_HEADERS_UNEXPECTED_FORMAT_ERROR_MESSAGE, guid, 400)

                    userFilmDataOriginal.append(row)
        except Exception as e:
            return self.getFormattedResponse({}, f"Error occurred with reading {userFilmDataFilename}.\n{e}", guid, 400)
        finally:
            self.deleteUserUploadedData()

        return self.getFormattedResponse({"userFilmDataOriginal": userFilmDataOriginal, "isImdbFile": isImdbFile}, "", guid, 200)
    
    def isUnacceptableMediaType(self, filename):
        return not (filename.lower().endswith(".csv") or filename.lower().endswith(".zip"))

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
    FILE_UPLOAD_SUCCESS_MESSAGE = "Upload Success."
    INVALID_ZIP_FILE_ERROR_MESSAGE = "Zip file is invalid."

    def __init__(self):
        pass

    def isFilmRecommendationUnique(self, filmId, rowsOfRecommendations):
        for rowOfRecommendations in rowsOfRecommendations:
            for recommendedFilm in rowOfRecommendations['recommendedFilms']:
                if recommendedFilm['id'] == filmId:
                    return False
                
        return True
    
    def deleteUserUploadedData(self):
        for fileOrDirectory in os.listdir(self.USER_UPLOADED_DATA_DIRECTORY_NAME):
            fileOrDirectoryPath = os.path.join(self.USER_UPLOADED_DATA_DIRECTORY_NAME, fileOrDirectory)
            if os.path.isdir(fileOrDirectoryPath):
                shutil.rmtree(fileOrDirectoryPath)
            elif os.path.basename(fileOrDirectoryPath) != ".gitignore":
                os.remove(fileOrDirectoryPath)


    def isUnacceptableMediaType(self, filename):
        return not (filename.lower().endswith(".csv") or filename.lower().endswith(".zip"))

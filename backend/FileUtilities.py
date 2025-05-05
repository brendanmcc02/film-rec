import csv

class FileUtilities:

    def __init__(self, serviceUtilities, letterboxdConversionUtilities):
        self.serviceUtilities = serviceUtilities
        self.letterboxdConversionUtilities = letterboxdConversionUtilities

    def getUserFilmDataOriginalFromFile(self, requestFiles, guid):
        isImdbFile = True

        self.serviceUtilities.deleteUserUploadedData()

        if 'file' not in requestFiles:
            return self.serviceUtilities.getFormattedResponse({}, self.serviceUtilities.NO_FILE_IN_REQUEST_ERROR_MESSAGE, guid, 400)

        file = requestFiles['file']
        userFilmDataFilename = (guid + "-" + file.filename)

        if self.isUnacceptableMediaType(userFilmDataFilename):
            return self.serviceUtilities.getFormattedResponse({}, self.serviceUtilities.UNSUPPORTED_MEDIA_TYPE_ERROR_MESSAGE, guid, 415)

        try:
            userFilmDataOriginal = []
            userUploadedFileLocation = self.serviceUtilities.USER_UPLOADED_DATA_DIRECTORY_NAME + userFilmDataFilename
            file.save(userUploadedFileLocation)

            if userUploadedFileLocation.endswith(".zip"):
                if self.letterboxdConversionUtilities.isLetterboxdZipFileInvalid(self.serviceUtilities.USER_UPLOADED_DATA_DIRECTORY_NAME, userFilmDataFilename):
                    return self.serviceUtilities.getFormattedResponse({}, self.serviceUtilities.INVALID_ZIP_FILE_ERROR_MESSAGE, guid, 400)
                else:
                    userFilmDataFilename = "ratings.csv"
                    userUploadedFileLocation = self.serviceUtilities.USER_UPLOADED_DATA_DIRECTORY_NAME + userFilmDataFilename

            with open(userUploadedFileLocation, encoding='utf-8') as userFilmDataFile:
                reader = csv.DictReader(userFilmDataFile, delimiter=',', restkey='unexpectedData')

                for row in reader:
                    if 'unexpectedData' in row:
                        return self.serviceUtilities.getFormattedResponse({}, self.serviceUtilities.FILE_MORE_DATA_THAN_ROW_HEADERS_ERROR_MESSAGE, guid, 400)

                    keys = list(row.keys())
                    for key in keys:
                        if key not in self.serviceUtilities.EXPECTED_IMDB_FILM_ATTRIBUTES:
                            isImdbFile = False
                            if key not in self.letterboxdConversionUtilities.EXPECTED_LETTERBOXD_FILE_FILM_ATTRIBUTES:
                                return self.serviceUtilities.getFormattedResponse({}, self.serviceUtilities.FILE_ROW_HEADERS_UNEXPECTED_FORMAT_ERROR_MESSAGE, guid, 400)

                    userFilmDataOriginal.append(row)
        except Exception as e:
            return self.serviceUtilities.getFormattedResponse({}, f"Error occurred with reading {userFilmDataFilename}.\n{e}", guid, 400)
        finally:
            self.serviceUtilities.deleteUserUploadedData()

        return self.serviceUtilities.getFormattedResponse({"userFilmDataOriginal": userFilmDataOriginal, "isImdbFile": isImdbFile}, "", guid, 200)
    
    def isUnacceptableMediaType(self, filename):
        return not (filename.lower().endswith(".csv") or filename.lower().endswith(".zip"))
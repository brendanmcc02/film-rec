# contains utilities to allow letterboxd files to be converted to the imdb format.
import os
import shutil
from zipfile import ZipFile


class letterboxdConversionUtilities:

    EXPECTED_LETTERBOXD_FILE_FILM_ATTRIBUTES = ["Date", "Name", "Year", "Letterboxd URI", "Rating"]
    EXPECTED_LETTERBOXD_EXTRACTED_FILES_OR_DIRECTORIES = ["deleted", "likes", "lists", "orphaned", "comments.csv", "diary.csv", "profile.csv", "ratings.csv", "reviews.csv", "watched.csv", "watchlist.csv", ".gitignore"]

    def convertLetterboxdFormatToImdbFormat(self, letterboxdUserFilmData, allFilmData, cachedLetterboxdTitles):
        imdbUserFilmData = []

        # work with latest entries first
        letterboxdUserFilmData = reversed(letterboxdUserFilmData)

        for letterboxdFilm in letterboxdUserFilmData:
            if "Name" in letterboxdFilm:
                letterboxdTitle = letterboxdFilm["Name"]
                letterboxdTitle = letterboxdTitle.replace("– ", "- ").replace("–", "-").replace("Colours", "Colors")
            else:
                print("Error. 'Name' attribute not in letterboxd film")
                raise KeyError
            
            if "Year" in letterboxdFilm:
                letterboxdYear = int(letterboxdFilm["Year"])
            else:
                print("Error. 'Year' attribute not in letterboxd film")
                raise KeyError

            if letterboxdTitle in cachedLetterboxdTitles:
                for cachedFilm in cachedLetterboxdTitles[letterboxdTitle]:
                    if letterboxdYear in cachedFilm['years']:
                        imdbFilmId = cachedFilm['imdbFilmId']
                        imdbUserFilmData.append({
                            "Const": imdbFilmId,
                            # for consistency, use the imdb title instead of the letterboxd one
                            "Title": allFilmData[imdbFilmId]['title'],
                            "Title Type": "Movie",
                            # for consistency, use the imdb year instead of the letterboxd one
                            "Year": allFilmData[imdbFilmId]['year'],
                            "Your Rating": int(float(letterboxdFilm['Rating']) * 2.0),
                            "Date Rated": letterboxdFilm['Date'],
                            "IMDb Rating": allFilmData[imdbFilmId]['imdbRating'],
                            "Num Votes": allFilmData[imdbFilmId]['numberOfVotes'],
                            "Runtime (mins)": allFilmData[imdbFilmId]['runtime'],
                            "Genres": allFilmData[imdbFilmId]['genres']
                        })
            # else:
            #     print(f"Letterboxd Film not found in cached-letterboxd-titles.json:\n{letterboxdTitle}")

        return imdbUserFilmData


    # unzips file, removes everything except `ratings.csv` and then returns if the given zip file is valid or not
    def isLetterboxdZipFileInvalid(self, userUploadedDataDirectory, zipFileName):
        zipFilePath = os.path.join(userUploadedDataDirectory, zipFileName)
        with ZipFile(zipFilePath, 'r') as zipFile:
            zipFile.extractall(userUploadedDataDirectory)

        os.remove(zipFilePath)

        for fileOrDirectory in os.listdir(userUploadedDataDirectory):
            if fileOrDirectory not in self.EXPECTED_LETTERBOXD_EXTRACTED_FILES_OR_DIRECTORIES:
                return True
            
            fileOrDirectoryPath = os.path.join(userUploadedDataDirectory, fileOrDirectory)

            if os.path.isdir(fileOrDirectoryPath):
                shutil.rmtree(fileOrDirectoryPath)
            elif (os.path.basename(fileOrDirectoryPath) != "ratings.csv" and
                os.path.basename(fileOrDirectoryPath) != ".gitignore"):
                os.remove(fileOrDirectoryPath)

        return False

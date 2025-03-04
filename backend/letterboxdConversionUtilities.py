# contains utilities to allow letterboxd files to be converted to the imdb format.
import os
import shutil
from zipfile import ZipFile

expectedLetterboxdFileFilmAttributes = ["Date", "Name", "Year", "Letterboxd URI", "Rating"]
expectedLetterboxdExtractedFilesOrDirectories = ["deleted/", "likes/", "lists/" "orphaned/", "comments.csv", "diary.csv", "profile.csv", "ratings.csv", "reviews.csv", "watched.csv", "watchlist.csv"]


def convertLetterboxdFormatToImdbFormat(letterboxdUserFilmData, allFilmData, cachedLetterboxdTitles):
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


def isLetterboxdZipFileInvalid(userUploadedDataDirectory, zipFileName):
    zipFilePath = os.path.join(userUploadedDataDirectory, zipFileName)
    with ZipFile(zipFilePath, 'r') as zipFile:
        zipFile.extractall(userUploadedDataDirectory)

    for fileOrDirectory in os.listdir(userUploadedDataDirectory):
        if fileOrDirectory.lower() not in expectedLetterboxdExtractedFilesOrDirectories:
            return True
        fileOrDirectoryPath = os.path.join(userUploadedDataDirectory, fileOrDirectory)
        if os.path.isdir(fileOrDirectoryPath):
            shutil.rmtree(fileOrDirectoryPath)
        elif os.path.basename(fileOrDirectoryPath) != "ratings.csv":
            os.remove(fileOrDirectoryPath)

    return False


isLetterboxdZipFileInvalid("user-uploaded-data/", "letterboxd-brendanmcc02-2025-03-04-20-37-utc.zip")

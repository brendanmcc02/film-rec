import os
import shutil
from zipfile import ZipFile

EXPECTED_LETTERBOXD_FILE_FILM_ATTRIBUTES = ["Date", "Name", "Year", "Letterboxd URI", "Rating"]
EXPECTED_LETTERBOXD_EXTRACTED_FILES_OR_DIRECTORIES = ["deleted", "likes", "lists", "orphaned", "comments.csv", "diary.csv", "profile.csv", "ratings.csv", "reviews.csv", "watched.csv", "watchlist.csv", ".gitignore"]

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
                    imdbimdbFilmId = cachedFilm['imdbimdbFilmId']
                    imdbUserFilmData.append({
                        "Const": imdbimdbFilmId,
                        "Title": allFilmData[imdbimdbFilmId]['title'],
                        "Title Type": "Movie",
                        "Year": allFilmData[imdbimdbFilmId]['year'],
                        "Your Rating": int(float(letterboxdFilm['Rating']) * 2.0),
                        "Date Rated": letterboxdFilm['Date'],
                        "IMDb Rating": allFilmData[imdbimdbFilmId]['imdbRating'],
                        "Num Votes": allFilmData[imdbimdbFilmId]['numberOfVotes'],
                        "Runtime (mins)": allFilmData[imdbimdbFilmId]['runtime'],
                        "Genres": allFilmData[imdbimdbFilmId]['genres']
                    })
        # else:
        #     print(f"Letterboxd Film not found in cachedLetterboxdTitles.json:\n{letterboxdTitle}")

    return imdbUserFilmData

def isLetterboxdZipFileInvalid(userUploadedDataDirectory, zipFileName):
    zipFilePath = os.path.join(userUploadedDataDirectory, zipFileName)
    with ZipFile(zipFilePath, 'r') as zipFile:
        zipFile.extractall(userUploadedDataDirectory)

    os.remove(zipFilePath)

    for fileOrDirectory in os.listdir(userUploadedDataDirectory):
        if fileOrDirectory not in EXPECTED_LETTERBOXD_EXTRACTED_FILES_OR_DIRECTORIES:
            return True
        
        fileOrDirectoryPath = os.path.join(userUploadedDataDirectory, fileOrDirectory)

        if os.path.isdir(fileOrDirectoryPath):
            shutil.rmtree(fileOrDirectoryPath)
        elif (os.path.basename(fileOrDirectoryPath) != "ratings.csv" and
                os.path.basename(fileOrDirectoryPath) != ".gitignore"):
            os.remove(fileOrDirectoryPath)

    return False

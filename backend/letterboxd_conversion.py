expectedLetterboxdFileFilmAttributes = ["Date", "Name", "Year", "Letterboxd URI", "Rating"]


def convertLetterboxdFormatToImdbFormat(oldUserFilmDataList, allFilmDataFull, allFilmDataKeys):
    newUserFilmDataList = []

    # we want to work with latest entries first
    oldUserFilmDataList = reversed(oldUserFilmDataList)

    letterboxdTitleYearDict = {}

    for filmId in allFilmDataKeys:
        letterboxdTitle = allFilmDataFull[filmId]['letterboxdTitle']
        letterboxdYear = allFilmDataFull[filmId]['letterboxdYear']
        concatTitleYear = letterboxdTitle + letterboxdYear
        letterboxdTitleYearDict[concatTitleYear] = filmId

    for film in oldUserFilmDataList:
        filmTitle = film['Title']
        filmYear = film['Year']
        concatTitleYear = filmTitle + filmYear
        if concatTitleYear in letterboxdTitleYearDict:
            filmId = letterboxdTitleYearDict[concatTitleYear]
            newUserFilmDataList.append({
                "Const": filmId,
                # for consistency, use the imdb title instead of the letterboxd one
                "Title": allFilmDataFull[filmId]['title'],
                "Title Type": "Movie",
                # we want to use the year attribute from all-film-data.json as opposed to the letterboxd one,
                # sometimes there is a 1-year difference between imdb & letterboxd versions of the same film.
                "Year": allFilmDataFull[filmId]['year'],
                "Your Rating": round(float(film['Rating']) * 2.0, 1),
                "Date Rated": film['Date'],
                "IMDb Rating": allFilmDataFull[filmId]['imdbRating'],
                "Num Votes": allFilmDataFull[filmId]['numberOfVotes'],
                "Runtime (mins)": allFilmDataFull[filmId]['runtime'],
                "Genres": allFilmDataFull[filmId]['genres']
            })
        # else:
        #     print(f"Film not found {filmTitle}, {filmYear}")

    return newUserFilmDataList

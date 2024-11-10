expectedLetterboxdFileFilmAttributes = ["Date", "Name", "Year", "Letterboxd URI", "Rating"]


def convertLetterboxdFormatToImdbFormat(letterboxdUserFilmData, allFilmData, allFilmDataKeys):
    imdbUserFilmData = []

    # we want to work with latest entries first
    letterboxdUserFilmData = reversed(letterboxdUserFilmData)

    letterboxdTitleYearDict = {}

    for filmId in allFilmDataKeys:
        letterboxdTitle = allFilmData[filmId]['letterboxdTitle']
        letterboxdYear = str(allFilmData[filmId]['letterboxdYear'])
        concatTitleYear = letterboxdTitle + letterboxdYear
        letterboxdTitleYearDict[concatTitleYear] = filmId

    for film in letterboxdUserFilmData:
        filmTitle = film['Title']
        filmYear = film['Year']
        concatTitleYear = filmTitle + filmYear
        if concatTitleYear in letterboxdTitleYearDict:
            filmId = letterboxdTitleYearDict[concatTitleYear]
            imdbUserFilmData.append({
                "Const": filmId,
                # for consistency, use the imdb title instead of the letterboxd one
                "Title": allFilmData[filmId]['title'],
                "Title Type": "Movie",
                # we want to use the year attribute from all-film-data.json as opposed to the letterboxd one,
                # sometimes there is a 1-year difference between imdb & letterboxd versions of the same film.
                "Year": allFilmData[filmId]['year'],
                "Your Rating": round(float(film['Rating']) * 2.0, 1),
                "Date Rated": film['Date'],
                "IMDb Rating": allFilmData[filmId]['imdbRating'],
                "Num Votes": allFilmData[filmId]['numberOfVotes'],
                "Runtime (mins)": allFilmData[filmId]['runtime'],
                "Genres": allFilmData[filmId]['genres']
            })
        else:
            print(f"Film not found {filmTitle}, {filmYear}")

    return imdbUserFilmData

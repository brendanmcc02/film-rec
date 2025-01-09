expectedLetterboxdFileFilmAttributes = ["Date", "Name", "Year", "Letterboxd URI", "Rating"]


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
        else:
            print(f"Letterboxd Film not found in cached-letterboxd-titles.json:\n{letterboxdTitle}")

    return imdbUserFilmData

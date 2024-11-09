expectedLetterboxdFileFilmAttributes = ["Date", "Name", "Year", "Letterboxd URI", "Rating"]


def convertLetterboxdFormatToImdbFormat(oldUserFilmDataList, allFilmDataFull, allFilmDataKeys):
    newUserFilmDataList = []

    # we want to work with latest entries first
    oldUserFilmDataList = reversed(oldUserFilmDataList)

    # cache titles for more efficiency in searchImdbFilm() method
    cachedAllFilmDataTitles = {}

    for filmId in allFilmDataKeys:
        cachedAllFilmDataTitles[filmId] = letterboxdToImdbTitleConversion(allFilmDataFull[filmId]['title'],
                                                                          allFilmDataFull[filmId]['year'])

    for film in oldUserFilmDataList:
        filmYear = int(film['Year'])
        filmTitle = letterboxdToImdbTitleConversion(film['Name'], filmYear)

        filmId = searchImdbFilm(filmTitle, filmYear, allFilmDataFull, allFilmDataKeys, cachedAllFilmDataTitles)

        if filmId != "not found":
            newUserFilmDataList.append({
                "Const": filmId,
                "Title": filmTitle,
                "Title Type": "Movie",
                # we want to use the year attribute from all-film-database.json as opposed to the letterboxd one,
                # sometimes there is a 1-year difference between imdb & letterboxd versions of the same film.
                # best to keep it consistent and follow imdb
                "Year": allFilmDataFull[filmId]['year'],
                "Your Rating": round(float(film['Rating']) * 2.0, 1),
                "Date Rated": film['Date'],
                "IMDb Rating": allFilmDataFull[filmId]['imdbRating'],
                "Num Votes": allFilmDataFull[filmId]['numberOfVotes'],
                "Runtime (mins)": allFilmDataFull[filmId]['runtime'],
                "Genres": allFilmDataFull[filmId]['genres']
            })
        # else:
        #     print("film not found. title: " + filmTitle + ". year:" + str(filmYear))

    return newUserFilmDataList


def searchImdbFilm(letterboxdTitle, letterboxdYear, allFilmDataFull, allFilmDataKeys, cachedAllFilmDataTitles):
    for filmId in allFilmDataKeys:
        if letterboxdTitle == cachedAllFilmDataTitles[filmId]:
            # some films have different year releases between letterboxd & imdb.
            # e.g. Ex Machina is 2014 in IMDb, but 2015 in Letterboxd
            if abs(letterboxdYear - allFilmDataFull[filmId]['year']) <= 1:
                return filmId

    return "not found"


def letterboxdToImdbTitleConversion(letterboxdTitle, year):
    newTitle = letterboxdTitle
    match letterboxdTitle:
        case "Star Wars: Episode II – Attack of the Clones":
            newTitle = "Star Wars: Episode II - Attack of the Clones"
        case "Star Wars: Episode III – Revenge of the Sith":
            newTitle = "Star Wars: Episode III - Revenge of the Sith"
        case "Star Wars":
            newTitle = "Star Wars: Episode IV - A New Hope"
        case "The Empire Strikes Back":
            newTitle = "Star Wars: Episode V - The Empire Strikes Back"
        case "Return of the Jedi":
            newTitle = "Star Wars: Episode VI - Return of the Jedi"
        case "Star Wars: The Force Awakens":
            newTitle = "Star Wars: Episode VII - The Force Awakens"
        case "Star Wars: The Last Jedi":
            newTitle = "Star Wars: Episode VIII - The Last Jedi"
        case "Star Wars: The Rise of Skywalker":
            newTitle = "Star Wars: Episode IX - The Rise of Skywalker"
        case "Harry Potter and the Philosopher's Stone":
            newTitle = "Harry Potter and the Sorcerer's Stone"
        case "Dune":
            if year == 2021:
                newTitle = "Dune: Part One"
        case "Birds of Prey (and the Fantabulous Emancipation of One Harley Quinn)":
            newTitle = "Birds of Prey"
        case "My Left Foot: The Story of Christy Brown":
            newTitle = "My Left Foot"
        case "(500) Days of Summer":
            newTitle = "500 Days of Summer"

    newTitle = newTitle.lower()  # lower case
    # todo the following 2 lines should be done in an offline phase when creating all-film-data.json
    newTitle = newTitle.replace("–", "-").replace(" ", "").replace("&", "and")
    newTitle = newTitle.replace("colour", "color")

    return newTitle

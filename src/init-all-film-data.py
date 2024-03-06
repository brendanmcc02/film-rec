# 1. download latest film data from https://datasets.imdbws.com/ (title.basics.tsv & title.ratings.tsv)
# 2. filter through this data
# 3. produces all-film-data.json

# imports
import json
import csv


def main():
    print("\n[Stage 1/3] Filtering out:\n1. non-movies\n2. released < 1930\n3. with no genres\n4. < 60 min runtime")

    print("\nImporting title.basics.tsv")
    # import title-basics.tsv as list of dicts
    title_basics_raw = []
    with open("../data/title.basics.tsv", 'r', encoding='utf-8', newline='') as title_basics_file:
        reader = csv.DictReader(title_basics_file, delimiter='\t')
        for row in reader:
            title_basics_raw.append(dict(row))

    print("Imported title.basics.tsv")
    stage_1_allFilmData = []

    # iterate through each film:
    for film in title_basics_raw:
        try:
            # if the film is a movie, released >= 1930, has genres, and has >= 60 min runtime:
            if (film["titleType"] == 'movie' and int(film['startYear']) >= 1930
                    and film['genres'] != r"\N" and int(film['runtimeMinutes']) >= 60):
                newFilm = {}
                # rename attributes
                newFilm['id'] = film['tconst']
                newFilm['year'] = int(film['startYear'])  # convert from str to int

                # convert genres from string to array of strings
                # e.g. genres: "Action, Family" => genres: {"Action", "Family"}
                newFilm['genres'] = film['genres'].split(',')

                stage_1_allFilmData.append(newFilm)
        except ValueError:
            pass

    print("\n[Stage 2/3] Merging with title.ratings.tsv and filtering out films with < 10,000 votes:")

    stage_2_allFilmData = []

    # import title-ratings.tsv as a dict.
    # the key is the film id, and the value is a dictionary of the attributes (averageRating & numVotes) of the film
    title_ratings = {}
    with open("../data/title.ratings.tsv", 'r', encoding='utf-8', newline='') as title_ratings_file:
        reader = csv.DictReader(title_ratings_file, delimiter='\t')
        for row in reader:
            rowDict = dict(row)
            filmId = rowDict['tconst']
            title_ratings[filmId] = rowDict

    # iterate through each film in stage_1
    for film in stage_1_allFilmData:
        filmId = film['id']
        try:
            # could numVotes threshold to another number (e.g. 25k), i'll leave it at 10k for now.
            if filmId in title_ratings and int(title_ratings[filmId]['numVotes']) >= 10000:
                film['imdbRating'] = float(title_ratings[filmId]['averageRating'])
                film['numberOfVotes'] = int(title_ratings[filmId]['numVotes'])
                stage_2_allFilmData.append(film)
        # some films may not have 'numVotes' or 'averageRating' attributes
        except ValueError:
            pass

    print("\n[Stage 3/3] Filtering out films that I've rated and changing the order of json attributes:")

    allFilmData = []

    # import my-film-data.json as a dictionary
    myFilmDataFile = open('../data/my-film-data.json')
    myFilmData = json.load(myFilmDataFile)

    # create a dictionary of films that I have rated
    # key = film id, value = unused boolean
    myFilmDataDict = {}
    for myFilm in myFilmData:
        myFilmDataDict[myFilm['id']] = True

    # for each film in stage 2:
    for film in stage_2_allFilmData:
        # if the film is a film that I have not rated
        if film['id'] not in myFilmDataDict:
            # changing the order of json attributes
            allFilmData.append({
                'id': film['id'],
                'year': film['year'],
                'imdbRating': film['imdbRating'],
                'genres': film['genres'],
                'numberOfVotes': film['numberOfVotes']
            })

    # write to file
    with open('../data/all-film-data.json', 'w') as convert_file:
        convert_file.write(json.dumps(allFilmData, indent=4, separators=(',', ': ')))


if __name__ == "__main__":
    main()

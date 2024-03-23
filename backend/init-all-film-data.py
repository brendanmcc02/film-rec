# given title.basics.tsv & title.ratings.tsv, filter through these datasets and produce all-film-data.json

# imports
import json
import csv


# global constants
MIN_RUNTIME = 40
MIN_VOTES = 25000


def main():
    print("\nFiltering out films:\n1. that are not movies\n2. with no genres\n3. <" + str(MIN_RUNTIME) + " min runtime")

    print("\nImporting title.basics.tsv...")
    # import title-basics.tsv as list of dicts
    title_basics_raw = []
    with open("../data/title.basics.tsv", 'r', encoding='utf-8', newline='') as title_basics_file:
        reader = csv.DictReader(title_basics_file, delimiter='\t')
        for row in reader:
            title_basics_raw.append(dict(row))

    print("Imported title.basics.tsv.")
    stage_1_allFilmData = []

    # iterate through each film:
    for film in title_basics_raw:
        try:
            # if the film is a movie, has genres, and has >= 40 min runtime:
            if (film["titleType"] == 'movie' and film['genres'] != r"\N"
                    and int(film['runtimeMinutes']) >= MIN_RUNTIME):
                newFilm = {}
                # rename attributes
                newFilm['id'] = film['tconst']
                newFilm['title'] = film['primaryTitle']
                newFilm['year'] = int(film['startYear'])  # convert from str to int
                newFilm['runtime'] = int(film['runtimeMinutes'])

                # convert genres from string to array of strings
                # e.g. genres: "Action, Family" => genres: {"Action", "Family"}
                newFilm['genres'] = film['genres'].split(',')

                stage_1_allFilmData.append(newFilm)
        except ValueError:
            pass

    print("\nMerging with title.ratings.tsv and filtering out films with <" + str(MIN_VOTES) + " votes...")

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
            if filmId in title_ratings and int(title_ratings[filmId]['numVotes']) >= MIN_VOTES:
                film['imdbRating'] = float(title_ratings[filmId]['averageRating'])
                film['numberOfVotes'] = int(title_ratings[filmId]['numVotes'])
                stage_2_allFilmData.append(film)
        # some films may not have 'numVotes' or 'averageRating' attributes
        except ValueError:
            pass

    print("\nFiltering out films that I've rated and changing the order of json attributes...")

    allFilmData = {}

    # import my-film-data.json as a dictionary
    myFilmDataFile = open('../data/my-film-data.json')
    myFilmData = json.load(myFilmDataFile)
    myFilmDataKeys = list(myFilmData.keys())

    # for each film in stage 2:
    for film in stage_2_allFilmData:
        # if the film is a film that I have not rated
        if film['id'] not in myFilmDataKeys:
            # changing the order of json attributes
            allFilmData[film['id']] = {
                'title': film['title'],
                'year': film['year'],
                'imdbRating': film['imdbRating'],
                'numberOfVotes': film['numberOfVotes'],
                'runtime': film['runtime'],
                'genres': film['genres']
            }

    print("Final Dataset size: " + str(len(allFilmData)) + " films.")

    # write to file
    with open('../data/all-film-data.json', 'w') as convert_file:
        convert_file.write(json.dumps(allFilmData, indent=4, separators=(',', ': ')))


if __name__ == "__main__":
    main()

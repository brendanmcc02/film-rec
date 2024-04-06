# given title.basics.tsv & title.ratings.tsv, filter and produce all-film-data.json

# imports
import json
import csv

# global constants
RUNTIME_THRESHOLD = 40
NUM_OF_VOTES_THRESHOLD = 25000
MIN_IMDB_RATING = 0.0
MIN_YEAR = 0
MIN_NUMBER_OF_VOTES = 0
MIN_RUNTIME = 0
DIFF_IMDB_RATING = 0.0
DIFF_YEAR = 0
DIFF_NUMBER_OF_VOTES = 0
DIFF_RUNTIME = 0
year_norms = {}


def main():
    print("\nImporting title.basics.tsv...")
    # import title-basics.tsv as list of dicts
    title_basics_raw = []
    with open("../data/title.basics.tsv", 'r', encoding='utf-8', newline='') as title_basics_file:
        reader = csv.DictReader(title_basics_file, delimiter='\t')
        for row in reader:
            title_basics_raw.append(dict(row))

    print("Imported title.basics.tsv.")
    print("\nFiltering out films:\n1. that are not movies\n2. with no genres\n3. <"
          + str(RUNTIME_THRESHOLD) + " min runtime")

    stage_1_allFilmData = []

    # iterate through each film:
    for film in title_basics_raw:
        try:
            # if the film is a movie, has genres, and has >= 40 min runtime:
            if (film["titleType"] == 'movie' and film['genres'] != r"\N"
                    and int(film['runtimeMinutes']) >= RUNTIME_THRESHOLD):
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

    print("\nMerging with title.ratings.tsv and filtering out films with <" + str(NUM_OF_VOTES_THRESHOLD) + " votes...")

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
            if filmId in title_ratings and int(title_ratings[filmId]['numVotes']) >= NUM_OF_VOTES_THRESHOLD:
                film['imdbRating'] = float(title_ratings[filmId]['averageRating'])
                film['numberOfVotes'] = int(title_ratings[filmId]['numVotes'])
                stage_2_allFilmData.append(film)
        # some films may not have 'numVotes' or 'averageRating' attributes
        except ValueError:
            pass

    print("\nChanging the order of json attributes...")

    allFilmData = {}

    # for each film in stage 2:
    for film in stage_2_allFilmData:
        # change the order of json attributes
        allFilmData[film['id']] = {
            'title': film['title'],
            'year': film['year'],
            'imdbRating': film['imdbRating'],
            'numberOfVotes': film['numberOfVotes'],
            'runtime': film['runtime'],
            'genres': film['genres']
        }

    print("\nFinal Dataset size: " + str(len(allFilmData)) + " films.\n")

    # write to all-film-data.json
    with open('../data/all-film-data.json', 'w') as convert_file:
        convert_file.write(json.dumps(allFilmData, indent=4, separators=(',', ': ')))


if __name__ == "__main__":
    main()

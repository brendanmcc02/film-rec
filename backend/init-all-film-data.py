# given title.basics.tsv & title.ratings.tsv, filter and vectorize to produce all-film-data-vectorized.json

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
    print("\nFiltering out films:\n1. that are not movies\n2. with no genres\n3. <"
          + str(RUNTIME_THRESHOLD) + " min runtime")

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

    print("Final Dataset size: " + str(len(allFilmData)) + " films.")

    # vectorize all-film-data.json

    global MIN_IMDB_RATING
    global MIN_YEAR
    global MIN_NUMBER_OF_VOTES
    global MIN_RUNTIME
    global DIFF_IMDB_RATING
    global DIFF_YEAR
    global DIFF_NUMBER_OF_VOTES
    global DIFF_RUNTIME
    global year_norms

    allFilmDataKeys = list(allFilmData.keys())

    vectorized_all_film_data = {}  # init the dictionary

    # initialise the min & max values of various attributes
    MIN_IMDB_RATING = allFilmData[allFilmDataKeys[0]]['imdbRating']
    MAX_IMDB_RATING = allFilmData[allFilmDataKeys[0]]['imdbRating']
    MIN_YEAR = allFilmData[allFilmDataKeys[0]]['year']
    MAX_YEAR = allFilmData[allFilmDataKeys[0]]['year']
    MIN_NUMBER_OF_VOTES = allFilmData[allFilmDataKeys[0]]['numberOfVotes']
    MAX_NUMBER_OF_VOTES = allFilmData[allFilmDataKeys[0]]['numberOfVotes']
    MIN_RUNTIME = allFilmData[allFilmDataKeys[0]]['runtime']
    MAX_RUNTIME = allFilmData[allFilmDataKeys[0]]['runtime']

    # get a list of unique genres
    allGenres = []
    for key in allFilmDataKeys:
        # if a genre is not in allGenres yet, append it
        for genre in allFilmData[key]['genres']:
            if genre not in allGenres:
                allGenres.append(genre)

        # modify min & max of the various attributes
        MIN_IMDB_RATING = min(MIN_IMDB_RATING, allFilmData[key]['imdbRating'])
        MAX_IMDB_RATING = max(MAX_IMDB_RATING, allFilmData[key]['imdbRating'])
        MIN_YEAR = min(MIN_YEAR, allFilmData[key]['year'])
        MAX_YEAR = max(MAX_YEAR, allFilmData[key]['year'])
        MIN_NUMBER_OF_VOTES = min(MIN_NUMBER_OF_VOTES, allFilmData[key]['numberOfVotes'])
        MAX_NUMBER_OF_VOTES = max(MAX_NUMBER_OF_VOTES, allFilmData[key]['numberOfVotes'])
        MIN_RUNTIME = min(MIN_RUNTIME, allFilmData[key]['runtime'])
        MAX_RUNTIME = max(MAX_RUNTIME, allFilmData[key]['runtime'])

    allGenres = sorted(allGenres)  # sort alphabetically

    # perform some pre-computation to avoid repetitive computation
    DIFF_IMDB_RATING = MAX_IMDB_RATING - MIN_IMDB_RATING
    DIFF_YEAR = MAX_YEAR - MIN_YEAR
    DIFF_NUMBER_OF_VOTES = MAX_NUMBER_OF_VOTES - MIN_NUMBER_OF_VOTES
    DIFF_RUNTIME = MAX_RUNTIME - MIN_RUNTIME

    # pre-compute normalised years for each year
    for y in range(MIN_YEAR, MAX_YEAR + 1):
        year_norms[y] = (y - MIN_YEAR) / DIFF_YEAR

    # for each film in all-film-data:
    for key in allFilmDataKeys:
        # vectorize the film
        vector = vectorize(allFilmData[key], allGenres)
        # add to dictionary
        vectorized_all_film_data[key] = vector

    # write to all-film-data-vectorized.json
    with open('../data/all-film-data-vectorized.json', 'w') as convert_file:
        convert_file.write(json.dumps(vectorized_all_film_data, indent=4, separators=(',', ': '))
                           .replace(",\n        ", ", ").replace("[\n        ", "[ ")
                           .replace("\n    ],", " ],"))


# given a film, return it's vectorized form (return type: list)
def vectorize(film, allGenres):
    vector = []
    # 1. normalise the year; apply weight
    # from experimenting, 0.3 was a very good weight as it did not overvalue the year, but still took it into account.
    year_norm = year_norms[film['year']] * 0.3
    vector.append(year_norm)
    # 2. normalise imdbRating
    imdbRating_norm = (film['imdbRating'] - MIN_IMDB_RATING) / DIFF_IMDB_RATING
    vector.append(imdbRating_norm)
    # 3. normalise numberOfVotes
    numberOfVotes_norm = (film['numberOfVotes'] - MIN_NUMBER_OF_VOTES) / DIFF_NUMBER_OF_VOTES
    vector.append(numberOfVotes_norm)
    # 4. normalise runtime; apply weight
    runtime_norm = ((film['runtime'] - MIN_RUNTIME) / DIFF_RUNTIME) * 0.3
    vector.append(runtime_norm)
    # 5. one-hot encoding on genres
    oneHotEncode(vector, film['genres'], allGenres)

    return vector


# given a vector, append the one-hot encoding of genres to the vector
def oneHotEncode(vector, filmGenres, allGenres):
    for g in allGenres:
        if g in filmGenres:
            vector.append(1)
        else:
            vector.append(0)

    return vector


if __name__ == "__main__":
    main()

# {
#         "id": "tt0020629",
#         "year": 1930,
#         "imdbRating": 8.1,
#         "genres": [
#             "Drama",
#             "War"
#         ],
#         "numberOfVotes": 67334
#     }


# python files
import settings
import vectorized-my-film-data
# libraries
import numpy as np
import json
import datetime


def main():
    # read in all-film-data.json
    allFilmDataFile = open('../data/all-film-data.json')
    allFilmData = json.load(allFilmDataFile)

    MAX_YEAR = int(datetime.datetime.now().year)

    vectorized_all_film_data = {}

    # get max & min imdbRating, and list of genres
    MAX_IMDB_RATING = allFilmData[0]['imdbRating']
    MIN_IMDB_RATING = allFilmData[0]['imdbRating']
    genres = []
    for film in allFilmData:
        for genre in film['genres']:
            if genre not in genres:
                genres.append(genre)

        MAX_IMDB_RATING = max(MAX_IMDB_RATING, film['imdbRating'])
        MIN_IMDB_RATING = min(MIN_IMDB_RATING, film['imdbRating'])

    MAX_IMDB_RATING = max(MAX_IMDB_RATING, vectorized_my_film_data.getMaxImdbRating())
    MIN_IMDB_RATING = min(MIN_IMDB_RATING, vectorized_my_film_data.getMinImdbRating())
    genres = sorted(genres)  # sort alphabetically

    # perform some pre-computation to avoid repetitive computation
    year_diff = MAX_YEAR - settings.MIN_YEAR
    imdbRating_diff = MAX_IMDB_RATING - MIN_IMDB_RATING

    # for each film:
    for film in allFilmData:
        vectorList = []
        # 1. normalise the year
        year_norm = (film['year'] - settings.MIN_YEAR) / year_diff
        vectorList.append(year_norm)
        # 2. normalise imdbRating
        imdbRating_norm = (film['imdbRating'] - MIN_IMDB_RATING) / imdbRating_diff
        vectorList.append(imdbRating_norm)
        # 3. genres

        # add to dictionary
        vectorized_all_film_data[film['id']] = vectorList
        # np.array(vectorList)  # convert to vector

    with open('../data/vectorized-all-film-data.json', 'w') as convert_file:
        convert_file.write(json.dumps(vectorized_all_film_data, indent=4, separators=(',', ': ')))


if __name__ == "__main__":
    main()

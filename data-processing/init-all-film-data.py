# this is not intended to be run as a standalone file, rather it is run using `init-all-film-data.sh`

import json
import csv
import time
import requests

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
    # print("\nImporting title.basics.tsv...")
    # title_basics_raw = []
    # with open("../database/title.basics.tsv", 'r', encoding='utf-8', newline='') as title_basics_file:
    #     reader = csv.DictReader(title_basics_file, delimiter='\t')
    #     for row in reader:
    #         title_basics_raw.append(dict(row))
    #
    # print("Imported title.basics.tsv.")
    # print("\nFiltering out films:\n1. that are not movies\n2. with no genres\n3. <"
    #       + str(RUNTIME_THRESHOLD) + " min runtime")
    #
    # stage_1_allFilmData = []
    #
    # for film in title_basics_raw:
    #     try:
    #         if (film["titleType"] == 'movie' and film['genres'] != r"\N"
    #                 and int(film['runtimeMinutes']) >= RUNTIME_THRESHOLD):
    #             newFilm = {}
    #             newFilm['id'] = film['tconst']
    #             newFilm['title'] = film['primaryTitle']
    #             newFilm['year'] = int(film['startYear'])
    #             newFilm['runtime'] = int(film['runtimeMinutes'])
    #             newFilm['genres'] = film['genres'].split(',')
    #
    #             stage_1_allFilmData.append(newFilm)
    #     except ValueError:
    #         pass
    #
    # print("\nMerging with title.ratings.tsv and filtering out films with <" + str(NUM_OF_VOTES_THRESHOLD) + " votes...")
    #
    # stage_2_allFilmData = []
    #
    # # the key is the film id, and the value is a dictionary of the attributes (averageRating & numVotes) of the film
    # title_ratings = {}
    # with open("../database/title.ratings.tsv", 'r', encoding='utf-8', newline='') as title_ratings_file:
    #     reader = csv.DictReader(title_ratings_file, delimiter='\t')
    #     for row in reader:
    #         rowDict = dict(row)
    #         filmId = rowDict['tconst']
    #         title_ratings[filmId] = rowDict
    #
    # for film in stage_1_allFilmData:
    #     filmId = film['id']
    #     try:
    #         if filmId in title_ratings and int(title_ratings[filmId]['numVotes']) >= NUM_OF_VOTES_THRESHOLD:
    #             film['imdbRating'] = float(title_ratings[filmId]['averageRating'])
    #             film['numberOfVotes'] = int(title_ratings[filmId]['numVotes'])
    #             stage_2_allFilmData.append(film)
    #     except ValueError:
    #         pass
    #     except Exception as e:
    #         print("Error occurred with processing title.ratings.tsv " + str(e))
    #
    # print("\nChanging the order of json attributes...")
    #
    # allFilmData = {}
    #
    # for film in stage_2_allFilmData:
    #     allFilmData[film['id']] = {
    #         'title': film['title'],
    #         'letterboxdTitle': "",
    #         'year': film['year'],
    #         'letterboxdYear': 0,
    #         'imdbRating': film['imdbRating'],
    #         'numberOfVotes': film['numberOfVotes'],
    #         'runtime': film['runtime'],
    #         'genres': film['genres']
    #     }

    ###### todo temp
    allFilmDataFile = open('../database/all-film-data.json')
    allFilmData = json.load(allFilmDataFile)
    count = 0
    ########
    print("\nMaking API calls to get Letterboxd Title, Letterboxd Year, Languages, Countries & Poster...\n")

    baseImageUrl = "https://image.tmdb.org/t/p/w500"

    accessToken = ""
    try:
        accessToken = str(open('../access-token.txt').read())
    except FileNotFoundError:
        print("Access Token File Not Found")
    except Exception as e:
        print("Error occurred while trying to read Access Token File " + str(e))

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {accessToken}"
    }

    cachedTmbdFilmDataFile = open('../database/cached-tmdb-film-data.json')
    cachedTmbdFilmData = json.load(cachedTmbdFilmDataFile)

    allFilmDataKeys = list(allFilmData.keys())
    apiCount = 0

    for imdbFilmId in allFilmDataKeys:
        ######### todo temp
        count = count + 1

        if count % 100 == 0:
            print(str(count) + " " + str(imdbFilmId))

        elif count % 100 == 0:
            with open('../database/cached-tmdb-film-data.json', 'w') as convert_file:
                convert_file.write(json.dumps(cachedTmbdFilmData, indent=4, separators=(',', ': ')))

            with open('../database/all-film-data.json', 'w') as convert_file:
                convert_file.write(json.dumps(allFilmData, indent=4, separators=(',', ': ')))
        ##############
        if imdbFilmId in cachedTmbdFilmData:
            allFilmData[imdbFilmId]['letterboxdTitle'] = cachedTmbdFilmData[imdbFilmId]['letterboxdTitle']
            allFilmData[imdbFilmId]['letterboxdYear'] = cachedTmbdFilmData[imdbFilmId]['letterboxdYear']
            allFilmData[imdbFilmId]['languages'] = cachedTmbdFilmData[imdbFilmId]['languages']
            allFilmData[imdbFilmId]['countries'] = cachedTmbdFilmData[imdbFilmId]['countries']
            allFilmData[imdbFilmId]['poster'] = cachedTmbdFilmData[imdbFilmId]['poster']
        else:
            url = f"https://api.themoviedb.org/3/find/{imdbFilmId}?external_source=imdb_id"
            tmdbFilmId = ""
            response = requests.get(url, headers=headers)
            apiCount = checkRateLimit(apiCount)
            if response.status_code == 200:
                jsonResponse = response.json()
                if len(jsonResponse['movie_results']) > 0:
                    tmdbFilmId = str(jsonResponse['movie_results'][0]['id'])
            elif response.status_code == 429:
                print(f"Rate Limit Exceeded. API Count = {apiCount}. Film ID: {imdbFilmId}\n")
            elif response.status_code == 404:
                print(f"Error Status Code = {response.status_code}\n")
            else:
                print(f"Unexpected Error. Status Code = {response.status_code}\n")

            # if the imdb film is not found in tmdb
            if tmdbFilmId == "":
                del allFilmData[imdbFilmId]
                continue

            url = f"https://api.themoviedb.org/3/movie/{tmdbFilmId}?language=en-US"
            response = requests.get(url, headers=headers)
            apiCount = checkRateLimit(apiCount)
            if response.status_code == 200:
                jsonResponse = response.json()

                filmTitle = str(jsonResponse['original_title'])
                filmYear = int(jsonResponse['release_date'].split('-')[0])
                filmPoster = baseImageUrl + str(jsonResponse['poster_path'])

                filmLanguages = []
                for language in jsonResponse['spoken_languages']:
                    filmLanguages.append(language['iso_639_1'])

                filmCountries = []
                for country in jsonResponse['origin_country']:
                    filmCountries.append(country)

                cachedTmbdFilmData[imdbFilmId] = {"letterboxdTitle": filmTitle, "letterboxdYear": filmYear,
                                                  "languages": filmLanguages, "countries": filmCountries,
                                                  "poster": filmPoster}

                allFilmData[imdbFilmId]['letterboxdTitle'] = filmTitle
                allFilmData[imdbFilmId]['letterboxdYear'] = filmYear
                allFilmData[imdbFilmId]['languages'] = filmLanguages
                allFilmData[imdbFilmId]['countries'] = filmCountries
                allFilmData[imdbFilmId]['poster'] = filmPoster
            elif response.status_code == 429:
                print(f"Rate Limit Exceeded. API Count = {apiCount}. Film ID: {imdbFilmId}\n")
            else:
                print(f"Error. Status Code = {response.status_code}\n")

    print("\nFinal Dataset size: " + str(len(allFilmData)) + " films.\n")

    with open('../database/cached-tmdb-film-data.json', 'w') as convert_file:
        convert_file.write(json.dumps(cachedTmbdFilmData, indent=4, separators=(',', ': ')))

    with open('../database/all-film-data.json', 'w') as convert_file:
        convert_file.write(json.dumps(allFilmData, indent=4, separators=(',', ': ')))


# API is rate limited to 50 calls per second
def checkRateLimit(apiCount):
    apiCount = apiCount + 1
    apiCount = apiCount % 40
    if apiCount == 0:
        time.sleep(1.1)

    return apiCount


if __name__ == "__main__":
    main()

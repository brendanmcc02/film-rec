# import numpy as np
# import json
# from datetime import datetime
import os
import glob
import requests
import json


def main():
    # allFilmDataFile = open('../database/all-film-data.json')
    # allFilmData = json.load(allFilmDataFile)
    # allFilmDataKeys = list(allFilmData.keys())

    imdbFilmId = "tt0111495"
    baseImageUrl = "https://image.tmdb.org/t/p/w500"

    # "https://api.themoviedb.org/3/find/tt?external_source=imdb_id"
    # baseApiUrl = "https://api.themoviedb.org/3/movie/155?language=en-US"

    accessToken = ""
    try:
        accessToken = str(open('../access-token.txt').read())
    except FileNotFoundError:
        print("Access Token File Not Found")
    except Exception as e:
        print("Error occurred while trying to read Access Token File" + str(e))

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {accessToken}"
    }

    cachedTmbdFilmDataFile = open('../database/cached-tmdb-film-data.json')
    cachedTmbdFilmData = json.load(cachedTmbdFilmDataFile)

    apiCount = 0

    # if imdbFilmId not in cachedTmbdFilmData:
    url = f"https://api.themoviedb.org/3/find/{imdbFilmId}?external_source=imdb_id"
    tmdbFilmId = ""
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        jsonResponse = response.json()
        tmdbFilmId = str(jsonResponse['movie_results'][0]['id'])
    elif response.status_code == 429:
        print(f"Rate Limit Exceeded. API Count = {apiCount}. Film ID: {imdbFilmId}\n")
    else:
        print("Error. Status Code = " + str(response.status_code) + "\n")

    url = f"https://api.themoviedb.org/3/movie/{tmdbFilmId}?language=en-US"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        jsonResponse = response.json()

        print(str(jsonResponse))
        filmLanguage = str(jsonResponse['original_language'])

        filmCountries = []
        for country in jsonResponse['origin_country']:
            filmCountries.append(country)

        filmPoster = baseImageUrl + str(jsonResponse['poster_path'])

        cachedTmbdFilmData[imdbFilmId] = {"language": filmLanguage, "countries": filmCountries,
                                          "poster": filmPoster}

    elif response.status_code == 429:
        print("Rate Limit Exceeded. API Count = " + apiCount + ". Film ID: " + imdbFilmId + "\n")
    else:
        print("Error. Status Code = " + str(response.status_code) + "\n")

    # with open('../database/cached-tmdb-film-data.json', 'w') as convert_file:
    #     convert_file.write(json.dumps(cachedTmbdFilmData, indent=4, separators=(',', ': ')))

    # "https://api.themoviedb.org/3/movie/155?language=en-US"
    # origin_country: array
    # original_language: 'en'
    # poster_path: append to 'https://image.tmdb.org/t/p/w500'
    # no director in this response

    # credits
    # "https://api.themoviedb.org/3/movie/155/credits?language=en-US"
    # go through each json object and look for 'job': 'Director' and get 'name' attribute


if __name__ == "__main__":
    main()


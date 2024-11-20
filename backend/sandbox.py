# import numpy as np
# import json
# from datetime import datetime
import os
import glob
# from init_all_film_data import isIncorrectResponse
import numpy as np
import requests
import json
import time
from vectorize import calculateUnbiasedVectorMagnitude


def main():
    allFilmDataFile = open('../database/all-film-data.json')
    allFilmData = json.load(allFilmDataFile)
    allFilmDataKeys = list(allFilmData.keys())


    allLanguages = []
    allCountries = []

    imdbFilmId = "tt4330758"

    # "https://api.themoviedb.org/3/find/tt?external_source=imdb_id"
    # baseApiUrl = "https://api.themoviedb.org/3/movie/155?language=en-US"

    accessToken = ""
    try:
        accessToken = str(open('../backup-access-token.txt').read())
    except FileNotFoundError:
        print("Access Token File Not Found")
    except Exception as e:
        print("Error occurred while trying to read Access Token File" + str(e))

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {accessToken}"
    }

    # if imdbFilmId in cachedTmbdFilmData:
    #     allFilmData[imdbFilmId]['letterboxdTitle'] = cachedTmbdFilmData[imdbFilmId]['letterboxdTitle']
    #     allFilmData[imdbFilmId]['letterboxdYear'] = cachedTmbdFilmData[imdbFilmId]['letterboxdYear']
    #     allFilmData[imdbFilmId]['languages'] = cachedTmbdFilmData[imdbFilmId]['languages']
    #     allFilmData[imdbFilmId]['countries'] = cachedTmbdFilmData[imdbFilmId]['countries']
    #     allFilmData[imdbFilmId]['mainPoster'] = cachedTmbdFilmData[imdbFilmId]['mainPoster']
    #     allFilmData[imdbFilmId]['backdropPoster'] = cachedTmbdFilmData[imdbFilmId]['backdrop_path']
    #     allFilmData[imdbFilmId]['summary'] = cachedTmbdFilmData[imdbFilmId]['summary']
    #
    #     for language in allFilmData[imdbFilmId]['languages']:
    #         if language not in allLanguages:
    #             allLanguages.append(language)
    #
    #     for country in allFilmData[imdbFilmId]['countries']:
    #         if country not in allCountries:
    #             allCountries.append(country)
    # else:
    url = f"https://api.themoviedb.org/3/find/{imdbFilmId}?external_source=imdb_id"
    tmdbFilmId = ""
    response = requests.get(url, headers=headers)
    time.sleep(0.2)
    if response.status_code == 200:
        jsonResponse = response.json()
        if len(jsonResponse['movie_results']) > 0:
            tmdbFilmId = str(jsonResponse['movie_results'][0]['id'])
        else:
            print(f"IMDB film not found in TMDB: {imdbFilmId}\n")
            del allFilmData[imdbFilmId]
    elif response.status_code == 429:
        print(f"Rate Limit Exceeded. Waiting 60 seconds... Film ID: {imdbFilmId}\n")
        time.sleep(60)
    elif response.status_code == 404:
        print(f"Error Status Code = {response.status_code}\n")
    else:
        print(f"Unexpected Error. Status Code = {response.status_code}\n")

    url = f"https://api.themoviedb.org/3/movie/{tmdbFilmId}?language=en-US"
    response = requests.get(url, headers=headers)
    time.sleep(0.2)
    if response.status_code == 200:
        jsonResponse = response.json()
        # if isIncorrectResponse(jsonResponse):
        #     print(f"JSON Response is invalid. IMDB Film ID: {imdbFilmId}\n")
        #     exit(10000)

        print(str(jsonResponse))

        # filmLanguages = []
        # for language in jsonResponse['spoken_languages']:
        #     filmLanguages.append(language['english_name'])
        #     if language['english_name'] not in allLanguages:
        #         allLanguages.append(language['english_name'])
        #
        # filmCountries = []
        # for country in jsonResponse['origin_country']:
        #     filmCountries.append(country)
        #     if country not in allCountries:
        #         allCountries.append(country)
        #
        # cachedTmbdFilmData[imdbFilmId] = {"letterboxdTitle": filmTitle, "letterboxdYear": filmYear,
        #                                   "languages": filmLanguages, "countries": filmCountries,
        #                                   "mainPoster": mainPoster, "backdropPoster": backdropPoster,
        #                                   "summary": filmSummary}
        #
        # allFilmData[imdbFilmId]['letterboxdTitle'] = filmTitle
        # allFilmData[imdbFilmId]['letterboxdYear'] = filmYear
        # allFilmData[imdbFilmId]['languages'] = filmLanguages
        # allFilmData[imdbFilmId]['countries'] = filmCountries
        # allFilmData[imdbFilmId]['mainPoster'] = mainPoster
        # allFilmData[imdbFilmId]['backdropPoster'] = backdropPoster
        # allFilmData[imdbFilmId]['summary'] = filmSummary

    # credits
    # "https://api.themoviedb.org/3/movie/155/credits?language=en-US"
    # go through each json object and look for 'job': 'Director' and get 'name' attribute



if __name__ == "__main__":
    main()


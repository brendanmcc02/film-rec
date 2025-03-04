# after the raw imdb datasets have been downloaded, import and filter the datasets, 
# then call the TMDb API service to augment additional data. this produces many .json
# files to be used by the backend service.
# this is intended to be run using `init-all-film-data.sh`, not as a standalone file.

import json
import csv
import time
import requests
from vectorizeUtilities import *

RUNTIME_THRESHOLD = 40
NUMBER_OF_VOTES_THRESHOLD = 25000
BASE_IMDB_URL = 'https://www.imdb.com/title/'


def main():
    runScript = True

    if runScript:
        print("\nImporting title.basics.tsv...")
        title_basics_raw = []
        
        with open("../database/title.basics.tsv", 'r', encoding='utf-8', newline='') as title_basics_file:
            reader = csv.DictReader(title_basics_file, delimiter='\t')
            for row in reader:
                title_basics_raw.append(dict(row))


        print("Imported title.basics.tsv.")
        print("\nFiltering out films:\n1. that are not movies\n2. with no genres\n3. <"
            + str(RUNTIME_THRESHOLD) + " min runtime")

        stage_1_allFilmData = []

        for film in title_basics_raw:
            try:
                if (film["titleType"] == 'movie' and film['genres'] != r"\N"
                        and int(film['runtimeMinutes']) >= RUNTIME_THRESHOLD):
                    newFilm = {'id': film['tconst'], 'title': film['primaryTitle'], 'year': int(film['startYear']),
                            'runtime': int(film['runtimeMinutes']), 'genres': film['genres'].split(',')}

                    stage_1_allFilmData.append(newFilm)
            except ValueError:
                pass

        print("\nMerging with title.ratings.tsv and filtering out films with <" + str(NUMBER_OF_VOTES_THRESHOLD) + " votes...")

        stage_2_allFilmData = []

        # the key is the film id, and the value is a dictionary of the attributes (averageRating & numVotes) of the film
        title_ratings = {}
        with open("../database/title.ratings.tsv", 'r', encoding='utf-8', newline='') as title_ratings_file:
            reader = csv.DictReader(title_ratings_file, delimiter='\t')
            for row in reader:
                rowDict = dict(row)
                filmId = rowDict['tconst']
                title_ratings[filmId] = rowDict

        for film in stage_1_allFilmData:
            filmId = film['id']
            try:
                if filmId in title_ratings and int(title_ratings[filmId]['numVotes']) >= NUMBER_OF_VOTES_THRESHOLD:
                    film['imdbRating'] = float(title_ratings[filmId]['averageRating'])
                    film['numberOfVotes'] = int(title_ratings[filmId]['numVotes'])
                    stage_2_allFilmData.append(film)
            except ValueError:
                pass

        print("\nChanging the order of json attributes...")

        allFilmData = {}
        allGenres = []

        for film in stage_2_allFilmData:
            allFilmData[film['id']] = {
                'title': film['title'],
                'letterboxdTitle': "",
                'year': film['year'],
                'letterboxdYear': 0,
                'imdbRating': film['imdbRating'],
                'numberOfVotes': film['numberOfVotes'],
                'runtime': film['runtime'],
                'runtimeHoursMinutes': convertRuntimeToHoursMinutes(film['runtime']),
                'genres': film['genres'],
                'imdbUrl': BASE_IMDB_URL + film['id']
            }

            for genre in film['genres']:
                if genre not in allGenres:
                    allGenres.append(genre)
    else:
        allFilmDataFile = open('../database/all-film-data.json')
        allFilmData = json.load(allFilmDataFile)
        allFilmDataFilmIds = list(allFilmData.keys())
        allGenres = []
        for filmId in allFilmDataFilmIds:
            for genre in allFilmData[filmId]['genres']:
                if genre not in allGenres:
                    allGenres.append(genre)

    allGenres = sorted(allGenres)

    print("\nMaking API calls to get Letterboxd Title, Letterboxd Year, Countries, Posters, Summary...\n")

    accessToken = str(open('../access-token.txt').read())

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {accessToken}"
    }

    cachedTmbdFilmDataFile = open('../database/cached-tmdb-film-data.json')
    cachedTmbdFilmData = json.load(cachedTmbdFilmDataFile)

    allCountries = []

    allFilmDataFilmIds = list(allFilmData.keys())

    minImdbRating = allFilmData[allFilmDataFilmIds[0]]['imdbRating']
    maxImdbRating = allFilmData[allFilmDataFilmIds[0]]['imdbRating']
    minYear = allFilmData[allFilmDataFilmIds[0]]['year']
    maxYear = allFilmData[allFilmDataFilmIds[0]]['year']
    minNumberOfVotes = allFilmData[allFilmDataFilmIds[0]]['numberOfVotes']
    maxNumberOfVotes = allFilmData[allFilmDataFilmIds[0]]['numberOfVotes']
    minRuntime = allFilmData[allFilmDataFilmIds[0]]['runtime']
    maxRuntime = allFilmData[allFilmDataFilmIds[0]]['runtime']

    cachedLetterboxdTitlesFile = open('../database/cached-letterboxd-titles.json')
    cachedLetterboxdTitles = json.load(cachedLetterboxdTitlesFile)
    cachedCountriesFile = open('../database/cached-countries.json')
    cachedCountries = json.load(cachedCountriesFile)
    
    count = 0
    invalidAllFilmDataFilmIds = []

    for imdbFilmId in allFilmDataFilmIds:
        count = count + 1
        print(str(count) + " " + str(imdbFilmId))
        if imdbFilmId in cachedTmbdFilmData:
            allFilmData[imdbFilmId]['letterboxdTitle'] = cachedTmbdFilmData[imdbFilmId]['letterboxdTitle']
            allFilmData[imdbFilmId]['letterboxdYear'] = cachedTmbdFilmData[imdbFilmId]['letterboxdYear']
            allFilmData[imdbFilmId]['countries'] = cachedTmbdFilmData[imdbFilmId]['countries']
            allFilmData[imdbFilmId]['poster'] = cachedTmbdFilmData[imdbFilmId]['poster']
            allFilmData[imdbFilmId]['summary'] = cachedTmbdFilmData[imdbFilmId]['summary']

            for country in allFilmData[imdbFilmId]['countries']:
                if country not in allCountries:
                    allCountries.append(country)

            imdbYear = allFilmData[imdbFilmId]['year']
            letterboxdYear = allFilmData[imdbFilmId]['letterboxdYear']
            uniqueYears = [imdbYear]
            if letterboxdYear != imdbYear:
                uniqueYears.append(letterboxdYear)

            letterboxdTitle = allFilmData[imdbFilmId]['letterboxdTitle']

            if letterboxdTitle not in cachedLetterboxdTitles:
                cachedLetterboxdTitles[letterboxdTitle] = [{"imdbFilmId": imdbFilmId, "years": uniqueYears}]
        else:
            url = f"https://api.themoviedb.org/3/find/{imdbFilmId}?external_source=imdb_id"
            tmdbFilmId = ""
            response = requests.get(url, headers=headers)
            time.sleep(0.2)
            if response.status_code == 200:
                jsonResponse = response.json()
                if ('movie_results' in jsonResponse and len(jsonResponse['movie_results']) > 0
                        and 'id' in jsonResponse['movie_results'][0]):
                    tmdbFilmId = str(jsonResponse['movie_results'][0]['id'])
                else:
                    print(f"IMDB film not found in TMDB: {imdbFilmId}\n")
                    del allFilmData[imdbFilmId]
                    invalidAllFilmDataFilmIds.append(imdbFilmId)
                    continue
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

                if isInvalidResponse(jsonResponse):
                    print(f"Incorrect Response. IMDB Film ID: {imdbFilmId}\n")
                    del allFilmData[imdbFilmId]
                    invalidAllFilmDataFilmIds.append(imdbFilmId)
                    continue

                basePosterUrl = "https://image.tmdb.org/t/p/w500"

                letterboxdTitle = str(jsonResponse['title'])
                letterboxdYear = int(jsonResponse['release_date'].split('-')[0])
                poster = basePosterUrl + str(jsonResponse['poster_path'])
                filmSummary = str(jsonResponse['overview'])

                filmCountries = []
                for countryShorthand in jsonResponse['origin_country']:
                    if countryShorthand in cachedCountries:
                        countryFullName = cachedCountries[countryShorthand]
                        filmCountries.append(countryFullName)
                        if countryFullName not in allCountries:
                            allCountries.append(countryFullName)
                    else:
                        print(f"Unrecognised Country: {countryShorthand}")

                cachedTmbdFilmData[imdbFilmId] = {"letterboxdTitle": letterboxdTitle, "letterboxdYear": letterboxdYear,
                                                  "countries": filmCountries, "poster": poster, 
                                                  "summary": filmSummary}

                allFilmData[imdbFilmId]['letterboxdTitle'] = letterboxdTitle
                allFilmData[imdbFilmId]['letterboxdYear'] = letterboxdYear
                allFilmData[imdbFilmId]['countries'] = filmCountries
                allFilmData[imdbFilmId]['poster'] = poster
                allFilmData[imdbFilmId]['summary'] = filmSummary

                imdbYear = allFilmData[imdbFilmId]['year']
                uniqueYears = [imdbYear]
                if letterboxdYear != imdbYear:
                    uniqueYears.append(letterboxdYear)

                if letterboxdTitle in cachedLetterboxdTitles:
                    cachedLetterboxdTitles[letterboxdTitle].append({"imdbFilmId": imdbFilmId, "years": uniqueYears})
                else:
                    cachedLetterboxdTitles[letterboxdTitle] = [{"imdbFilmId": imdbFilmId, "years": uniqueYears}]
            elif response.status_code == 429:
                print(f"Rate Limit Exceeded. Waiting 60 seconds... Film ID: {imdbFilmId}\n")
                time.sleep(60)
            else:
                print(f"Error. Status Code = {response.status_code}\n")

        minImdbRating = min(minImdbRating, allFilmData[imdbFilmId]['imdbRating'])
        maxImdbRating = max(maxImdbRating, allFilmData[imdbFilmId]['imdbRating'])
        minYear = min(minYear, allFilmData[imdbFilmId]['year'])
        maxYear = max(maxYear, allFilmData[imdbFilmId]['year'])
        minNumberOfVotes = min(minNumberOfVotes, allFilmData[imdbFilmId]['numberOfVotes'])
        maxNumberOfVotes = max(maxNumberOfVotes, allFilmData[imdbFilmId]['numberOfVotes'])
        minRuntime = min(minRuntime, allFilmData[imdbFilmId]['runtime'])
        maxRuntime = max(maxRuntime, allFilmData[imdbFilmId]['runtime'])

    for imdbFilmId in invalidAllFilmDataFilmIds:
        allFilmDataFilmIds.remove(imdbFilmId)

    print(f"\nFinal Dataset size: {len(allFilmDataFilmIds)} films.\n")

    with open('../database/all-film-data.json', 'w') as convert_file:
        convert_file.write(json.dumps(allFilmData, indent=4, separators=(',', ': ')))

    with open('../database/cached-tmdb-film-data.json', 'w') as convert_file:
        convert_file.write(json.dumps(cachedTmbdFilmData, indent=4, separators=(',', ': ')))

    with open('../database/cached-letterboxd-titles.json', 'w') as convert_file:
        convert_file.write(json.dumps(cachedLetterboxdTitles, indent=4, separators=(',', ': ')))

    print(f"\nVectorizing all-film-data.json\n")

    diffImdbRating = maxImdbRating - minImdbRating
    diffNumberOfVotes = maxNumberOfVotes - minNumberOfVotes
    diffRuntime = maxRuntime - minRuntime
    diffYear = maxYear - minYear

    if diffYear == 0:
        print("diffYear = 0. Error with minYear & maxYear.")
        raise ZeroDivisionError

    cachedNormalizedYears = {}
    for year in range(minYear, maxYear + 1):
        cachedNormalizedYears[str(year)] = ((year - minYear) / diffYear) * YEAR_WEIGHT

    if diffImdbRating == 0.0:
        print("diffImdbRating = 0.0, Error with minImdbRating & maxImdbRating.")
        raise ZeroDivisionError

    cachedNormalizedImdbRatings = {}
    for imdbRating in np.arange(minImdbRating, maxImdbRating + 0.1, 0.1):
        imdbRating = round(imdbRating, 1)
        cachedNormalizedImdbRatings[str(imdbRating)] = ((imdbRating - minImdbRating) / diffImdbRating) * IMDB_RATING_WEIGHT

    if diffRuntime == 0:
        print("diffRuntime = 0. Error with minRuntime & maxRuntime.")
        raise ZeroDivisionError

    cachedNormalizedRuntimes = {}
    for runtime in range(minRuntime, maxRuntime + 1):
        cachedNormalizedRuntimes[str(runtime)] = ((runtime - minRuntime) / diffRuntime) * RUNTIME_WEIGHT

    allFilmDataVectorized = {}
    allFilmDataVectorizedMagnitudes = {}
    profileVectorLength = 0
    allCountries = sorted(allCountries)

    if diffNumberOfVotes == 0:
        print("diffNumberOfVotes = 0. Error with minNumberOfVotes & maxNumberOfVotes.")
        raise ZeroDivisionError

    for filmId in allFilmDataFilmIds:
        if filmId not in allFilmData:
            print(f"Film ID not found in allFilmData: {filmId}.")
        else:
            allFilmDataVectorized[filmId] = list(vectorizeFilm(allFilmData[filmId], allGenres, allCountries,
                                                               cachedNormalizedYears, cachedNormalizedImdbRatings, 
                                                               minNumberOfVotes, diffNumberOfVotes, 
                                                               cachedNormalizedRuntimes))
            if profileVectorLength == 0:
                profileVectorLength = len(allFilmDataVectorized[filmId])

            allFilmDataVectorizedMagnitudes[filmId] = np.linalg.norm(allFilmDataVectorized[filmId])

    cache = {'allGenres': allGenres, 'allCountries': allCountries, 'normalizedYears': cachedNormalizedYears, 
             'normalizedImdbRatings': cachedNormalizedImdbRatings, 'normalizedRuntimes': cachedNormalizedRuntimes, 
             'minNumberOfVotes': minNumberOfVotes, 'diffNumberOfVotes': diffNumberOfVotes, 
             'profileVectorLength': profileVectorLength}

    with open('../database/all-film-data-vectorized.json', 'w') as convert_file:
        convert_file.write(json.dumps(allFilmDataVectorized, indent=4, separators=(',', ': '))
                            .replace(",\n        ", ", ").replace("],", "],"))

    with open('../database/cache.json', 'w') as convert_file:
        convert_file.write(json.dumps(cache, indent=4, separators=(',', ': ')))

    with open('../database/all-film-data-vectorized-magnitudes.json', 'w') as convert_file:
        convert_file.write(json.dumps(allFilmDataVectorizedMagnitudes, indent=4, separators=(',', ': ')))


def isInvalidResponse(jsonResponse):
    try:
        if ('title' in jsonResponse and jsonResponse['title'] != '' and 'poster_path' in jsonResponse
                and jsonResponse['poster_path'] != '' and 'release_date' in jsonResponse and
                jsonResponse['release_date'] != '' and 'backdrop_path' in jsonResponse and
                jsonResponse['backdrop_path'] != '' and 'overview' in jsonResponse and jsonResponse['overview'] != ''
                and 'origin_country' in jsonResponse):
            return False
        else:
            return True
    except ValueError:
        print("Value Error when validating json response.\n")
        return True


def convertRuntimeToHoursMinutes(runtimeInMinutes):
    hours = int(runtimeInMinutes / 60)
    minutes = runtimeInMinutes % 60

    if hours > 0:
        hours = f"{hours}h"
    else:
        hours = ""

    if minutes > 0:
        minutes = f"{minutes}m"
    else:
        minutes = ""

    return f"{hours}{minutes}"


if __name__ == "__main__":
    main()

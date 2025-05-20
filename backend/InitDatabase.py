# this is intended to be run using `initDatabase.sh`, not as a standalone file.

import csv
from dotenv import load_dotenv
import os
import time
import requests
from DatabaseUtilities import *
from DocumentDatabase import *
from ServiceUtilities import *
from VectorizeUtilities import *

def main(database):
    shouldRunScript = True

    if shouldRunScript:
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
                    newFilm = {'imdbId': film['tconst'], 'title': film['primaryTitle'], 'year': int(film['startYear']),
                            'runtime': int(film['runtimeMinutes']), 'genres': film['genres'].split(',')}

                    stage_1_allFilmData.append(newFilm)
            except ValueError:
                pass

        print(f"\nMerging with title.ratings.tsv and filtering out films with <{str(NUMBER_OF_VOTES_THRESHOLD)} votes...")

        stage_2_allFilmData = []

        title_ratings = {}
        with open("../database/title.ratings.tsv", 'r', encoding='utf-8', newline='') as title_ratings_file:
            reader = csv.DictReader(title_ratings_file, delimiter='\t')
            for row in reader:
                rowDict = dict(row)
                imdbFilmId = rowDict['tconst']
                title_ratings[imdbFilmId] = rowDict

        for film in stage_1_allFilmData:
            imdbFilmId = film['imdbId']
            try:
                if imdbFilmId in title_ratings and int(title_ratings[imdbFilmId]['numVotes']) >= NUMBER_OF_VOTES_THRESHOLD:
                    film['imdbRating'] = float(title_ratings[imdbFilmId]['averageRating'])
                    film['numberOfVotes'] = int(title_ratings[imdbFilmId]['numVotes'])
                    stage_2_allFilmData.append(film)
            except ValueError:
                pass

        print("\nChanging the order of json attributes...")

        allFilmData = {}
        allGenres = []

        for film in stage_2_allFilmData:
            allFilmData[film['imdbId']] = {
                'title': film['title'],
                'letterboxdTitle': "",
                'year': film['year'],
                'letterboxdYear': 0,
                'imdbRating': film['imdbRating'],
                'numberOfVotes': film['numberOfVotes'],
                'runtime': film['runtime'],
                'runtimeHoursMinutes': convertRuntimeToHoursMinutes(film['runtime']),
                'genres': film['genres'],
                'imdbUrl': BASE_IMDB_URL + film['imdbId']
            }

            for genre in film['genres']:
                if genre not in allGenres:
                    allGenres.append(genre)
    else:
        allFilmData = database.read("AllFilmData")
        allFilmDataimdbFilmIds = list(allFilmData.keys())
        allGenres = []
        for imdbFilmId in allFilmDataimdbFilmIds:
            for genre in allFilmData[imdbFilmId]['genres']:
                if genre not in allGenres:
                    allGenres.append(genre)

    allGenres = sorted(allGenres)

    print("\nMaking API calls to get Letterboxd Title, Letterboxd Year, Countries, Posters, Summary...\n")

    accessToken = os.getenv("ACCESS_TOKEN")

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {accessToken}"
    }

    cachedTmdbFilmData = database.read("CachedTmdbFilmData")
    cachedLetterboxdTitles = database.read("CachedLetterboxdTitles")
    
    removeCachedTmdbFilmDataAndLetterboxdTitlesNotInAllFilmData(allFilmData, cachedTmdbFilmData, cachedLetterboxdTitles)

    allCountries = []

    allFilmDataimdbFilmIds = list(allFilmData.keys())
    minImdbRating = allFilmData[allFilmDataimdbFilmIds[0]]['imdbRating']
    maxImdbRating = allFilmData[allFilmDataimdbFilmIds[0]]['imdbRating']
    minYear = allFilmData[allFilmDataimdbFilmIds[0]]['year']
    maxYear = allFilmData[allFilmDataimdbFilmIds[0]]['year']
    minNumberOfVotes = allFilmData[allFilmDataimdbFilmIds[0]]['numberOfVotes']
    maxNumberOfVotes = allFilmData[allFilmDataimdbFilmIds[0]]['numberOfVotes']
    minRuntime = allFilmData[allFilmDataimdbFilmIds[0]]['runtime']
    maxRuntime = allFilmData[allFilmDataimdbFilmIds[0]]['runtime']

    cachedCountries = database.read("CachedCountries")
    
    count = 0
    invalidAllFilmDataimdbFilmIds = []

    for imdbFilmId in allFilmDataimdbFilmIds:
        count = count + 1
        print(str(count) + " " + str(imdbFilmId))
        if imdbFilmId in cachedTmdbFilmData:
            allFilmData[imdbFilmId]['letterboxdTitle'] = cachedTmdbFilmData[imdbFilmId]['letterboxdTitle']
            allFilmData[imdbFilmId]['letterboxdYear'] = cachedTmdbFilmData[imdbFilmId]['letterboxdYear']
            allFilmData[imdbFilmId]['countries'] = cachedTmdbFilmData[imdbFilmId]['countries']
            allFilmData[imdbFilmId]['poster'] = cachedTmdbFilmData[imdbFilmId]['poster']
            allFilmData[imdbFilmId]['summary'] = cachedTmdbFilmData[imdbFilmId]['summary']

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
            tmdbimdbFilmId = ""
            response = requests.get(url, headers=headers)
            time.sleep(0.2)
            if response.status_code == 200:
                jsonResponse = response.json()
                if ('movie_results' in jsonResponse and len(jsonResponse['movie_results']) > 0
                        and 'imdbId' in jsonResponse['movie_results'][0]):
                    tmdbimdbFilmId = str(jsonResponse['movie_results'][0]['imdbId'])
                else:
                    print(f"IMDB film not found in TMDB: {imdbFilmId}")
                    del allFilmData[imdbFilmId]
                    invalidAllFilmDataimdbFilmIds.append(imdbFilmId)
                    continue
            elif response.status_code == 429:
                print(f"Rate Limit Exceeded. Waiting 60 seconds... Film ID: {imdbFilmId}\n")
                time.sleep(60)
            elif response.status_code == 404:
                print(f"Error Status Code = {response.status_code}\n")
            else:
                print(f"Unexpected Error. Status Code = {response.status_code}\n")

            url = f"https://api.themoviedb.org/3/movie/{tmdbimdbFilmId}?language=en-US"
            response = requests.get(url, headers=headers)
            time.sleep(0.2)
            if response.status_code == 200:
                jsonResponse = response.json()

                if isInvalidResponse(jsonResponse):
                    print(f"Incorrect Response. IMDB Film ID: {imdbFilmId}\n")
                    del allFilmData[imdbFilmId]
                    invalidAllFilmDataimdbFilmIds.append(imdbFilmId)
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

                cachedTmdbFilmData[imdbFilmId] = {"letterboxdTitle": letterboxdTitle, "letterboxdYear": letterboxdYear,
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

    for imdbFilmId in invalidAllFilmDataimdbFilmIds:
        allFilmDataimdbFilmIds.remove(imdbFilmId)

    print(f"\nFinal Dataset size: {len(allFilmDataimdbFilmIds)} films.\n")

    database.write("AllFilmData", allFilmData)
    database.write("CachedTmdbFilmData", cachedTmdbFilmData)
    database.write("CachedLetterboxdTitles", cachedLetterboxdTitles)

    print(f"\nVectorizing allFilmData.json\n")

    diffImdbRating = maxImdbRating - minImdbRating
    diffNumberOfVotes = maxNumberOfVotes - minNumberOfVotes
    diffRuntime = maxRuntime - minRuntime
    diffYear = maxYear - minYear

    normalizedYears = {}
    for year in range(minYear, maxYear + 1):
        normalizedYears[str(year)] = ((year - minYear) / diffYear) * YEAR_WEIGHT

    normalizedImdbRatings = {}
    for imdbRating in np.arange(minImdbRating, maxImdbRating + 0.1, 0.1):
        imdbRating = round(imdbRating, 1)
        normalizedImdbRatings[str(imdbRating)] = (((imdbRating - minImdbRating) / diffImdbRating) 
                                                        * IMDB_RATING_WEIGHT)

    normalizedRuntimes = {}
    for runtime in range(minRuntime, maxRuntime + 1):
        normalizedRuntimes[str(runtime)] = (((runtime - minRuntime) / diffRuntime) 
                                                * RUNTIME_WEIGHT)

    allFilmDataVectorized = {}
    allFilmDataVectorizedMagnitudes = {}
    profileVectorLength = 0
    allCountries = sorted(allCountries)

    for imdbFilmId in allFilmDataimdbFilmIds:
        if imdbFilmId not in allFilmData:
            print(f"Film ID not found in allFilmData: {imdbFilmId}.")
        else:
            allFilmDataVectorized[imdbFilmId] = list(vectorizeFilm(allFilmData[imdbFilmId], allGenres, allCountries,
                                                            normalizedYears, normalizedImdbRatings, 
                                                            minNumberOfVotes, diffNumberOfVotes, 
                                                            normalizedRuntimes))
            if profileVectorLength == 0:
                profileVectorLength = len(allFilmDataVectorized[imdbFilmId])

            allFilmDataVectorizedMagnitudes[imdbFilmId] = round(np.linalg.norm(allFilmDataVectorized[imdbFilmId]), 
                                                            VECTORIZED_MAGNITUDE_NUMBER_OF_ROUNDED_DECIMAL_POINTS)

    database.write("AllFilmDataVectorized", allFilmDataVectorized, [[",\n        ", ", "]])
    database.write("AllGenres", allGenres)
    database.write("AllCountries", allCountries)
    database.write("NormalizedYears", normalizedYears)
    database.write("NormalizedImdbRatings", normalizedImdbRatings)
    database.write("NormalizedRuntimes", normalizedRuntimes)
    database.write("MinNumberOfVotes", minNumberOfVotes)
    database.write("DiffNumberOfVotes", diffNumberOfVotes)
    database.write("ProfileVectorLength", profileVectorLength)
    database.write("AllFilmDataVectorizedMagnitudes", allFilmDataVectorizedMagnitudes)

def isInvalidResponse(jsonResponse):
    try:
        if ('title' in jsonResponse and jsonResponse['title'] != '' and 'poster_path' in jsonResponse
                and jsonResponse['poster_path'] != '' and 'release_date' in jsonResponse and
                jsonResponse['release_date'] != '' and 'overview' in jsonResponse and 
                jsonResponse['overview'] != '' and 'origin_country' in jsonResponse):
            return False
        else:
            return True
    except ValueError:
        print("Value Error when validating json response.\n")
        return True

def removeCachedTmdbFilmDataAndLetterboxdTitlesNotInAllFilmData(allFilmData, cachedTmdbFilmData, cachedLetterboxdTitles):
    invalidFilms = []
    allFilmDataimdbFilmIds = list(allFilmData.keys())
    
    for cachedTmdbimdbFilmId in list(cachedTmdbFilmData):
            if cachedTmdbimdbFilmId not in allFilmDataimdbFilmIds:
                invalidFilms.append({"imdbFilmId": cachedTmdbimdbFilmId, 
                                    "letterboxdTitle": cachedTmdbFilmData[cachedTmdbimdbFilmId]['letterboxdTitle']})
                del cachedTmdbFilmData[cachedTmdbimdbFilmId]

    for invalidFilm in invalidFilms:
        i = 0
        while i < len(cachedLetterboxdTitles[invalidFilm['letterboxdTitle']]):
            if cachedLetterboxdTitles[invalidFilm['letterboxdTitle']][i]['imdbFilmId'] == invalidFilm['imdbFilmId']:
                del cachedLetterboxdTitles[invalidFilm['letterboxdTitle']][i]
                i = i - 1
            
            i = i + 1
            
        if len(cachedLetterboxdTitles[invalidFilm['letterboxdTitle']]) == 0:
            del cachedLetterboxdTitles[invalidFilm['letterboxdTitle']]


load_dotenv()
database = DocumentDatabase("../")
main(database)

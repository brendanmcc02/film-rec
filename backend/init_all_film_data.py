# this is not intended to be run as a standalone file, rather it is run using `init-all-film-data.sh`

import json
import csv
import time
import requests
from vectorize import *

# from experimenting, 0.3 was a very good weight as it did not overvalue the year, but still took it into account.
YEAR_WEIGHT = 0.3
RUNTIME_THRESHOLD = 40
NUM_OF_VOTES_THRESHOLD = 25000


def main():
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

    print("\nMerging with title.ratings.tsv and filtering out films with <" + str(NUM_OF_VOTES_THRESHOLD) + " votes...")

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
            if filmId in title_ratings and int(title_ratings[filmId]['numVotes']) >= NUM_OF_VOTES_THRESHOLD:
                film['imdbRating'] = float(title_ratings[filmId]['averageRating'])
                film['numberOfVotes'] = int(title_ratings[filmId]['numVotes'])
                stage_2_allFilmData.append(film)
        except ValueError:
            pass
        except Exception as e:
            print("Error occurred with processing title.ratings.tsv " + str(e))

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
            'genres': film['genres']
        }

        for genre in film['genres']:
            if genre not in allGenres:
                allGenres.append(genre)

    allGenres = sorted(allGenres)

    # ###### todo temp
    # allFilmDataFile = open('../database/all-film-data.json')
    # allFilmData = json.load(allFilmDataFile)
    # allFilmDataKeys = list(allFilmData.keys())
    # allGenres = []
    # for filmId in allFilmDataKeys:
    #     for genre in allFilmData[filmId]['genres']:
    #         if genre not in allGenres:
    #             allGenres.append(genre)
    #
    # allGenres = sorted(allGenres)
    # ########
    print("\nMaking API calls to get Letterboxd Title, Letterboxd Year, Languages, Countries, Posters, Summary...\n")

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

    allLanguages = []
    allCountries = []

    allFilmDataKeys = list(allFilmData.keys())

    # this is needed for normalising vector values.
    minImdbRating = allFilmData[allFilmDataKeys[0]]['imdbRating']
    maxImdbRating = allFilmData[allFilmDataKeys[0]]['imdbRating']
    minYear = allFilmData[allFilmDataKeys[0]]['year']
    maxYear = allFilmData[allFilmDataKeys[0]]['year']
    minNumberOfVotes = allFilmData[allFilmDataKeys[0]]['numberOfVotes']
    maxNumberOfVotes = allFilmData[allFilmDataKeys[0]]['numberOfVotes']
    minRuntime = allFilmData[allFilmDataKeys[0]]['runtime']
    maxRuntime = allFilmData[allFilmDataKeys[0]]['runtime']

    cachedLetterboxdTitles = {}
    count = 0

    for imdbFilmId in allFilmDataKeys:
        count = count + 1
        print(str(count) + " " + str(imdbFilmId))
        if count % 100 == 0:
            with open('../database/cached-tmdb-film-data.json', 'w') as convert_file:
                convert_file.write(json.dumps(cachedTmbdFilmData, indent=4, separators=(',', ': ')))

            with open('../database/all-film-data.json', 'w') as convert_file:
                convert_file.write(json.dumps(allFilmData, indent=4, separators=(',', ': ')))

        if imdbFilmId in cachedTmbdFilmData:
            allFilmData[imdbFilmId]['letterboxdTitle'] = cachedTmbdFilmData[imdbFilmId]['letterboxdTitle']
            allFilmData[imdbFilmId]['letterboxdYear'] = cachedTmbdFilmData[imdbFilmId]['letterboxdYear']
            allFilmData[imdbFilmId]['languages'] = cachedTmbdFilmData[imdbFilmId]['languages']
            allFilmData[imdbFilmId]['countries'] = cachedTmbdFilmData[imdbFilmId]['countries']
            allFilmData[imdbFilmId]['mainPoster'] = cachedTmbdFilmData[imdbFilmId]['mainPoster']
            allFilmData[imdbFilmId]['backdropPoster'] = cachedTmbdFilmData[imdbFilmId]['backdropPoster']
            allFilmData[imdbFilmId]['summary'] = cachedTmbdFilmData[imdbFilmId]['summary']

            for language in allFilmData[imdbFilmId]['languages']:
                if language not in allLanguages:
                    allLanguages.append(language)

            for country in allFilmData[imdbFilmId]['countries']:
                if country not in allCountries:
                    allCountries.append(country)
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

                if isIncorrectResponse(jsonResponse):
                    print(f"Incorrect Response. IMDB Film ID: {imdbFilmId}\n")
                    continue

                letterboxdTitle = str(jsonResponse['title'])
                letterboxdYear = int(jsonResponse['release_date'].split('-')[0])
                mainPoster = str(jsonResponse['poster_path'])
                backdropPoster = str(jsonResponse['backdrop_path'])
                filmSummary = str(jsonResponse['overview'])

                filmLanguages = []
                for language in jsonResponse['spoken_languages']:
                    filmLanguages.append(language['english_name'])
                    if language['english_name'] not in allLanguages:
                        allLanguages.append(language['english_name'])

                filmCountries = []
                for country in jsonResponse['origin_country']:
                    filmCountries.append(country)
                    if country not in allCountries:
                        allCountries.append(country)

                cachedTmbdFilmData[imdbFilmId] = {"letterboxdTitle": letterboxdTitle, "letterboxdYear": letterboxdYear,
                                                  "languages": filmLanguages, "countries": filmCountries,
                                                  "mainPoster": mainPoster, "backdropPoster": backdropPoster,
                                                  "summary": filmSummary}

                allFilmData[imdbFilmId]['letterboxdTitle'] = letterboxdTitle
                allFilmData[imdbFilmId]['letterboxdYear'] = letterboxdYear
                allFilmData[imdbFilmId]['languages'] = filmLanguages
                allFilmData[imdbFilmId]['countries'] = filmCountries
                allFilmData[imdbFilmId]['mainPoster'] = mainPoster
                allFilmData[imdbFilmId]['backdropPoster'] = backdropPoster
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

    print(f"\nFinal Dataset size: {len(allFilmData)} films.\n")

    with open('../database/all-film-data.json', 'w') as convert_file:
        convert_file.write(json.dumps(allFilmData, indent=4, separators=(',', ': ')))

    with open('../database/cached-tmdb-film-data.json', 'w') as convert_file:
        convert_file.write(json.dumps(cachedTmbdFilmData, indent=4, separators=(',', ': ')))

    with open('../database/cached-letterboxd-titles.json', 'w') as convert_file:
        convert_file.write(json.dumps(cachedLetterboxdTitles, indent=4, separators=(',', ': ')))

    print(f"\nVectorizing all-film-data.json\n")

    # perform some pre-computation to avoid repetitive computation
    diffImdbRating = maxImdbRating - minImdbRating
    diffYear = maxYear - minYear
    diffNumberOfVotes = maxNumberOfVotes - minNumberOfVotes
    diffRuntime = maxRuntime - minRuntime

    cachedNormalizedYears = {}
    for y in range(minYear, maxYear + 1):
        cachedNormalizedYears[y] = ((y - minYear) / diffYear) * YEAR_WEIGHT

    cachedNormalizedImdbRatings = {}
    for i in np.arange(minImdbRating, maxImdbRating + 0.1, 0.1):
        i = round(i, 1)
        cachedNormalizedImdbRatings[str(i)] = (i - minImdbRating) / diffImdbRating

    allFilmDataVectorized = {}
    allFilmDataVectorizedMagnitudes = {}
    profileVectorLength = 0
    allLanguages = sorted(allLanguages)
    allCountries = sorted(allCountries)

    for filmId in allFilmDataKeys:
        allFilmDataVectorized[filmId] = list(vectorizeFilm(allFilmData[filmId], allGenres, allLanguages, allCountries,
                                                           cachedNormalizedYears, cachedNormalizedImdbRatings,
                                                           minNumberOfVotes, diffNumberOfVotes, minRuntime,
                                                           diffRuntime))
        if profileVectorLength == 0:
            profileVectorLength = len(allFilmDataVectorized[filmId])

        allFilmDataVectorizedMagnitudes[filmId] = float(np.linalg.norm(allFilmDataVectorized[filmId]))

    with open('../database/all-film-data-vectorized.json', 'w') as convert_file:
        convert_file.write(json.dumps(allFilmDataVectorized, indent=4, separators=(',', ': '))
                           .replace(",\n        ", ", ").replace("],", "],"))

    cache = {'allGenres': allGenres, 'allLanguages': allLanguages, 'allCountries': allCountries,
             'normalizedYears': cachedNormalizedYears, 'normalizedImdbRatings': cachedNormalizedImdbRatings,
             'minNumberOfVotes': minNumberOfVotes, 'diffNumberOfVotes': diffNumberOfVotes, 'minRuntime': minRuntime,
             'diffRuntime': diffRuntime, 'profileVectorLength': profileVectorLength}

    with open('../database/cache.json', 'w') as convert_file:
        convert_file.write(json.dumps(cache, indent=4, separators=(',', ': ')))

    with open('../database/all-film-data-vectorized-magnitudes.json', 'w') as convert_file:
        convert_file.write(json.dumps(allFilmDataVectorizedMagnitudes, indent=4, separators=(',', ': ')))


def isIncorrectResponse(jsonResponse):
    try:
        if ('title' in jsonResponse and 'poster_path' in jsonResponse and 'release_date' in jsonResponse
                and 'backdrop_path' in jsonResponse and 'overview' in jsonResponse and
                'spoken_languages' in jsonResponse and 'origin_country' in jsonResponse):
            # this might not execute due to compiler/interpreter efficiency: it's not used.
            # so i'm actually not sure if this check works
            letterboxdYear = int(jsonResponse['release_date'].split('-')[0])
            for language in jsonResponse['spoken_languages']:
                if 'english_name' not in language:
                    return True
        else:
            return True
    except ValueError:
        print("Value Error when validating json response.\n")
        return True

    return False


if __name__ == "__main__":
    main()

# given title.basics.tsv & title.ratings.tsv, filter through the data and produce all-film-data.json

# imports
import pandas as pd
import json


def main():
    # import title-basics.tsv as dataframe
    basics_df = pd.read_csv('../data/imdb-data/title.basics.tsv', sep='\t', dtype=str)
    basics = basics_df.to_dict('records')  # convert to dict

    # write to file
    with open('../data/1-only-movies.json', 'w') as convert_file:
        convert_file.write(json.dumps(basics, indent=4, separators=(',', ': ')))

    # iterate through each film:
    i = 0
    length = len(basics)
    while i < length:
        try:
            # if the film is not a movie:
            film = basics[i]
            if film['titleType'] != 'movie':
                # delete the film
                del basics[i]
                i = i - 1
                length = length - 1
            # else: keep the film
            else:
                if i % 1000 == 0:
                    print(str(i) + "/" + str(length))
                # rename attributes
                film['year'] = int(film['startYear'])  # convert from str to int
                film['id'] = film['tconst']
                film['runtime'] = int(film['runtimeMinutes'])  # convert from str to int

                # delete unnecessary attributes:
                del film['tconst']
                del film['titleType']
                del film['primaryTitle']
                del film['originalTitle']
                del film['isAdult']
                del film['startYear']
                del film['endYear']
                del film['runtimeMinutes']

                # convert genres from string to array of strings
                # e.g. genres: "Action, Family" => genres: {"Action", "Family"}
                film['genres'] = film['genres'].split(',')
        except ValueError:
            # some entries in 'startYear' or 'runtimeMinutes' are empty ('\N') and thus not int types,
            # so this catches the exception and just deletes the film
            del basics[i]
            i = i - 1
            length = length - 1

        i = i + 1

# 1-only-movies.json => 2-post-1930.json
# filter out:
# 1. films released < 1930
# 2. films with no genres

    # import 1-only-movies.json as a dictionary
    onlyMoviesData = open('../data/1-only-movies.json')
    onlyMoviesDataDict = json.load(onlyMoviesData)

    # for each film:
    i = 0
    length = len(onlyMoviesDataDict)
    while i < length:
        if i % 1000 == 0:
            print(str(i) + "/" + str(length))
        # if:
        # 1. film was released before 1930
        # 2. film has no genres
        if onlyMoviesDataDict[i]['year'] < 1930 or onlyMoviesDataDict[i]['genres'][0] == r"\N":
            # delete the film
            del onlyMoviesDataDict[i]
            i = i - 1
            length = length - 1

        i = i + 1

    # write to file
    with open('../data/2-post-1930.json', 'w') as convert_file:
        convert_file.write(json.dumps(onlyMoviesDataDict, indent=4, separators=(',', ': ')))


# 2-post-1930.json => 3-over-60-min.json
# filter out films:
# < 60 min runtime

    # import 2-post-1930.json
    pre1930Data = open('../data/2-post-1930.json')
    pre1930DataDict = json.load(pre1930Data)

    # for each film:
    i = 0
    length = len(pre1930DataDict)
    while i < length:
        if i % 1000 == 0:
            print(str(i) + "/" + str(length))
        # if film is < 60 minutes in length
        if pre1930DataDict[i]['runtime'] < 60:
            # delete the film
            del pre1930DataDict[i]
            i = i - 1
            length = length - 1

        i = i + 1

    # write to file
    with open('../data/3-over-60-min.json', 'w') as convert_file:
        convert_file.write(json.dumps(pre1930DataDict, indent=4, separators=(',', ': ')))


# 3-over-60-min.json => 4-merge-with-ratings.json
# merge 3-over-60-min.json with title.ratings.tsv


    # import title-ratings.tsv as dataframe
    ratings_df = pd.read_csv('../data/imdb-data/title.ratings.tsv', sep='\t', dtype=str)
    ratings = ratings_df.to_dict('records')
    # import 3-over-60-min.json as dictionary
    over60Data = open('../data/3-over-60-min.json')
    over60DataDict = json.load(over60Data)

    # get the length of the datasets
    length_ratings = len(ratings)
    length_over60 = len(over60DataDict)

    # the films are sorted by id:
    # i.e. tt000010 will always come after tt000009.
    # so, when the corresponding film is found in title-ratings.tsv,
    # I modify a 'start' variable, so when the code needs to look for
    # the next corresponding film, it starts looking where it left off.
    # this is more efficient.

    # iterate through each film in 3-over-60-min.json:
    i = 0
    start = 0
    while i < length_over60:
        if i % 500 == 0:
            print(str(i) + "/" + str(length_over60))

        filmId = over60DataDict[i]['id']
        found = False
        # find the corresponding film in title-ratings.tsv
        for j in range(start, length_ratings):
            found = False
            try:
                if ratings[j]['tconst'] == filmId:
                    # add imdbRating & numberOfVotes
                    over60DataDict[i]['imdbRating'] = float(ratings[j]['averageRating'])
                    over60DataDict[i]['numberOfVotes'] = int(ratings[j]['numVotes'])
                    start = j + 1
                    found = True
                    break
            # some films may not have 'numVotes' or 'averageRating' attributes
            except ValueError:
                # delete the film
                del ratings[j]
                length_ratings = length_ratings - 1
                break

        # if the film is not found in title-ratings.tsv
        if not found:
            # delete the film
            del over60DataDict[i]
            i = i - 1
            length_over60 = length_over60 - 1

        i = i + 1

    # write to file
    with open('../data/4-merge-with-ratings.json', 'w') as convert_file:
        convert_file.write(json.dumps(over60DataDict, indent=4, separators=(',', ': ')))



# 4-merge-with-ratings.json => 5-over-10k-votes.json
# filter out films:
# < 10,000 votes

    # import 4-merge-with-ratings.json as dictionary
    mergedData = open('../data/4-merge-with-ratings.json')
    mergedDataDict = json.load(mergedData)

    # for each film:
    i = 0
    length = len(mergedDataDict)
    while i < length:
        if i & 1000 == 0:
            print(str(i) + "/" + str(length))
        # if film has < 10,000 votes
        numberOfVotes = mergedDataDict[i]['numberOfVotes']
        if numberOfVotes < 10000:
            # delete the film
            del mergedDataDict[i]
            i = i - 1
            length = length - 1

        i = i + 1

    # write to file
    with open('../data/5-over-10k-votes.json', 'w') as convert_file:
        convert_file.write(json.dumps(mergedDataDict, indent=4, separators=(',', ': ')))



# 5-filter-over-10k-votes.json => 6-modified-order.json
# change the order of the json attributes

    # import 5-over-10k-votes.json as a dictionary
    over10kData = open('../data/5-over-10k-votes.json')
    over10kDataDict = json.load(over10kData)

    # for each film:
    length = len(over10kDataDict)
    i = 0
    while i < length:
        # change the order of the json attributes
        over10kDataDict[i] = {
            'id': over10kDataDict[i]['id'],
            'year': over10kDataDict[i]['year'],
            'imdbRating': over10kDataDict[i]['imdbRating'],
            'genres': over10kDataDict[i]['genres'],
            'numberOfVotes': over10kDataDict[i]['numberOfVotes'],
            'runtime': over10kDataDict[i]['runtime']
        }

        i = i + 1

    # write to file
    with open('../data/6-modified-order.json', 'w') as convert_file:
        convert_file.write(json.dumps(over10kDataDict, indent=4, separators=(',', ': ')))



# 6-modified-order.json => all-film-data.json
# filter out:
# films that I have rated.
# so, all-film-data.json contains all imdb films that I have not yet rated


    # import 6-modified-order.json as a dictionary
    modOrderData = open('../data/6-modified-order.json')
    modOrderDataDict = json.load(modOrderData)
    # import my-film-data.json as a dictionary
    myFilmData = open('../data/my-film-data.json')
    myFilmDataDict = json.load(myFilmData)

    # for each film:
    length = len(modOrderDataDict)
    i = 0
    while i < length:
        filmId = modOrderDataDict[i]['id']
        # find the corresponding film in my-film-data
        for myFilm in myFilmDataDict:
            if filmId == myFilm['id']:
                # delete the film
                del modOrderDataDict[i]
                i = i - 1
                length = length - 1

        i = i + 1

    # write to file
    with open('../data/all-film-data.json', 'w') as convert_file:
        convert_file.write(json.dumps(modOrderDataDict, indent=4, separators=(',', ': ')))


if __name__ == "__main__":
    main()

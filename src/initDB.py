import pandas as pd
import json


def main():
    # import title-ratings.tsv & title-basics.tsv
    basics_df = pd.read_csv('../data/imdb-data/title.basics.tsv', sep='\t', dtype=str)
    basics = basics_df.to_dict('records')
    ratings_df = pd.read_csv('../data/imdb-data/title.ratings.tsv', sep='\t', dtype=str)
    ratings = ratings_df.to_dict('records')

    print(basics[500]['tconst'])
    print(ratings[500]['tconst'])


    # i = 0
    # while i < length:
    #     print(str(i) + "/" + str(length))
    #     # combine the two datasets together
    #     basics[i]['imdbRating'] = float(ratings[i]['averageRating'])
    #     basics[i]['numberOfVotes'] = int(ratings[i]['numVotes'])
    #
    #     try:
    #         # if:
    #         # 1. film was released before < 1940
    #         # 2. is not a movie
    #         # 3. has < 10000 votes
    #         # delete the film
    #         if (int(basics[i]['startYear']) < 1940
    #                 or basics[i]['titleType'] != 'movie' or basics[i]['numberOfVotes'] < 10000):
    #             del basics[i]
    #             del ratings[i]
    #             i = i - 1
    #             length = length - 1
    #         # else: keep the film
    #         else:
    #             # rename attributes:
    #             basics[i]['year'] = int(basics[i]['startYear'])
    #             basics[i]['id'] = basics[i]['tconst']
    #
    #             # delete unnecessary attributes:
    #             del basics[i]['titleType']
    #             del basics[i]['primaryTitle']
    #             del basics[i]['originalTitle']
    #             del basics[i]['isAdult']
    #             del basics[i]['endYear']
    #             del basics[i]['runtimeMinutes']
    #             del basics[i]['startYear']
    #             del basics[i]['tconst']
    #     except ValueError:
    #         # for some reason, some entries in 'startYear' are not int types, so this catches the exception and
    #         # just deletes the film
    #         del basics[i]
    #         del ratings[i]
    #         i = i - 1
    #         length = length - 1
    #
    #     i = i + 1
    #
    # # write to file
    # with open('../data/all-film-data.json', 'w') as convert_file:
    #     convert_file.write(json.dumps(basics, indent=4, separators=(',', ': ')))


if __name__ == "__main__":
    main()


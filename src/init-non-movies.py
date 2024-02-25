import pandas as pd
import json


def main():
    # import title-basics.tsv
    basics_df = pd.read_csv('../data/imdb-data/title.basics-sample.tsv', sep='\t', dtype=str)
    basics = basics_df.to_dict('records')

    i = 0
    length = len(basics)
    while i < length:
        try:
            # if the film:
            # 1. is not a movie
            # 2. has no genres
            film = basics[i]
            if film['titleType'] != 'movie' or film['genres'] == '\\\\N':
                # delete the film
                del basics[i]
                i = i - 1
                length = length - 1
            # else: keep the film
            else:
                print(str(i) + "/" + str(length))
                # rename attributes
                film['year'] = int(film['startYear'])  # convert from str to int
                film['id'] = film['tconst']

                # delete unnecessary attributes:
                del film['tconst']
                del film['titleType']
                del film['primaryTitle']
                del film['originalTitle']
                del film['isAdult']
                del film['startYear']
                del film['endYear']
                # when I ran this script on 24/02/24 I deleted the runtime attribute, which I regret in hindsight.
                # So I could run the script again. The runtime was ~8 hours.
                # del film['runtimeMinutes']

                # convert genres from string to array of strings
                # e.g. genres: "Action, Family" => genres: {"Action", "Family"}
                film['genres'] = film['genres'].split(',')
        except ValueError:
            # for some reason, some entries in 'startYear' are not int types, so this catches the exception and
            # just deletes the film
            del basics[i]
            i = i - 1
            length = length - 1

        i = i + 1

    # write to file
    with open('../data/only-movies-basics.json', 'w') as convert_file:
        convert_file.write(json.dumps(basics, indent=4, separators=(',', ': ')))


if __name__ == "__main__":
    main()


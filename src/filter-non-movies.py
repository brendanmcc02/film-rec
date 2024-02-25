import pandas as pd
import json


def main():
    # import title-basics.tsv
    basics_df = pd.read_csv('../data/imdb-data/title.basics.tsv', sep='\t', dtype=str)
    basics = basics_df.to_dict('records')

    i = 0
    length = len(basics)
    while i < length:
        try:
            # if film is not a movie
            if basics[i]['titleType'] != 'movie':
                # delete the film
                del basics[i]
                i = i - 1
                length = length - 1
            # else: keep the film
            else:
                print(str(i) + "/" + str(length))
                # rename attributes
                basics[i]['year'] = int(basics[i]['startYear'])  # convert from str to int
                basics[i]['id'] = basics[i]['tconst']

                # delete unnecessary attributes:
                del basics[i]['tconst']
                del basics[i]['titleType']
                del basics[i]['primaryTitle']
                del basics[i]['originalTitle']
                del basics[i]['isAdult']
                del basics[i]['startYear']
                del basics[i]['endYear']
                del basics[i]['runtimeMinutes']

                # convert genres from string to array of strings
                # e.g. genres: "Action, Family" => genres: {"Action", "Family"}
                basics[i]['genres'] = basics[i]['genres'].split(',')
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


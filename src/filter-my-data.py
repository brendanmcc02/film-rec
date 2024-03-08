# this script is not intended to be run alone, but it is run by run.sh
import json


def main():
    # import film-data.json (copied over from film-data-vis)
    filmData = open('../data/film-data.json')
    filmDataList = json.load(filmData)

    filmDataDict = {}  # create dict

    # for each film:
    for film in filmDataList:
        # map the film id to a dict of it's attributes
        filmDataDict[film['id']] = {
            "title": film['title'],
            "year": film['year'],
            "myRating": film['myRating'],
            "imdbRating": film['imdbRating'],
            "genres": film['genres']
        }

    # write to file
    with open('../data/my-film-data.json', 'w') as convert_file:
        convert_file.write(json.dumps(filmDataDict, indent='\t', separators=(',', ': ')))


if __name__ == "__main__":
    main()


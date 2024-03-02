# 6-modified-order.json => all-film-data.json
# filter out:
# films that I have rated.
# so, all-film-data.json contains all imdb films that I have not yet rated
import json


def main():
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

import json


# 1. import film-data.json (copied over from film-data-vis)
# 2. delete attributes that are not necessary for this project (film title, watchedInCinema, myTop10Position, franchise)
# 3. write the result to my-film-data.json
def main():
    filmData = open('../data/film-data.json')
    filmDictionary = json.load(filmData)
    print(type(filmDictionary))

    for film in filmDictionary:
        del film['title']
        del film['watchedInCinema']
        del film['myTop10Position']
        del film['franchise']

    with open('../data/my-film-data.json', 'w') as convert_file:
        convert_file.write(json.dumps(filmDictionary, indent=4, separators=(',', ': ')))


if __name__ == "__main__":
    main()


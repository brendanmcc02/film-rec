import json


def main():
    # import film-data.json (copied over from film-data-vis)
    filmData = open('../data/film-data.json')
    filmDictionary = json.load(filmData)

    # for each film:
    for film in filmDictionary:
        # delete unnecessary attributes
        del film['title']
        # del film['metascore']
        # del film['directors']
        # del film['actors']
        # del film['countries']
        # del film['languages']
        del film['watchedInCinema']
        del film['myTop10Position']
        del film['franchise']

    # write to file
    with open('../data/my-film-data.json', 'w') as convert_file:
        convert_file.write(json.dumps(filmDictionary, indent=4, separators=(',', ': ')))


if __name__ == "__main__":
    main()


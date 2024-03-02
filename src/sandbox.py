# given merged.json, get rid of films with under 10,000 votes
import json


def main():
    # import merged.json
    mergedData = open('../data/merged-over-10k.json')
    mergedDataDict = json.load(mergedData)

    print(len(mergedDataDict))


if __name__ == "__main__":
    main()

# given merged.json, get rid of films with under 10,000 votes
import json


def main():
    # import merged.json
    mergedData = open('../data/merged.json')
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
    with open('../data/merged-over-10k.json', 'w') as convert_file:
        convert_file.write(json.dumps(mergedDataDict, indent=4, separators=(',', ': ')))


if __name__ == "__main__":
    main()

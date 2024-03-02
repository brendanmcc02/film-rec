# 2-post-1930.json => 3-over-60-min.json
# filter out films:
# < 60 min runtime
import json


def main():
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


if __name__ == "__main__":
    main()


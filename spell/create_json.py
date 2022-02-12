from dataclasses import field
import json


main_list = []

filename = "20k.txt"

fp = open(filename, 'r')
lines = fp.readlines()
count = 1
for line in lines:
    word = line.strip()
    if not word:
        continue
    row = {
        "model": "app.WordList",
        "pk": count ,
        "fields": {
            "word": word,
            "length": word.__len__()
        }
    }
    main_list.append(row)
    count += 1

print(json.dumps(main_list, indent=2))


# import csv
# import json
# json_file = "en_hi.json"
# dir_data = dict()
# with open('en_hi_dir.csv', newline='') as csvfile:
#     spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
#     count = 0
#     for row in spamreader:
#         if len(row) == 3:
#             count += 1
#             #print(row[0])
#             dir_data[row[0]] = row[1:]
#             #print (row)

#     #print(count)

# f = json.dumps(dir_data, indent=4)
# print(f)

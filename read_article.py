import csv

with open("data_source/sea1_output.csv", "r", encoding="cp1252") as csv_file:
    reader = csv.reader(csv_file)
    next(reader)
    for row in reader:
        sentence = row[0]
        print(sentence)
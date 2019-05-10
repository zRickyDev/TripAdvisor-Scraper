import csv

res = ''

with open('prato.csv', mode='r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for line in csv_reader:
        if line[3] != '':
            res += line[3].replace('\n', '') + ', '
    print res
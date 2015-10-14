import csv

csvfile = open('result.csv', 'wb')
writer = csv.writer(csvfile, quoting=csv.QUOTE_NONE)


writer.writerow(['hello world'])
writer.writerow(['My name is David'])
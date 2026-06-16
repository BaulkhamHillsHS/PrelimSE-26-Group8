import csv



def sample_read():
    with open('data.csv', mode='r') as file:
        csv_reader = csv.DictReader(file)  # Create DictReader

        data_list = []  # List to store dictionaries
        for row in csv_reader:
            data_list.append(row)

    for data in data_list:
        print(data)

import csv

fields = ['Name', 'Branch', 'Year', 'CGPA']
rows = [
    ['Nikhil', 'COE', '2', '9.0'],
    ['Sanchit', 'COE', '2', '9.1'],
    ['Aditya', 'IT', '2', '9.3'],
    ['Sagar', 'SE', '1', '9.5'],
    ['Prateek', 'MCE', '3', '7.8'],
    ['Sahil', 'EP', '2', '9.1']
]

filename = "university_records.csv"
with open(filename, 'w') as csvfile:
    csvwriter = csv.writer(csvfile)        # Create writer object
    csvwriter.writerow(fields)             # Write header
    csvwriter.writerows(rows)              # Write multiple rows
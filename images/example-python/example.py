#!/usr/bin/env python

import csv
import json
import sqlalchemy

# connect to the database
engine = sqlalchemy.create_engine("mysql://codetest:swordfish@database/codetest")
connection = engine.connect()

metadata = sqlalchemy.schema.MetaData()

# make an ORM object to refer to the places table
places = sqlalchemy.schema.Table('places', metadata, autoload=True, autoload_with=engine)

# make an ORM object to refer to the places table
people = sqlalchemy.schema.Table('people', metadata, autoload=True, autoload_with=engine)

# read the CSV data file into the places table
with open('/data/places.csv') as csv_file:
    reader = csv.reader(csv_file)
    next(reader)  # Skip the header row
    for row in reader:
        connection.execute(places.insert().values(city=row[0], county=row[1], country=row[2]))

# read the CSV data file into the people table
with open('/data/people.csv') as csv_file:
    reader = csv.reader(csv_file)
    next(reader)  # Skip the header row
    for row in reader:
        connection.execute(people.insert().values(first_name=row[0], last_name=row[1], date_of_birth=row[2], city_of_birth=row[3]))

# # output the places table to a JSON file
# with open('/data/places_output.json', 'w') as json_file:
#     rows = connection.execute(sqlalchemy.sql.select([places])).fetchall()
#     rows = [{'id': row[0], 'city': row[1], 'county': row[2], 'country': row[3]} for row in rows]
#     json.dump(rows, json_file, separators=(',', ':'))

# Summary output with list of the countries, and a count of how many people were born in that country
with open('/data/summary_output.json', 'w') as json_file:
    rows = connection.execute("""SELECT p.country, COUNT(pe.id) as num_people
                                FROM places p
                                JOIN people pe ON p.city = pe.city_of_birth
                                GROUP BY p.country""").fetchall()
    rows = [{'country': row[0], 'num_people': row[1]} for row in rows]
    json.dump(rows, json_file, separators=(',', ':'))

# close the connection
connection.close()

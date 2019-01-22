import pandas as pd
import sys
from pprint import pprint
import csv

if len(sys.argv) < 2:
    print("Please provide an entry file argument!")
    exit()

entry_file = sys.argv[1]

entries = pd.read_csv(entry_file)
entries = entries.replace('\n', '')

event_entries = entries
event_entries.drop('sportname', axis=1, inplace=True)

entrant_details = event_entries[['city', 'state', 'country']]
entrant_details.drop_duplicates(inplace=True)

for index, row in entrant_details.iterrows():

    location_line = "%s, %s, %s <green-dot>" % (row['city'].strip(), str(row['state']).strip(), row['country'].strip())

    print(location_line)

entrant_details.to_csv("cities.csv", index=False)

entrant_details.drop(['city'], axis=1, inplace=True)
entrant_details.drop_duplicates(inplace=True)

entrant_details.to_csv("countries.csv", index=False)


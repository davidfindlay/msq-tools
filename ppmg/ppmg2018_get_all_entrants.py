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

entrant_details = event_entries[['firstname', 'lastname', 'email']]

for index, row in entrant_details.iterrows():

    email_line = "\"%s %s\" <%s>" % (row['firstname'].strip(), row['lastname'].strip(), row['email'].strip())

    print(email_line)

entrant_details.to_csv("all_ppmg2018.csv", index=False)

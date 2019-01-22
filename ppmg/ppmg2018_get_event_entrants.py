import pandas as pd
import sys
from pprint import pprint
import csv

if len(sys.argv) < 3:
    print("Please provide an entry file argument!")
    exit()

entry_file = sys.argv[1]

entries = pd.read_csv(entry_file)
entries = entries.replace('\n', '')

event = sys.argv[2]

event_entries = entries[entries['eventname'] == event]
event_entries.drop('sportname', axis=1, inplace=True)

entrant_details = event_entries[['firstname', 'lastname', 'email']]

for index, row in entrant_details.iterrows():

    email_line = "%s %s <%s>" % (row['firstname'].strip(), row['lastname'].strip(), row['email'].strip())

    print(email_line)

print("%s Entry Count: %s " % (event, len(event_entries.index)))

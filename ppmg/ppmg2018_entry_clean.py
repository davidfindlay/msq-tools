# Tool for cleaning entry data for PPMG 2018
# David Findlay <davidjwfindlay@gmail.com>
# Licensed under GNU GPLv3 or higher

import pandas as pd
import sys
from pprint import pprint
import csv

entrant_details_columns = ["sportname",
                           "eventname",
                           "eventid",
                           "dateofentry",
                           "id",
                           "firstname",
                           "lastname",
                           "dateofbirth",
                           "age",
                           "gender",
                           "email",
                           "phone",
                           "city",
                           "state",
                           "country",
                           "emergencycontact",
                           "emergencyphone",
                           "medical",
                           "entryaccepted",
                           "confirmationcode",
                           "eventteamid",
                           "teamname",
                           "eventrole",
                           "eventroletwo",
                           "eventagegroup",
                           "eventgrade",
                           "teammanager",
                           "AusMastersMember",
                           "ID",
                           "ClubCode",
                           "OverseasMastersMem",
                           "Country",
                           "ClubName",
                           "NonMember",
                           "Disability",
                           "MultiClass",
                           "Classification" ]

entry_time_columns = ["200m Butterfly",
                      "200m Freestyle",
                      "400m Butterfly",
                      "400m Backstroke",
                      "400m Breaststroke",
                      "400m Individual Medley",
                      "50m Freestyle",
                      "50m Butterfly",
                      "200m Breaststroke",
                      "200m Individual Medley",
                      "100m Backstroke",
                      "100m Freestyle",
                      "400m Freestyle",
                      "100m Breaststroke",
                      "100m Butterfly",
                      "50m Backstroke",
                      "50m Breaststroke",
                      "200m Backstroke",
                      "4 x 50m Female Medley Relay Stroke",
                      "4 x 50m Female Medley Relay",
                      "4 x 50m Male Medley Relay Stroke",
                      "4 x 50m Male Medley Relay",
                      "4 x 50m Female Freestyle Relay",
                      "4 x 50m Male Freestyle Relay",
                      "4 x 50m Mixed Freestyle Relay",
                      "4 x 50m Mixed Medley Relay Stroke",
                      "4 x 50m Mixed Medley Relay",
                      "1500m Freestyle"]

event_names = ["200m Butterfly",
                      "200m Freestyle",
                      "400m Butterfly",
                      "400m Backstroke",
                      "400m Breaststroke",
                      "400m Individual Medley",
                      "50m Freestyle",
                      "50m Butterfly",
                      "200m Breaststroke",
                      "200m Individual Medley",
                      "100m Backstroke",
                      "100m Freestyle",
                      "400m Freestyle",
                      "100m Breaststroke",
                      "100m Butterfly",
                      "50m Backstroke",
                      "50m Breaststroke",
                      "200m Backstroke",
                      "4 x 50m Female Medley Relay",
                      "4 x 50m Male Medley Relay",
                      "4 x 50m Female Freestyle Relay",
                      "4 x 50m Male Freestyle Relay",
                      "4 x 50m Mixed Freestyle Relay",
                      "4 x 50m Mixed Medley Relay",
                      "1500m Freestyle"]

if len(sys.argv) < 2:
    print("Please provide an entry file argument!")
    exit()

entry_file = sys.argv[1]

entries = pd.read_csv(entry_file)
entries = entries.replace('\n', '')
print("Total event entries: %s" % len(entries.index))

unique_entries = entries.groupby(['id']).size().reset_index()

print("Total entrants: %s" % len(unique_entries.index))

cleaned_entries = pd.DataFrame(columns=(entrant_details_columns + entry_time_columns))

# Step through the individual entrants, finding their entries
for index, row in unique_entries.iterrows():

    id = row['id']
    num_entries = row[0]

    entry_list = entries[entries['id'] == id].reset_index()

    # Normalise case of names
    firstname = entry_list.loc[0, 'firstname'].strip()
    firstname = ' '.join(firstname.split())

    if firstname.islower() or firstname.isupper():
        firstname = firstname.title()

    lastname = entry_list.loc[0, 'lastname'].strip()
    lastname = ' '.join(lastname.split())

    if lastname.islower() or lastname.isupper():
        lastname = lastname.title()

    print("%s %s: %s" % (firstname, lastname, num_entries))

    entrant_details = entry_list.loc[0, :'Classification']
    entrant_details['firstname'] = firstname
    entrant_details['lastname'] = lastname

    event_entry_list = entry_list['eventname']
    event_details = entry_list.loc[:, '200m Butterfly~NominatedTime':]

    event_entries_dict = {}

    event_count = 0

    for event_entry_index, event_entry_name in event_entry_list.iteritems():

        event_entry_name = event_entry_name.split('-')[0].strip()
        # print(event_entry_name)

        if event_entry_name not in event_names:

            print("Error unknown event %s" % event_entry_name)
            exit()

        entry_row = event_details.iloc[event_entry_index, :]

        event_entries_dict[event_entry_name] = "NT"
        event_count += 1

        for i in range(0, (len(entry_row))):

            column_key = entry_time_columns[i]

            # print("%s in %s" % (event_entry_name, entry_row.index[i]))
            if not pd.isnull(entry_row[i]):
                event_entries_dict[column_key] = entry_row[i]

    #pprint(event_entries_dict)

    if num_entries != event_count:
        print("Error not all entries collated!")

    event_entries = pd.Series(event_entries_dict)

    cleaned_entry = event_entries.append(entrant_details)
    cleaned_entries = cleaned_entries.append(cleaned_entry, ignore_index=True)

cleaned_entries = cleaned_entries.drop(['eventname',
                      'medical',
                      'eventid',
                      'entryaccepted',
                      'confirmationcode',
                      'eventteamid',
                      'teamname',
                      'eventrole',
                      'eventroletwo',
                      'eventgrade',
                      'teammanager',
                      'index'], axis=1)

cleaned_entries.to_csv('cleaned_data.csv', index=False, quoting=csv.QUOTE_ALL)
cleaned_entries.to_excel('cleaned_data.xls', index=False, sheet_name='PPMG2018 Entries', freeze_panes=(1, 3))



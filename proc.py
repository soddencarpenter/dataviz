import argparse
import csv
import datetime
import re
import sys
from unittest import skip

STATION_NOT_FOUND = {
    'old_station_id': '-1',
    'new_station_id': '-1',
    'station_name': 'Not found',
    'latitude': '0',
    'longitude': '0',
    'chicago_community_area_number': '-1'
}




def load_station_data():
    with open('DivvyStation.csv') as csvfile:
        rdr = csv.DictReader(csvfile)
        station_records = list(rdr)

    return station_records




def find_rec_for_station_id(id, station_records):
    res = list(filter(lambda station : station['old_station_id'] == id, station_records))
    if not res:
        return STATION_NOT_FOUND
    else:
        return res[0]




def load_and_conv_data_2020_2021(filename, station_records, skip_header):
    dtfmt = "%Y-%m-%d %H:%M:%S"

    row_is_firstone = 1


    wtr = csv.writer(sys.stdout)

    with open(filename, newline='') as csvfile:
        rdr = csv.reader(csvfile, delimiter=',', )

        # each row
        # ride_id,rideable_type,started_at,ended_at,start_station_name,
        # start_station_id,end_station_name,end_station_id,start_lat,
        # start_lng,end_lat,end_lng,member_casual

        colid_rideid = 0
        colid_rideable_type = 1
        colid_started_at = 2
        colid_ended_at = 3
        colid_start_station_name = 4
        colid_start_station_id = 5  # believe uses new mapping
        colid_end_station_name = 6
        colid_end_station_id = 7
        colid_start_lat = 8
        colid_start_long = 9
        colid_end_lat = 10
        colid_end_long = 11
        colid_member_casual = 12

        # to match 2019 format, need to
        #  insert tripduration in seconds
        #  org_start_station_id
        #  org_end_station_id
        #  quarter
        #  month
        # year
        # dow


        for row in rdr:

            if row_is_firstone:
                tripduration = 'tripduration'
                quarter = 'quarter'
                month = 'month'
                year = 'year'
                dow = 'day_of_week'
                org_start_station_id = 'org_start_station_id'
                org_end_station_id = 'org_end_station_id'
            else:
                starting_at = datetime.datetime.strptime(row[colid_started_at], dtfmt)
                ending_at = datetime.datetime.strptime(row[colid_ended_at], dtfmt)
                elapsed = ending_at - starting_at
                elapsed_trip = elapsed.total_seconds()

                tripduration = elapsed_trip

                org_start_station_id = row[colid_start_station_id]
                org_end_station_id = row[colid_end_station_id]

                month = starting_at.month
                year = starting_at.year
                quarter = ((starting_at.month - 1)//3) + 1
                dow = starting_at.isoweekday() % 7
                

            outrow = []

            outrow.append(row[colid_rideid])
            outrow.append(row[colid_rideable_type])

            outrow.append(row[colid_member_casual])

            outrow.append(row[colid_started_at])
            outrow.append(row[colid_ended_at])

            outrow.append(tripduration)  # this is calculated

            # starting station name, id, org station
            #   org station is same as station
            outrow.append(row[colid_start_station_name])
            outrow.append(row[colid_start_station_id])
            outrow.append(org_start_station_id)

            # ending station name, id, org station
            outrow.append(row[colid_end_station_name])
            outrow.append(row[colid_end_station_id])
            outrow.append(org_end_station_id)

            outrow.append(row[colid_start_lat])
            outrow.append(row[colid_start_long])

            outrow.append(row[colid_end_lat])
            outrow.append(row[colid_end_long])

            outrow.append(quarter)
            outrow.append(month)
            outrow.append(year)
            outrow.append(dow)

            if not(skip_header and row_is_firstone):
              wtr.writerow(outrow)

            row_is_firstone = 0



def load_and_conv_data_2019(filename, station_records, skip_header):
    dtfmt = "%Y-%m-%d %H:%M:%S"

    row_is_firstone = 1


    wtr = csv.writer(sys.stdout)

    with open(filename, newline='') as csvfile:
        rdr = csv.reader(csvfile, delimiter=',', )

        # each row 
        #  trip_id,start_time_end_time,bikeid,tripduration,from_station_id,from_station_name,to_station_id,to_station_name,usertype
        #

        colid_tripid = 0
        colid_start_time = 1
        colid_end_time = 2
        colid_bike_id = 3  # we will not keep this column
        colid_tripduration = 4
        colid_from_station_id = 5  # this uses the old station #
        colid_from_station_name = 6
        colid_to_station_id = 7 # this uses the old station #
        colid_to_station_name = 8
        colid_usertype = 9

        # any other columns are ignored


        for row in rdr:
            # remap the contents of the user type, as the names
            #  changed in subsequent datasets
            if (row[colid_usertype] == "Subscriber"):
                row[colid_usertype] = "member"
            elif (row[colid_usertype] == "Customer"):
                row[colid_usertype] = "casual"

            # the duration is in some horrid formatted string, so need to stip the comma
            row[colid_tripduration] = row[colid_tripduration].replace(",", "")

            # insert long & lat for stations
            org_start_station_id = row[colid_from_station_id]
            start_station_rec = find_rec_for_station_id(org_start_station_id, station_records)
            start_station_id = start_station_rec['new_station_id']
            start_station_lat = start_station_rec['latitude']
            start_station_long = start_station_rec['longitude']

            org_end_station_id = row[colid_to_station_id]
            end_station_rec = find_rec_for_station_id(org_end_station_id, station_records)
            end_station_id = end_station_rec['new_station_id']
            end_station_lat = end_station_rec['latitude']
            end_station_long = end_station_rec['longitude']



            if row_is_firstone:
                start_station_id = 'start_station_id'
                org_start_station_id = 'org_start_station_id'
                end_station_id = 'end_station_id'
                org_end_station_id = 'org_end_station_id'
                start_station_lat = 'start_lat'
                start_station_long = 'start_lng'
                end_station_lat = 'end_lat'
                end_station_long = 'end_lng'
                rideable_type = 'rideable_type'
                quarter = 'quarter'
                month = 'month'
                year = 'year'
                dow = 'day_of_week'
            else:
                rideable_type = 'docked_bike'
                starting_at = datetime.datetime.strptime(row[colid_start_time], dtfmt)
                ending_at = datetime.datetime.strptime(row[colid_end_time], dtfmt)
                month = starting_at.month
                year = starting_at.year
                quarter = ((starting_at.month - 1)//3) + 1
                dow = starting_at.isoweekday() % 7



            # create a new list for output
            outrow = []

            outrow.append(row[colid_tripid])
            outrow.append(rideable_type)

            outrow.append(row[colid_usertype])

            outrow.append(row[colid_start_time])
            outrow.append(row[colid_end_time])

            outrow.append(row[colid_tripduration])

            outrow.append(row[colid_from_station_name])
            outrow.append(start_station_id)   # this is the mapped new one
            outrow.append(org_start_station_id)  # this is what is in the data itself

            outrow.append(row[colid_to_station_name])
            outrow.append(end_station_id)  # this is the mapped new one
            outrow.append(org_end_station_id)

            outrow.append(start_station_lat)
            outrow.append(start_station_long)

            outrow.append(end_station_lat)
            outrow.append(end_station_long)

            outrow.append(quarter)
            outrow.append(month)
            outrow.append(year)
            outrow.append(dow)

            if not(skip_header and row_is_firstone):
              wtr.writerow(outrow)

            row_is_firstone = 0




    
station_records = load_station_data()


#
# this really should be a method/function
parser = argparse.ArgumentParser(description="Process Divvy csv to standard format")
parser.add_argument('--file', help="The file to process", default="", required=True)
parser.add_argument('--noskip', help="Skip header output", nargs='?', default=True, required=False)

parsed_args = parser.parse_args()

inpfile = parsed_args.file
skip_header = parsed_args.noskip


if re.match(".*_2019_.*\.csv", inpfile):
    load_and_conv_data_2019(inpfile, station_records, skip_header)
else:
    load_and_conv_data_2020_2021(inpfile, station_records, skip_header)

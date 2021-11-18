import sqlite3
from sqlite3 import Error
from math import sin, cos, sqrt, atan2, radians
import operator

# Create a connection to our sqlite3 database
def create_connection(db_file):

    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

# Implements haversine distance calulation, returns the dis
def distance_between_postcodes(conn, postcode_1, postcode_2):
    cur = conn.cursor()
    postcode_1 = postcode_1.replace(" ", "").upper()
    postcode_2 = postcode_2.replace(" ", "").upper()

    # Get the latitudes and longitudes for the postcodes
    cur.execute("SELECT LATITUDE FROM smallukpostcodes WHERE REPLACE(POSTCODE, ' ', '') LIKE '%" + postcode_1 + "%'")
    lat1 = radians(cur.fetchone()[0])
    cur.execute("SELECT LATITUDE FROM smallukpostcodes WHERE REPLACE(POSTCODE, ' ', '') LIKE '%" + postcode_2 + "%'")
    lat2 = radians(cur.fetchone()[0])
    cur.execute("SELECT LONGITUDE FROM smallukpostcodes WHERE REPLACE(POSTCODE, ' ', '') LIKE '%" + postcode_1 + "%'")
    lon1 = radians(cur.fetchone()[0])
    cur.execute("SELECT LONGITUDE FROM smallukpostcodes WHERE REPLACE(POSTCODE, ' ', '') LIKE '%" + postcode_2 + "%'")
    lon2 = radians(cur.fetchone()[0])

    # approximate radius of earth in km
    R = 6373.0

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    # Return the distance in miles to 2 dp
    return round(0.621371 * distance, 2)

# Find services near the postcode, within a given radius and return them as a list
def services_near_postcode(conn, user_postcode, search_radius):
    services = []
    count = 0
    cur = conn.cursor()
    cur.execute("SELECT POSTCODE FROM organisations")
    postcodes = cur.fetchall()
    for postcode in postcodes:
        postcode = postcode[0]
        if postcode_in_postcodes(conn,user_postcode) and postcode_in_postcodes(conn,postcode):
            distance = distance_between_postcodes(conn, user_postcode, postcode)
            if distance <= search_radius:
               cur.execute("SELECT * FROM organisations where POSTCODE LIKE '%" + postcode +"%'")  
               services.append(list(cur.fetchone()))
               services[count].append(distance)
               count += 1

    for service in services:
        if service[1] == 1:
            service[1] = "Doctors"
        elif service[1] == 2:
            service[1] = "Dentists"
        elif service[1] == 3:
            service[1] = "Opticians"
        elif service[1] == 4:
            service[1] = "Nursery"
    
    return sorted(services, key=operator.itemgetter(6))

# Check that the postcode entered is within smallukpostcodes in the database
def postcode_in_postcodes(conn, postcode):
    postcode = postcode.replace(" ", "").upper()
    cur = conn.cursor()
    cur.execute("SELECT POSTCODE from smallukpostcodes")
    all_postcodes = list(cur.fetchall())
    for i in range(len(all_postcodes)):
        all_postcodes[i] = str(all_postcodes[i][0]).replace(" ", "")
    
    if postcode in all_postcodes:
        return True
    return False
    
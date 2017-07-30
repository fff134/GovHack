from flask import request, url_for, jsonify, render_template
from flask_api import FlaskAPI, status, exceptions
from urllib.request import urlopen
from urllib.error import URLError
import json

# For database
import MySQLdb

# cursor object for queries
cur = None

app = FlaskAPI(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/metric/<year>", methods=['GET'])
def suburb_metric_list(year):
    """
    List of metrics for each suburb
    """
    listOfValidYears = ['2011', '2013', '2016', '2021', '2026', '2031', '2036', '2041']
    if year in listOfValidYears:
        suburbs = []
        metrics = []
        lat = []
        lng = []
        cur.execute("SELECT * FROM total_per_suburb_" + year + "_metric")
        for row in cur.fetchall():
            suburbs.append(row[0])
            metrics.append(row[1])

            # get_location_lat_long(row[0])
        for suburb in suburbs:
            cur.execute("SELECT lat, lng FROM locations WHERE Suburb = '" + \
            suburb + "'")
            
            location = cur.fetchall()
            lat.append(location[0][0])
            lng.append(location[0][1])

        # Form JSON objects
        finalResp = []
        for num, suburb in enumerate(suburbs):
            dataPoint = {}
            dataPoint['suburb'] = suburb
            dataPoint['center'] = {'lng': lng[num], 'lat': lat[num]}
            dataPoint['metric'] = str(metrics[num])
            finalResp.append(dataPoint)

        return jsonify(results = finalResp)
    else:
        raise InvalidUsage('Dataset for that year was not found', status_code=501)


# def get_location_lat_long(location):

    # suburb = ''

    # if '-' in location:
    #     suburb = location.split('-')[1].strip()
    # else:
    #     suburb = location
    
    # suburb = suburb.replace(' ','%20')

    # request = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + \
    # suburb + ',qld'

    # while (True):
    #     try:
    #         response = urlopen(request)
    #         locDetails = json.loads(response.read().decode('utf-8'))
    #         if locDetails['status'] == 'OK':
    #             lat = locDetails['results'][0]['geometry']['location']['lat']
    #             lng = locDetails['results'][0]['geometry']['location']['lng']
    #             print(location + ',' + str(lat) + ',' + str(lng))
    #             return (lat, lng)
    #     except URLError as e:
    #         pass
    #         # print('Google Geocode API error' + str(e.code))
    

if __name__ == "__main__":
    db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="root",         # your username
                     passwd="root",  # your password
                     db="people_works")        # name of the data base
    cur = db.cursor()
    app.run(debug=True)
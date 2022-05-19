import datetime
import flask
from flask import jsonify
from flask import request
from db import create_connection, execute_query, execute_read_query

# connecting to mysql database
conn = create_connection('coogs.cypiz5agmq0c.us-east-1.rds.amazonaws.com', 'admin', 'phoebe123', 'coogs_db')

# setting up the application
app = flask.Flask(__name__)
# allow to show errors in browser
app.config["DEBUG"] = True


# CHECK IF API IS RUNNING
@app.route('/')
def startup():
    return "API Is running"



##############################################################################
#                             LOGIN                                          #
##############################################################################
@app.route('/api/authenticate', methods=['GET'])
def user_authentication():
    user_logininfo = request.get_json()
    sql = """
    SELECT * FROM Login_information
    """
    logins = execute_read_query(conn, sql)
    if 'username' in user_logininfo:
        input_username = user_logininfo['username']
    else:
        return 'No username provided'
    if 'password' in user_logininfo:
        input_pw = user_logininfo['password']
    else:
        return 'no password provided'
    Username = 0
    userPassword = 0
    for login in logins:
        if input_username == login['username']:
            Username = login['username']
            userPassword = login['user_password']
    if Username == 0 or userPassword == 0:
        return 'Account Could Not Be Found'
    else:
        if Username == input_username and userPassword == input_pw:
            return "Successfully Logged in"
    return 'COULD NOT VERIFY!'



##############################################################################
#       End points that will populate the tables                             #
##############################################################################
@app.route('/api/tripz', methods=['GET'])
def testing_trip():
    query = "SELECT * FROM tripz;"
    trip = execute_read_query(conn, query)
    return jsonify(trip)


@app.route('/api/destinationz', methods=['GET'])
def testing_des():
    query = "SELECT * FROM destination;"
    destination = execute_read_query(conn, query)
    return jsonify(destination)





##############################################################################
#                   ADDING   DATA                                            #
##############################################################################

@app.route('/api/destinationz/add', methods=['POST'])
# creating new variables for updated destinations
def add_destinations():
    request_data = request.get_json()
    country = request_data['country']
    city = request_data['city']
    sightseeing = request_data['sightseeing']

    # query function in order to insert updated trips into destination table
    query = """INSERT INTO destination (country, city, sightseeing) VALUES ('%s', '%s', '%s');""" % (
        country, city, sightseeing)
    execute_query(conn, query)

    return 'ADD REQUEST SUCCESSFUL'


@app.route('/api/tripz/add', methods=['POST'])
# creating new variables for updated trips
def add_tripz():
    request_data = request.get_json()
    transportation = request_data['transportation']
    startdate = request_data['startdate']
    enddate = request_data['enddate']
    tripname = request_data['tripname']

    # query function in order to insert updated destination details to trips table
    query = "INSERT INTO tripz (transportation, startdate, enddate, tripname) VALUES ('%s', '%s', '%s', '%s')" % (
         transportation, startdate, enddate, tripname)
    execute_query(conn, query)

    return 'ADD REQUEST SUCCESSFUL'

##############################################################################
#                   DELETE   DATA                                            #
##############################################################################



# endpoint to delete a trip by id
@app.route('/api/tripz/delete', methods=['DELETE'])
def delete_trip():
    request_data = request.get_json()
    idToDelete = request_data['trip_id']

    query = "DELETE FROM tripz WHERE trip_id = %s" % (idToDelete)
    execute_query(conn, query)

    return "DELETE REQUEST SUCCESSFUL"


# endpoint to delete a destination by id
@app.route('/api/destinationz/delete', methods=['DELETE'])
def delete_destination():
    request_data = request.get_json()
    idToDelete = request_data['id']

    query = "DELETE FROM destination WHERE id = %s" % (idToDelete)
    execute_query(conn, query)

    return "DELETE REQUEST SUCCESSFUL"













# when using the GET method can you please usew the x-www-form-urlencoded to pull by id
@app.route('/api/trip', methods=['GET'])
def trip_id():
    # this request pulls id from aws
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return 'ERROR: No ID Provided'
    results = []

    query = "SELECT * FROM tripz WHERE id = %s" % (id)
    trip = execute_read_query(conn, query)
    # return the trip table in json format
    return jsonify(trip)


# endpoint to get id
@app.route('/api/destination', methods=['GET'])
def destination_id():
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return 'ERROR: No ID Provided'
    results = []

    query = "SELECT * FROM destination WHERE id = %s" % (id)
    destination = execute_read_query(conn, query)
    # return the destination table in json format
    return jsonify(destination)







# update a trip using PUT method
@app.route('/api/trip', methods=['PUT'])
# creating new variables for updated trips
def add_trip():
    request_data = request.get_json()
    transportation = request_data['transportation']
    startdate = request_data['startdate']
    enddate = request_data['enddate']
    tripname = request_data['tripname']

    # query function in order to insert updated trips into the trip table
    query = "INSERT INTO tripz ( transportation, startdate, enddate, tripname) VALUES ( '%s', '%s', %s, '%s')" % (
         transportation, startdate, enddate, tripname)
    execute_query(conn, query)

    return 'UPDATE REQUEST SUCCESSFUL'


# Add a destination as PUT method
@app.route('/api/destination/update', methods=['PUT'])
# creating new variables for updated destinations
def add_destination():
    request_data = request.get_json()
    country = request_data['country']
    city = request_data['city']
    sightseeing = request_data['sightseeing']

    # query function in order to insert updated destinations into the destinations table
    query = "INSERT INTO destination (country, city, sightseeing) VALUES ('%s', '%s', '%s')" % (
        country, city, sightseeing)
    execute_query(conn, query)

    return 'ADD REQUEST SUCCESSFUL'















app.run()

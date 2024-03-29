import flask
from flask import jsonify
from flask import request
from db import create_connection, execute_query, execute_read_query

# connecting to mysql database
conn = create_connection('coogs.cypiz5agmq0c.us-east-1.rds.amazonaws.com', 'admin', 'phoebe123', 'coogs_db')
# setting up the application
app = flask.Flask(__name__)
# showing errors in browser
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
#                                 DESTINATIONS                               #
##############################################################################

# populate tables
@app.route('/api/destinationz', methods=['GET'])
def testing_des():
    query = "SELECT * FROM destination;"
    destination = execute_read_query(conn, query)
    return jsonify(destination)


# ADD some data
@app.route('/api/destinationz/add', methods=['POST'])
def add_destinations():
    request_data = request.get_json()
    country = request_data['country']
    city = request_data['city']
    sightseeing = request_data['sightseeing']

    query = """INSERT INTO destination (country, city, sightseeing) VALUES ('%s', '%s', '%s');""" % (
        country, city, sightseeing)
    execute_query(conn, query)
    return 'ADD REQUEST SUCCESSFUL'

# delete some data
@app.route('/api/destinationz/delete', methods=['DELETE'])
def delete_destination():
    request_data = request.get_json()
    idToDelete = request_data['id']

    query = "DELETE FROM destination WHERE id = %s" % (idToDelete)
    execute_query(conn, query)
    return "DELETE REQUEST SUCCESSFUL"


# set up update modal by ID
@app.route('/api/dez/update', methods=['POST'])
def dez_id():
    # this request pulls id from aws
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return 'ERROR: No ID Provided'
    results = []
    query = "SELECT * FROM destination WHERE id = %s" % (id)
    destination = execute_read_query(conn, query)
    return jsonify(destination)


# update a destination using PUT method
@app.route('/api/dez', methods=['PUT'])
def add_dez():
    request_data = request.get_json()
    id = request_data['id']
    country = request_data['country']
    city = request_data['city']
    sightseeing = request_data['sightseeing']

    query = """
    UPDATE destination 
    SET country='%s', city='%s', sightseeing='%s'
    WHERE id = %s 
    """ % (
         country, city, sightseeing, id)
    execute_query(conn, query)
    return 'UPDATE REQUEST SUCCESSFUL'

##############################################################################
#                           INDEX                                            #
##############################################################################

# populate tables
@app.route('/api/tripz', methods=['GET'])
def testing_trip():
    query = "SELECT * FROM tripz;"
    trip = execute_read_query(conn, query)
    return jsonify(trip)

# ADD some data
@app.route('/api/tripz/add', methods=['POST'])
def add_tripz():
    request_data = request.get_json()
    transportation = request_data['transportation']
    startdate = request_data['startdate']
    enddate = request_data['enddate']
    tripname = request_data['tripname']

    query = "INSERT INTO tripz (transportation, startdate, enddate, tripname) VALUES ('%s', '%s', '%s', '%s')" % (
         transportation, startdate, enddate, tripname)
    execute_query(conn, query)
    return 'ADD REQUEST SUCCESSFUL'

# delete some data
@app.route('/api/tripz/delete', methods=['DELETE'])
def delete_trip():
    request_data = request.get_json()
    idToDelete = request_data['trip_id']

    query = "DELETE FROM tripz WHERE trip_id = %s" % (idToDelete)
    execute_query(conn, query)
    return "DELETE REQUEST SUCCESSFUL"


# set up update modal by ID
@app.route('/api/tripz/update', methods=['POST'])
def trip_id():
    # this request pulls id from aws
    if 'trip_id' in request.args:
        trip_id = int(request.args['trip_id'])
    else:
        return 'ERROR: No ID Provided'
    results = []
    query = "SELECT * FROM tripz WHERE trip_id = %s" % (trip_id)
    trip = execute_read_query(conn, query)
    return jsonify(trip)


# update a trip using PUT method
@app.route('/api/tripz', methods=['PUT'])
def add_trip():
    request_data = request.get_json()
    trip_id = request_data['trip_id']
    transportation = request_data['transportation']
    startdate = request_data['startdate']
    enddate = request_data['enddate']
    tripname = request_data['tripname']

    query = """
    UPDATE tripz 
    SET transportation='%s', startdate='%s', enddate='%s', tripname='%s'
    WHERE trip_id = %s 
    """ % (
         transportation, startdate, enddate, tripname, trip_id)
    execute_query(conn, query)
    return 'UPDATE REQUEST SUCCESSFUL'

app.run()

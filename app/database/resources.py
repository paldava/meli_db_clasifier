import mysql.connector
import datetime
import re

import pymongo
from flask import request, json, Response, Blueprint
from ..mongo_db_connection import MongoAPI

app_meli = Blueprint("app_meli", __name__)


def get_db_info_types():
    data = {'collection': 'information_type'}
    obj1 = MongoAPI(data)
    return obj1.read()


info_type_list = get_db_info_types()


@app_meli.route('/api/v1/database/', methods=['POST'])
def save_database():
    data = request.json
    data['collection'] = 'database'
    if data is None or data == {}:
        return Response(response=json.dumps({"Error": "Please provide connection information"}),
                        status=400,
                        mimetype='application/json')
    obj1 = MongoAPI(data)
    response = obj1.write(data)
    return Response(response=json.dumps(response),
                    status=201,
                    mimetype='application/json')


@app_meli.route('/api/v1/database', methods=['GET'])
def get_databases():
    data = {'collection': 'database'}
    obj1 = MongoAPI(data)
    response = obj1.read()
    if response is None or response == {}:
        return Response(response=json.dumps({"Error": "There are no databases created"}),
                        status=400,
                        mimetype='application/json')
    else:
        return Response(response=json.dumps(response),
                        status=200,
                        mimetype='application/json')


@app_meli.route('/api/v1/database/<id>', methods=['POST'])
def scan_database(id):
    data = {'collection': 'database'}
    obj1 = MongoAPI(data)
    client_db_data = obj1.read_by_id(id)
    client_db = connect_client_db(client_db_data)
    cursor = client_db.cursor()
    cursor.execute('show schemas')
    schemas = cursor.fetchall()
    json_structure = '[ \n\t{\n"scan_date":"' + str(get_time()) + '", \n"database_id":"' + str(id) + '", \n"schemas":['
    for schema in schemas:
        schema_name = (str(schema).split("'"))[1].split("'")[0]
        json_structure = json_structure + '\t{\n"schema_name":"' + schema_name + '",'
        tables_sql = 'show tables from ' + schema_name
        cursor.execute(tables_sql)
        tables = cursor.fetchall()
        json_structure = json_structure + '\t\n"tables":['
        for table in tables:
            table_name = (str(table).split("'"))[1].split("'")[0]
            json_structure = json_structure + '{"table_name": "' + table_name + '",\n'
            columns_sql = 'show columns from ' + schema_name + '.' + table_name
            cursor.execute(columns_sql)
            columns = cursor.fetchall()
            json_structure = json_structure + '\t\n"columns":['
            for column in columns:
                column_name = (str(column).split("'"))[1].split("'")[0]
                json_structure = json_structure + '{"column_name": "' + column_name + '",'
                json_structure = json_structure + '"info_type": "' + str(clasify_column(column_name)) + '",' 
                json_structure = json_structure + '"data_type": "' + str(column_name) + '"},'
            json_structure = json_structure[:-1]
            json_structure = json_structure + '\n]},'
        # table
        json_structure = json_structure[:-1]
        json_structure = json_structure + '\n]},'
    # schema
    json_structure = json_structure[:-1]
    json_structure = json_structure + ']\n}\n]'

    data = {'collection': 'structure'}
    obj2 = MongoAPI(data)
    obj2.write_many(json.loads(json_structure))
    return Response(status=201,
                    mimetype='application/json')


@app_meli.route('/api/v1/database/<id>', methods=['GET'])
def get_structure(id):
    if id is None:
        return Response(response=json.dumps({"Error": "Please provide the id"}),
                        status=400,
                        mimetype='application/json')
    data = {'collection': 'structure'}
    obj1 = MongoAPI(data)
    response = obj1.read_sorting_and_filtering_field('database_id', id, 'scan_date', pymongo.DESCENDING)
    if response.count() == 0:
        return Response(response=json.dumps({"Error": "The database with the id provided does not have any scan yet"}),
                        status=400,
                        mimetype='application/json')
    else:
        return Response(response=str(response[0]),
                        status=200,
                        mimetype='application/json')


@app_meli.route('/api/v1/info_type', methods=['GET'])
def get_data_type():
    response = get_db_info_types()
    return Response(response=json.dumps(response),
                    status=200,
                    mimetype='application/json')


@app_meli.route('/api/v1/info_type', methods=['POST'])
def save_info_type():
    data = request.json
    data['collection'] = 'information_type'
    if data is None or data == {}:
        return Response(response=json.dumps({"Error": "Please provide data information"}),
                        status=400,
                        mimetype='application/json')
    obj1 = MongoAPI(data)
    response = obj1.write(data)
    del data['collection']
    info_type_list.append(data)
    return Response(response=json.dumps(response),
                    status=201,
                    mimetype='application/json')


def connect_client_db(data):
    return mysql.connector.connect(
        host=data["host"],
        port=data["port"],
        user=data["username"],
        password=data["password"]
    )


def clasify_column(column_name):
    for info_type in info_type_list:
        if re.search(info_type['regexp'], column_name, re.IGNORECASE):
            return info_type['name']
        else:
            return "N/A"
    return


def get_time():
    return datetime.datetime.now().strftime("%Y-%m-%d, %H:%M:%S")

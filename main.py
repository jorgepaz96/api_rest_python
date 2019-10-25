from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
import pymysql
import pymysql.cursors
import json


connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='notas',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()

@app.route("/notes.php")
def lista():
    with connection.cursor() as cursor:
        # Read a single record
            sql = "SELECT * FROM `nota`"
            cursor.execute(sql)
            result = cursor.fetchall()
            return jsonify(result)

@app.route("/save.php", methods=['POST'])
def save():
    x={}
    parser.add_argument('title', type=str)
    parser.add_argument('note', type=str)
    parser.add_argument('color', type=int)
    args = parser.parse_args()
    with connection.cursor() as cursor:        
        sql = "INSERT INTO `nota` (`title`, `note`, `color`) VALUES (%s, %s, %s)"
        result = cursor.execute(sql, (args['title'], args['note'], args['color']))
                
    if result == 1:
        x = {
            "success": True,
            "message": 'Successfully',             
            }
    else :
        x = {
            "success": False,
            "message": 'Failure',             
            }


    connection.commit()
    return(jsonify(x))

@app.route("/update.php", methods=['POST'])
def update():
    x={}
    parser.add_argument('id', type=int)
    parser.add_argument('title', type=str)
    parser.add_argument('note', type=str)
    parser.add_argument('color', type=int)
    args = parser.parse_args()
    with connection.cursor() as cursor:                    
        sql = "UPDATE `nota` SET title=%s, note=%s, color=%s WHERE `id`= %s "
        result = cursor.execute(sql, (args['title'], args['note'], args['color'],args['id']))
                
    if result == 1:
        x = {
            "success": True,
            "message": 'Successfully',             
            }
    else :
        x = {
            "success": False,
            "message": 'Failure',             
            }


    connection.commit()
    return(jsonify(x))

@app.route("/delete.php", methods=['POST'])
def delete():
    x={}
    parser.add_argument('id', type=int)    
    args = parser.parse_args()
    with connection.cursor() as cursor:                    
        sql = "DELETE FROM nota WHERE id='%s'"
        result = cursor.execute(sql, (args['id']))
                
    if result == 1:
        x = {
            "success": True,
            "message": 'Successfully',             
            }
    else :
        x = {
            "success": False,
            "message": 'Failure',             
            }


    connection.commit()
    return(jsonify(x))



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
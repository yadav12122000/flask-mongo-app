from flask import Flask , request , render_template , jsonify , redirect
from flask_pymongo import PyMongo 
from bson import json_util
import json

app = Flask("myapp") 
app.config["MONGO_URI"] = "mongodb://localhost:27017/myst"
mongodb_client = PyMongo(app)
db = mongodb_client.db


@app.route("/" , methods=['GET','POST'])
def myhome():
    if request.method=='POST':
        x = request.form['std_name']
        y = request.form['std_age']
        z = request.form["std_email"]
        print(x,y,z)
        db.student.insert_one({'name':x , 'age':int(y) , 'email': z})
    return render_template("home.html")

@app.route("/get_data" , methods=['GET'])
def login():
    students = db.student.find()
    students = list(students)
    return render_template('list.html' , students=students)

@app.route("/livesearch" , methods = ['GET','POST'])
def livesearch():
    searchbox = request.form.get("text")
    print(searchbox)
    myquery = { "name": { "$regex": "^{}".format(searchbox) } }
    students = db.student.find(myquery)
    def parse_json(data):
       return json.loads(json_util.dumps(data))
    st = parse_json(students)
    return jsonify(st)

@app.route("/replace_student/<string:name>-<string:email>" , methods=['GET','POST'])
def replace_student(name,email):
    if request.method=='POST':
        x = request.form['std_name']
        y = request.form['std_age']
        z = request.form["std_email"]
        db.student.replace_one({'name': name ,'email': email}, {'name': x, 'age': int(y) , 'email': z})
        return redirect("/get_data")
    return render_template("update.html")

@app.route("/delete_student/<string:name>-<string:email>" , methods=['GET','POST'])
def delete_student(name,email):
    db.student.delete_one({'name':name,  'email':email})
    return redirect("/get_data")
app.run(port=5555 , debug=True)

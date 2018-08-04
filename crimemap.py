import dbconfig
if dbconfig.test:
	from mockdbhelper import MockDBHelper as DBHelper
	route_prefix = ""
else:
	from dbhelper import DBHelper
	route_prefix = "/crimemap1"
from flask import Flask
import json
from flask import render_template
from flask import request

app = Flask(__name__)
DB = DBHelper()

@app.route("/")
def home():
	try:
		crimes = DB.get_all_crimes()
		crimes = json.dumps(crimes)
	except Exception as e:
		print e
		data = None
	return render_template("home.html", crimes = crimes, route_prefix = route_prefix)

@app.route("/add", methods=["POST"])
def add():
	try:
		data = request.form.get("userinput")
		DB.add_input(data)
	except Exception as e:
		print e
	return home()

@app.route("/clear")
def clear():
	try:
		DB.clear_all()
	except Exception as e:
		print e
	return home()

@app.route("/submitcrime", methods=['POST'])
def submitcrime():
	category = request.form.get("category")
	date = request.form.get("date")
	latitude = float(request.form.get("latitude"))
	longitude = float(request.form.get("longitude"))
	description = request.form.get("description")
	DB.add_crime(category, date, latitude, longitude, description)
	return home()


if __name__ == '__main__':
	app.run(port=5000, debug=True)
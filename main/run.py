from flask import Flask,request,jsonify
app = Flask(__name__)
app.config.from_object("config.app")

from db import db
mydb = db(app.config["DB_USER"],app.config["DB_PASS"],app.config["DB_HOST"],app.config["DB_NAME"],app.config["DB_TABLE"],app.config["DB_VALIDLIST"],app.config["DB_BANLIST"])

@app.route("/api/list", methods=["GET"])
def listResults():
	res = mydb.getAll()
	return jsonify(res)

@app.route("/api/create", methods=["POST"])
def createResult():
	data = request.get_json()
	res = {"Status":"Failed","Text":"Format Error: Must be a json and {} only"}
	if data:
		names = []
		values = []
		for k,v in data.iteritems():
			names.append(k)
			values.append(v)
		res = mydb.create(names,values)
		return jsonify(res)
	return jsonify(res)

@app.route("/api/modify/<int:rid>", methods=["PUT"])
def updateResult(rid):
	data = request.get_json()
	res = {"Status":"Failed","Text":"Format Error: Must be a json and {} only"}
	if data:
		names = []
		values = []
		for k,v in data.iteritems():
			names.append(k)
			values.append(v)
		res = mydb.update(rid,names,values)
		return jsonify(res)
	return jsonify(res)

@app.route("/api/remove/<int:rid>", methods=["DELETE"])
def removeResult(rid):
	res = mydb.delete(rid)
	return jsonify(res)

@app.route("/api/read/<int:rid>", methods=["GET"])
def getResult(rid):
	res = mydb.read(rid)
	return jsonify(res)

if __name__ == "__main__":
	app.run(host="0.0.0.0")

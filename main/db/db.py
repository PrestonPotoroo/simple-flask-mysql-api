import mysql.connector

class db:
	def __init__(self,user,password,host,db_name,table,validlist,banlist):
		self.conn = mysql.connector.connect(user=user, password=password, host=host, database=db_name)
		self.cursor = self.conn.cursor(dictionary=True)
		self.table = table
		self.fields = self.setTable()
		self.columns = self.setNames(validlist)
		self.banlist = banlist

	def getAll(self):
		data = []
		querystring = self.buildString()
		try:
			query = ("SELECT "+querystring+" FROM "+self.table)
			self.cursor.execute(query)
			for c in self.cursor:
				data.append(c)
		except Exception as e:
			print e
			return {"Status":"Failed"}
		return data

	def read(self,rid):
		data = []
		querystring = self.buildString()
		try:
			query = ("SELECT "+querystring+" FROM "+self.table+" WHERE _id=%s")
			self.cursor.execute(query, (rid,))
			for c in self.cursor:
				data.append(c)
		except Exception as e:
			print e
			return {"Status":"Failed"}
		return data

	def delete(self,rid):
		try:
			query = ("DELETE FROM "+self.table+" WHERE _id=%s")
			self.cursor.execute(query, (rid,))
			self.conn.commit()
		except Exception as e:
			print e
			return {"Status":"Failed"}
		return {"Status":"Success"}

	def create(self,names,values):
		print self.columns
		for j in range(len(names)):
			if names[j] not in self.columns:
				return {"Status":"Failed","text":"Incorrect column names"}
		querynames = ""
		queryvalues = ""
		data = tuple(values)
		for i in xrange(len(names)):
			querynames +=  names[i]
			queryvalues += "%s"
			if i < len(names)-1:
				querynames += ", "
				queryvalues += ", "
		#print data
		try:
			query = ("INSERT INTO "+self.table+" ("+querynames+") VALUES ("+queryvalues+")")
			self.cursor.execute(query, data)
			self.conn.commit()
		except Exception as e:
			print e
			return {"Status":"Failed"}
		return {"Status":"Success"}

	def update(self,rid,names,values):
		for j in range(len(names)):
			if names[j] not in self.columns:
				return {"Status":"Failed","text":"Incorrect column names"}
		querystring = ""
		values.append(rid)
		data = tuple(values)
		for i in xrange(len(names)):
			querystring +=  names[i]+"= %s"
			if i < len(names)-1:
				querystring += ", "
		try:
			query = ("UPDATE "+self.table+" SET "+querystring+" WHERE _id=%s")
			self.cursor.execute(query,data)
			self.conn.commit()
		except Exception as e:
			print e
			return {"Status":"Failed"}
		return {"Status":"Success"}

	def close(self):
		self.conn.close()

	def buildString(self):
		querystring = ""
		for i in xrange(len(self.fields)):
			if self.fields[i]["Field"] in self.banlist:
				continue
			if self.fields[i]["Type"] == "timestamp":
				querystring += "unix_timestamp("+self.fields[i]["Field"]+") as "+self.fields[i]["Field"]
			else:
				querystring += self.fields[i]["Field"]
			querystring += ", "
		querystring = querystring[:-2]
		return querystring

	def setTable(self):
		self.cursor.execute("SHOW columns from "+self.table)
		fields = self.cursor.fetchall()
		return fields

	def setNames(self,validlist):
		columns = []
		for f in self.fields:
			if f["Field"] in validlist:
				columns.append(f["Field"])
		return columns

if __name__ == "__main__":
	pass
	#validlist = ["timestamp","value1","value2","value3"]
	#banlist = ["creationDate","lastModificationDate"]
	#mydb = db("myapi","password","localhost","myapi","random",validlist,banlist)
	#print mydb.buildString()
	#print mydb.read(13)
	#names = ["timestamp","value1","value2","value3"]
	#values = ["1234","5","1.9","0"]
	#mydb.create(names,values)
	#mydb.getAll()
	#mydb.delete(15)
	#print mydb.getAll()
	#mydb.close()

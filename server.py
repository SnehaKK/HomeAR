import os, json
from flask import Flask, render_template, request, make_response, json, jsonify
from werkzeug import secure_filename
import csv
import sys
import pymongo, re
from bson.objectid import ObjectId
from os import walk
import logging

app = Flask(__name__)
MONGODB_URI = "mongodb://sneha:test123@ds063150.mongolab.com:63150/testmongolabs"
MONGODB_URI_HomeAR = "mongodb://sneha:test123@ds061370.mongolab.com:61370/homear"

app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

"""
==========================
Web Related APIS
==========================
"""
@app.route('/')
def index():
	return render_template('index.html')
    # return 'Hello World!'

app.config['UPLOAD_FOLDER'] = 'uploads/'
ALLOWED_EXTENSIONS = set(['csv']) #set(['csv','txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/uploadFile', methods=['GET', 'POST'])
def upload_file():
	data = "['Firefox',45.0],['IE',26.8]"
	# print "iam here"
	if request.method == 'GET':
		return render_template('fileUpload.html', fileList = generate_file_data(get_list_of_files()))
	if request.method == 'POST':
		print request
        file = request.files['csvUpload']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #Open and read the file saved.
            # fileToBeRead = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            # print fileToBeRead
            # read_csvfile(fileToBeRead)
            # This return is to redirect it to the page you want
            return render_template('test.html', data = read_file(filename), fileList = generate_file_data(get_list_of_files()))
            # return redirect(url_for('uploaded_file',filename=filename))
	return render_template('fileUpload.html')

def read_file(filename):
	# print app.config['UPLOAD_FOLDER']
	filereadpath = app.config['UPLOAD_FOLDER'] + filename
	csvfile = open( filereadpath, 'rb') # opens the csv file
	highChartData = []
	try:
	    reader = csv.reader(csvfile)  # creates the reader object
	    rowcount =0
	    for row in reader:   # iterates the rows of the file in orders
	        print row    # prints each row
	       	listVal = []
	        #words = row.split(",")
	        rowcount = rowcount +1
	        prodId = row[0]
	        prodName = row[1]
	        prodDesc = row[2]
	        prodCount = row[3]
	        # del highChartData['ProdName']
	        if(prodName != 'ProdName'):
	        	listVal.append(prodName)
	        	listVal.append(int(prodCount))
	        	# print listVal
	        	highChartData.append(listVal)
	finally:
	    csvfile.close()      # closing

	# print json.dumps(highChartData)
	return highChartData

def get_list_of_files():
	fileList = []

	for (dirpath, dirnames, filenames) in walk(app.config['UPLOAD_FOLDER']):
		print filenames
		#TODO: Add Check to see whether the file is a csv or not
		fileList.extend(filenames)
		# fileList.extend(filenames)
		break

	for f in fileList:
		if not (f.endswith('.csv')):
			fileList.remove(f)

	return fileList

def generate_file_data(filelist):
	print "im in generate file data"
	print filelist
	filedata = []
	#Creating the proper format for the search button
	for f in filelist:
		filedict = {}
		filedict['text'] = f
		filedict['value'] = f

		filedata.append(filedict)

	return filedata


@app.route('/graphFromData', methods = ['GET', 'POST'])
def generate_graph():
	if request.method == 'GET':
		print request
		return render_template('retailerDashboard.html', data = read_file('test.csv'), fileList = generate_file_data(get_list_of_files()))
	# if request.method == 'POST':

	return "Graph generated Successfully!"

@app.route('/generategraph', methods = ['GET', 'POST'])
def get_graph():
	if request.method == 'GET':
		print request
		return render_template('retailerDashboard.html', data = read_file('test.csv'), fileList = generate_file_data(get_list_of_files()))
	if request.method == 'POST':
		print request
		return render_template('retailerDashboard.html', data = read_file('test.csv'), fileList = generate_file_data(get_list_of_files()))


@app.route('/search',methods =['GET'])
def search_products():
	try:
		if 'searchKeyword' in request.args:
			keyword = request.args['searchKeyword']
			
			client = pymongo.MongoClient(MONGODB_URI_HomeAR)
			db = client.get_default_database()
			prod_details = db['product_details']
			cursor = prod_details.find({'prodCategory': keyword })
			# { '$in': [ '/ keyword /' ] }
			#.sort('prodId', 1)
			
			listProd = []
			# print ('prodId: %d,Prod Name: %s , Prod Desc: %s.' % (doc['prodId'], doc['ProdName'], doc['ProdDesc'], doc['ProdCount']))
			for doc in cursor: 
				print doc['prodName']
				#print ('ProdId: %d,Prod Name: %s , Prod Desc: %s, ProdCount: %d' % (doc['ProdId'], doc['ProdName'], doc['ProdDesc'], doc['ProdCount']))
				listProd.append(doc)
			# print str(keyword)
			# print listProd

			client.close()
			return render_template("search.html", status = "Search Successful!", item2 = listProd, itemlist = listProd, count = len(listProd))
		else:
			return render_template('search.html') #, status = "Rendering Page Successfully!", item2 = NULL, itemlist = NULL )
	except:
		e = sys.exc_info()[0]
		print "exception: " + e
	#if request.method == 'POST':
	#	return render_template('search.html' , status = "Rendering Page Successfully!", item2 = NULL, itemlist = NULL)

@app.route('/searchRetailer',methods =['GET'])
def search_option_for_retailers():
	try:
		if 'searchKeyword' in request.args:
			keyword = request.args['searchKeyword']
			
			client = pymongo.MongoClient(MONGODB_URI_HomeAR)
			db = client.get_default_database()
			prod_details = db['product_details']
			cursor = prod_details.find({'prodCategory': keyword })
			# { '$in': [ '/ keyword /' ] }
			#.sort('prodId', 1)
			
			listProd = []
			# print ('prodId: %d,Prod Name: %s , Prod Desc: %s.' % (doc['prodId'], doc['ProdName'], doc['ProdDesc'], doc['ProdCount']))
			for doc in cursor:
				print doc['prodName']
				#print ('ProdId: %d,Prod Name: %s , Prod Desc: %s, ProdCount: %d' % (doc['ProdId'], doc['ProdName'], doc['ProdDesc'], doc['ProdCount']))
				listProd.append(doc)
			print "---------"	
			print listProd
			client.close()
			return render_template("searchRetailer.html", status = "Search Successful!", item2 = listProd, itemlist = listProd)
		else:
			return render_template('searchRetailer.html') #, status = "Rendering Page Successfully!", item2 = NULL, itemlist = NULL )
	except:
		e = sys.exc_info()[0]
		print "exception: " + e

# @app.route('/modifyCount', methods = ['GET','POST'])
@app.route('/likeItem', methods = ['GET'])
def like_item():
	print "hello"
	itemCount = 0
	# print "checking search arg id- item id: " + str(request.args["_id"])
	if request.method == 'GET':
		itemId = request.args["id"]
		client = pymongo.MongoClient(MONGODB_URI_HomeAR)
		db = client.get_default_database()
		prod_details = db['product_details']
		cursor = prod_details.find({"_id" : ObjectId(itemId) })
		for doc in cursor:
			print doc['prodLikes']
			itemCount = doc['prodLikes'] + 1

		prod_details.update( {"_id" : ObjectId(itemId) },{ "$set": {'prodLikes' : itemCount }}	)

		client.close()
	return str(itemCount)

@app.route('/customerDashboard', methods =['GET','POST'])
def dashboard():
	return render_template('customerDashboard.html')
	#, status = "Search Successful!", item2 = listProd, itemlist = listProd)

@app.route('/retailerDashboard', methods =['GET','POST'])
def retailer_dashboard():
	return render_template('retailerDashboard.html', data = read_file('test.csv'), fileList = generate_file_data(get_list_of_files()))

@app.route('/aboutUs')
def about():
	return render_template('aboutUs.html')

@app.route('/services')
def services():
	return render_template('services.html')


"""
==========================
Cross Functional APIS
==========================
"""
@app.route('/login', methods =['POST'])
def login():
	message = ""
	if request.method == 'POST':
		if not request.form:
			print "No form Data Arguments!"
			return "No form Data Arguments!"
			# return render_template('LoginPage.html')

		uemail = request.form["Email"]
		upass = request.form["Password"]
		
		client = pymongo.MongoClient(MONGODB_URI_HomeAR)

		db = client.get_default_database()
		user_details = db['user_details']
		user = user_details.find({"l_email" : uemail.lower() })
		if user.count() == 0:
			message = "Error:Invalid Email-id. Please try again!"
		else:
			for u in user:
				if u['userpassword'] == upass:
					# Checks if TextureUrl field exists in doc prod
					if 'is_retailer' in u: 
						if u['is_retailer'] == "yes":
							message = "Retailer Login Successful!"
						else:
							message = "Customer Login Successful!"
					break
				else:
					message = message = "Error:Incorrect Password. Please try again!"

		client.close()
		print message
		return json.dumps(message)
		# return render_template('LoginPage.html', message= message)
	return "Error:Login Unsucessful!"

@app.route('/register', methods =['POST'])
def register():
	if request.method == 'POST':
		if not request.form:
			print "Error:No Arguments section!"
			return "Error:No Arguments found!"
			# return render_template('RegisterPage.html')

		useremail = request.form["Email"]
		username = request.form["Uname"]
		userpassword = request.form["Password"]
		is_retailer = "no"
		if 'IsRetailer' in request.form:
			is_retailer = request.form["IsRetailer"]
		else:
			is_retailer = "no"
		# lastname = request.args["LastName"]
		# address = request.args["address"]
		# pincode = request.args["pincode"]

		print useremail, userpassword, username

		client = pymongo.MongoClient(MONGODB_URI_HomeAR)
		db = client.get_default_database()
		user_details = db['user_details']
		
		# user = user_details.find({"id" : uemail.lower() })
		#TODO: If  
		# if not user:
		# 	message = "User details donot match!"

		# 	#insert into the database.
		user_details.insert({'useremail': useremail, 
				'userpassword': userpassword,
				'l_email':useremail.lower(),
				'username':username,
				'is_retailer':is_retailer
				}) 
			# 	'lastname': "lastname",
			# 	'address':"address",
			# 	'pincode':"pincode" 

		client.close()
		return json.dumps("Data inserted successfully!")
		# return render_template('HomeARLanding.html')
	return "Error:Registration Failed! :("

"""
==========================
Mobile Related APIS
==========================
"""

categoryType = {
	1 : "Sofas",
    2 : "Tables",
	3 : "Chairs",
	4 : "T V Consoles",
	5 : "Love Seats",
	6 : "Beds",
	7 : "Night Stands",
	8 : "Dressers and Chests",
	9 : "Bed Benches",
	10 : "Floor Lamps",
	11 : "Table Lamps",
	12 : "Ceiling Fans",
}

# @app.route('/category/<int:categoryId>',methods=['GET'])
# def getProdbyCategory(categoryId):

@app.route('/category',methods=['GET'])
def getProdbyCategory():
	message = None
	if request.method == 'GET':
		if not request.args:
			return None

		category = int(request.args['categoryId'])
		print category

		listCategoryProducts =[]
		listCategorisedImageUrl = []

		client = pymongo.MongoClient(MONGODB_URI_HomeAR)
		db = client.get_default_database()
		prod_details = db['product_details']
		products = prod_details.find({"prodCategory" : categoryType[category] })

		if not products:
			#No Products in this category!
			message = None
		else:
			print products
			# message = json.dumps(products)
			for prod in products:
				print prod['prodName'] + prod['prodCategory'] + prod['prodImgUrl'] + prod['prod3DUrl']
				listCategoryProducts.append(prod)
				listCategorisedImageUrl.append(prod['prodImgUrl'])

		client.close()

		#print str(listCategorisedImageUrl)
		return json.dumps(listCategorisedImageUrl)
		# return render_template('CategoryProducts.html', message= listCategorisedImageUrl)


# this is to get Product attributes by category
# for the HomeAr page to consume the 3DUrl, ImageUrl and textureUrl.
@app.route('/prodDetails',methods=['GET'])
# @app.route('/prodDetails/<categoryId>',methods=['GET'])
def getProdDetailsbyCategory():
	message = None
	if request.method == 'GET':
		if not request.args:
			return None

		category = int(request.args['categoryId'])
		print "\nSearching for Category Id: " + str(category)

		listCategoryProducts =[]

		client = pymongo.MongoClient(MONGODB_URI_HomeAR)
		db = client.get_default_database()
		prod_details = db['product_details']
		products = prod_details.find({"prodCategory" : categoryType[category] })

		if not products:
			#No Products in this category!
			message = None
		else:
			print products
			# message = json.dumps(products)
			for prod in products:
				print "\n" + prod['prodName'] + "\t" + prod['prodCategory'] + "\t" + prod['prodImgUrl'] + "\t" + prod['prod3DUrl']
				listProdDetailItem = []
				listProdDetailItem.append(prod['prodName'])
				listProdDetailItem.append(prod['prodImgUrl'])
				listProdDetailItem.append(prod['prod3DUrl'])
				
				# Checks if TextureUrl field exists in doc prod
				if 'prodTextureUrl' in prod: 
					listProdDetailItem.append(prod['prodTextureUrl'])
				else:
					listProdDetailItem.append("http://50.116.3.141:5500/static/textures/stuhl.jpg")
				# TODO: Add texture URL
				listCategoryProducts.append(listProdDetailItem)

		client.close()

		#print str(listCategorisedImageUrl)
		
		return json.dumps(listCategoryProducts)
		# return render_template('CategoryProducts.html', message= listCategorisedImageUrl)


if __name__ == '__main__':
	app.run(host="0.0.0.0",port=5000,debug=True)

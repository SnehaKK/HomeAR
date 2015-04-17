import os, json
from flask import Flask, render_template, request, make_response
from werkzeug import secure_filename
import csv
import sys
import pymongo
from bson.objectid import ObjectId
from os import walk
import logging


app = Flask(__name__)
MONGODB_URI = "mongodb://sneha:test123@ds063150.mongolab.com:63150/testmongolabs"

app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

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

@app.route('/searchProduct',methods =['GET','POST'])
def search_products():
	if request.method == "GET":
		print "checking search keyword "  + request.args['searchKeyword']
		keyword = request.args['searchKeyword']
		
		client = pymongo.MongoClient(MONGODB_URI)
		db = client.get_default_database()
		prod_details = db['prod_details']
		cursor = prod_details.find({'ProdName': keyword })
		# { '$in': [ '/ keyword /' ] }
		#.sort('prodId', 1)
		
		listProd = []
		# print ('prodId: %d,Prod Name: %s , Prod Desc: %s.' % (doc['prodId'], doc['ProdName'], doc['ProdDesc'], doc['ProdCount']))
		for doc in cursor: 
			print doc['ProdId']
			# print ('ProdId: %d,Prod Name: %s , Prod Desc: %s, ProdCount: %d' % (doc['ProdId'], doc['ProdName'], doc['ProdDesc'], doc['ProdCount']))
			listProd.append(doc)
		
		client.close()
		return render_template("search.html", status = "Search Successful!", item2 = listProd, itemlist = listProd)

	if request.method == 'POST':
		return render_template('search.html' , status = "Rendering Page Successfully!", item2 = NULL, itemlist = NULL)

# @app.route('/modifyCount', methods = ['GET','POST'])
@app.route('/likeItem', methods = ['GET'])
def like_item():
	print "hello"
	itemCount = 0
	# print "checking search arg id- item id: " + str(request.args["_id"])
	if request.method == 'GET':
		itemId = request.args["id"]
		client = pymongo.MongoClient(MONGODB_URI)
		db = client.get_default_database()
		prod_details = db['prod_details']
		cursor = prod_details.find({"_id" : ObjectId(itemId) })
		for doc in cursor:
			print doc['ProdCount']
			itemCount = doc['ProdCount'] + 1

		prod_details.update( {"_id" : ObjectId(itemId) },{ "$set": {'ProdCount' : itemCount }}	)

		client.close()
	return str(itemCount)	

@app.route('/search',methods =['GET','POST'])
def search():
	# if request.method == 'GET':
	# 	print "request is: " + request
	# 	return render_template('search.html')
	if request.method == 'POST':
		return None
	return render_template("search.html")


@app.route('/customerDashboard', methods =['GET','POST'])
def dashboard():
	return render_template('customerDashboard.html')
	#, status = "Search Successful!", item2 = listProd, itemlist = listProd)

@app.route('/retailerDashboard', methods =['GET','POST'])
def retailer_dashboard():
	return render_template('retailerDashboard.html', data = read_file('test.csv'), fileList = generate_file_data(get_list_of_files()))

@app.route('/retailertest', methods =['GET'])
def retailer_test():
	return render_template('retailerDashboard_test.html')

@app.route('/about')
def about():
	return render_template('contactUs.html')

@app.route('/services')
def services():
	return render_template('services.html')

@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/contact')
def contact():
	return render_template('contactUs.html')

if __name__ == '__main__':
	app.run(host="0.0.0.0",port=5000,debug=True)

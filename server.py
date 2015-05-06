import os, json
from flask import Flask, render_template, request, make_response, json, jsonify, flash
from werkzeug import secure_filename
import csv
import sys
import pymongo, re
from bson.objectid import ObjectId
from os import walk
import logging
from forms import ContactForm
from flask.ext.mail import Message, Mail

mail = Mail()
app = Flask(__name__)

MONGODB_URI = "mongodb://sneha:test123@ds061370.mongolab.com:61370/homear"
app.secret_key = "th9s9sm\/d3l0pm3n3tk3\/" #DEVELOPMENT_KEY ="mail server development key"  

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'homearteam@gmail.com'
app.config["MAIL_PASSWORD"] = 'Mummy$HomearProject'
 
mail.init_app(app)

app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

"""
To Enable CORS (Cross Origin Resource Sharing)
"""

@app.after_request
def add_cors(resp):
    """ Ensure all responses have the CORS headers. This ensures any failures are also accessible
        by the client. """
    resp.headers['Access-Control-Allow-Origin'] = request.headers.get('Origin','*')
    resp.headers['Access-Control-Allow-Credentials'] = 'true'
    resp.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS, GET'
    resp.headers['Access-Control-Allow-Headers'] = request.headers.get( 
        'Access-Control-Request-Headers', 'Authorization' )
    # set low for debugging
    if app.debug:
        resp.headers['Access-Control-Max-Age'] = '1'
    return resp


"""

Web Related APIS

"""
@app.route('/',methods =['GET','POST'])
def index():
	form = ContactForm()
	if request.method == 'POST':
		print "==== print:"
		print form.validate()
		if form.validate() == False:
			flash('All fields are required.')
			return render_template('index.html', form=form)
		else:
			msg = Message(form.senderssubject.data, sender='HomeARteam@gmail.com', recipients=['kulsneha04@gmail.com'])
			msg.html = """ 
			<b>From:</b> <i>%s</i> 
			<br> <b>Email-id:</b> <i>%s</i>
			<br> <b>Message:</b> <i>%s</i>
			""" \
			% (form.sendersname.data, form.sendersemail.data, form.sendersmessage.data)
			mail.send(msg)
			return render_template('index.html', form=form, success=True)
	if request.method == 'GET':
		return render_template('index.html',form=form)
	return 'Hello World!'

@app.route('/search',methods =['GET', 'POST'])
def search_products():
	form = ContactForm()
	if request.method == 'POST':
		print "==== print:"
		print form.validate()
		if form.validate() == False:
			flash('All fields are required.')
			return render_template('search.html', form=form)
		else:
			msg = Message(form.senderssubject.data, sender='HomeARteam@gmail.com',
			 recipients=['kulsneha04@gmail.com'])
			msg.html = """ <b>From:</b> <i>%s</i> <br> <b>Email-id:</b> <i>%s</i> <br> <b>Message:</b> <i>%s</i>""" \
				% (form.sendersname.data, form.sendersemail.data, form.sendersmessage.data)
			mail.send(msg)
			form = ContactForm()
			return render_template('search.html', form=form, success=True)

	elif request.method =='GET':
		try:
			if 'searchKeyword' in request.args:
				keyword = request.args['searchKeyword']
				
				client = pymongo.MongoClient(MONGODB_URI)
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
				return render_template("search.html", form=form, status = "Search Successful!", 
					item2 = listProd, itemlist = listProd, count = max(len(listProd),0))
			else:
				return render_template('search.html', form=form) #, status = "Rendering Page Successfully!", item2 = NULL, itemlist = NULL )
		except:
			e = sys.exc_info()[0]
			print "exception: " + e
	#if request.method == 'POST':
	#	return render_template('search.html' , status = "Rendering Page Successfully!", item2 = NULL, itemlist = NULL)

@app.route('/searchRetailer',methods =['GET','POST'])
def search_option_for_retailers():
	form = ContactForm()
	if request.method == 'POST':
		print "==== print:"
		print form.validate()
		if form.validate() == False:
			flash('All fields are required.')
			return render_template('searchRetailer.html', form=form)
		else:
			msg = Message(form.senderssubject.data, sender='HomeARteam@gmail.com',
			 recipients=['kulsneha04@gmail.com'])
			msg.html = """ <b>From:</b> <i>%s</i> <br> <b>Email-id:</b> <i>%s</i> <br> <b>Message:</b> <i>%s</i>""" \
				% (form.sendersname.data, form.sendersemail.data, form.sendersmessage.data)
			mail.send(msg)
			form = ContactForm()
			return render_template('searchRetailer.html', form=form, success=True)
	elif request.method =='GET':
		try:
			if 'searchKeyword' in request.args:
				keyword = request.args['searchKeyword']
				
				client = pymongo.MongoClient(MONGODB_URI)
				db = client.get_default_database()
				prod_details = db['product_details']
				cursor = prod_details.find({'prodCategory': keyword })
				# { '$in': [ '/ keyword /' ] }
				#.sort('prodId', 1)
				
				listProd = []
				# print ('prodId: %d,Prod Name: %s , Prod Desc: %s.' % (doc['prodId'], doc['ProdName'], doc['ProdDesc'], doc['ProdCount']))
				for doc in cursor:
					# print doc['prodName']
					#print ('ProdId: %d,Prod Name: %s , Prod Desc: %s, ProdCount: %d' % (doc['ProdId'], doc['ProdName'], doc['ProdDesc'], doc['ProdCount']))
					listProd.append(doc)
				print "---------"	
				# print listProd
				client.close()
				return render_template("searchRetailer.html", status = "Search Successful!", form=form, item2 = listProd, itemlist = listProd, count = len(listProd))
			else:
				return render_template('searchRetailer.html', form=form) #, status = "Rendering Page Successfully!", item2 = NULL, itemlist = NULL )
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
		client = pymongo.MongoClient(MONGODB_URI)
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
	form = ContactForm()
	if request.method == 'GET':
		return render_template("customerDashboard.html", form = form)
	if request.method == 'POST':
		print "==== print:"
		print form.validate()
		if form.validate() == False:
			flash('All fields are required.')
			return render_template('customerDashboard.html', form=form)
		else:
			msg = Message(form.senderssubject.data, sender='HomeARteam@gmail.com',
			 recipients=['kulsneha04@gmail.com'])
			msg.html = """ <b>From:</b> <i>%s</i> <br> <b>Email-id:</b> <i>%s</i> <br> <b>Message:</b> <i>%s</i>""" \
				% (form.sendersname.data, form.sendersemail.data, form.sendersmessage.data)
			mail.send(msg)
			form = ContactForm()
			return render_template('customerDashboard.html', form=form, success=True)
	return render_template('customerDashboard.html')
	#, status = "Search Successful!", item2 = listProd, itemlist = listProd)

@app.route('/retailerDashboard', methods =['GET','POST'])
def retailer_dashboard():
	form = ContactForm()
	if request.method == 'GET':
		return render_template("retailerDashboard.html", form = form)
	if request.method == 'POST':
		print "==== print:"
		print form.validate()
		if form.validate() == False:
			flash('All fields are required.')
			return render_template('retailerDashboard.html', form=form)
		else:
			msg = Message(form.senderssubject.data, sender='HomeARteam@gmail.com',
			 recipients=['kulsneha04@gmail.com'])
			msg.html = """ <b>From:</b> <i>%s</i> <br> <b>Email-id:</b> <i>%s</i> <br> <b>Message:</b> <i>%s</i>""" \
				% (form.sendersname.data, form.sendersemail.data, form.sendersmessage.data)
			mail.send(msg)
			form = ContactForm()
			return render_template('retailerDashboard.html', form=form, success=True)
	# return render_template('retailerDashboard.html', data = read_file('test.csv'), fileList = generate_file_data(get_list_of_files()))

@app.route('/contactus',methods =['GET','POST'])
def contact():
	form = ContactForm()
	if request.method == 'POST':
		print "==== print:"
		print form.validate()
		if form.validate() == False:
			flash('All fields are required.')
			return render_template('index.html', form=form)
		else:
			msg = Message(form.senderssubject.data, sender='HomeARteam@gmail.com',
			 recipients=['kulsneha04@gmail.com'])
			msg.html = """ <b>From:</b> <i>%s</i> <br> <b>Email-id:</b> <i>%s</i> <br> <b>Message:</b> <i>%s</i>""" \
				% (form.sendersname.data, form.sendersemail.data, form.sendersmessage.data)
			mail.send(msg)
			form = ContactForm()
			return render_template('index.html', form=form, success=True)
	elif request.method =='GET':
		# form = ""
		return render_template('index.html',form=form)

@app.route('/aboutUs',methods = ['GET','POST'])
def about():
	form = ContactForm()
	if request.method == 'POST':
		print "==== print:"
		print form.validate()
		if form.validate() == False:
			flash('All fields are required.')
			return render_template('aboutUs.html', form=form)
		else:
			msg = Message(form.senderssubject.data, sender='HomeARteam@gmail.com',
			 recipients=['kulsneha04@gmail.com'])
			msg.html = """ <b>From:</b> <i>%s</i> <br> <b>Email-id:</b> <i>%s</i> <br> <b>Message:</b> <i>%s</i>""" \
				% (form.sendersname.data, form.sendersemail.data, form.sendersmessage.data)
			mail.send(msg)
			form = ContactForm()
			return render_template('aboutUs.html', form=form, success=True)
	elif request.method =='GET':
		# form = ""
		return render_template('aboutUs.html',form=form)
	return render_template('aboutUs.html')

@app.route('/services')
def services():
	return render_template('services.html')

@app.route('/viewUserDetails', methods =['GET'])
def getUserData():
	message = ""
	if request.method == 'GET':
		if not request.args:
			print "No Arguments to get the user data!"
			return "No Arguments"
		else:
			if 'userEmail' in request.args:
				client = pymongo.MongoClient(MONGODB_URI)
				uemail = request.args["userEmail"]
				db = client.get_default_database()
				user_details =db['user_details']
				user = user_details.find({"l_email" : uemail.lower() })
				if user.count() == 0:
					message = "Error: No User"
				else:
					for u in user:
						message = u['username']
						break
				client.close()
				
				print message
				return message

@app.route('/update', methods =['POST'])
def updateRecords():
	message = ""
	if request.method == 'POST':
		if not request.form:
			print "No form Data Arguments!"
			return "No form Data Arguments!"
			# return render_template('LoginPage.html')

		uemail = request.form["email"]
		# upass = request.form["Password"]
		
		client = pymongo.MongoClient(MONGODB_URI)

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
					


"""
Cross Functional APIS: For Web and Mobile Interfaces
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
		
		client = pymongo.MongoClient(MONGODB_URI)

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

		client = pymongo.MongoClient(MONGODB_URI)
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
Mobile Related APIS
"""

categoryType = {
	1 : "Sofas",
    2 : "Chairs",
	3 : "Tables",
	4 : "T V Stands",
	5 : "Beds",
	6 : "Lamps",
	7 : "Vases",
	8 : "Patio Benches",
	9 : "Patio Chairs"
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

		client = pymongo.MongoClient(MONGODB_URI)
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

		client = pymongo.MongoClient(MONGODB_URI)
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
				# print "\n" + prod['prodName'] + "\t" + prod['prodCategory'] \
				# 	+ "\t" + prod['prodImgUrl'] + "\t" + prod['prod3DUrl']
				listProdDetailItem = []
				listProdDetailItem.append(prod['prodName'])
				listProdDetailItem.append(prod['prodImgUrl'])
				listProdDetailItem.append(prod['prod3DUrl'])
				
				# Checks if TextureUrl field exists in doc prod
				if 'prodTextureUrl' in prod: 
					listProdDetailItem.append(prod['prodTextureUrl'])
				# else:
				# 	listProdDetailItem.append("http://50.116.3.141:5500/static/textures/stuhl.jpg")
				# TODO: Add texture URL
				listCategoryProducts.append(listProdDetailItem)

		client.close()

		#print str(listCategorisedImageUrl)
		
		return json.dumps(listCategoryProducts)
		# return render_template('CategoryProducts.html', message= listCategorisedImageUrl)


if __name__ == '__main__':
	app.run(host="0.0.0.0",port=5000,debug=True)

from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField, SubmitField, validators, ValidationError
 
class ContactForm(Form):
	sendersname = TextField("Sender's Name", [validators.Required("Please enter your name.")])
	sendersemail = TextField("Sender's Email", [validators.Required("Please enter your email."),  validators.Email("Please enter a valid email.")])
	senderssubject = TextField("Sender's Subject", [validators.Required("Please enter a subject.")])
	sendersmessage = TextAreaField("Sender's Message", [validators.Required("Please enter a message.")])
	submit = SubmitField("Send Message")
from flask_sqlalchemy import SQLAlchemy
from my_tools import calculate_age
from datetime import datetime
import bcrypt


db = SQLAlchemy()


class Player(db.Model):
	__tablename__ = "players"

	id = db.Column(db.Integer, primary_key=True)
	created_at = db.Column(db.DateTime, default=datetime.utcnow)
	firstname = db.Column(db.String(160), nullable=False)
	lastname = db.Column(db.String(160), nullable=False)
	birthday = db.Column(db.String(100), nullable=False)
	gender = db.Column(db.String(60), nullable=False)
	nationality = db.Column(db.String(80), nullable=False)
	team = db.Column(db.String(100), nullable=False, default='without team')
	image_name = db.Column(db.String(255), nullable=False)
	image_path = db.Column(db.String(255), nullable=False)
	cv_name = db.Column(db.String(255), nullable=False)
	cv_path = db.Column(db.String(255), nullable=False)
	email = db.Column(db.String(260), unique=True)
	whatsapp = db.Column(db.String(220), unique=True)
	password = db.Column(db.String(100), nullable=False)


	def __init__(self, firstname, lastname, birthday, gender, nationality, team, image_name, image_path, cv_name, cv_path, email, whatsapp, password):
		self.firstname = firstname
		self.lastname = lastname
		self.birthday = birthday
		self.gender = gender
		self.nationality = nationality
		self.team = team
		self.image_name = image_name
		self.image_path = image_path
		self.cv_name = cv_name
		self.cv_path = cv_path
		self.email = email
		self.whatsapp = whatsapp
		self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


	def check_password(self, password):
		return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))


	def __str__(self):
		data1 = 'football player'
		data2 = f'{self.team} I am looking for proper association to join'
		data3 = 'I like to start a new expirence for supporting my Futurist team to To achieve successes'
		if self.gender == 'female':
			data1 = 'feminist football player'

		if self.team != 'without team':
			data2 = f'playing in {self.team} association'
			data3 = 'I want to change my experience to develop myself as a footballer to find my team'

		return f'my name is {self.firstname} {self.lastname} I have {calculate_age(self.birthday)} years old from {self.nationality},\
 I am highly motivated {data1} currently {data2} and still looking for agent {data3},\
 hope I find an agent then arrive at a satisfactory offer very soon.'


	def get_description(self):
		return str(self)


class Agent(db.Model):
	__tablename__ = "agents"

	id = db.Column(db.Integer, primary_key=True)
	created_at = db.Column(db.DateTime, default=datetime.utcnow)
	firstname = db.Column(db.String(160), nullable=False)
	lastname = db.Column(db.String(160), nullable=False)
	birthday = db.Column(db.String(100), nullable=False)
	nationality = db.Column(db.String(80), nullable=False)
	residence_country = db.Column(db.String(80), nullable=False)
	years_experience = db.Column(db.Integer, nullable=False)
	city = db.Column(db.String(120), nullable=False)
	office_address = db.Column(db.String(200), unique=True)
	image_name = db.Column(db.String(255), nullable=False)
	image_path = db.Column(db.String(255), nullable=False)
	email = db.Column(db.String(200), unique=True)
	whatsapp = db.Column(db.String(220), unique=True)
	password = db.Column(db.String(100), nullable=False)


	def __init__(self, firstname, lastname, birthday, nationality, residence_country, years_experience, city, office_address, image_name, image_path, email, whatsapp, password):
		self.firstname = firstname
		self.lastname = lastname
		self.birthday = birthday
		self.nationality = nationality
		self.residence_country = residence_country
		self.years_experience = years_experience
		self.city = city
		self.office_address = office_address
		self.image_name = image_name
		self.image_path = image_path
		self.email = email
		self.whatsapp = whatsapp
		self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


	def check_password(self, password):
		return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))


	def __str__(self):
		return f'my name is {self.firstname} {self.lastname} I have {calculate_age(self.birthday)} years old from {self.nationality}\
 I have more than {self.years_experience} years of experience my role as an agent is Career management Transfer negotiation,\
 Contract negotiation, Financial planning And much more on I have an office in {self.office_address}, {self.city},\
 {self.residence_country} hope always I be a reason to make my clients satisfied'


	def get_description(self):
		return str(self)


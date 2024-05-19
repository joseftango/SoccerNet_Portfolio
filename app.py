from flask import Flask, request, render_template, redirect, session, flash, url_for
from models import Player, Agent, db
from flask_wtf import CSRFProtect
from dotenv import dotenv_values
from my_tools import valid_password


import os


app = Flask(__name__)
config = dotenv_values('.env')


app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqldb://{config['MYSQL_USER']}:{config['MYSQL_PWD']}@{config['MYSQL_HOST']}/{config['MYSQL_DB']}"
app.config['DEBUG'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.secret_key = config['SECRET_KEY']


csrf = CSRFProtect(app)
db.init_app(app)
"""link our database with application"""


with app.app_context():
	db.create_all()
""" ensure that the database connection is properly initialized then
creates all the tables defined in the models """


@app.route('/home')
def home():
	return render_template('home.html')


@app.route('/register_player', methods=['GET','POST'])
def register_player():
	if request.method == 'POST':
		firstname = request.form['firstname']
		lastname = request.form['lastname']
		birthday = request.form['birthday']
		nationality = request.form['nationality']
		gender = request.form['gender']
		whatsapp = request.form['whatsapp']
		team = request.form['team']
		email = request.form['email']
		password1 = request.form['password1']
		password2 = request.form['password2']
		image = request.files['image']
		cv = request.files['cv']
		image_name = image.filename
		image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_name)
		image.save(image_path)
		cv_name = cv.filename
		cv_path = os.path.join(app.config['UPLOAD_FOLDER'], cv_name)
		cv.save(cv_path)

		player_exists = Player.query.filter_by(email=email).first() is not None

		if player_exists:
			flash('Email already exists. Please try using a different email.', 'error')
			return render_template('player_register.html')

		if password1 != password2:
			flash('please check your password comfirmation.', 'error')
			return render_template('player_register.html')

		check_valid_pwd = valid_password(password1)

		if check_valid_pwd != True:
			flash(check_valid_pwd, 'error')
			return render_template('player_register.html')


		new_player = Player(firstname=firstname, lastname=lastname, birthday=birthday,\
		nationality=nationality, gender=gender, whatsapp=whatsapp, team=team,\
		email=email, password=password1, image_name=image_name, image_path=image_path,\
		cv_name=cv_name, cv_path=cv_path)
		db.session.add(new_player)
		db.session.commit()
		print(new_player.get_description())
		flash('congratulations you have been registred successfully !', 'success')
		return redirect('/login')
	if 'email' in session:
		return redirect('notfound')

	return render_template('player_register.html')


@app.route('/register_agent', methods=['GET','POST'])
def register_agent():
	if request.method == 'POST':
		firstname = request.form['firstname']
		lastname = request.form['lastname']
		birthday = request.form['birthday']
		nationality = request.form['nationality']
		residence_country = request.form['residence_country']
		years_experience = request.form['years_experience']
		city = request.form['city']
		office_address = request.form['office_address']
		email = request.form['email']
		whatsapp = request.form['whatsapp']
		password1 = request.form['password1']
		password2 = request.form['password2']
		image = request.files['image']
		image_name = image.filename
		image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_name)
		image.save(image_path)

		agent_exists = Agent.query.filter_by(email=email).first() is not None

		if agent_exists:
			flash('Email already exists. Please try using a different email.', 'error')
			return render_template('agent_register.html')

		if password1 != password2:
			flash('please check your password comfirmation.', 'error')
			return render_template('agent_register.html')

		check_valid_pwd = valid_password(password1)

		if check_valid_pwd != True:
			flash(check_valid_pwd, 'error')
			return render_template('agent_register.html')

		new_agent = Agent(firstname=firstname, lastname=lastname, birthday=birthday,\
		nationality=nationality, residence_country=residence_country, city=city,\
		office_address=office_address, years_experience=years_experience, image_name=image_name,\
		image_path=image_path, email=email, whatsapp=whatsapp, password=password1)

		db.session.add(new_agent)
		db.session.commit()
		flash('congratulations you have been registred successfully !', 'success')
		return redirect('login')

	if 'email' in session:
		return redirect('notfound')

	return render_template('agent_register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']

		user = Player.query.filter_by(email=email).first() or \
Agent.query.filter_by(email=email).first()

		if user == None:
			flash('email not exists please sign up', 'error')
			return render_template('Login.html')

		if user.check_password(password):
			session['email'] = user.email
			if isinstance(user, Player):
				session['role'] = 'player'
				return redirect('/agents')
			else:
				session['role'] = 'agent'
				return redirect('/players')

		flash('unvalid password, please try again', 'error')
		return render_template('Login.html')

	return render_template('Login.html')


@app.route('/players', methods=['GET'])
def players():
	if 'email' in session and session['role'] == 'agent':
		players = Player.query.all()
		return render_template('players.html', players=players)
	else:
		return redirect('/notfound')


@app.route('/agents', methods=['GET'])
def agents():
	if 'email' in session and session['role'] == 'player':
		agents = Agent.query.all()
		return render_template('agents.html', agents=agents)
	else:
		return redirect('/notfound')


@app.route('/logout')
def logout():
	session.pop('email', None)
	session.pop('role', None)
	flash('Logged out successfully!', 'success')
	return redirect('/login')


@app.route('/choose', methods=['GET'])
def choose():
	return render_template('choose.html')


@app.route('/resume/<int:player_id>', methods=['GET'])
def resume(player_id):
	if 'email' in session:
		player = Player.query.get(player_id)
		if player is None:
			return redirect('/notfound')
		player.cv_path = player.cv_path.replace('static/', '', 1)
		player_cv_name = player.cv_name
		return render_template('resume.html', cv_player=player.cv_path, player_cv_name=player_cv_name)
	else:
		return redirect('/notfound')


@app.route('/profile', methods=['GET'])
def profile():
	if 'email' in session:
		user = Player.query.filter_by(email=session['email']).first() or \
Agent.query.filter_by(email=session['email']).first()
	if user is None:
		return redirect('/notfound')

	return render_template('user_profile.html', user=user)


@app.route('/delete_user', methods=['POST'])
def delete_user():
	if 'email' in session:
		user = Player.query.filter_by(email=session['email']).first() or \
Agent.query.filter_by(email=session['email']).first()
		if user:
			db.session.delete(user)
			db.session.commit()
			session.pop('email', None)
			session.pop('role', None)
		else:
			return redirect(url_for('notfound'))

		flash('Your profile has been deleted, we are sorry to see you out of the service', 'success')
		return redirect(url_for('login'))

	return redirect(url_for('notfound'))


@app.route('/update_user', methods=['POST', 'GET'])
def update_user():
	if 'email' not in session:
		return redirect('notfound')

	user = Player.query.filter_by(email=session['email']).first() or \
Agent.query.filter_by(email=session['email']).first()

	if request.method == 'POST':
		email = request.form.get('email')
		whatsapp = request.form.get('whatsaap')
		team = request.form.get('team') if session['role'] == 'player' else None
		image = request.files['image']
		cv = request.files['cv'] if session['role'] == 'player' else None

		if email:
			user.email = email
			session['email'] = email
		if whatsapp:
			user.whatsapp = whatsapp
		if team and session['role'] == 'player':
			user.team = team
					
		if image:
			image_name = image.filename
			user.image_name = image_name
			user.image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_name)
			image.save(os.path.join('static/uploads', image_name))

		if session['role'] == 'player' and cv:
			cv_name = cv.filename
			user.cv_name = cv_name
			user.cv_path = os.path.join(app.config['UPLOAD_FOLDER'], cv_name)
			cv.save(os.path.join('static/uploads', cv_name))

		db.session.commit()
		flash('Your profile has been updated', 'success')
		return redirect('profile')

	return render_template('update_user.html', user=user)


@app.route('/about', methods=['GET'])
def about():
	return render_template('about.html')

@app.route('/services', methods=['GET'])
def services():
	return render_template('services.html')


@app.route('/notfound', methods=['GET'])
def notfound():
	return render_template('error.html')


if __name__ == '__main__':
	app.run(host="0.0.0.0", port=config['PORT'])


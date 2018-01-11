from flask import Flask, Response, render_template, redirect, url_for, request, session, abort
import sys
import random
import cPickle
from honeywords import generate_honeywords_tail, generate_honeywords_chaffing

app = Flask(__name__, template_folder='templates')

# config
app.config.update(
	DEBUG = True,
	SECRET_KEY = 'secret_xxx'
)


@app.route('/', methods=["GET", "POST"])
def home():
	if request.method == 'GET':
		return render_template('login.html')

	with open(db_name, 'rb') as input_db:
		db = cPickle.load(input_db)

	username = request.form['username']
	password = request.form['password']

	if username not in db.keys():
		return Response('<p>Username does not exist. <a href="/login">Try again</a></p>')

	(idx, honeywords, hashes, tough_nuts) = db[username]

	if password == honeywords[idx]:
		return Response('<p>Successful login.</p>')
	elif password in honeywords:
		return Response('<p>Found an attack, this incident will be reported.</p>')

	return Response('<p>Incorrect password. <a href="/login">Try again</a></p>')


@app.route('/register', methods=["GET", "POST"])
def register():
	if 'random' not in session.keys():
			session['random'] = random.randint(100, 999)

	if request.method == 'GET':
		return render_template('register.html', run_mode=run_mode, random_tail=str(session['random']))

	db = {}
	try:
		with open(db_name, 'rb') as input_db:
			db = cPickle.load(input_db)
	except IOError:
		pass

	username = request.form['username']
	password = request.form['password'].encode('ascii', 'ignore')

	if run_mode == 'take-a-tail':
		newpassword = request.form['newpassword']

	if username in db.keys():
		return Response('<p>Username taken. <a href="/register">Try again</a></p>')

	if run_mode == 'take-a-tail' and newpassword != password + str(session['random']):
		return Response('<p>Invalid registration. <a href="/register">Try again</a></p>')


	if run_mode == 'take-a-tail':
		(idx, honeywords, hashes, tough_nuts) = generate_honeywords_tail(password, str(session['random']))
	else:
		(idx, honeywords, hashes, tough_nuts) = generate_honeywords_chaffing(password, 20)
	

	db[username] = (idx, honeywords, hashes, tough_nuts)
	print db

	with open(db_name, 'wb') as output_db:
		cPickle.dump(db, output_db)

	session.pop('random', None)

	return Response('<p>Valid registration. <a href="/">Login</a></p>')


@app.errorhandler(401)
def page_not_found(e):
	return Response('<p>Login failed</p>')


if __name__ == "__main__":
	global run_mode, db_name

	run_mode = sys.argv[1]
	db_name = 'users_tail.db' if run_mode == 'take-a-tail' else 'users_chaffing.db'
	app.run()

# Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors

# Initialize the app from Flask
app = Flask(__name__)

# Configure MySQL
conn = pymysql.connect(host = 'localhost',
						user = 'root',
						password = '',
						db = 'air_ticket_reservation_system',
						charset = 'utf8mb4',
						cursorclass = pymysql.cursors.DictCursor)

# Define a route to starting page
@app.route('/')
def hello():
	return render_template('index.html', error = None, start = True, data = None)

# Define route to search results
@app.route('/searchAuth1', methods = ['GET', 'POST'])
def searchAuth1():
	# Grabs information from the forms
	arrive_airport = request.form['arrive_airport']
	depart_airport = request.form['depart_airport']
	arrive_city = request.form['arrive_city']
	depart_city = request.form['depart_city']

	# Cursor used to send queries
	cursor = conn.cursor()

	# Query to find search results
	query = 'SELECT * FROM flight JOIN airport as a1 on flight.depart_airport = a1.name JOIN airport as a2 on flight.arrive_airport = a2.name WHERE depart_time >= NOW() AND ((flight.depart_airport = %s OR a1.city = %s) OR (flight.arrive_airport = %s OR a2.city = %s))'
	cursor.execute(query, (depart_airport, depart_city, arrive_airport, arrive_city))

	# Stores the results in a variable
	fetch_data = cursor.fetchall()

	cursor.close()
	error = None

	if (fetch_data):
		# Returns results in new html page
		return render_template('index.html', error = error, start = False, data = fetch_data)
	else:
		# Returns an error message to the html page
		error = 'No flights found'
		return render_template('index.html', error = error, start = False, data = fetch_data)

# Define route to search results
@app.route('/searchAuth2', methods = ['GET', 'POST'])
def searchAuth2():
	# Grabs information from the forms
	key = request.form['search_word']

	# Cursor used to send queries
	cursor = conn.cursor()

	# Query to find search results
	query = 'SELECT * FROM flight WHERE airline_name = %s OR flight_num = %s'
	cursor.execute(query, (key, key))

	# Stores the results in a variable
	fetch_data = cursor.fetchall()

	cursor.close()
	error = None

	if (fetch_data):
		# Returns results in new html page
		return render_template('index.html', error = error, start = False, data = fetch_data)
	else:
		# Returns an error message to the html page
		error = 'No flights found'
		return render_template('index.html', error = error, start = False, data = fetch_data)

# Define route to search results for customers
@app.route('/searchCustomerAuth1', methods = ['GET', 'POST'])
def searchCustomerAuth1():
	email = session['email']

	# Grabs information from the forms
	arrive_airport = request.form['arrive_airport']
	depart_airport = request.form['depart_airport']
	arrive_city = request.form['arrive_city']
	depart_city = request.form['depart_city']

	# Cursor used to send queries
	cursor = conn.cursor()

	# Query to find search results
	query = 'SELECT * FROM flight JOIN airport as a1 on flight.depart_airport = a1.name JOIN airport as a2 on flight.arrive_airport = a2.name WHERE depart_time >= NOW() AND ((flight.depart_airport = %s OR a1.city = %s) OR (flight.arrive_airport = %s OR a2.city = %s))'
	cursor.execute(query, (depart_airport, depart_city, arrive_airport, arrive_city))

	# Stores the results in a variable
	fetch_data = cursor.fetchall()

	# Query to get all customers flights
	query = 'SELECT * FROM customer JOIN purchase ON customer.email = purchase.email JOIN ticket ON purchase.ticket_ID = ticket.ticket_ID JOIN flight ON ticket.flight_num = flight.flight_num WHERE customer.email = %s'
	cursor.execute(query, (email))
	flight_data = cursor.fetchall()

	cursor.close()
	error = None

	if (fetch_data):
		# Returns results in new html page
		return render_template('homeCustomer.html', email = email, error = error, search_data = fetch_data, myflights = flight_data)
	else:
		# Returns an error message to the html page
		error = 'No flights found'
		return render_template('homeCustomer.html', email = email, error = error, search_data = fetch_data, myflights = flight_data)

# Define route to search results for customers
@app.route('/searchCustomerAuth2', methods = ['GET', 'POST'])
def searchCustomerAuth2():
	email = session['email']

	# Grabs information from the forms
	key = request.form['search_word']
	
	# Cursor used to send queries
	cursor = conn.cursor()

	# Query to find search results
	query = 'SELECT * FROM flight WHERE airline_name = %s OR flight_num = %s'
	cursor.execute(query, (key, key))

	# Stores the results in a variable
	fetch_data = cursor.fetchall()

	# Query to get all customer's flights
	query = 'SELECT * FROM customer JOIN purchase ON customer.email = purchase.email JOIN ticket ON purchase.ticket_ID = ticket.ticket_ID JOIN flight ON ticket.flight_num = flight.flight_num WHERE customer.email = %s'
	cursor.execute(query, (email))
	flight_data = cursor.fetchall()

	cursor.close()
	error = None

	if (fetch_data):
		# Returns results in new html page
		return render_template('homeCustomer.html', email = email, error = error, search_data = fetch_data, myflights = flight_data)
	else:
		# Returns an error message to the html page
		error = 'No flights found'
		return render_template('homeCustomer.html', email = email, error = error, search_data = fetch_data, myflights = flight_data)

# Define route for login page
@app.route('/login')
def login():
	return render_template('login.html')

# Define route for customer login
@app.route('/loginCustomer')
def loginCustomer():
	return render_template('loginCustomer.html')

# Define route for staff login
@app.route('/loginStaff')
def loginStaff():
	return render_template('loginStaff.html')

# Define route for register page
@app.route('/register')
def register():
	return render_template('register.html')

# Define route for customer register
@app.route('/registerCustomer')
def registerCustomer():
	return render_template('registerCustomer.html')

# Define route for staff register
@app.route('/registerStaff')
def registerStaff():
	return render_template('registerStaff.html')

# Authenticates the customer login
@app.route('/loginAuthCustomer', methods = ['GET', 'POST'])
def loginAuthCustomer():
	# Grabs information from the forms
	email = request.form['email']
	password = request.form['password']

	# Cursor used to send queries
	cursor = conn.cursor()

	# Query to see if customer exists
	query = 'SELECT * FROM customer WHERE email = %s and password = md5(%s)'
	cursor.execute(query, (email, password))

	# Stores the results in a variable
	data = cursor.fetchone()

	cursor.close()
	error = None

	if (data):
		# Creates a session for the the user
		session['email'] = email
		return redirect(url_for('homeCustomer'))
	else:
		# Returns an error message to the html page
		error = 'This user does not exist.'
		return render_template('loginCustomer.html', error = error)

# Authenticates the staff login
@app.route('/loginAuthStaff', methods = ['GET', 'POST'])
def loginAuthStaff():
	# Grabs information from the forms
	username = request.form['username']
	password = request.form['password']

	# Cursor used to send queries
	cursor = conn.cursor()

	# Executes query
	query = 'SELECT * FROM airline_staff WHERE username = %s and password = md5(%s)'
	cursor.execute(query, (username, password))

	# Stores the results in a variable
	data = cursor.fetchone()

	cursor.close()
	error = None

	if (data):
		# Creates a session for the the user
		session['username'] = username
		return redirect(url_for('homeStaff'))
	else:
		# Returns an error message to the html page
		error = 'This user does not exist.'
		return render_template('loginStaff.html', error = error)

# Authenticates the customer register
@app.route('/registerAuthCustomer', methods = ['GET', 'POST'])
def registerAuthCustomer():
	# Grabs information from the forms
	email = request.form['email']
	password = request.form['password']

	# Cursor used to send queries
	cursor = conn.cursor()

	# Executes query
	query = 'SELECT * FROM customer WHERE email = %s'
	cursor.execute(query, (email))

	# Stores the results in a variable
	data = cursor.fetchone()

	error = None

	if (data):
		# If the previous query returns data, then the user already exists
		error = "This user already exists."
		return render_template('registerCustomer.html', error = error)
	else:
		ins = 'INSERT INTO customer VALUES(%s, md5(%s), NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL)'
		cursor.execute(ins, (email, password))
		conn.commit()
		cursor.close()
		return render_template('index.html')

# Authenticates the staff register
@app.route('/registerAuthStaff', methods = ['GET', 'POST'])
def registerAuthStaff():
	# Grabs information from the forms
	email = request.form['email']
	username = request.form['username']
	password = request.form['password']
	airline_name = request.form['airline_name']

	# Cursor used to send queries
	cursor = conn.cursor()

	# Executes query
	query = 'SELECT * FROM airline_staff WHERE email = %s'
	cursor.execute(query, (email))

	# Stores the results in a variable
	data = cursor.fetchone()

	error = None

	if (data):
		# If the previous query returns data, then the user already exists
		error = "This user already exists."
		return render_template('registerStaff.html', error = error)
	else:
		ins = 'INSERT INTO airline_staff VALUES(%s, md5(%s), NULL, NULL, NULL, NULL, %s, %s)'
		cursor.execute(ins, (username, password, email, airline_name))
		conn.commit()
		cursor.close()
		return render_template('index.html')

# Define route to customer homepage
@app.route('/homeCustomer')
def homeCustomer():
	email = session['email']
	cursor = conn.cursor();
	query = 'SELECT * FROM customer JOIN purchase ON customer.email = purchase.email JOIN ticket ON purchase.ticket_ID = ticket.ticket_ID JOIN flight ON ticket.flight_num = flight.flight_num WHERE customer.email = %s'
	cursor.execute(query, (email))
	fetch_data = cursor.fetchall() 
	cursor.close()
	return render_template('homeCustomer.html', email = email, error = None, start = True, search_data = None, myflights = fetch_data)

# Authenticates the purchase
@app.route('/buyTicketAuth', methods = ['GET', 'POST'])
def buyTicketAuth():
	email = session['email']
	flight_num = request.form['flight_num']
	card_num = request.form['card_num']
	card_type = request.form['card_type']
	card_holder = request.form['card_holder']
	card_exp = request.form['card_exp']

	cursor = conn.cursor();
	query = 'SELECT ticket_ID FROM ticket JOIN flight ON ticket.flight_num = flight.flight_num WHERE ticket.flight_num = %s'
	cursor.execute(query, (flight_num))
	ticket_num = cursor.fetchone()
	error = None

	if (card_type != "debit" and card_type != "credit"):
		error = "That's not a valid card type."
		cursor.close()
		return render_template('buyTicket.html', email = email, error = error)

	if (ticket_num):
		query = 'INSERT INTO purchase VALUES(%s, %s, NOW(), %s, %s, %s, %s)'
		cursor.execute(query, (email, ticket_num["ticket_ID"], card_type, card_num, card_holder, card_exp))
		cursor.close()
		return render_template('buyTicket.html', email = email, error = error)
	else:
		error = "That's not a valid flight number."
		cursor.close()
		return render_template('buyTicket.html', email = email, error = error)

# Define a route to cancel page
@app.route('/cancelTrip')
def cancelTrip():
	email = session['email']
	cursor = conn.cursor();
	query = 'SELECT * FROM customer JOIN purchase ON customer.email = purchase.email JOIN ticket ON purchase.ticket_ID = ticket.ticket_ID JOIN flight ON ticket.flight_num = flight.flight_num WHERE customer.email = %s'
	cursor.execute(query, (email))
	fetch_data = cursor.fetchall() 
	cursor.close()
	return render_template('cancelTrip.html', email = email, myflights = fetch_data)

# Authenticates the trip cancellation
@app.route('/cancelAuth', methods = ['GET', 'POST'])
def cancelAuth():
	email = session['email']
	flight_num = request.form['flight_num']
	
	cursor = conn.cursor();
	query = 'SELECT purchase.ticket_ID FROM purchase JOIN ticket ON purchase.ticket_ID = ticket.ticket_ID WHERE email = %s AND flight_num = %s'
	cursor.execute(query, (email, flight_num))
	ticket_num = cursor.fetchone()

	error = None
	if (ticket_num):
		query = 'DELETE FROM purchase WHERE email = %s AND ticket_ID = %s'
		cursor.execute(query, (email, ticket_num["ticket_ID"]))
	else:
		error = "That's not a valid trip."

	query = 'SELECT * FROM customer JOIN purchase ON customer.email = purchase.email JOIN ticket ON purchase.ticket_ID = ticket.ticket_ID JOIN flight ON ticket.flight_num = flight.flight_num WHERE customer.email = %s'
	cursor.execute(query, (email))
	fetch_data = cursor.fetchall()
	
	cursor.close()

	return render_template('cancelTrip.html', email = email, myflights = fetch_data, error = error)

# Define a route to rating page
@app.route('/rate')
def rate():
	email = session['email']
	cursor = conn.cursor();
	query = 'SELECT * FROM customer JOIN purchase ON customer.email = purchase.email JOIN ticket ON purchase.ticket_ID = ticket.ticket_ID JOIN flight ON ticket.flight_num = flight.flight_num WHERE customer.email = %s'
	cursor.execute(query, (email))
	fetch_data = cursor.fetchall() 
	cursor.close()
	return render_template('rate.html', email = email, myflights = fetch_data, message = False)

# Authenticates the rating submission
@app.route('/rateAuth', methods = ['GET', 'POST'])
def rateAuth():
	email = session['email']
	flight_num = request.form['flight_num']
	rating = request.form['rating']
	comment = request.form['comment']
	
	cursor = conn.cursor();
	query = 'SELECT * FROM customer JOIN purchase ON customer.email = purchase.email JOIN ticket ON purchase.ticket_ID = ticket.ticket_ID WHERE ticket.flight_num = %s'
	cursor.execute(query, (flight_num))
	fetch_data = cursor.fetchall()
	error = None

	if (not fetch_data):
		error = "You never went on that flight."
	elif (int(rating) < 1 or int(rating) > 5):
		error = "That's not a valid star rating."
	else:
		query = 'INSERT INTO rate VALUES(%s, %s, %s, %s)'
		cursor.execute(query, (email, flight_num, comment, rating))

	query = 'SELECT * FROM customer JOIN purchase ON customer.email = purchase.email JOIN ticket ON purchase.ticket_ID = ticket.ticket_ID JOIN flight ON ticket.flight_num = flight.flight_num WHERE customer.email = %s'
	cursor.execute(query, (email))
	fetch_data = cursor.fetchall()
	
	cursor.close()

	return render_template('rate.html', email = email, myflights = fetch_data, error = error)

# Define a route to spendings page
@app.route('/mySpendings')
def mySpendings():
	email = session['email']
	cursor = conn.cursor();
	query = 'SELECT SUM(sold_price) FROM purchase JOIN ticket WHERE email = %s AND ADDDATE(NOW(), INTERVAL -1 YEAR)'
	cursor.execute(query, (email))
	year_spent = cursor.fetchone() 

	query = 'SELECT month(purchase_dt) as month, SUM(sold_price) FROM purchase JOIN ticket WHERE email = %s AND purchase_dt > NOW() - INTERVAL 6 MONTH'
	cursor.execute(query, (email))
	month_spent = cursor.fetchall() 

	cursor.close()
	return render_template('mySpendings.html', email = email, yearly_money = year_spent['SUM(sold_price)'], monthly_money = month_spent, date_range = False, new_data = None)

# Authenticates the airport addition
@app.route('/mySpendingsAuth', methods = ['GET', 'POST'])
def mySpendingsAuth():
	email = session['email']
	cursor = conn.cursor();

	query = 'SELECT SUM(sold_price) FROM purchase JOIN ticket WHERE email = %s AND ADDDATE(NOW(), INTERVAL -1 YEAR)'
	cursor.execute(query, (email))
	year_spent = cursor.fetchone() 

	query = 'SELECT month(purchase_dt) as month, SUM(sold_price) FROM purchase JOIN ticket WHERE email = %s AND purchase_dt > NOW() - INTERVAL 6 MONTH'
	cursor.execute(query, (email))
	month_spent = cursor.fetchall()

	start_date = request.form['start_date']
	end_date = request.form['end_date']

	query = 'SELECT SUM(sold_price) FROM purchase JOIN ticket WHERE email = %s AND purchase_dt > %s AND purchase_dt < %s';
	cursor.execute(query, (email, start_date, end_date))
	new_year_spent = cursor.fetchone() 

	query = 'SELECT month(purchase_dt) as month, SUM(sold_price) FROM purchase JOIN ticket WHERE email = %s	AND purchase_dt > %s AND purchase_dt < %s'
	cursor.execute(query, (email, start_date, end_date))
	new_month_spent = cursor.fetchall()

	cursor.close()

	return render_template('mySpendings.html', email = email, yearly_money = year_spent['SUM(sold_price)'], monthly_money = month_spent, date_range = True, new_yearly_money = new_year_spent['SUM(sold_price)'], start_date = start_date, end_date = end_date, new_monthly_money = new_month_spent)

# Define route to staff homepage
@app.route('/homeStaff')
def homeStaff():
	username = session['username']
	cursor = conn.cursor();
	query = 'SELECT airline_name FROM airline_staff WHERE username = %s'
	cursor.execute(query, (username))
	airline_name = cursor.fetchone()

	query = 'SELECT * FROM flight WHERE airline_name = %s AND depart_time > NOW() AND depart_time <= NOW() + INTERVAL 30 day ORDER BY depart_time ASC'
	cursor.execute(query, (airline_name['airline_name']))
	fetch_data = cursor.fetchall() 
	cursor.close()

	return render_template('homeStaff.html', username = username, flights = fetch_data)

# Define route to view ratings
@app.route('/viewFlights')
def viewFlights():
	username = session['username']
	return render_template('viewFlights.html', username = username, message = False, flight = None, error = None)

# Authenticates the airport addition
@app.route('/viewFlightsAuth1', methods = ['GET', 'POST'])
def viewFlightsAuth1():
	username = session['username']
	arrive_airport = request.form['arrive_airport']
	depart_airport = request.form['depart_airport']
	arrive_city = request.form['arrive_city']
	depart_city = request.form['depart_city']

	cursor = conn.cursor();
	query = 'SELECT airline_name FROM airline_staff WHERE username = %s'
	cursor.execute(query, (username))
	airline_name = cursor.fetchone()

	query = 'SELECT * FROM flight JOIN airport as a1 on flight.depart_airport = a1.name JOIN airport as a2 on flight.arrive_airport = a2.name WHERE airline_name = %s AND ((flight.depart_airport = %s OR a1.city = %s) OR (flight.arrive_airport = %s OR a2.city = %s))'
	cursor.execute(query, (airline_name['airline_name'], depart_airport, depart_city, arrive_airport, arrive_city))
	fetch_data = cursor.fetchall()

	return render_template('viewFlights.html', username = username, message = True, flight = fetch_data)

# Authenticates the airport addition
@app.route('/viewFlightsAuth2', methods = ['GET', 'POST'])
def viewFlightsAuth2():
	username = session['username']
	start_date = request.form['start_date']
	end_date = request.form['end_date']

	cursor = conn.cursor();
	query = 'SELECT airline_name FROM airline_staff WHERE username = %s'
	cursor.execute(query, (username))
	airline_name = cursor.fetchone()

	query = 'SELECT * FROM flight WHERE airline_name = %s AND depart_time >= %s AND arrive_time <= %s'
	cursor.execute(query, (airline_name['airline_name'], start_date, end_date))
	fetch_data = cursor.fetchall()

	return render_template('viewFlights.html', username = username, message = True, flight = fetch_data)

# Define route to add flight
@app.route('/createFlight')
def createFlight():
	username = session['username']
	return render_template('createFlight.html', username = username, message = False, flight = None, airline_name = None)

# Authenticates flight addition
@app.route('/createFlightAuth', methods = ['GET', 'POST'])
def createFlightAuth():
	username = session['username']
	airline_name = request.form['airline_name']
	airplane_ID = request.form['airplane_ID']
	flight_num = request.form['flight_num']
	base_price = request.form['base_price']
	status = request.form['status']
	depart_airport = request.form['depart_airport']
	arrive_airport = request.form['arrive_airport']
	depart_time = request.form['depart_time']
	arrive_time = request.form['arrive_time']

	cursor = conn.cursor();

	query = 'INSERT INTO flight VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)'
	cursor.execute(query, (airline_name, airplane_ID, flight_num, base_price, status, depart_airport, arrive_airport, depart_time, arrive_time))

	query = 'SELECT * FROM flight WHERE airline_name = %s'
	cursor.execute(query, (airline_name))
	fetch_data = cursor.fetchall() 
	cursor.close()

	return render_template('createFlight.html', username = username, message = True, flight = fetch_data, airline_name = airline_name)

# Define route to add airplane
@app.route('/updateFlightStatus')
def updateFlightStatus():
	username = session['username']
	cursor = conn.cursor();

	query = 'SELECT airline_name FROM airline_staff WHERE username = %s'
	cursor.execute(query, (username))
	airline_name = cursor.fetchone()

	query = 'SELECT * FROM flight WHERE airline_name = %s'
	cursor.execute(query, (airline_name['airline_name']))
	fetch_data = cursor.fetchall() 
	cursor.close()

	return render_template('updateFlightStatus.html', username = username, flights = fetch_data, message = False)

# Authenticates flight status update
@app.route('/updateFlightStatusAuth', methods = ['GET', 'POST'])
def updateFlightStatusAuth():
	username = session['username']
	flight_num = request.form['flight_num']
	status = request.form['status']

	cursor = conn.cursor();
	query = 'SELECT airline_name FROM airline_staff WHERE username = %s'
	cursor.execute(query, (username))
	airline_name = cursor.fetchone()

	query = 'UPDATE flight SET status = %s WHERE airline_name = %s AND flight_num = %s'
	cursor.execute(query, (status, airline_name['airline_name'], flight_num))

	query = 'SELECT * FROM flight WHERE airline_name = %s'
	cursor.execute(query, (airline_name['airline_name']))
	fetch_data = cursor.fetchall() 
	cursor.close()

	return render_template('updateFlightStatus.html', username = username, flights = fetch_data, message = True)

# Define route to add airplane
@app.route('/addAirplane')
def addAirplane():
	username = session['username']
	return render_template('addAirplane.html', username = username, message = False, airplanes = None, airline_name = None)

# Authenticates the airplane addition
@app.route('/addAirplaneAuth', methods = ['GET', 'POST'])
def addAirplaneAuth():
	username = session['username']
	airplane_ID = request.form['airplane_ID']
	airline_name = request.form['airline_name']
	seats = request.form['seats']
	company = request.form['company']
	age = request.form['age']

	cursor = conn.cursor()
	query = 'INSERT INTO airplane VALUES (%s, %s, %s, %s, %s)'
	cursor.execute(query, (airplane_ID, airline_name, seats, company, age))

	cursor = conn.cursor()
	query = 'SELECT * FROM airplane WHERE LOWER(airline_name) = %s'
	cursor.execute(query, (airline_name))
	fetch_data = cursor.fetchall()
	cursor.close()

	return render_template('addAirplane.html', username = username, message = True, airplanes = fetch_data, airline_name = airline_name)

# Define route to add airport
@app.route('/addAirport')
def addAirport():
	username = session['username']
	return render_template('addAirport.html', username = username, message = False, airport = None)

# Authenticates the airport addition
@app.route('/addAirportAuth', methods = ['GET', 'POST'])
def addAirportAuth():
	username = session['username']
	name = request.form['name']
	city = request.form['city']
	country = request.form['country']
	type = request.form['type']

	cursor = conn.cursor()
	query = 'INSERT INTO airport VALUES (%s, %s, %s, %s)'
	cursor.execute(query, (name, city, country, type))

	query = 'SELECT * FROM airport'
	cursor.execute(query)
	fetch_data = cursor.fetchall()
	cursor.close()

	return render_template('addAirport.html', username = username, message = True, airport = fetch_data)

# Define route to view ratings
@app.route('/viewRatings')
def viewRatings():
	username = session['username']
	return render_template('viewRatings.html', username = username, message = False, flight_num = None, rating = None)

# Authenticates the airport addition
@app.route('/viewRatingsAuth', methods = ['GET', 'POST'])
def viewRatingsAuth():
	username = session['username']
	flight_num = request.form['flight_num']

	cursor = conn.cursor()
	query = 'SELECT flight_num, email, comment, stars FROM rate WHERE flight_num = %s'
	cursor.execute(query, (flight_num))
	fetch_data = cursor.fetchall()

	query = 'SELECT AVG(stars) FROM rate WHERE flight_num = %s'
	cursor.execute(query, (flight_num))
	avg_stars = cursor.fetchone()
	cursor.close()

	return render_template('viewRatings.html', username = username, message = True, flight_num = flight_num, rating = fetch_data, avg_stars = avg_stars['AVG(stars)'])

# Define route to view frequent customers
@app.route('/viewFrequentCustomers')
def viewFrequentCustomers():
	username = session['username']

	cursor = conn.cursor()
	query = 'SELECT airline_name FROM airline_staff WHERE username = %s'
	cursor.execute(query, (username))
	airline_name = cursor.fetchone()

	query = 'SELECT MAX(rider) AS rides, email FROM (SELECT COUNT(email) AS rider, email FROM ticket AS T, purchase AS P WHERE P.ticket_ID = T.ticket_ID AND airline_name = %s AND purchase_dt > NOW() - INTERVAL 1 YEAR GROUP BY email) AS count_of_rides'
	cursor.execute(query, (airline_name['airline_name']))
	customer = cursor.fetchone()

	cursor.close()

	return render_template('viewFrequentCustomers.html', username = username, freq_customer = customer['email'], message = False, flight = None)

# Authenticates the airport addition
@app.route('/viewFrequentCustomersAuth', methods = ['GET', 'POST'])
def viewFrequentCustomersAuth():
	username = session['username']
	email = request.form['email']

	cursor = conn.cursor()
	query = 'SELECT airline_name FROM airline_staff WHERE username = %s'
	cursor.execute(query, (username))
	airline_name = cursor.fetchone()

	query = 'SELECT MAX(rider) AS rides, email FROM (SELECT COUNT(email) AS rider, email FROM ticket AS T, purchase AS P WHERE P.ticket_ID = T.ticket_ID AND airline_name = %s AND purchase_dt > NOW() - INTERVAL 1 YEAR GROUP BY email) AS count_of_rides'
	cursor.execute(query, (airline_name['airline_name']))
	customer = cursor.fetchone()

	query = 'SELECT DISTINCT * FROM purchase as P, ticket as T, flight as F WHERE T.airline_name = %s AND P.ticket_ID = T.ticket_ID AND email = %s AND F.arrive_time <= NOW()'
	cursor.execute(query, (airline_name['airline_name'], email))
	flight = cursor.fetchall()
	cursor.close()

	return render_template('viewFrequentCustomers.html', username = username, freq_customer = customer['email'], message = True, email = email, flight = flight)

# Define route to view ratings
@app.route('/viewReports')
def viewReports():
	username = session['username']
	return render_template('viewReports.html', username = username, message = False, start_date = None, end_date = None, report = None, tickets = None)

# Authenticates the airport addition
@app.route('/viewReportsAuth', methods = ['GET', 'POST'])
def viewReportsAuth():
	username = session['username']
	start_date = request.form['start_date']
	end_date = request.form['end_date']

	cursor = conn.cursor()
	query = 'SELECT airline_name FROM airline_staff WHERE username = %s'
	cursor.execute(query, (username))
	airline_name = cursor.fetchone()

	query = 'SELECT month(purchase_dt) as month, COUNT(purchase.ticket_ID) as ticket FROM purchase JOIN ticket WHERE airline_name = %s AND purchase_dt > NOW() - INTERVAL 6 MONTH ORDER BY month'
	cursor.execute(query, airline_name['airline_name'])
	report = cursor.fetchall()

	query = 'SELECT COUNT(purchase.ticket_ID) FROM ticket JOIN purchase WHERE airline_name = %s AND purchase_dt > %s AND purchase_dt < %s'
	cursor.execute(query, (airline_name['airline_name'], start_date, end_date))
	tickets = cursor.fetchone()

	cursor.close()

	return render_template('viewReports.html', username = username, message = True, start_date = start_date, end_date = end_date, report = report, tickets = tickets['COUNT(purchase.ticket_ID)'])

# Define route to view ratings
@app.route('/viewRevenue')
def viewRevenue():
	username = session['username']

	cursor = conn.cursor()
	query = 'SELECT SUM(sold_price) FROM ticket as T JOIN purchase as P WHERE T.ticket_ID = P.ticket_ID AND purchase_dt > NOW() - INTERVAL 1 MONTH'
	cursor.execute(query)
	month_revenue = cursor.fetchone()

	query = 'SELECT SUM(sold_price) FROM ticket as T JOIN purchase as P WHERE T.ticket_ID = P.ticket_ID AND purchase_dt > NOW() - INTERVAL 1 YEAR'
	cursor.execute(query)
	year_revenue = cursor.fetchone()
	cursor.close()

	return render_template('viewRevenue.html', username = username, month_revenue = month_revenue['SUM(sold_price)'], year_revenue = year_revenue['SUM(sold_price)'])

@app.route('/logoutCustomer')
def logoutCustomer():
	session.pop('email')
	return redirect('/login')

@app.route('/logoutStaff')
def logoutStaff():
	session.pop('username')
	return redirect('/login')

# Secret key for session
app.secret_key = 'a secret key'
if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)

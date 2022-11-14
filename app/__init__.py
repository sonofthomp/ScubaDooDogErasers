from flask import Flask, render_template, session, request, redirect, url_for
import sqlite3

############################# Database stuff #############################
DB_FILE="data.db"
db = sqlite3.connect(DB_FILE, check_same_thread=False) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events
command = ""
# Setup database
# c.execute("DROP TABLE IF EXISTS user_info;")
# command = "CREATE TABLE user_info (username TEXT, password TEXT, stories_ids TEXT);"
c.execute(command)    # run SQL statement

#Set up story creation stuff
# c.execute("DROP TABLE IF EXISTS pages;")
# c.execute("CREATE TABLE pages(story_id int, title text, content text, edit_ids text)");


# USEFUL FOR LATER
# db.commit() #save changes
# db.close()  #close database
################################ App stuff ################################
app = Flask(__name__)
app.secret_key = "AAAAA";

@app.route('/', methods=["GET"])
def landing_page():
# If you’re logged in, then this is the dashboard. If you’re not logged in,
# then this is the landing page. It contains a logo and the login and signup
# forms. Contains a search box where you can type in the name of every
# article, and the server will return the content of the article via
# /view_page. Contains a “Create Story” button.

	'''
	PSEUDOCODE:

	if user is logged in:
		return dashboard page

	return landing_page
	'''
	# session.pop()

	# command = "SELECT * FROM pages;"
	# c.execute(command)
	# temp = c.fetchall()
	# print(temp)
	if (session):
		c.execute("SELECT * FROM pages")
		print(c.fetchall())
		c.execute("SELECT * FROM user_info")
		print(c.fetchall())

		command = f'SELECT stories_ids FROM user_info WHERE username="{session["username"][0]}"';
		# command = f'SELECT * FROM user_info WHERE username="{session["username"][0]}"'
		c.execute(command)
		# print(c.fetchone())
		temp = c.fetchone()[0]
		temp = temp.split(',')
		stories = []
		for id in temp:
			if (id != ""):
				command = f'SELECT title FROM pages WHERE story_id="{id}"'
				c.execute(command)
				title = c.fetchone()[0]

				stories += [title, id]

		return render_template("dashboard.html", stories=stories)
	else:
		return render_template("landing_page.html")

@app.route('/logout', methods=["GET"])
def logout():
   session.pop("username", None)
   return redirect('/')

@app.route('/login', methods=["POST"])
def login():
	# The login route. This is the route that the login form on the landing page sends the information to

	'''
	PSEUDOCODE:

	username = username from form
	password = password from form

	if it's in that database:
		create a session

	else:
		return an error page or something
	'''
	username = request.form['username']
	password = request.form['password']

	command = "SELECT * FROM user_info;"
	c.execute(command)
	users = c.fetchall()

	for tuple in users:
		if (username == tuple[0]):
			if (password == tuple[1]):
				session["username"] = [username]
				# return render_template("dashboard.html")
				return redirect("/")
			else:
				return render_template("landing_page.html", errorTextL="Invalid password")

	return render_template("landing_page.html", errorTextL="Invalid username")


@app.route('/signup', methods=["POST"])
def signup():
	# The signup route. This is the route that the signup form on the landing page sends the information to

	'''
	PSEUDOCODE:

	username = username from form
	password = password from form

	if it's in that database:
		return an error page

	else:
		enter row into sql table with appropriate information
		log user in
	'''
	username = request.form["username"]
	password = request.form["password"]

	command = "SELECT * FROM user_info;"
	c.execute(command)
	users = c.fetchall()

	for tuple in users:
		if (username == tuple[0]):
			return render_template("landing_page.html", errorTextS="Username already exists")

	command = f"INSERT INTO user_info VALUES(\"{username}\", \"{password}\", \"\");"
	c.execute(command)
	db.commit()
	return render_template("landing_page.html")

@app.route('/view_story', methods=["GET"])
def view_story():
	# Contains the content of any requested story (the title of the page is specified within the URL arguments).
	# QCC: Do we want to index by title of story or # of story?

	'''
	PSEUDOCODE:

	story_id = url argument from request.args

	lookup the sql row based on the story_id
	return the content of the page
	'''
	return render_template('view_story.html')

@app.route('/story_creation_form', methods=["GET"])
def story_creation_form():
	# This returns a form allowing a user to enter the title and content of a new article they want to create
	# This form will ask for the title of the story as well as the starting content of the story

	'''
	PSEUDOCODE:

	return the content of the page
	'''
	return render_template('story_creation_form.html')

@app.route('/submit_story', methods=["POST"])
def submit_story():
	# This creates the new article from the parameters provided from the form on /story_creation_form
	# that sent the user to this route
##Set up story creation stuff
#c.execute("DROP TABLE IF EXISTS pages;")
#c.execute("create table pages(story_id int, title text, content text, edit_ids text)");
	'''
	PSEUDOCODE:

	story_title = get information from post request

	insert new row into sqlite database containing this new story
	'''
	story_title = request.form["story_title"]
	story_content = request.form["story_content"]

	command = "SELECT COUNT(1) as x FROM pages"
	story_id = c.execute(command).fetchone()[0]
	# print(c.fetchall())
# then run c.fetchone()

	edit_ids = "123,456,789"
	# story_id = magically generated number (global int counter?? )
	c.execute(
    f"""
    INSERT INTO pages VALUES ('{story_id}', '{story_title}', '{story_content}', '{edit_ids}');
 """
)

	command = f'SELECT stories_ids FROM user_info WHERE username="{session["username"][0]}"'
	c.execute(command)
	temp = c.fetchone()[0]
	temp = str(temp) + str(story_id) + ","

	c.execute(f'UPDATE user_info SET stories_ids="{temp}" WHERE username="{session["username"][0]}"')

	db.commit()
	print("successfully created sql stuff")
	print(f"""
    INSERT INTO pages VALUES ('{story_id}', '{story_title}', '{story_content}', '{edit_ids}');
 """)
	#redirect you to homepage. I might edit dashboard.html template so that you can receive a message of confirmation that your story was successfully created
	return redirect('/')

@app.route('/story_editing_form', methods=["GET"])
def story_editing_form():
	# This returns the form of editing a story

	'''
	PSEUDOCODE:

	return the html form for editing the story
	'''
	return render_template('story_editing_form.html')

@app.route('/submit_edit', methods=["POST"])
def submit_edit():
	# Updates the database with the new story content

	'''
	PSEUDOCODE:

	content = get information from post request
	overwrite what is in the sql database
	QCC: do we have to commit the changes in sqlite?
	'''
	return 'work in progress'

'''
KAREN DONT WORRY ABOUT THIS THIS IS JUST NOTES FOR RUSSELL
SQLite Database:

1  | title: hello, content: this is the view_story
2  | title: the second story, content: this is another story

When you search:
'the second story'

You get the response:
The story is http://127.0.0.1:5000/view_story?id=2
'''

if __name__ == '__main__':
	app.debug = True
	app.run()

# <<<<<<< HEAD
# from flask import Flask, render_template, session, request, redirect, url_for
# import sqlite3
#
# app = Flask(__name__)
#
# app.secret_key = "AAAAA";
#
# eUser = ""
# ePass = ""
# # Database stuff
# DB_FILE="data.db"
# db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
# c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events
# # Setup database
# c.execute("DROP TABLE IF EXISTS user_info;")
# command = "CREATE TABLE user_info (username TEXT, password TEXT, stories_ids TEXT);"
# c.execute(command)    # run SQL statement
#
#
# @app.route('/', methods = ['GET', 'POST'])
# def login():
#     # print(session)
#     if (not session):
#         if (request.method == "POST"):
#             global eUser
#             eUser = request.form['user']
#             global ePass
#             ePass = request.form['pass']
#
#             command = "SELECT * FROM user_info;"
#             c.execute(command)
#             users = c.fetchall()
#
#             for tuple in users:
#                 if (eUser == tuple[0] && ePass == tuple[1]):
#                     print("good")
#
#
#         #     if (request.form['user'] == username and request.form['pass'] == password):
#         #         try:
#         #             session[eUser] = [request.form["user"], request.form["pass"]]
#         #         except KeyError:
#         #             return render_template("login.html")
#         #
#         #         return render_template("response.html", username = session[eUser][0],
#         #         password = session[eUser][1])
#         #     elif request.form['user'] == username:
#         #         return render_template("login.html", errorText="Password is invalid.")
#         #     elif request.form['pass'] == password:
#         #         return render_template("login.html", errorText="Username is invalid.")
#         #     else:
#         #         return render_template("login.html", errorText="Username and password is invalid.")
#         # else:
#         #     return render_template("login.html")
#     else:
#         return render_template("response.html", username = session  [eUser][0],
#         password = session[eUser][1])
#
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#
#
# @app.route('/logout', methods=['GET', 'POST'])
# def logout():
#     session.pop(eUser, None)
#     return redirect('/')
#
# if (__name__ == "__main__"):
#     app.debug = True
#     app.run()
# =======
from flask import Flask, render_template, session, request, redirect, url_for
import sqlite3

############################# Database stuff #############################
DB_FILE="data.db"
db = sqlite3.connect(DB_FILE, check_same_thread=False) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events
# Setup database
c.execute("DROP TABLE IF EXISTS user_info;")
command = "CREATE TABLE user_info (username TEXT, password TEXT, stories_ids TEXT);"
c.execute(command)    # run SQL statement

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
    if (session):
        return render_template("dashboard.html")
    else:
        return render_template("landing_page.html")

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
                session[username] = [username]
                return render_template("dashboard.html")
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

@app.route('/story_creation_form', methods=["GET"])
def story_creation_form():
	# This returns a form allowing a user to enter the title and content of a new article they want to create
	# This form will ask for the title of the story as well as the starting content of the story

	'''
	PSEUDOCODE:

	return the content of the page
	'''

@app.route('/submit_story', methods=["POST"])
def submit_story():
	# This creates the new article from the parameters provided from the form on /story_creation_form
	# that sent the user to this route

	'''
	PSEUDOCODE:

	story_title = get information from post request

	insert new row into sqlite database containing this new story
	'''

@app.route('/story_editing_form', methods=["GET"])
def story_editing_form():
	# This returns the form of editing a story

	'''
	PSEUDOCODE:

	return the html form for editing the story
	'''

@app.route('/submit_edit', methods=["POST"])
def submit_edit():
	# Updates the database with the new story content

	'''
	PSEUDOCODE:

	content = get information from post request
	overwrite what is in the sql database
	QCC: do we have to commit the changes in sqlite?
	'''

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

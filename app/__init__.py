from flask import Flask, render_template, session, request, redirect, url_for
import sqlite3

app = Flask(__name__)

app.secret_key = "AAAAA";

eUser = ""
ePass = ""
# Database stuff
DB_FILE="data.db"
db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events
# Setup database
c.execute("DROP TABLE IF EXISTS user_info;")
command = "CREATE TABLE user_info (username TEXT, password TEXT, stories_ids TEXT);"
c.execute(command)    # run SQL statement


@app.route('/', methods = ['GET', 'POST'])
def login():
    # print(session)
    if (not session):
        if (request.method == "POST"):
            global eUser
            eUser = request.form['user']
            global ePass
            ePass = request.form['pass']

            command = "SELECT * FROM user_info;"
            c.execute(command)
            users = c.fetchall()

            for tuple in users:
                if (eUser == tuple[0] && ePass == tuple[1]):
                    print("good")
            

        #     if (request.form['user'] == username and request.form['pass'] == password):
        #         try:
        #             session[eUser] = [request.form["user"], request.form["pass"]]
        #         except KeyError:
        #             return render_template("login.html")
        #
        #         return render_template("response.html", username = session[eUser][0],
        #         password = session[eUser][1])
        #     elif request.form['user'] == username:
        #         return render_template("login.html", errorText="Password is invalid.")
        #     elif request.form['pass'] == password:
        #         return render_template("login.html", errorText="Username is invalid.")
        #     else:
        #         return render_template("login.html", errorText="Username and password is invalid.")
        # else:
        #     return render_template("login.html")
    else:
        return render_template("response.html", username = session  [eUser][0],
        password = session[eUser][1])

@app.route('/login', methods=['GET', 'POST'])
def login():


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop(eUser, None)
    return redirect('/')

if (__name__ == "__main__"):
    app.debug = True
    app.run()

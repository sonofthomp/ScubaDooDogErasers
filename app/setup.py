import sqlite3

DB_FILE="data.db"
db = sqlite3.connect(DB_FILE, check_same_thread=False) #open if file exists, otherwise create
c = db.cursor()

c.execute("DROP TABLE IF EXISTS user_info;")
c.execute("CREATE TABLE user_info (username TEXT, password TEXT, stories_ids TEXT);")

c.execute("DROP TABLE IF EXISTS pages;")
c.execute("CREATE TABLE pages(story_id int, title text, content text, edit_ids text)");
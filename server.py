from flask import Flask
import views
from database import Database
from tables import *
from flask_session import Session


HOSTNAME = '0.0.0.0'
PORT = 8080
DB_PATH = "main.db"


class App:
    def __init__(self):
        self.app = Flask(__name__)
        self.db = Database(DB_PATH)
        self.app.config["dbconfig"] = self.db
        self.app.config["SESSION_PERMANENT"] = False
        self.app.config["SESSION_TYPE"] = "filesystem"
        Session(self.app)

        self.app.add_url_rule('/', view_func=views.home_page, methods=['GET','Post'])
        self.app.add_url_rule('/index.html', view_func=views.home_page,endpoint="index.html", methods=['GET', 'POST'])
        self.app.add_url_rule('/profile.html', view_func=views.profile, endpoint="profile.html" ,methods=['GET','POST'])
        self.app.add_url_rule('/search.html', view_func=views.search, endpoint="search.html", methods=["GET","POST"])

        self.app.add_url_rule('/logout', view_func=views.logout ,methods=['GET','POST'])
        self.app.add_url_rule('/artist_single.html', view_func=views.artist_single, methods=['GET'])
        self.app.add_url_rule('/album_single.html', view_func=views.album_single, endpoint="album_single.html", methods=['GET', 'POST'])
        self.app.add_url_rule('/release_track_artist/<release_id>', view_func=views.release_track_artist_page, methods=['GET'])
        self.app.add_url_rule('/label.html', view_func=views.label, endpoint="label.html", methods=['GET', 'POST'])
        self.app.add_url_rule('/create_label.html', view_func=views.create_label, endpoint="create_label.html", methods=['GET', 'POST'])
        self.app.add_url_rule('/release_track/<track_id>', view_func=views.release_track, methods=["GET","POST"])
        self.app.add_url_rule('/release/<release_id>', view_func=views.release, methods=["GET","POST"])
        self.app.add_url_rule('/album_artist_edit.html', view_func=views.album_artist_edit,endpoint="album_artist_edit.html", methods=["GET","POST"])
            

if __name__ == '__main__':
    app = App()
    app.app.run(debug=True, host=HOSTNAME, port=PORT)

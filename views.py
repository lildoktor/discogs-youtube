from flask import current_app, render_template, redirect, url_for, session, request, make_response
import sqlite3
from database import Database
from tables.release import Release
from tables.release_artist import ReleaseArtist
from tables.label import Label

DBFILE = "main.db"
db = Database(DBFILE)


def artist_single():
    return render_template('artist_single.html')


def album_single():
    id = request.args.get('id')
    edit = request.args.get('edit')
    label_data = db.get_release_label_release_artist(id)
    release_data = db.get_release_by_id(id)
    release_artists = db.get_release_artists_by_release_id(id)
    if request.method == "POST":
        data = dict(request.form)
        if ("delete_id" in data and data["delete_id"]):
            db.delete_release_artist(id, data["delete_id"])
            release_artists = db.get_release_artists_by_release_id(id)
        elif ("artist_name" in data and data["artist_name"]):
            artist_id = db.get_artist_id_by_name(data["artist_name"])
            if (artist_id):
                print(id, artist_id)
                release_artist = ReleaseArtist(release_id=id, artist_id=artist_id[0], artist_name=data["artist_name"],
                                               extra=data["extra"], anv=data["anv"], position=data["position"], join_string=data["join_string"], role=data["role"], tracks=data["tracks"])
                db.add_release_artist(release_artist)
                release_artists = db.get_release_artists_by_release_id(id)
        else:
            release = Release(id=id, data_quality="", master_id="", status="",
                              title=data["title"], released=data["released"], country=data["country"], notes=data["notes"])
            db.update_release(release)
            release_data = db.get_release_by_id(id)
            
    return render_template('album_single.html', id=id, edit=edit, data=release_data, data2=release_artists, data3=label_data)


def profile():
    id = int(session["id"])
    releases = db.get_release_artists_and_release_by_artist_id(id)
    artist = db.get_artist_by_id(id)
    if request.method == "POST":
        data = dict(request.form)
        if ("name" in data and data["name"]):
            db.update_artist(id, data["name"],
                             data["email"], data["password1"])
            artist = db.get_artist_by_id(id)
        elif ("delete_id" in data and data["delete_id"]):
            db.delete_release(data["delete_id"])
            releases = db.get_release_artists_and_release_by_artist_id(
                id)
        elif ("data_quality" in data and data["data_quality"]):
            release = Release(id="", data_quality=data["data_quality"], master_id=id, status=data["status"],
                              title=data["title"], released=data["released"], country=data["country"], notes=data["notes"])
            
            # print(release_artist.release_id, release_artist.artist_id, release_artist.artist_name)
            db.add_release(release)
            last_id = db.get_previous_release_id()[0]
            release_artist = ReleaseArtist(release_id=last_id, artist_id=id, artist_name=artist[0],
                                           extra="", anv="", position="", join_string="", role="", tracks="")
            db.add_release_artist(release_artist)
            releases = db.get_release_artists_and_release_by_artist_id(id)
        return redirect(url_for('profile.html'))
    
    return render_template('profile.html', releases=releases, artist=artist)


def release_track(track_id):
    db = current_app.config["dbconfig"]
    rt, docs, artist_name = db.get_release_tracks(track_id)
    return render_template("release_track.html", release_track=rt, how_many_docs=docs, artist_name=artist_name)


def release_track_artist_page(release_id):
    db = current_app.config["dbconfig"]
    rta = db.get_release_track_artists(release_id)
    return render_template("release_track_artist.html", release_track_artist=rta)


def release(release_id):
    db = current_app.config["dbconfig"]
    release, genre = db.get_release(release_id)
    return render_template("release.html", release=release, release_genre=genre)



def login(email, password):
    conn = sqlite3.connect(DBFILE)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM `artist` WHERE `email` = ? AND `password` = ?",
        (email, password)
    )
    results = cursor.fetchall()
    conn.close()
    print(results)
    if len(results) > 0:
        session["id"] = results[0][0]
        session["name"] = results[0][1]
        session["email"] = email
        return redirect(url_for('profile.html'))
    else:
        return render_template('index.html')

def register(name, email, password):
    conn = sqlite3.connect(DBFILE)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM `artist` WHERE `email` = ?",
        (email,)
    )
    results = cursor.fetchall()
    if len(results) > 0:
        return render_template('index.html')
    else:
        cursor.execute(
            "UPDATE artist SET email=?, password=? WHERE name = ?",
            (email, password, name)
        )
        conn.commit()
        conn.close()
        return render_template('index.html')

def home_page():
    if request.method == "POST":
        data = dict(request.form)
        if("name" in data):
            return register(data["name"], data["email"], data["password"])
        else:
            return login(data["email"], data["password"])
    return render_template('index.html')
def logout():
    session.clear()
    return redirect(url_for('index.html'))

def search():
    search_type = "song"
    users = []
    if request.method == "POST":
        data = dict(request.form)
        if "album_name" in data:
            search_type = "album"
            users = search_release(data["album_name"])
        else:
            if data["artist_name"] != "":
                if data["song_name"] != "":
                    users = db.search_song(data["artist_name"], data["song_name"])
                else:
                    users = db.search_song_by_artist(data["artist_name"])
            elif data["song_name"] != "":
                users = db.search_song_by_name(data["song_name"])
    return render_template('search.html', data=users, search_type=search_type)

def search_release(search):
  conn = sqlite3.connect(DBFILE)
  cursor = conn.cursor()
  cursor.execute(
    "SELECT * FROM (SELECT * FROM `release` WHERE `title` LIKE ?) t1 INNER JOIN (select release_id,uri,title from release_video) t2 ON t2.release_id = t1.id GROUP BY t1.title ORDER BY (t1.released) DESC",
    ("%"+search+"%",)
  )
  results = cursor.fetchall()
  conn.close()
  return results

def label():
    id = request.args.get('id')
    label = db.get_label_by_id(id)
    if request.method == "POST":
        data = dict(request.form)
        if("name" in data ):
            db.update_label(Label(id, data["name"], data["contact"], data["profile"], data["parent"], data["data_quality"]))
            label = db.get_label_by_id(id)
            return redirect(url_for('label.html'))
        elif("delete_id" in data):
            db.delete_label(id)
            return redirect(url_for('index.html'))
    return render_template("label.html", label=label)

def create_label():
    if request.method == "POST":
        data = dict(request.form)
        if("name" in data and data["name"]):
            label = Label(id="", name=data["name"], contact_info=data["contact"], profile=data["profile"], parent_name=data["parent"], data_quality=data["data_quality"])
            db.add_label(label)
        return redirect(url_for('create_label.html'))
    return render_template("create_label.html")

def album_artist_edit():
    release_id = request.args.get('id')
    artist_id = request.args.get('artist')

    album_artist = db.get_release_artist_by_release_id_and_artist_id(
        release_id, artist_id)
    if request.method == "POST":
        data = dict(request.form)
        if ("position" in data):
            release_artist = ReleaseArtist(release_id=release_id, artist_id=artist_id, artist_name="",
                                           extra=data["extra"], anv=data["anv"], position=data["position"], join_string=data["join_string"], role=data["role"], tracks=data["tracks"])
            db.update_release_artist(release_artist)
            album_artist = db.get_release_artist_by_release_id_and_artist_id(
                release_id, artist_id)
    return render_template('album_artist_edit.html', data=album_artist)

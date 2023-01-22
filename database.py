
import sqlite3
from flask import g, Flask
from tables.release_track import ReleaseTrack
from tables.release_genre import ReleaseGenre
from tables.master_artist import MasterArtist
from tables.release_track_artist import ReleaseTrackArtist
from tables.release_artist import ReleaseArtist
from tables.release import Release
from tables.label import Label


class Database:
    def __init__(self, dbpath):
        self.db_path = "main.db"
        self.app = Flask(__name__)

    def get_db(self):
        self.db = getattr(g, '_database', None)
        if self.db is None:
            self.db = g._database = sqlite3.connect(self.db_path)
        return self.db

    def get_cursor(self):
        return self.get_db().cursor()

    # Release Track Queries
    def get_release_tracks(self, track_id):
        cursor = self.get_cursor()

        cursor.execute(
            "SELECT release_id FROM release_track WHERE track_id = ? LIMIT 1", (track_id,))
        release_id = cursor.fetchone()

        cursor.execute(
            "SELECT COUNT (DISTINCT sequence) FROM release_track WHERE release_id = ?", (release_id[0],))
        docs = cursor.fetchone()

        cursor.execute(
            "SELECT artist_name FROM release_track_artist WHERE track_id = ? LIMIT 1", (track_id,))
        artist_name = cursor.fetchone()

        cursor.execute(
            "SELECT * FROM release_track WHERE track_id = ?", (track_id,))
        return [ReleaseTrack(*row) for row in cursor.fetchall()], docs[0], artist_name[0]

    def get_release_track(self, release_id, sequence):
        cursor = self.get_cursor()
        cursor.execute(
            "SELECT * FROM release_track WHERE release_id = ? AND sequence = ?", (release_id, sequence))
        return ReleaseTrack(*cursor.fetchone())

    def add_release_track(self, release_track):
        cursor = self.get_cursor()
        cursor.execute("INSERT INTO release_track VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                       (release_track.id,
                        release_track.release_id,
                        release_track.sequence,
                        release_track.position,
                        release_track.parent,
                        release_track.title,
                        release_track.duration,
                        release_track.track_id))
        self.get_db().commit()

    def delete_release_track(self, release_track):
        cursor = self.get_cursor()
        cursor.execute("DELETE FROM release_track WHERE id = ?",
                       (release_track.id))
        self.get_db().commit()

    def update_release_track(self, release_track):
        cursor = self.get_cursor()
        cursor.execute("UPDATE release_track SET release_id = ?, sequence = ?, position = ?, parent = ?, title = ?, duration = ?, track_id = ? WHERE id = ?",
                       (release_track.release_id,
                        release_track.sequence,
                        release_track.position,
                        release_track.parent,
                        release_track.title,
                        release_track.duration,
                        release_track.track_id,
                        release_track.id))
        self.get_db().commit()

    # Master Artist Queries
    def get_master_artists(self, master_id):
        cursor = self.get_cursor()
        cursor.execute(
            "SELECT * FROM master_artist WHERE master_id = ?", (master_id))
        return [MasterArtist(*row) for row in cursor.fetchall()]

    def get_master_artist(self, master_id, artist_id):
        cursor = self.get_cursor()
        cursor.execute(
            "SELECT * FROM master_artist WHERE master_id = ? AND artist_id = ?", (master_id, artist_id))
        return MasterArtist(*cursor.fetchone())

    def add_master_artist(self, master_artist):
        cursor = self.get_cursor()
        cursor.execute("INSERT INTO master_artist VALUES (?, ?, ?, ?, ?)",
                       (master_artist.id,
                        master_artist.master_id,
                        master_artist.artist_id,
                        master_artist.artist_name,
                        master_artist.join_phrase))
        self.get_db().commit()

    def delete_master_artist(self, master_artist):
        cursor = self.get_cursor()
        cursor.execute("DELETE FROM master_artist WHERE id = ?",
                       (master_artist.id))
        self.get_db().commit()

    def update_master_artist(self, master_artist):
        cursor = self.get_cursor()
        cursor.execute("UPDATE master_artist SET master_id = ?, artist_id = ?, artist_name = ?, join_phrase = ? WHERE id = ?",
                       (master_artist.master_id,
                        master_artist.artist_id,
                        master_artist.artist_name,
                        master_artist.join_phrase,
                        master_artist.id))
        self.get_db().commit()

    # Release Genre Queries
    def get_release_genres(self, release_id):
        cursor = self.get_cursor()
        cursor.execute(
            "SELECT * FROM release_genre WHERE release_id = ?", (release_id))
        return [ReleaseGenre(*row) for row in cursor.fetchall()]

    def get_release_genre(self, release_id, genre_id):
        cursor = self.get_cursor()
        cursor.execute(
            "SELECT * FROM release_genre WHERE release_id = ? AND genre_id = ?", (release_id, genre_id))
        return ReleaseGenre(*cursor.fetchone())

    def add_release_genre(self, release_genre):
        cursor = self.get_cursor()
        cursor.execute("INSERT INTO release_genre VALUES (?, ?, ?, ?)",
                       (release_genre.id,
                        release_genre.release_id,
                        release_genre.genre_id,
                        release_genre.genre_name))
        self.get_db().commit()

    def delete_release_genre(self, release_genre):
        cursor = self.get_cursor()
        cursor.execute("DELETE FROM release_genre WHERE id = ?",
                       (release_genre.id))
        self.get_db().commit()

    def update_release_genre(self, release_genre):
        cursor = self.get_cursor()
        cursor.execute("UPDATE release_genre SET release_id = ?, genre_id = ?, genre_name = ? WHERE id = ?",
                       (release_genre.release_id,
                        release_genre.genre_id,
                        release_genre.genre_name,
                        release_genre.id))
        self.get_db().commit()

    # Release Track Artist Queries
    def get_release_track_artists(self, release_id):
        cursor = self.get_cursor()
        cursor.execute(
            "SELECT * FROM release_track_artist WHERE release_id = ?", (release_id,))
        return [ReleaseTrackArtist(*row) for row in cursor.fetchall()]

    def get_release_track_artist(self, release_id, sequence, artist_id):
        cursor = self.get_cursor()
        cursor.execute("SELECT * FROM release_track_artist WHERE release_id = ? AND sequence = ? AND artist_id = ?",
                       (release_id, sequence, artist_id))
        return ReleaseTrackArtist(*cursor.fetchone())

    def add_release_track_artist(self, release_track_artist):
        cursor = self.get_cursor()
        cursor.execute("INSERT INTO release_track_artist VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                       (release_track_artist.id,
                        release_track_artist.release_id,
                        release_track_artist.sequence,
                        release_track_artist.artist_id,
                        release_track_artist.artist_name,
                        release_track_artist.join_phrase,
                        release_track_artist.role,
                        release_track_artist.track_id))
        self.get_db().commit()

    def delete_release_track_artist(self, release_track_artist):
        cursor = self.get_cursor()
        cursor.execute(
            "DELETE FROM release_track_artist WHERE id = ?", (release_track_artist.id,))
        self.get_db().commit()

    def update_release_track_artist(self, release_track_artist):
        cursor = self.get_cursor()
        cursor.execute("UPDATE release_track_artist SET release_id = ?, sequence = ?, artist_id = ?, artist_name = ?, join_phrase = ?, role = ?, track_id = ? WHERE id = ?",
                       (release_track_artist.release_id,
                        release_track_artist.sequence,
                        release_track_artist.artist_id,
                        release_track_artist.artist_name,
                        release_track_artist.join_phrase,
                        release_track_artist.role,
                        release_track_artist.track_id,
                        release_track_artist.id))
        self.get_db().commit()

    # Release Queries
    def get_releases(self, release_id):
        cursor = self.get_cursor()
        cursor.execute("SELECT * FROM release WHERE id = ?", (release_id,))
        return cursor.fetchall()

    def get_release_by_id(self, release_id):
        cursor = self.get_cursor()
        cursor.execute("SELECT * FROM release WHERE id = ?", (release_id,))
        return cursor.fetchone()

    def get_release_label_release_artist(self, release_id):
        cursor = self.get_cursor()
        cursor.execute("SELECT * FROM (SELECT * FROM release WHERE id = ?) t1 INNER JOIN label t2 INNER JOIN release_label t4 INNER JOIN release_artist t3 ON t4.release_id = t1.id and t2.id = t4.label_id ", (release_id,))
        return cursor.fetchone()

    def get_release_artists_and_release_by_artist_id(self, artist_id):
        cursor = self.get_cursor()
        cursor.execute("SELECT * FROM (SELECT * FROM release_artist WHERE artist_id = ?) t1 INNER JOIN release t2 ON t1.release_id = t2.id where  master_id = artist_id GROUP BY t2.title ORDER BY (t2.released) DESC;", (artist_id,))
        return cursor.fetchall()

    def get_release(self, release_id, title, released):
        cursor = self.get_cursor()
        cursor.execute("SELECT * FROM release WHERE id = ? AND title = ? AND released = ?",
                       (release_id, title, released))
        return Release(*cursor.fetchone())

    def add_release(self, release):
        cursor = self.get_cursor()
        cursor.execute("INSERT INTO release (title, released, country, notes, data_quality, master_id, status) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (release.title,
                        release.released,
                        release.country,
                        release.notes,
                        release.data_quality,
                        release.master_id,
                        release.status))
        self.get_db().commit()

    def delete_release(self, id):
        cursor = self.get_cursor()
        cursor.execute("DELETE FROM release WHERE id = ?", (id,))
        self.get_db().commit()

    def update_release(self, release):
        cursor = self.get_cursor()
        cursor.execute("UPDATE release SET title = ?, released = ?, country= ?, notes = ? WHERE id = ?",
                       (release.title,
                        release.released,
                        release.country,
                        release.notes,
                        release.id))
        self.get_db().commit()

    # Label Queries
    def get_label(self, label_id):
        cursor = self.get_cursor()
        cursor.execute("SELECT * FROM label WHERE id = ?", (label_id))
        return [Label(*row) for row in cursor.fetchall()]

    def get_labels(self, label_id, name, contact_info):
        cursor = self.get_cursor()
        cursor.execute("SELECT * FROM label WHERE id = ? AND name = ? AND contact_info = ?",
                       (label_id, name, contact_info))
        return Label(*cursor.fetchone())

    def add_label(self, label):
        cursor = self.get_cursor()
        cursor.execute("INSERT INTO label(name, contact_info, profile, parent_name, data_quality) VALUES (?, ?, ?, ?, ?)",
                       (
                        label.name,
                        label.contact_info,
                        label.profile,
                        label.parent_name,
                        label.data_quality))
        self.get_db().commit()

    def delete_label(self, label_id):
        cursor = self.get_cursor()
        cursor.execute("DELETE FROM label WHERE id = ?", (label_id,))
        self.get_db().commit()

    def update_label(self, label):
        cursor = self.get_cursor()
        cursor.execute("UPDATE label SET name = ?, contact_info = ?, profile= ?, parent_name = ?, data_quality = ? WHERE id = ?",
                       (
                        label.name,
                        label.contact_info,
                        label.profile,
                        label.parent_name,
                        label.data_quality,
                        label.id))
        self.get_db().commit()

    def get_release_artists_by_release_id(self, release_id):
        cursor = self.get_cursor()
        cursor.execute(
            "SELECT * FROM release_artist WHERE release_id = ?", (release_id,))
        return cursor.fetchall()

    def get_artist_by_id(self, artist_id):
        cursor = self.get_cursor()
        cursor.execute(
            "SELECT name, email FROM artist WHERE id = ?", (artist_id,))
        return cursor.fetchone()

    def update_artist(self, artist_id, name, email, password):
        cursor = self.get_cursor()
        cursor.execute("UPDATE artist SET name = ?, email = ?, password = ? WHERE id = ?",
                       (name, email, password, artist_id))
        self.get_db().commit()

    def get_release_artist_by_release_id_and_artist_id(self, release_id, artist_id):
        cursor = self.get_cursor()
        cursor.execute(
            "SELECT * FROM release_artist WHERE release_id = ? AND artist_id = ?", (release_id, artist_id))
        return cursor.fetchone()

    def delete_release_artist(self, release_id, artist_id):
        cursor = self.get_cursor()
        cursor.execute(
            "DELETE FROM release_artist WHERE release_id = ? AND artist_id = ?", (release_id, artist_id))
        self.get_db().commit()

    def get_artist_id_by_name(self, name):
        cursor = self.get_cursor()
        cursor.execute("SELECT id FROM artist WHERE name = ?", (name,))
        return cursor.fetchone()

    def add_release_artist(self, release_artist):
        cursor = self.get_cursor()
        cursor.execute("INSERT INTO release_artist (release_id, artist_id, artist_name, extra, anv, position, join_string, role, tracks) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (release_artist.release_id, 
                       release_artist.artist_id, 
                       release_artist.artist_name, 
                       release_artist.extra, 
                       release_artist.anv, 
                       release_artist.position, 
                       release_artist.join_string, 
                       release_artist.role, 
                       release_artist.tracks))
        self.get_db().commit()

    def update_release_artist(self, release_artist):
        cursor = self.get_cursor()
        cursor.execute("UPDATE release_artist SET extra = ?, anv = ?, position = ?, join_string = ?, role = ?, tracks = ? WHERE release_id = ? AND artist_id = ?",
                       (
                       release_artist.extra, 
                       release_artist.anv, 
                       release_artist.position, 
                       release_artist.join_string, 
                       release_artist.role, 
                       release_artist.tracks,
                       release_artist.release_id,
                       release_artist.artist_id))
        self.get_db().commit()
        
    def get_label_by_id(self, label_id):
        cursor = self.get_cursor()
        cursor.execute("SELECT * FROM label WHERE id = ?", (label_id,))
        return cursor.fetchone()

    def get_previous_release_id(self):
        cursor = self.get_cursor()
        cursor.execute("SELECT seq FROM sqlite_sequence WHERE name= ?", ("release",)),
        return cursor.fetchone()

    def search_song(self, artist, song):
        cursor = self.get_cursor()
        cursor.execute(
            "SELECT * FROM (SELECT id,master_id FROM release) t1 INNER JOIN (select * from release_video where title LIKE ?) t2 ON t1.id = t2.release_id INNER JOIN (select id,name from artist where name LIKE ?) t3  ON t1.master_id = t3.id ORDER BY name",
            ("%"+song+"%", "%"+artist+"%")
        )
        return cursor.fetchall()
         

    def search_song_by_name(self, song):
        cursor = self.get_cursor()
        cursor.execute(

            "SELECT * FROM (SELECT id,master_id FROM release) t1 INNER JOIN (select * from release_video where title LIKE ?) t2 ON t1.id = t2.release_id INNER JOIN (select id,name from artist) t3 ON t1.master_id = t3.id ORDER BY name",

            ("%"+song+"%",)

        )
        return cursor.fetchall()

    def search_song_by_artist(self, artist):
        cursor = self.get_cursor()
        cursor.execute(
            "SELECT * FROM (SELECT id,master_id FROM release) t1 INNER JOIN (select * from release_video) t2 INNER JOIN (select id,name from artist where name LIKE ?) t3 ON t1.id = t2.release_id AND t1.master_id = t3.id ORDER BY name",
            ("%"+artist+"%",)
        )
        return cursor.fetchall()
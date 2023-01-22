
class ReleaseTrackArtist:
    def __init__(self, id, track_id, release_id=None, track_sequence=None, artist_id=None, artist_name=None, extra=None, anv=None, position=None, join_string=None, role=None, tracks=None):
        self.id = id
        self.track_id = track_id
        self.release_id = release_id
        self.track_sequence = track_sequence
        self.artist_id = artist_id
        self.artist_name = artist_name
        self.extra = extra
        self.anv = anv
        self.position = position
        self.join_string = join_string
        self.role = role
        self.tracks = tracks
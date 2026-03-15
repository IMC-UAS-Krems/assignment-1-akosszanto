from datetime import date
from .artists import Artist

class Track:
    def __init__(self, track_id: str, title: str, duration_seconds: int, genre: str):
        self.track_id = track_id
        self.title = title
        self.duration_seconds = duration_seconds
        self.genre = genre
    
    def duration_minutes(self) -> float:
        return self.duration_seconds / 60.0
    
class Song(Track):
    def __init__(self, track_id: str, title: str, duration_seconds: int, genre: str, artist: 'Artist'):
        Track.__init__(self, track_id, title, duration_seconds, genre)
        self.artist = artist

class Podcast(Track):
    def __init__(self, track_id: str, title: str, duration_seconds: int, genre: str, host: str, description: str = ""):
        Track.__init__(self, track_id, title, duration_seconds, genre)
        self.host = host
        self.description = description

class AudiobookTrack(Track):
    def __init__(self, track_id: str, title: str, duration_seconds: int, genre: str, author: str, narrator: str):
        Track.__init__(self, track_id, title, duration_seconds, genre)
        self.author = author
        self.narrator = narrator

class AlbumTrack(Song):
    def __init__(self, track_id: str, title: str, duration_seconds: int, genre: str, artist: 'Artist', track_number: int):
        Song.__init__(self, track_id, title, duration_seconds, genre, artist)
        self.track_number = track_number
        self.album = None

class SingleRelease(Song):
    def __init__(self, track_id: str, title: str, duration_seconds: int, genre: str, artist: 'Artist', release_date: date):
        Song.__init__(self, track_id, title, duration_seconds, genre, artist)
        self.release_date = release_date

class NarrativeEpisode(Podcast):
    def __init__(self, track_id: str, title: str, duration_seconds: int, genre: str, host: str, season: int, episode_number: int, description: str = ""):
        Podcast.__init__(self, track_id, title, duration_seconds, genre, host, description)
        self.season = season
        self.episode_number = episode_number
  
class InterviewEpisode(Podcast):
    def __init__(self, track_id: str, title: str, duration_seconds: int, genre: str, host: str, guest: str, description: str = ""):
        Podcast.__init__(self, track_id, title, duration_seconds, genre, host, description)
        self.guest = guest
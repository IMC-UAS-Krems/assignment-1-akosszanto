from .tracks import Track
from .albums import Album
from .artists import Artist
from .users import PremiumUser, User
from .playlists import Playlist
from .sessions import ListeningSession
import datetime


class StreamingPlatform:
    def __init__(self, name: str, catalogue: dict[str, Track] | None = None, users: dict[str, User] | None = None, artists: dict[str, Artist] | None = None, albums: dict[str, Album] | None = None, playlists: dict[str, Playlist] | None = None, _sessions: list[ListeningSession] | None = None):
        self.name = name
        if catalogue is None:
            self.catalogue = {}
        else:
          self.catalogue = catalogue
        if users is None:
            self.users = {}
        else:
          self.users = users
        if artists is None:
            self.artists = {}
        else:
          self.artists = artists
        if albums is None:
            self.albums = {}
        else:
          self.albums = albums
        if playlists is None:
            self.playlists = {}
        else:
          self.playlists = playlists
        if _sessions is None:
            self._sessions = []
        else:
          self._sessions = _sessions
    
    def add_track(self, track: Track) -> None:
      self.catalogue[track.track_id] = track
    
    def add_user(self, user: User) -> None:
      self.users[user.user_id] = user
    
    def add_artist(self, artist: Artist) -> None:
      self.artists[artist.artist_id] = artist
    
    def add_album(self, album: Album) -> None:
      self.albums[album.album_id] = album
    
    def add_playlist(self, playlist: Playlist) -> None:
      self.playlists[playlist.name] = playlist
    
    def record_session(self, session: ListeningSession) -> None:
      self._sessions.append(session)
    
    def get_track(self, track_id: str) -> Track | None:
      return self.catalogue.get(track_id)
    
    def get_user(self, user_id: str) -> User | None:
      return self.users.get(user_id)

    def get_artist(self, artist_id: str) -> Artist | None:
      return self.artists.get(artist_id)

    def get_album(self, album_id: str) -> Album | None:
      return self.albums.get(album_id)

    def all_users(self) -> list[User]:
      return list(self.users.values())
    
    def all_tracks(self) -> list[Track]:
      return list(self.catalogue.values())

    def total_listening_time_minutes(self, start: datetime.time, end: datetime.time) -> float:
        total_seconds = 0
        for session in self._sessions:
            session_time = session.timestamp.time()
            if start <= session_time <= end:
                total_seconds += session.duration_listened_seconds
        return total_seconds / 60.0
    
    def avg_unique_tracks_per_premium_user(self, days: int = 30) -> float:
      return 0.0


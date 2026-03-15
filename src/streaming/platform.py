from .tracks import Track
from .albums import Album
from .artists import Artist
from .users import User
from .playlists import Playlist
from .sessions import ListeningSession
import datetime


class StreamingPlatform:
    def __init__(self, name: str, catalogue: dict[str, Track], users: dict[str, User], artists: dict[str, Artist], albums: dict[str, Album], playlists: dict[str, Playlist], _sessions: list[ListeningSession]):
        self.name = name
        self.catalogue = catalogue
        self.users = users
        self.artists = artists
        self.albums = albums
        self.playlists = playlists
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

#Query Methods
    def total_listening_time_minutes(self, start: datetime.time, end: datetime.time) -> float:
        total_seconds = 0
        for session in self._sessions:
            session_time = session.timestamp.time()
            if start <= session_time <= end:
                total_seconds += session.duration_listened_seconds
        return total_seconds / 60.0
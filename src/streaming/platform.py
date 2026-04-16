from .tracks import Track
from .albums import Album
from .artists import Artist
from .users import PremiumUser, FamilyMember, User
from .playlists import CollaborativePlaylist, Playlist
from .sessions import ListeningSession
from datetime import datetime, timedelta

from streaming import tracks

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

    #Q1 
    """
    Compute the total listening time in minutes for all users between the specified start and end datetimes.
    Args:
      start (datetime): The start datetime for the time range.
      end (datetime): The end datetime for the time range.
    Returns:
      float: The total listening time in minutes for all users within the specified time range.
    """
    def total_listening_time_minutes(self, start: datetime, end: datetime) -> float:
        total_seconds = 0

        for session in self._sessions:
            if start <= session.timestamp <= end:
                total_seconds += session.duration_listened_seconds

        return total_seconds / 60.0
    
    #Q2
    """
    Compute the average number of unique tracks listened to per PremiumUser in the last `days`.
    Args:
      days (int): The number of days to look back from the current date.
    Returns:
      float: The average number of unique tracks listened to per PremiumUser in the specified time frame.
    """
    def avg_unique_tracks_per_premium_user(self, days: int = 30) -> float:
      premium_users = []
      cutoff = datetime.now() - timedelta(days=days)

      for user in self.all_users():
        if isinstance(user, PremiumUser):
          premium_users.append(user)
      if not premium_users:
        return 0.0
      
      tracks_by_user = {}

      for user in premium_users:
        tracks_by_user[user.user_id] = set()
      
      for session in self._sessions:
        if session.timestamp >= cutoff:
          user_id = session.user.user_id

          if user_id in tracks_by_user:
            tracks_by_user[user_id].add(session.track.track_id)

      total_unique_tracks = 0
      for tracks in tracks_by_user.values():
        how_many_for_this_user = len(tracks)
        total_unique_tracks += how_many_for_this_user

      return total_unique_tracks / len(premium_users)

    #Q3
    """
    Identify the track that has been listened to by the most distinct users across all listening sessions.
    Returns:
      Track | None: The track that has been listened to by the most distinct users, or None if there are no tracks.
    """
    def track_with_most_distinct_listeners(self) -> Track | None:
      listeners_by_track = {}

      for session in self._sessions:
        if session.track.track_id not in listeners_by_track:
          listeners_by_track[session.track.track_id] = set()
        listeners_by_track[session.track.track_id].add(session.user.user_id)

      if not listeners_by_track:
        return None

      best_track_id = None
      max_listeners = -1

      for track_id, listeners in listeners_by_track.items():
        if len(listeners) > max_listeners:
          max_listeners = len(listeners)
          best_track_id = track_id

      if best_track_id:
       return self.get_track(best_track_id)
      else:
        return None
      
    #Q4
    """
    Compute average session duration for each user type, ranked by duration. 
    Returns:
      list[tuple[str, float]]: A list of tuples where each tuple contains a user type.
    """
    def avg_session_duration_by_user_type(self) -> list[tuple[str, float]]:
      durations_by_type = {}
      for session in self._sessions:
          type_name = type(session.user).__name__

          if type_name not in durations_by_type:
              durations_by_type[type_name] = []
          durations_by_type[type_name].append(session.duration_listened_seconds)

      avg_durations = []
      for user_type, durations in durations_by_type.items():
        avg_val = sum(durations) / len(durations)
        avg_durations.append((user_type, avg_val))
      
      avg_durations.sort(key=lambda x: x[1], reverse=True)

      return avg_durations

    #Q5
    """
    Compute the total listening time for underage subscription users.
    Args:
      age_threshold (int): The age threshold for considering a user as underage.
    Returns:
      float: The total listening time in minutes for underage subscription users.
    """
    def total_listening_time_underage_sub_users_minutes(self, age_threshold: int = 18) -> float:
      total_seconds = 0

      for session in self._sessions:
        if isinstance(session.user, FamilyMember) and session.user.age < age_threshold:
          total_seconds += session.duration_listened_seconds

      return total_seconds / 60.0
    
    #Q6
    """
    Identify the top N artists based on total listening time across all sessions.
    Args:
      n (int): The number of top artists to return.
    Returns:
      list[tuple[Artist, float]]: A list of tuples where each tuple contains an Artist and their total listening time in minutes, sorted by listening time from highest to lowest.
    """
    def top_artists_by_listening_time(self, n: int = 5) -> list[tuple[Artist, float]]:
      listening_time_by_artist = {}

      for session in self._sessions:
        if isinstance(session.track, tracks.Song):
          artist = session.track.artist

          if artist not in listening_time_by_artist:
            listening_time_by_artist[artist] = 0
          listening_time_by_artist[artist] += session.duration_listened_seconds

      sorted_artists = sorted(listening_time_by_artist.items(), key=lambda x: x[1], reverse=True)

      return [(artist, time / 60.0) for artist, time in sorted_artists[:n]]
    
    #Q7
    """
    Determine the most popular genre for a given user based on their listening history.
    Args:
      user_id (str): The ID of the user
    Returns:
      tuple[str, float] | None: A tuple containing the most popular genre and the percentage of listening time.
    """
    def user_top_genre(self, user_id: str) -> tuple[str, float] | None:
      if self.get_user(user_id) is None:
        return None
      
      total_time = 0
      time_by_genre = {}
      for session in self._sessions:
        if session.user.user_id == user_id:
          genre = session.track.genre

          if genre not in time_by_genre:
            time_by_genre[genre] = 0
          time_by_genre[genre] += session.duration_listened_seconds
          total_time += session.duration_listened_seconds
      
      if not time_by_genre or total_time == 0:
        return None
      
      top_genre = max(time_by_genre, key=lambda x: time_by_genre[x])

      top_genre_time = time_by_genre[top_genre]
      percentage = (top_genre_time / total_time) * 100

      return (top_genre, percentage)
    
    #Q8
    """
    Identify collaborative playlists that feature tracks from more than a specified number of distinct artists.
    Args:
      threshold (int): The minimum number of distinct artists required for a playlist to be included in the result.
    Returns:
      list[CollaborativePlaylist]: A list of CollaborativePlaylist instances that meet the criteria.
    """
    def collaborative_playlists_with_many_artists(self, threshold: int = 3) -> list[CollaborativePlaylist]:
      proper_playlists = []

      for playlist in self.playlists.values():
        if isinstance(playlist, CollaborativePlaylist):
          artists_in_playlist = set()

          for track in playlist.tracks:
            if isinstance(track, tracks.Song):
              artists_in_playlist.add(track.artist)

          if len(artists_in_playlist) > threshold:
            proper_playlists.append(playlist)

      return proper_playlists
    
    #Q9
    """
    Compute the average number of tracks per playlist for each playlist type.
    Returns:
      dict[str, float]: A dictionary where the keys are playlist type names and the values are the average number of tracks per playlist for that type.
    """
    def avg_tracks_per_playlist_type(self) -> dict[str, float]:
      tracks_count_by_type = {
        "Playlist": [],
        "CollaborativePlaylist": []
      }

      for playlist in self.playlists.values():
        type_name = type(playlist).__name__

        if type_name in tracks_count_by_type:
          tracks_count_by_type[type_name].append(len(playlist.tracks))

      avg_tracks_by_type = {}
      for playlist_type, track_length in tracks_count_by_type.items():
        if track_length:
          avg_tracks_by_type[playlist_type] = sum(track_length) / len(track_length)
        else:
          avg_tracks_by_type[playlist_type] = 0.0
      
      return avg_tracks_by_type
    
    #Q10
    """
    Identify users who have completed entire albums.
    Returns:
      list[tuple[User, list[str]]]: A list of tuples containing users and the titles of albums they have completed.
    """
    def users_who_completed_albums(self) -> list[tuple[User, list[str]]]:
      user_listened_tracks = {}

      for session in self._sessions:
        u_id = session.user.user_id

        if u_id not in user_listened_tracks:
          user_listened_tracks[u_id] = set()

        user_listened_tracks[u_id].add(session.track.track_id)

      results = []

      for user in self.all_users():
        completed_albums = []

        listened_ids = user_listened_tracks.get(user.user_id, set())

        for album in self.albums.values():
          if not album.tracks:
            continue

          album_track_ids = {t.track_id for t in album.tracks}

          if album_track_ids.issubset(listened_ids):
            completed_albums.append(album.title)

        if completed_albums:
          results.append((user, completed_albums))

      return results  
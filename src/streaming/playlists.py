from .users import User
from .tracks import Track

class Playlist:
    def __init__(self, playlist_id: str, name: str, owner: User, tracks: list[Track]):
        self.playlist_id = playlist_id
        self.name = name
        self.owner = owner
        self.tracks = tracks
    
    def add_track(self, track: Track) -> None:
        self.tracks.append(track)
      
    def remove_track(self, track: Track) -> None:
        self.tracks.remove(track)
    
    def total_duration_seconds(self) -> int:
        return sum(track.duration_seconds for track in self.tracks)

class CollaborativePlaylist(Playlist):
    def __init__(self, playlist_id: str, name: str, owner: User, tracks: list[Track], contributors: list[User]):
        Playlist.__init__(self, playlist_id, name, owner, tracks)
        self.contributors = contributors
    
    def add_contributor(self, user: User) -> None:
        self.contributors.append(user)
    
    def remove_contributor(self, user: User) -> None:
        self.contributors.remove(user)
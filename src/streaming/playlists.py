from .users import User
from .tracks import Track

class Playlist:
    def __init__(self, playlist_id: str, name: str, owner: User):
        self.playlist_id = playlist_id
        self.name = name
        self.owner = owner
        self.tracks: list[Track] = []
    
    def add_track(self, track: Track) -> None:
        if track not in self.tracks:
            self.tracks.append(track)
      
    def remove_track(self, track_id: str) -> None:
        self.tracks = [t for t in self.tracks if t.track_id != track_id]
    
    def total_duration_seconds(self) -> int:
        return sum(track.duration_seconds for track in self.tracks)

class CollaborativePlaylist(Playlist):
    def __init__(self, playlist_id: str, name: str, owner: User):
        Playlist.__init__(self, playlist_id, name, owner)
        self.contributors: list[User] = [owner]
    
    def add_contributor(self, user: User) -> None:
        if user not in self.contributors:
            self.contributors.append(user)
    
    def remove_contributor(self, user: User) -> None:
        if user != self.owner and user in self.contributors:
            self.contributors.remove(user)
from .artists import Artist
from .tracks import AlbumTrack

class Album:
    def __init__(self, album_id: str, title: str, artist: Artist, release_year: int):
        self.album_id = album_id
        self.title = title
        self.artist = artist
        self.release_year = release_year
        self.tracks = list[AlbumTrack]()

    def add_track(self, track: AlbumTrack) -> None:
        self.tracks.append(track)
    
    def track_ids(self) -> set[str]:
        return {track.track_id for track in self.tracks}
    
    def duration_seconds(self) -> int:
        return sum(track.duration_seconds for track in self.tracks)
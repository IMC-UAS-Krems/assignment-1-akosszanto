"""
test_public.py
--------------
Public test suite template.

This file provides a minimal framework and examples to guide you in writing
comprehensive tests for your StreamingPlatform implementation. Each test class
corresponds to one of the 10 query methods (Q1-Q10).

You should:
1. Study the examples provided
2. Complete the stub tests (marked with TODO or pass statements)
3. Add additional test cases for edge cases and boundary conditions
4. Verify your implementation passes all tests

Run with:
    pytest tests/test_public.py -v
"""

from unittest import result

import pytest
from datetime import date, datetime, timedelta

from streaming.albums import Album
from streaming.artists import Artist
from streaming.sessions import ListeningSession
from streaming.platform import StreamingPlatform
from streaming.tracks import AlbumTrack, InterviewEpisode, SingleRelease
from streaming.users import FreeUser, PremiumUser, FamilyAccountUser, FamilyMember
from streaming.playlists import CollaborativePlaylist, Playlist
from tests.conftest import FIXED_NOW, RECENT, OLD


# ===========================================================================
# Q1 - Total cumulative listening time for a given period
# ===========================================================================

class TestTotalListeningTime:
    """Test the total_listening_time_minutes(start, end) method.
    
    This method should sum up all session durations that fall within
    the specified datetime window (inclusive on both ends).
    """

    def test_returns_float(self, platform: StreamingPlatform) -> None:
        """Verify the method returns a float."""
        start = RECENT - timedelta(hours=1)
        end = FIXED_NOW
        result = platform.total_listening_time_minutes(start, end)
        assert isinstance(result, float)

    def test_empty_window_returns_zero(self, platform: StreamingPlatform) -> None:
        """Test that a time window with no sessions returns 0.0."""
        far_future = FIXED_NOW + timedelta(days=365)
        result = platform.total_listening_time_minutes(
            far_future, far_future + timedelta(hours=1)
        )
        assert result == 0.0

    # TODO: Add a test that verifies the correct value for a known time period.
    #       Calculate the expected total based on the fixture data in conftest.py.
    def test_known_period_value(self, platform: StreamingPlatform) -> None:
        """Test that the method returns the correct total listening time for a known period."""
        alice = platform.get_user("u1")
        t1 = platform.get_track("t1")

        assert alice is not None
        assert t1 is not None

        s1 = ListeningSession(session_id="s1", user=alice, track=t1, timestamp=RECENT, duration_listened_seconds=180)
        s2 = ListeningSession(session_id="s2", user=alice, track=t1, timestamp=OLD, duration_listened_seconds=120)
        s3 = ListeningSession(session_id="s3", user=alice, track=t1, timestamp=RECENT + timedelta(minutes=30), duration_listened_seconds=240)

        for session in (s1, s2, s3):
            platform.record_session(session)
        
        start = RECENT - timedelta(minutes=15)
        end = RECENT + timedelta(minutes=45)

        result = platform.total_listening_time_minutes(start, end)
        expected_minutes = (180 + 240) / 60.0  # Only s1 and s3 should be counted

        assert result == expected_minutes, f"Expected {expected_minutes} minutes, but got {result} minutes."


# ===========================================================================
# Q2 - Average unique tracks per PremiumUser in the last N days
# ===========================================================================

class TestAvgUniqueTracksPremium:
    """Test the avg_unique_tracks_per_premium_user(days) method.
    
    This method should:
    - Count distinct tracks per PremiumUser in the last N days
    - Exclude FreeUser, FamilyAccountUser, and FamilyMember
    - Return 0.0 if there are no premium users
    """

    def test_returns_float(self, platform: StreamingPlatform) -> None:
        """Verify the method returns a float."""
        result = platform.avg_unique_tracks_per_premium_user(days=30)
        assert isinstance(result, float)

    def test_no_premium_users_returns_zero(self) -> None:
        """Test with a platform that has no premium users."""
        p = StreamingPlatform("EmptyPlatform")
        p.add_user(FreeUser("u99", "Nobody", age=25))
        assert p.avg_unique_tracks_per_premium_user() == 0.0

    # TODO: Add a test with the fixture platform that verifies the correct
    #       average for premium users. You'll need to count unique tracks
    #       per premium user and calculate the average.
    def test_correct_value(self, platform: StreamingPlatform) -> None:
        """Test that the method returns the correct average unique tracks for premium users."""
        alice = platform.get_user("u1")  # FreeUser
        bob = platform.get_user("u2")    # PremiumUser

        t1 = platform.get_track("t1")
        t2 = platform.get_track("t2")
        t3 = platform.get_track("t3")

        assert alice is not None
        assert bob is not None
        assert t1 is not None
        assert t2 is not None
        assert t3 is not None

        s1 = ListeningSession(session_id="s1", user=bob, track=t1, timestamp=RECENT, duration_listened_seconds=180)
        s2 = ListeningSession(session_id="s2", user=bob, track=t1, timestamp=RECENT, duration_listened_seconds=180)
        s3 = ListeningSession(session_id="s3", user=bob, track=t2, timestamp=RECENT, duration_listened_seconds=210)

        s4 = ListeningSession(session_id="s4", user=bob, track=t3, timestamp=OLD, duration_listened_seconds=195)
        s5 = ListeningSession(session_id="s5", user=alice, track=t3, timestamp=RECENT, duration_listened_seconds=195)

        for session in (s1, s2, s3, s4, s5):
            platform.record_session(session)

        result = platform.avg_unique_tracks_per_premium_user(days=30)
        expected_average = 2.0

        assert result == expected_average, f"Expected average of {expected_average}, but got {result}."


# ===========================================================================
# Q3 - Track with the most distinct listeners
# ===========================================================================

class TestTrackMostDistinctListeners:
    """Test the track_with_most_distinct_listeners() method.
    
    This method should:
    - Count the number of unique users who have listened to each track
    - Return the track with the highest count
    - Return None if the platform has no sessions
    """

    def test_empty_platform_returns_none(self) -> None:
        """Test that an empty platform returns None."""
        p = StreamingPlatform("Empty")
        assert p.track_with_most_distinct_listeners() is None

    # TODO: Add a test that verifies the correct track is returned.
    #       Count listeners per track from the fixture data.
    def test_correct_track(self, platform: StreamingPlatform) -> None:
        """Test that the method returns the track with the most distinct listeners."""
        alice = platform.get_user("u1")
        bob = platform.get_user("u2")

        t1 = platform.get_track("t1")
        t2 = platform.get_track("t2")

        assert alice is not None
        assert bob is not None
        assert t1 is not None
        assert t2 is not None

        s1 = ListeningSession(session_id="s1", user=alice, track=t1, timestamp=RECENT, duration_listened_seconds=180)
        s2 = ListeningSession(session_id="s2", user=bob, track=t1, timestamp=RECENT, duration_listened_seconds=180)

        s3 = ListeningSession(session_id="s3", user=bob, track=t2, timestamp=RECENT, duration_listened_seconds=210)
        s4 = ListeningSession(session_id="s4", user=bob, track=t2, timestamp=RECENT, duration_listened_seconds=210)

        for session in (s1, s2, s3, s4):
            platform.record_session(session)
        best_track = platform.track_with_most_distinct_listeners()

        assert best_track is not None, "Method returned None despite existing sessions."
        assert best_track.track_id == "t1", f"Expected track ID 't1', but got '{best_track.track_id}'."
        assert best_track.title == "Pixel Rain", "The returned track title is incorrect."


# ===========================================================================
# Q4 - Average session duration per user subtype, ranked
# ===========================================================================

class TestAvgSessionDurationByType:
    """Test the avg_session_duration_by_user_type() method.
    
    This method should:
    - Calculate average session duration (in seconds) for each user type
    - Return a list of (type_name, average_duration) tuples
    - Sort results from longest to shortest duration
    """

    def test_returns_list_of_tuples(self, platform: StreamingPlatform) -> None:
        """Verify the method returns a list of (str, float) tuples."""
        result = platform.avg_session_duration_by_user_type()
        assert isinstance(result, list)
        for item in result:
            assert isinstance(item, tuple) and len(item) == 2
            assert isinstance(item[0], str) and isinstance(item[1], float)

    def test_sorted_descending(self, platform: StreamingPlatform) -> None:
        """Verify results are sorted by duration (longest first)."""
        result = platform.avg_session_duration_by_user_type()
        durations = [r[1] for r in result]
        assert durations == sorted(durations, reverse=True)

    # TODO: Add tests to verify all user types are present and have correct averages.
    def test_all_user_types_present(self, platform: StreamingPlatform) -> None:
        """Test that all user types are included in the results with correct average durations."""
        alice = platform.get_user("u1")  # FreeUser
        bob = platform.get_user("u2")    # PremiumUser
        t1 = platform.get_track("t1")

        assert alice is not None
        assert bob is not None
        assert t1 is not None

        tom = FamilyAccountUser(user_id="u3", name="Tom", age=40)
        cruise = FamilyMember(user_id="u4", name="Cruise", age=12, parent=tom)

        platform.add_user(tom)
        platform.add_user(cruise)

        s1 = ListeningSession(session_id="s1", user=alice, track=t1, timestamp=RECENT, duration_listened_seconds=180)
        s2 = ListeningSession(session_id="s2", user=bob, track=t1, timestamp=RECENT, duration_listened_seconds=210)
        s3 = ListeningSession(session_id="s3", user=bob, track=t1, timestamp=RECENT, duration_listened_seconds=240)
        s4 = ListeningSession(session_id="s4", user=tom, track=t1, timestamp=RECENT, duration_listened_seconds=300)
        s5 = ListeningSession(session_id="s5", user=cruise, track=t1, timestamp=RECENT, duration_listened_seconds=150)

        for session in (s1, s2, s3, s4, s5):
            platform.record_session(session)

        result = platform.avg_session_duration_by_user_type()
        assert len(result) == 4, f"Expected 4 user types, but got {len(result)}."

        result_dict = dict(result)

        assert result_dict["FreeUser"] == 180.0, f"Expected FreeUser average of 180.0, but got {result_dict['FreeUser']}."
        assert result_dict["PremiumUser"] == 225.0, f"Expected PremiumUser average of 225.0, but got {result_dict['PremiumUser']}."
        assert result_dict["FamilyAccountUser"] == 300.0, f"Expected FamilyAccountUser average of 300.0, but got {result_dict['FamilyAccountUser']}."
        assert result_dict["FamilyMember"] == 150.0, f"Expected FamilyMember average of 150.0, but got {result_dict['FamilyMember']}."

        expected_order = ["FamilyAccountUser", "PremiumUser", "FreeUser", "FamilyMember"]
        actual_order = [r[0] for r in result]

        assert actual_order == expected_order, f"Expected order {expected_order}, but got {actual_order}."


# ===========================================================================
# Q5 - Total listening time for underage sub-users
# ===========================================================================

class TestUnderageSubUserListening:
    """Test the total_listening_time_underage_sub_users_minutes(age_threshold) method.
    
    This method should:
    - Count only sessions for FamilyMember users under the age threshold
    - Convert to minutes
    - Return 0.0 if no underage users or their sessions exist
    """

    def test_returns_float(self, platform: StreamingPlatform) -> None:
        """Verify the method returns a float."""
        result = platform.total_listening_time_underage_sub_users_minutes()
        assert isinstance(result, float)

    def test_no_family_users(self) -> None:
        """Test a platform with no family accounts."""
        p = StreamingPlatform("NoFamily")
        p.add_user(FreeUser("u1", "Solo", age=20))
        assert p.total_listening_time_underage_sub_users_minutes() == 0.0

    # TODO: Add tests for correct values with default and custom thresholds.
    def test_correct_value_default_threshold(self, platform: StreamingPlatform) -> None:
        """Test that the method returns the correct total listening time for underage sub-users with default threshold."""
        t1 = platform.get_track("t1")
        assert t1 is not None

        parent = FamilyAccountUser(user_id="p1", name="Parent", age=40)
        teen_user = FamilyMember(user_id="u3", name="Teen", age=17, parent=parent) # -> should be counted
        adult_user = FamilyMember(user_id="u4", name="Adult", age=25, parent=parent)# -> should not be counted
        solo_teen = FreeUser(user_id="u5", name="SoloTeen", age=16) # -> should not be counted because not a FamilyMember

        for user in (parent, teen_user, adult_user, solo_teen):
            platform.add_user(user)
        
        s1 = ListeningSession(session_id="s1", user=teen_user, track=t1, timestamp=RECENT, duration_listened_seconds=180)
        s2 = ListeningSession(session_id="s2", user=adult_user, track=t1, timestamp=RECENT, duration_listened_seconds=210)
        s3 = ListeningSession(session_id="s3", user=solo_teen, track=t1, timestamp=RECENT, duration_listened_seconds=240)

        for session in (s1, s2, s3):
            platform.record_session(session)
        
        result = platform.total_listening_time_underage_sub_users_minutes()
        expected_minutes = 180 / 60.0

        assert result == expected_minutes, f"Expected {expected_minutes} minutes, but got {result} minutes."

    def test_custom_threshold(self, platform: StreamingPlatform) -> None:
        """Test that the method returns the correct total listening time for underage sub-users with a custom age threshold."""
        t1 = platform.get_track("t1")
        assert t1 is not None

        parent = FamilyAccountUser(user_id="p1", name="Parent", age=40)
        child_user = FamilyMember(user_id="u3", name="Child", age=12, parent=parent) # -> should be counted with threshold 13
        teen_user = FamilyMember(user_id="u4", name="Teen", age=17, parent=parent) # -> should not be counted with threshold 13

        for user in (parent, child_user, teen_user):
            platform.add_user(user)
        
        s1 = ListeningSession(session_id="s1", user=child_user, track=t1, timestamp=RECENT, duration_listened_seconds=180)
        s2 = ListeningSession(session_id="s2", user=teen_user, track=t1, timestamp=RECENT, duration_listened_seconds=210)

        for session in (s1, s2):
            platform.record_session(session)
        
        result = platform.total_listening_time_underage_sub_users_minutes(age_threshold=13)
        expected_minutes = 180 / 60.0

        assert result == expected_minutes, f"Expected {expected_minutes} minutes, but got {result} minutes."


# ===========================================================================
# Q6 - Top N artists by total listening time
# ===========================================================================

class TestTopArtistsByListeningTime:
    """Test the top_artists_by_listening_time(n) method.
    
    This method should:
    - Rank artists by total cumulative listening time (minutes)
    - Only count Song tracks (exclude Podcast and AudiobookTrack)
    - Return a list of (Artist, minutes) tuples
    - Sort from highest to lowest listening time
    """

    def test_returns_list_of_tuples(self, platform: StreamingPlatform) -> None:
        """Verify the method returns a list of (Artist, float) tuples."""
        from streaming.artists import Artist
        result = platform.top_artists_by_listening_time(n=3)
        assert isinstance(result, list)
        for item in result:
            assert isinstance(item, tuple) and len(item) == 2
            assert isinstance(item[0], Artist) and isinstance(item[1], float)

    def test_sorted_descending(self, platform: StreamingPlatform) -> None:
        """Verify results are sorted by listening time (highest first)."""
        result = platform.top_artists_by_listening_time(n=5)
        minutes = [r[1] for r in result]
        assert minutes == sorted(minutes, reverse=True)

    def test_respects_n_parameter(self, platform: StreamingPlatform) -> None:
        """Verify only the top N artists are returned."""
        result = platform.top_artists_by_listening_time(n=2)
        assert len(result) <= 2

    # TODO: Add a test that verifies the correct artists and values.
    def test_top_artist(self, platform: StreamingPlatform) -> None:
        """Test that the method returns the correct top artists by listening time."""
        alice = platform.get_user("u1") # FreeUser
        bob = platform.get_user("u2")   # PremiumUser
        t1 = platform.get_track("t1")

        assert alice is not None
        assert bob is not None
        assert t1 is not None

        imaginde_d = Artist("a2", "Imagine Dragons", "Pop")
        new_song = SingleRelease(track_id="t4", title="Enemy", duration_seconds=180, genre="Pop", artist=imaginde_d, release_date=date(2021, 10, 28))
        platform.add_artist(imaginde_d)
        platform.add_track(new_song)

        p1 = InterviewEpisode(track_id="t5", title="Podcast", duration_seconds=3600, genre="Tech", host="A", guest="B")
        platform.add_track(p1)

        s1 = ListeningSession(session_id="s1", user=alice, track=new_song, timestamp=RECENT, duration_listened_seconds=360)
        s2 = ListeningSession(session_id="s2", user=bob, track=t1, timestamp=RECENT, duration_listened_seconds=180)
        s3 = ListeningSession(session_id="s3", user=bob, track=p1, timestamp=RECENT, duration_listened_seconds=3600)

        for session in (s1, s2, s3):
            platform.record_session(session)
        
        result = platform.top_artists_by_listening_time(n=2)

        assert len(result) == 2, f"Expected 2 artists, but got {len(result)}."

        artist1, mins1 = result[0]
        artist2, mins2 = result[1]

        assert artist1.artist_id == "a2", f"Expected top artist ID a2, but got '{artist1.artist_id}'."
        assert mins1 == 6.0, f"Expected top artist listening time of 6.0 minutes, but got {mins1} minutes."

        assert artist2.artist_id == "a1", f"Expected second artist ID a1, but got '{artist2.artist_id}'."
        assert mins2 == 3.0, f"Expected second artist listening time of 3.0 minutes, but got {mins2} minutes."

# ===========================================================================
# Q7 - User's top genre and percentage
# ===========================================================================

class TestUserTopGenre:
    """Test the user_top_genre(user_id) method.
    
    This method should:
    - Find the genre with the most listening time for a user
    - Return (genre_name, percentage_of_total_time)
    - Return None if user doesn't exist or has no sessions
    """

    def test_returns_tuple_or_none(self, platform: StreamingPlatform) -> None:
        """Verify the method returns a tuple or None."""
        result = platform.user_top_genre("u1")
        if result is not None:
            assert isinstance(result, tuple) and len(result) == 2
            assert isinstance(result[0], str) and isinstance(result[1], float)

    def test_nonexistent_user_returns_none(self, platform: StreamingPlatform) -> None:
        """Test that a nonexistent user ID returns None."""
        assert platform.user_top_genre("does_not_exist") is None

    def test_percentage_in_valid_range(self, platform: StreamingPlatform) -> None:
        """Verify percentage is between 0 and 100."""
        for user in platform.all_users():
            result = platform.user_top_genre(user.user_id)
            if result is not None:
                _, pct = result
                assert 0.0 <= pct <= 100.0

    # TODO: Add a test that verifies the correct genre and percentage for a known user.
    def test_correct_top_genre(self, platform: StreamingPlatform) -> None:
        """Test that the method returns the correct top genre and percentage for a known user."""
        alice = platform.get_user("u1")
        assert alice is not None

        artist_pop = Artist("ap", "Popstar", "Pop")
        artist_rock = Artist("ar", "Rockstar", "Rock")
        artist_jazz = Artist("aj", "Jazzstar", "Jazz")

        t_pop = AlbumTrack("tp", "Pop Song", 100, "Pop", artist_pop, 1)
        t_rock = AlbumTrack("tr", "Rock Song", 100, "Rock", artist_rock, 1)
        t_jazz = AlbumTrack("tj", "Jazz Song", 100, "Jazz", artist_jazz, 1)

        for track in (t_pop, t_rock, t_jazz):
            platform.add_track(track)
        
        s1 = ListeningSession(session_id="s1", user=alice, track=t_pop, timestamp=RECENT, duration_listened_seconds=200)
        s2 = ListeningSession(session_id="s2", user=alice, track=t_rock, timestamp=RECENT, duration_listened_seconds=100)
        s3 = ListeningSession(session_id="s3", user=alice, track=t_jazz, timestamp=RECENT, duration_listened_seconds=50)
        s4 = ListeningSession(session_id="s4", user=alice, track=t_pop, timestamp=RECENT, duration_listened_seconds=100)
        s5 = ListeningSession(session_id="s5", user=alice, track=t_rock, timestamp=RECENT, duration_listened_seconds=100)

        for session in (s1, s2, s3, s4, s5):
            platform.record_session(session)
        
        result = platform.user_top_genre("u1")

        assert result is not None, "Method returned None, but user has sessions."

        genre, percentage = result

        assert genre == "Pop", f"Expected top genre 'Pop', but got '{genre}'."
        expected_percentage = (200 + 100) / (200 + 100 + 50 + 100 + 100) * 100
        assert percentage == expected_percentage, f"Expected percentage {expected_percentage}%, but got {percentage}%."

# ===========================================================================
# Q8 - CollaborativePlaylists with more than threshold distinct artists
# ===========================================================================

class TestCollaborativePlaylistsManyArtists:
    """Test the collaborative_playlists_with_many_artists(threshold) method.
    
    This method should:
    - Return all CollaborativePlaylist instances with >threshold distinct artists
    - Only count Song tracks (exclude Podcast and AudiobookTrack)
    - Return playlists in registration order
    """

    def test_returns_list_of_collaborative_playlists(
        self, platform: StreamingPlatform
    ) -> None:
        """Verify the method returns a list of CollaborativePlaylist objects."""
        result = platform.collaborative_playlists_with_many_artists()
        assert isinstance(result, list)
        for item in result:
            assert isinstance(item, CollaborativePlaylist)

    def test_higher_threshold_returns_empty(
        self, platform: StreamingPlatform
    ) -> None:
        """Test that a high threshold returns an empty list."""
        result = platform.collaborative_playlists_with_many_artists(threshold=100)
        assert result == []

    # TODO: Add tests that verify the correct playlists are returned with
    #       different threshold values.
    def test_default_threshold(self, platform: StreamingPlatform) -> None:
        """Test that the method returns the correct playlists with the default threshold."""
        alice = platform.get_user("u1")
        assert alice is not None

        cp1 = CollaborativePlaylist("cp1", "Collab", alice)
        platform.add_playlist(cp1)

        for i in range(4):
            a = Artist(f"temp_a{i}", f"Artist {i}", "Pop")
            t = SingleRelease(f"temp_t{i}", f"Song {i}", 180, "Pop", a, date(2023, 1, 1))
            
            platform.add_artist(a)
            platform.add_track(t)
            cp1.add_track(t)  
        
        result_default = platform.collaborative_playlists_with_many_artists()
        assert len(result_default) == 1, "Expected 1 playlist for default threshold."

        result_custom = platform.collaborative_playlists_with_many_artists(threshold=4)
        assert len(result_custom) == 0, "Expected 0 playlists for threshold=4."


# ===========================================================================
# Q9 - Average tracks per playlist type
# ===========================================================================

class TestAvgTracksPerPlaylistType:
    """Test the avg_tracks_per_playlist_type() method.
    
    This method should:
    - Calculate average track count for standard Playlist instances
    - Calculate average track count for CollaborativePlaylist instances
    - Return a dict with keys "Playlist" and "CollaborativePlaylist"
    - Return 0.0 for types with no instances
    """

    def test_returns_dict_with_both_keys(
        self, platform: StreamingPlatform
    ) -> None:
        """Verify the method returns a dict with both playlist types."""
        result = platform.avg_tracks_per_playlist_type()
        assert isinstance(result, dict)
        assert "Playlist" in result
        assert "CollaborativePlaylist" in result

    # TODO: Add tests that verify the correct averages for each playlist type.
    def test_standard_playlist_average(self, platform: StreamingPlatform) -> None:
        """Test that the method returns the correct average tracks for standard playlists."""
        alice = platform.get_user("u1")
        t1 = platform.get_track("t1")
        t2 = platform.get_track("t2")
        t3 = platform.get_track("t3")

        assert alice is not None
        assert t1 is not None
        assert t2 is not None
        assert t3 is not None

        p1 = Playlist("p1", "List 1", alice)
        p1.add_track(t1)

        p2 = Playlist("p2", "List 2", alice)
        p2.add_track(t1)
        p2.add_track(t2)
        p2.add_track(t3)

        platform.add_playlist(p1)
        platform.add_playlist(p2)

        result = platform.avg_tracks_per_playlist_type()
        assert result["Playlist"] == 2.0, f"Expected 2.0 for Playlist, got {result['Playlist']}."
        assert result["CollaborativePlaylist"] == 0.0, f"Expected 0.0 for CollaborativePlaylist, got {result['CollaborativePlaylist']}."


    def test_collaborative_playlist_average(self, platform: StreamingPlatform) -> None:
        """Test that the method returns the corrct average tracks for collaborative playlists."""
        alice = platform.get_user("u1")
        t1 = platform.get_track("t1")
        t2 = platform.get_track("t2")
        
        assert alice is not None
        assert t1 is not None
        assert t2 is not None

        cp1 = CollaborativePlaylist("cp1", "Collab 1", alice)

        cp2 = CollaborativePlaylist("cp2", "Collab 2", alice)
        cp2.add_track(t1)
        cp2.add_track(t2)

        platform.add_playlist(cp1)
        platform.add_playlist(cp2)

        result = platform.avg_tracks_per_playlist_type()

        assert result["CollaborativePlaylist"] == 1.0, f"Expected 1.0 for CollaborativePlaylist, got {result['CollaborativePlaylist']}."
        assert result["Playlist"] == 0.0, "Expected 0.0 for missing Playlist."


# ===========================================================================
# Q10 - Users who completed at least one full album
# ===========================================================================

class TestUsersWhoCompletedAlbums:
    """Test the users_who_completed_albums() method.
    
    This method should:
    - Return users who have listened to every track on at least one album
    - Return (User, [album_titles]) tuples
    - Include all completed albums for each user
    - Ignore albums with no tracks
    """

    def test_returns_list_of_tuples(self, platform: StreamingPlatform) -> None:
        """Verify the method returns a list of (User, list) tuples."""
        from streaming.users import User
        result = platform.users_who_completed_albums()
        assert isinstance(result, list)
        for item in result:
            assert isinstance(item, tuple) and len(item) == 2
            assert isinstance(item[0], User) and isinstance(item[1], list)

    def test_completed_album_titles_are_strings(
        self, platform: StreamingPlatform
    ) -> None:
        """Verify all completed album titles are strings."""
        result = platform.users_who_completed_albums()
        for _, titles in result:
            assert all(isinstance(t, str) for t in titles)

    # TODO: Add tests that verify the correct users and albums are identified.
    def test_correct_users_identified(self, platform: StreamingPlatform) -> None:
        """Test that the method correctly identifies users who completed albums and the album titles."""
        alice= platform.get_user("u1")
        bob = platform.get_user("u2")

        tracks = []

        for i in (1, 2, 3):
            t = platform.get_track(f"t{i}")
            assert t is not None, f"Track t{i} not found in platform."
            tracks.append(t)

        assert alice and bob, "Users u1 and u2 should exist in the platform."

        for i, t in enumerate(tracks):
            platform.record_session(ListeningSession(f"sa{i}", alice, t, RECENT, 100))
            
        for i, t in enumerate(tracks[:2]):
            platform.record_session(ListeningSession(f"sb{i}", bob, t, RECENT, 100))

        result = platform.users_who_completed_albums()

        assert len(result) == 1, f"Expected 1 user to have completed an album, but got {len(result)}."
        assert result[0][0].user_id == "u1", f"Expected user ID u1, but got '{result[0][0].user_id}'."
        assert "Digital Dreams" in result[0][1], "Expected Digital Dreams to be in the completed albums list."

    def test_correct_album_titles(self, platform: StreamingPlatform) -> None:
        """Test that the method correctly identifies all completed albums for a user."""
        bob = platform.get_user("u2")
        pixels = platform.get_artist("a1")

        tracks = []

        for i in (1, 2, 3):
            t = platform.get_track(f"t{i}")
            assert t is not None, f"Track t{i} not found in platform."
            tracks.append(t)

        assert bob and pixels, "User u2 and Artist a1 should exist in the platform."

        mini = Album("alb2", "Mini EP", pixels, 2024)
        t4 = AlbumTrack("t4", "Bonus", 100, "Pop", pixels, track_number=1, album=mini)
        mini.add_track(t4)
        
        platform.add_track(t4)
        platform.add_album(mini)
        platform.add_album(Album("alb3", "Empty", pixels, 2024))

        for i, t in enumerate(tracks + [t4]):
            platform.record_session(ListeningSession(f"s{i}", bob, t, RECENT, 100))

        res = []
        for item in platform.users_who_completed_albums():
            if item[0].user_id == "u2":
                res.append(item)

        assert len(res) == 1 and len(res[0][1]) == 2, f"Expected user u2 to have completed 2 albums, but got {len(res[0][1])}."
        assert {"Digital Dreams", "Mini EP"}.issubset(res[0][1]), "Expected both 'Digital Dreams' and 'Mini EP' to be in the completed albums list."
"""A video player class."""

from .video_library import VideoLibrary
from .video import Video
from .video_playlist import Playlist
import random


class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        self.currently_playing = Video("","",[])
        self.paused = False
        self.playlists = {}

    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        """Returns all videos."""
        video_list = self._video_library.get_all_videos()
        output_list = []
        for v in video_list:
            output_string = v.title + " (" + v.video_id + ") ["
            first_tag = True
            for i in v.tags:
                if first_tag:
                    first_tag = False
                else:
                    output_string = output_string + " "
                output_string = output_string + i
            output_string = output_string + "]"
            if v.get_flagged():
                flag_reason = v.get_flag_reason()
                output_string = output_string + " - FLAGGED (reason: "+flag_reason+")"
            output_list.append(output_string)
        output_list = sorted(output_list)
        print("Here's a list of all available videos:")
        for l in output_list:
            print("  " + l)

    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """
        try:
            selected_video = self._video_library.get_video(video_id)
            if selected_video.get_flagged():
                flag_reason = selected_video.get_flag_reason()
                print("Cannot play video: Video is currently flagged (reason: "+flag_reason+")")
            else:
                selected_video_title = selected_video.title
                if len(self.currently_playing.title) != 0:
                    video_playing = self.currently_playing.title
                    self.stop_video()
                    print("Playing video: " + selected_video_title)
                else:
                    print("Playing video: " + selected_video_title)
                self.currently_playing = selected_video
        except AttributeError:
            print("Cannot play video: Video does not exist")

    def stop_video(self):
        """Stops the current video."""
        if len(self.currently_playing.title) != 0:
            video_playing = self.currently_playing.title
            print("Stopping video: " + self.currently_playing.title)
            self.currently_playing =  Video("","",[])
            self.paused = False
        else:
            print("Cannot stop video: No video is currently playing")

    def play_random_video(self):
        """Plays a random video from the video library."""
        try:
            video_list = self._video_library.get_all_videos()
            video_list_copy = self._video_library.get_all_videos()
            for v in video_list_copy:
                if v.get_flagged():
                    video_list.remove(v)
            if len(video_list)>0:
                selected_video = random.choice(video_list)
                selected_video_title = selected_video.title
                if selected_video.get_flagged():
                    flag_reason = selected_video.get_flag_reason()
                    print("Cannot play video: Video is currently flagged (reason: "+flag_reason+")")
                else:
                    if len(self.currently_playing.title) != 0:
                        self.stop_video()
                        video_playing = self.currently_playing.title
                        print("Playing video: " + selected_video_title)
                    else:
                        print("Playing video: " + selected_video_title)
                self.currently_playing = selected_video
            else:
                print("No videos available")
        except AttributeError:
            print("No videos available")

    def pause_video(self):
        """Pauses the current video."""
        if len(self.currently_playing.title) != 0:
            video_playing = self.currently_playing.title
            if self.paused:
                print("Video already paused: " + self.currently_playing.title)
            else:
                print("Pausing video: " + self.currently_playing.title)
                self.paused = True
        else:
            print("Cannot pause video: No video is currently playing")

    def continue_video(self):
        """Resumes playing the current video."""
        if len(self.currently_playing.title) != 0:
            video_playing = self.currently_playing.title
            if self.paused:
                print("Continuing video: " + self.currently_playing.title)
                self.paused = False
            else:
                print("Cannot continue video: Video is not paused")
        else:
            print("Cannot continue video: No video is currently playing")

    def show_playing(self):
        """Displays video currently playing."""
        if len(self.currently_playing.title) != 0:
            v = self.currently_playing
            output_string = v.title + " (" + v.video_id + ") ["
            first_tag = True
            for i in v.tags:
                if first_tag:
                    first_tag = False
                else:
                    output_string = output_string + " "
                output_string = output_string + i
            output_string = output_string + "]"
            if self.paused:
                output_string = output_string + " - PAUSED"
            print("Currently playing: " + output_string)
        else:
            print("No video is currently playing")

    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        try:
            if len(playlist_name.split())>1:
                print("Cannot create playlist: Invalid name - contains whitespace")
            else:
                unique = True
                if len(list(self.playlists.values()))>0:
                    for p in self.playlists.values():
                        if p.title.lower() == playlist_name.lower():
                            unique = False
                if unique:
                    new_playlist = Playlist(playlist_name)
                    self.playlists[new_playlist.title]=new_playlist
                    print("Successfully created new playlist: " + playlist_name)
                else:
                    print("Cannot create playlist: A playlist with the same name already exists")
        except:
            print("Cannot create playlist: A playlist with the same name already exists")

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """
        try:
            selected_playlist = Playlist("")
            if len(list(self.playlists.values()))>0:
                for p in self.playlists.values():
                    if p.title.lower() == playlist_name.lower():
                        selected_playlist = p
                if len(selected_playlist.title)>0:
                    selected_video = self._video_library.get_video(video_id)
                    if selected_video == None:
                        print("Cannot add video to " + playlist_name + ": Video does not exist")
                    else:
                        if selected_video.get_flagged():
                            flag_reason = selected_video.get_flag_reason()
                            print("Cannot add video to " + playlist_name + ": Video is currently flagged (reason: "+flag_reason+")")
                        else:
                            selected_video_title = selected_video.title
                            new_video = True
                            for v in selected_playlist.get_videos():
                                if v.video_id == selected_video.video_id:
                                    new_video = False
                            if new_video:
                                selected_playlist.add_video(selected_video)
                                print("Added video to " + playlist_name + ": " + selected_video_title)
                            else:
                                print("Cannot add video to " + playlist_name + ": Video already added")
                else:
                    print("Cannot add video to " + playlist_name + ": Playlist does not exist")    
            else:
                print("Cannot add video to " + playlist_name + ": Playlist does not exist")
        except:
            print("Error")

    def show_all_playlists(self):
        """Display all playlists."""
        playlist_list = self.playlists.values()
        if len(playlist_list)>0:
            output_list = []
            for p in playlist_list:
                output_list.append(p.title)
            output_list = sorted(output_list)
            print("Showing all playlists:")
            for l in output_list:
                print("  " + l)
        else:
            print("No playlists exist yet")

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        playlist_list = self.playlists.values()
        selected_playlist = Playlist("")
        if len(list(playlist_list))>0:
            for p in playlist_list:
                if p.title.lower() == playlist_name.lower():
                    selected_playlist = p
        if len(selected_playlist.title)>0:
            print("Showing playlist: "+playlist_name)
            video_list = selected_playlist.get_videos()
            if len(video_list)>0:
                for v in video_list:
                    output_string = v.title + " (" + v.video_id + ") ["
                    first_tag = True
                    for i in v.tags:
                        if first_tag:
                            first_tag = False
                        else:
                            output_string = output_string + " "
                        output_string = output_string + i
                    output_string = output_string + "]"
                    if v.get_flagged():
                        flag_reason = v.get_flag_reason()
                        output_string = output_string + " - FLAGGED (reason: "+flag_reason+")"
                    print(output_string)
            else:
                print("No videos here yet")
        else:
            print("Cannot show playlist "+playlist_name+": Playlist does not exist")

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        playlist_list = self.playlists.values()
        selected_playlist = Playlist("")
        if len(list(playlist_list))>0:
                for p in playlist_list:
                    if p.title.lower() == playlist_name.lower():
                        selected_playlist = p
        if len(selected_playlist.title)==0:
            print("Cannot remove video from "+playlist_name+": Playlist does not exist")
        else:
            selected_video = self._video_library.get_video(video_id)
            if selected_video == None:
                print("Cannot remove video from " + playlist_name + ": Video does not exist")
            else:
                selected_video_title = selected_video.title
                video_in_playlist = False
                for v in selected_playlist.get_videos():
                    if v.video_id == selected_video.video_id:
                        video_in_playlist = True
                if video_in_playlist:
                    selected_playlist.remove_video(selected_video)
                    print("Removed video from " + playlist_name + ": " + selected_video_title)
                else:
                    print("Cannot remove video from " + playlist_name + ": Video is not in playlist")


    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        try:
            playlist_list = self.playlists.values()
            selected_playlist = Playlist("")
            if len(list(playlist_list))>0:
                for p in playlist_list:
                    if p.title.lower() == playlist_name.lower():
                        selected_playlist = p
            if len(selected_playlist.title)==0:
                print("Cannot clear playlist "+playlist_name+": Playlist does not exist")
            else:
                for v in selected_playlist.get_videos():
                    selected_playlist.remove_video(v)
                print("Successfully removed all videos from "+playlist_name)
        except:
            print("Error")


    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        try:
            playlist_list = self.playlists.values()
            selected_playlist = Playlist("")
            if len(list(playlist_list))>0:
                for p in playlist_list:
                    if p.title.lower() == playlist_name.lower():
                        selected_playlist = p
            if len(selected_playlist.title)==0:
                print("Cannot delete playlist "+playlist_name+": Playlist does not exist")
            else:
                del self.playlists[selected_playlist.title]
                print("Deleted playlist: "+playlist_name)
        except:
            print("Error")

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        video_list = self._video_library.get_all_videos()
        output_list = []
        for v in video_list:
            if search_term.lower() in v.title.lower():
                if not v.get_flagged():
                    output_string = v.title + " (" + v.video_id + ") ["
                    first_tag = True
                    for i in v.tags:
                        if first_tag:
                            first_tag = False
                        else:
                            output_string = output_string + " "
                        output_string = output_string + i
                    output_string = output_string + "]"
                    output_list.append(output_string)
        output_list = sorted(output_list)
        if len(output_list) > 0:
            print("Here are the results for "+search_term+":")
            count = 1
            for l in output_list:
                print("  "+str(count)+") " + l)
                count += 1
            print("Would you like to play any of the above? If yes, specify the number of the video.")
            print("If your answer is not a valid number, we will assume it's a no.")
            command = input("")
            try:
                selected_video = output_list[int(command)-1]
                selected_video_id = selected_video.split(" (")[1]
                selected_video_id = selected_video_id.split(")")[0]
                selected_video_id.strip("(")
                selected_video = self._video_library.get_video(selected_video_id)
                self.play_video(selected_video.video_id)
            except:
                error = "Error"
        else:
            print ("No search results for "+search_term)

    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        video_list = self._video_library.get_all_videos()
        output_list = []
        for v in video_list:
            for t in v.tags:
                if video_tag.lower() in t.lower():
                    if not v.get_flagged():
                        output_string = v.title + " (" + v.video_id + ") ["
                        first_tag = True
                        for i in v.tags:
                            if first_tag:
                                first_tag = False
                            else:
                                output_string = output_string + " "
                            output_string = output_string + i
                        output_string = output_string + "]"
                        output_list.append(output_string)
        output_list = sorted(output_list)
        if len(output_list) > 0:
            print("Here are the results for "+video_tag+":")
            count = 1
            for l in output_list:
                print("  "+str(count)+") " + l)
                count += 1
            print("Would you like to play any of the above? If yes, specify the number of the video.")
            print("If your answer is not a valid number, we will assume it's a no.")
            command = input("")
            try:
                selected_video = output_list[int(command)-1]
                selected_video_id = selected_video.split(" (")[1]
                selected_video_id = selected_video_id.split(")")[0]
                selected_video_id.strip("(")
                selected_video = self._video_library.get_video(selected_video_id)
                self.play_video(selected_video.video_id)
            except:
                error = "Error"
        else:
            print ("No search results for "+video_tag)

    def flag_video(self, video_id, flag_reason=""):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        if len(flag_reason)==0:
            flag_reason = "Not supplied"
        selected_video = self._video_library.get_video(video_id)
        if selected_video == None:
            print("Cannot flag video: Video does not exist")
        else:
            if selected_video.get_flagged():
                print ("Cannot flag video: Video is already flagged")
            else:
                selected_video.set_flag(flag_reason)
                if self.currently_playing.video_id == selected_video.video_id:
                    self.stop_video()
                print("Successfully flagged video: "+selected_video.title + " (reason: "+flag_reason+")")
                

    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        selected_video = self._video_library.get_video(video_id)
        if selected_video == None:
            print("Cannot remove flag from video: Video does not exist")
        else:
            if not selected_video.get_flagged():
                print ("Cannot remove flag from video: Video is not flagged")
            else:
                selected_video.remove_flag
                print("Successfully removed flag from video: "+selected_video.title)
                

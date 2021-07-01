"""A video playlist class."""

from .video import Video
import traceback

class Playlist:
    """A class used to represent a Playlist."""

    def __init__(self, playlist_title: str):
        """Playlist constructor."""
        self._title = playlist_title
        self._videos = {}

    @property
    def title(self) -> str:
        """Returns the title of a video."""
        return self._title
    
    def get_videos(self):
        """Returns the title of a video."""
        return list(self._videos.values())

    def add_video(self, video_object):
        try:
            self._videos[video_object.video_id] = video_object
        except:
            traceback.print_exc()

    def remove_video(self, video_object):
        del self._videos[video_object.video_id]

    
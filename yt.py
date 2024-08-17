import re
from youtube_transcript_api import YouTubeTranscriptApi

class YT:
    def __init__(self):
        pass

    def get_transcript(self, url):
        video_id = self.get_video_id(url)
        return self.youtube(video_id)

    def youtube(self, video_id):
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
            transcript = ""
            for segment in transcript_list:
                transcript += segment["text"] + " "
            return transcript.strip()
        except Exception as e:
            print("Error:", e)
        return None

    def get_video_id(self, url):
        pattern = r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})"
        match = re.search(pattern, url)
        return match.group(1) if match else None
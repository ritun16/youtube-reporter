import os
import asyncio
from openai import AsyncOpenAI
from pytube import YouTube
import uuid

from prompt import REPORT_GENERATE_PROMPT
import config as cfg


class YouTubeReporter(object):
    def __init__(self, openai_api_key, yt_link, file_name):
        self._client = AsyncOpenAI(api_key=openai_api_key)
        self.yt_link = yt_link
        self.file_name = file_name
        self.yt_video_details = dict()
        self.meta_details = "| Title           | Views   | Length     | Rating | Author | Published Date   | Keywords      |\n"
        self.meta_details += "|----------------|---------|------------|--------|--------|------------------|---------------|\n"
        
    async def get_size(self):
        file_size = round(os.path.getsize(self.file_name)/(1024*1024), 2)
        if file_size < 25:
            return True
        else:
            return False
        
    async def convert_seconds(self, seconds):
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        remaining_seconds = seconds % 60
        return "{} hours {} minutes {} seconds".format(hours, minutes, remaining_seconds)
        
    async def get_transcript(self):
        try:
            yt_obj = YouTube(self.yt_link)
            yt_trans = yt_obj.streams.filter(only_audio=True)[0].download(filename=self.file_name)
            print("Youtube video is downloaded successfully!")
            file_size = await self.get_size()
            if not file_size:
                if os.path.isfile(yt_trans):
                    os.remove(yt_trans)
                return "ERROR", "Only supports {}MB of file size as of now. Equivalant to approximately {} minutes of video. Please try again with smaller videos!".format(cfg.VIDEO_SIZE, cfg.VIDEO_LENGTH)
            self.yt_video_details = {
                "Title": str(yt_obj.title),
                "Views": str(yt_obj.views),
                "Length": await self.convert_seconds(yt_obj.length),
                "Rating": str(yt_obj.rating),
                "Author": str(yt_obj.author),
                "Published Date": yt_obj.publish_date.strftime("%A, %B %d, %Y at %I:%M %p"),
                "Keywords": ", ".join(yt_obj.keywords),
            }
        except Exception as error:
            print("Youtube video download failed. Error: {}".format(str(error)))
            return "ERROR", "Youtube video download failed. Check the link is valid and please try again!"

        try:
            with open(yt_trans, "rb") as audio_file:
                transcription = await self._client.audio.transcriptions.create(model="whisper-1", file=audio_file)
            if os.path.isfile(yt_trans):
                os.remove(yt_trans)
            print("Youtube video is transcripted successfully!")
            return "SUCCESS", transcription.text
        except Exception as error:
            if os.path.isfile(yt_trans):
                os.remove(yt_trans)
            print("Youtube transcription failed. Error: {}".format(str(error)))
            return "ERROR", "Youtube transcription failed. Please try again!"
        
    async def get_report(self):
        status, transcript_text = await self.get_transcript()
        if status == "SUCCESS":
            try:
                stream_response = await self._client.chat.completions.create(
                              model=cfg.LLM_NAME,
                              temperature=cfg.LLM_TEMP,
                              messages=[
                                {"role": "system", "content": REPORT_GENERATE_PROMPT},
                                {"role": "user", "content": "YouTube video Title: {}\nYoutube video author: {}\n\nYoutube video transcript:\n{}".format(self.yt_video_details["Title"], self.yt_video_details["Author"], transcript_text)},
                              ],
                              stream=True
                            )
                print("Youtube streamed report generated successfully")
                self.meta_details += "| {} | {} | {} | {} | {} | {} | {} |\n".format(
                                                                                    self.yt_video_details["Title"],
                                                                                    self.yt_video_details["Views"],
                                                                                    self.yt_video_details["Length"],
                                                                                    self.yt_video_details["Rating"],
                                                                                    self.yt_video_details["Author"],
                                                                                    self.yt_video_details["Published Date"],
                                                                                    self.yt_video_details["Keywords"],
                                                                                )
                return "SUCCESS", stream_response, self.meta_details
            except Exception as error:
                print("LLM based report generation failed. Error: {}".format(str(error)))
                return "ERROR", "LLM based report generation failed. Please try again!", None
        else:
            return status, transcript_text, None
        


import os
import re
import asyncio
from openai import AsyncOpenAI
from pytube import YouTube
import uuid
import json
import traceback
import random
import string
from typing import TypedDict
from datetime import datetime,timedelta

import wikipedia

from prompt import REPORT_GENERATE_PROMPT, TERM_EXTRACTION_PROMPT, TOPIC_PROMPT
import config as cfg

wikipedia.set_lang("en")


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
        if file_size < cfg.VIDEO_SIZE:
            return True
        else:
            return False
        
    async def convert_seconds(self, seconds):
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        remaining_seconds = seconds % 60
        return "{} hours {} minutes {} seconds".format(hours, minutes, remaining_seconds)
    
    async def extract_json_from_string(self, s):
        pattern = re.compile(r'```json(.*?)```', re.DOTALL)
        match = pattern.search(s)

        if match:
            json_str = match.group(1).strip()
        else:
            json_str = s.strip()

        try:
            json_data = json.loads(json_str)
            return json_data
        except json.JSONDecodeError:
            raise ValueError("No valid JSON found in the provided string.")
        
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
            self.yt_video_details["Transcription Text"] = transcription.text
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
                traceback.print_exc()
                print("LLM based report generation failed. Error: {}".format(str(error)))
                return "ERROR", "LLM based report generation failed. Please try again!", None
        else:
            return status, transcript_text, None
        
        
    async def topic_reports(self):
        status, transcript_text = await self.get_transcript()
        topic_streamed_responses = []
        if status == "SUCCESS":
            try:
                term_prompt = TERM_EXTRACTION_PROMPT.format(transcript_text)
                term_response = await self._client.chat.completions.create(
                              model=cfg.LLM_NAME,
                              temperature=cfg.LLM_TEMP,
                              messages=[
                                {"role": "system", "content": term_prompt},
                                
                              ],
                              stream=False
                            )
                term_dict = await self.extract_json_from_string(term_response.choices[0].message.content)
                for term in term_dict["terms"]:
                    wiki_result = wikipedia.search(term, results = 1)
                    print("WIKI RESULT: ", wiki_result)
                    try:
                        wiki_page_object = wikipedia.page(wiki_result[0])
                        print("wiki_page_object.content", wiki_page_object.content)
                    except:
                        continue
                    topic_report_prompt = TOPIC_PROMPT.format(term, wiki_page_object.content)
                    topic_streamed_response = await self._client.chat.completions.create(
                          model=cfg.LLM_NAME,
                          temperature=cfg.LLM_TEMP,
                          messages=[
                            {"role": "system", "content": topic_report_prompt},

                          ],
                          stream=True
                        )
                    topic_streamed_responses.append(topic_streamed_response)
                return "SUCCESS", topic_streamed_responses, None
            except Exception as error:
                traceback.print_exc()
                print("LLM based report generation failed. Error: {}".format(str(error)))
                return "ERROR", "LLM based report generation failed. Please try again!", None
        else:
            return status, transcript_text, None
        


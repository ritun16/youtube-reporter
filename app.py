import os
import asyncio
import uuid
import streamlit as st

from backend import YouTubeReporter
import config as cfg


st.set_page_config(
    page_title="YouTube Video Reporter",
    layout="wide",
)

st.title("YouTube Video Reporter")

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", type="password")
    youtube_link = st.text_input("YouTube Link", value=cfg.SAMPLE_YT_VIDEO_LINK)
    generate_report = st.button("Generate Report")
    
markdown_output = st.empty()


async def main():
    file_name = './temp_data/{}.mp3'.format(uuid.uuid4().hex)    
    yt_reporter = YouTubeReporter(openai_api_key, youtube_link, file_name)

    status, stream_response = await yt_reporter.get_report()
    streamed_text = ""
    if status == "SUCCESS":
        async for chunk in stream_response:
            chunk_content = chunk.choices[0].delta.content
            if chunk_content is not None:
                streamed_text = streamed_text + chunk_content
                #print(chunk_content, end="")
                await asyncio.sleep(0.05)
                markdown_output.markdown(streamed_text)
    else:
        st.error(stream_response)
        print(status, stream_response)

if generate_report:
    if openai_api_key.strip() == "" or youtube_link.strip() == "":
        st.warning("Please enter both OpenAI API Key and YouTube Link")
    else:
        asyncio.run(main())

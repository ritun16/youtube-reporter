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

if "streamed_summary_text" not in st.session_state:
    st.session_state.streamed_summary_text = ""
    
if "streamed_topic_text" not in st.session_state:
    st.session_state.streamed_topic_text = ""

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", type="password")
    youtube_link = st.text_input("YouTube Link", value=cfg.SAMPLE_YT_VIDEO_LINK)
    generate_report = st.button("Generate Report")
    
# markdown_output = st.empty()
summary_col, topic_col = st.columns(2)
summary_markdown_output = summary_col.empty()
topic_markdown_output = topic_col.empty()


async def summary_report():
    file_name = './temp_data/{}.mp3'.format(uuid.uuid4().hex)    
    yt_reporter = YouTubeReporter(openai_api_key, youtube_link, file_name)

    status, stream_response, meta_details = await yt_reporter.get_report()
    if status == "SUCCESS":
        st.session_state.streamed_summary_text = st.session_state.streamed_summary_text + meta_details
        async for chunk in stream_response:
            chunk_content = chunk.choices[0].delta.content
            if chunk_content is not None:
                st.session_state.streamed_summary_text = st.session_state.streamed_summary_text + chunk_content
                await asyncio.sleep(0.05)
                summary_markdown_output.markdown(st.session_state.streamed_summary_text)
        st.download_button(
                label="Download Summary Report",
                data=st.session_state.streamed_summary_text,
                file_name="summary_report.md")
        st.session_state.streamed_summary_text = ""
    else:
        st.error(stream_response)
        print(status, stream_response)
        st.session_state.streamed_summary_text = ""
        
async def topic_report():
    file_name = './temp_data/{}.mp3'.format(uuid.uuid4().hex)    
    yt_reporter = YouTubeReporter(openai_api_key, youtube_link, file_name)

    status, topic_streamed_responses, _ = await yt_reporter.topic_reports()
    if status == "SUCCESS":
        for stream_response in topic_streamed_responses:
            async for chunk in stream_response:
                chunk_content = chunk.choices[0].delta.content
                if chunk_content is not None:
                    st.session_state.streamed_topic_text = st.session_state.streamed_topic_text + chunk_content
                    await asyncio.sleep(0.05)
                    topic_markdown_output.markdown(st.session_state.streamed_topic_text)
            st.session_state.streamed_topic_text = st.session_state.streamed_topic_text + "\n\n"
        st.download_button(
                label="Download Topic Report",
                data=st.session_state.streamed_topic_text,
                file_name="topic_report.md")
        st.session_state.streamed_topic_text = ""
    else:
        st.error(topic_streamed_responses)
        print(status, topic_streamed_responses)
        st.session_state.streamed_topic_text = ""
        

async def main():
    await asyncio.gather(
        summary_report(),
        topic_report()
    )
    
if generate_report:
    if openai_api_key.strip() == "" or youtube_link.strip() == "":
        st.warning("Please enter both OpenAI API Key and YouTube Link")
    else:
        asyncio.run(main())

REPORT_GENERATE_PROMPT = """Given a Youtube transcript, your task is to create a comprehensive report in markdown format. This
involves analyzing the content of the transcript, structuring the report with appropriate headings,
subheadings, and lists, and summarizing key points. The report should be clear, concise, and
informative.

1. **Start by reading the entire transcript carefully.** This will help you understand the overall
theme, main ideas, and important details. Pay attention to any recurring themes, crucial points made
by the speaker, and any data or statistics mentioned.

2. **Identify the main sections of the content.** Based on your understanding of the transcript,
divide the content into logical sections. These sections will form the main headings of your report.

3. **Write a brief introduction.** In markdown format, start your report with an introduction that
gives an overview of the video content. This should include the title of the video, the speaker's
name (if applicable), and a general summary of the video's topic and purpose.

# Introduction
This report summarizes the content of [Video Title] by [Speaker Name], which covers [general topic
or purpose of the video].


4. **Create headings for each main section.** For each section you identified, create a markdown
heading. Use `##` for main headings and `###` for any subheadings within those sections.

## [Main Section Title]
### [Subsection Title]


5. **Summarize key points under each heading.** Under each heading, summarize the key points
discussed in the video. Use bullet points or numbered lists to organize information clearly.

- Key point 1
- Key point 2
- Key point 3


6. **Include any important quotes or data.** If the speaker mentions any significant quotes,
statistics, or data, include these in your report. Use blockquotes for quotes and ensure any data is
accurately represented.

> "This is an important quote from the speaker."
According to the speaker, 70% of users prefer...


7. **Conclude with a summary and final thoughts.** End your report with a conclusion that summarizes
the main insights from the video and any final thoughts or reflections.

## Conclusion
In summary, [Video Title] provides comprehensive insights into [topic]. The key takeaways are...


8. **Review and edit your report.** Before finalizing your report, review it for clarity, coherence,
and accuracy. Ensure that it is well-organized and that all markdown formatting is correct.

Remember, your report should not only summarize the video content but also present it in a
structured, easy-to-read format. Use markdown formatting effectively to enhance the readability and
professionalism of your report."""

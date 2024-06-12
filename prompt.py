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


TERM_EXTRACTION_PROMPT = """You are tasked with analyzing a YouTube transcript to identify and list key terms. These terms can
include technical terms, significant points, important events, names of people, theories, or any
other critical information mentioned in the transcript. Your goal is to extract these terms without
providing descriptions or additional context. Maximum 10 key terms. Not more than that.

Here's how you should approach this task:

1. Read through the provided transcript carefully. Pay attention to the context in which words are
used to determine their importance.
2. Identify key terms based on the criteria given: technical terms, significant points, important
events, important names, important theories, or any other critical information.
3. List down the key terms you identify. Ensure that this list includes only the names or terms
without any descriptions or explanations.
4. Your list should be concise and only include words or phrases that are directly mentioned in the
transcript and are of notable importance.

Please format your response as following JSON:

{{"terms": ["Term 1", "Term 2", "Term 3" ...]}}

This list should be a straightforward enumeration of key terms extracted from the transcript,
without any additional commentary or detail.

Remember, the focus is on identifying terms that are essential to understanding the content of the
transcript. This might require you to discern between general conversation and parts of the
transcript that discuss key concepts or ideas.

<YT_TRANSCRIPT>{}</YT_TRANSCRIPT>

JSON Output: """


TOPIC_PROMPT = """Given the task of creating a short summary report about a specific topic based on Wikipedia search
results, follow these steps:

1. **Read the Topic:**
Begin by carefully reading the topic provided to you. This will help you understand what information
you are looking for in the Wikipedia search results.

<topic>
{}
</topic>

2. **Review the Wikipedia Search Results:**
Next, review the Wikipedia search results provided. These results contain various pieces of information
related to the topic. Your goal is to extract key points, facts, and insights from these results to
compile a comprehensive summary.

<wikipedia_results>
{}
</wikipedia_results>

3. **Create a Summary Report:**
Based on the information gathered from the Wikipedia search results, create a short summary report about
the topic. Your report should be concise, informative, and structured. Use markdown format for your
report to enhance readability and organization.

Here are some markdown formatting guidelines you may use:
- Use `#` for headings (e.g., `# [Topic]`)
- Use `##` for subheadings (e.g., `## Key Findings`)
- Use `-` for bullet points (e.g., `- Fact 1`)
- Use `**` to bold important points (e.g., `**Important:** This fact is crucial.`)

4. **Add Your Own Insights (Optional):**
If you feel that the Wikipedia search results are insufficient or lack depth on certain aspects of the
topic, you are allowed to add your own insights or conclusions to the summary. Make sure these
additions are clearly marked and justified based on the available information or general knowledge
about the topic.

5. **Finalize the Summary Report:**
Once you have compiled all the necessary information and insights, finalize your summary report.
Ensure that the report is well-organized, covers all relevant aspects of the topic, and adheres to
the markdown formatting guidelines."""

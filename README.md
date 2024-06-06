# YouTube Video Reporter

## Description
YouTube Video Reporter is a project that utilizes OpenAI LLM to generate a comprehensive summary report for any English YouTube video.

## Installation
To get started, follow these installation instructions:
1. Make sure you have Python installed on your system.
2. Clone this repository to your local machine.
3. Navigate to the project directory.
4. Install the required dependencies by running:
    ```
    pip install -r requirements.txt
    ```

## Usage
To use YouTube Video Reporter:
1. Obtain an OpenAI API key.
2. Provide the OpenAI API key and the URL of the YouTube video you want to summarize.
3. Run the application by executing the following command:
    ```
    streamlit run app.py
    ```
4. Follow the prompts in the Streamlit app to generate a summary report for the provided YouTube video.

**Note:** The application currently supports YouTube videos with a maximum size of 25 MB, corresponding to approximately 20-25 minutes of video length.

## License
[MIT License](LICENSE)

## Acknowledgments
- This project utilizes the OpenAI API.
- Special thanks to Streamlit for providing an easy-to-use framework for building interactive web applications.


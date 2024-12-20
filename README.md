Change YOUR_API_KEY to your Groq API key.

MoonAI YouTube Transcript Analyzer

This repository provides a GUI-based application for extracting and analyzing YouTube video transcripts. Using the YouTube Transcript API, it allows users to download, summarize, and interact with the video transcript through a chat interface powered by the Groq API.

Features

Download YouTube Transcripts: Enter a YouTube video URL to download its transcript.
Summarize Transcript: Summarize long video transcripts into clear bullet points.
Themed UI: Switch between light, dark, and cafe themes for a personalized experience.
Chat with AI: Interact with a chatbot to discuss the video summary using Groq’s LLM.
Copy Transcript/Summary: Easily copy the transcript or summarized content to the clipboard.
Requirements

Python 3.6 or higher
Required Python libraries:
PyQt6: For building the GUI
groq: For integrating with the Groq API
youtube-transcript-api: For fetching video transcripts from YouTube
re: For regular expressions to extract video IDs from URLs
Groq API Key: You will need an API key for Groq's LLM.
Installation

Clone the repository:
Fork this github
Install dependencies:
pip install -r requirements.txt
Set your Groq API key: In the main.py file, replace the GROQ_API_KEY placeholder with your actual Groq API key.
Usage

Run the Application:
python main.py
This will open a window where you can interact with the application.
Download Transcript:
Paste a YouTube video URL into the input field and click Download Transcript to fetch the transcript.
Summarize Transcript:
After downloading the transcript, click Summarize Transcript to generate a summarized version.
Chat with AI:
Click the chat logo to open a dialog and ask questions about the video summary.
Copy to Clipboard:
Use the Copy Summary button to copy the summary to your clipboard for easy sharing.
Screenshots

License

This project is licensed under the MIT License - see the LICENSE file for details.

Contributions

Contributions are welcome! Please fork the repository, create a new branch, and submit a pull request.

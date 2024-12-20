import sys
import re
import groq
from youtube_transcript_api import YouTubeTranscriptApi
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QTextEdit, QPushButton, QLabel, QFrame,
    QStatusBar, QDialog, QComboBox, QMenuBar, QMenu
)
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt
from PyQt6.QtCore import QSize


def extract_video_id(input_string):
    """Extract YouTube video ID from URL or return input if already an ID."""
    if re.match(r'http(s)?:\/\/', input_string):
        match = re.search(r'v=([^&]*)', input_string)
        if match:
            return match.group(1)
    elif 'youtu.be' in input_string:
        match = re.search(r'youtu\.be/([^&]*)', input_string)
        if match:
            return match.group(1)
    return input_string

class ChatDialog(QDialog):
    def __init__(self, groq_client, summary):
        super().__init__()
        self.groq_client = groq_client
        self.summary = summary
        self.chat_history = []
        self.initUI()

    def initUI(self):
        self.setWindowTitle('MoonAI Chatbot')
        layout = QVBoxLayout()

        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        layout.addWidget(self.chat_display)
        self.setStyleSheet("""
            QDialog {
                background-color: #f0f2f5;
                border: 1px solid #cfd9e0;
                border-radius: 8px;
            }
            QTextEdit {
                border: 1px solid #cfd9e0;
                border-radius: 10px;
                padding: 12px;
                font-size: 14px;
                font-family: Georgia, sans-serif;
                background-color: #ffffff;
                color: #333333;
            }
            QLineEdit {
                border: 1px solid #cfd9e0;
                border-radius: 10px;
                padding: 10px;
                font-size: 14px;
                font-family: Georgia, sans-serif;
                background-color: #ffffff;
                color: #333333;
            }
            QPushButton {
                background-color: #800080;
                color: white;
                border: none;
                padding: 12px 18px;
                border-radius: 8px;
                font-size: 14px;
                font-family: Georgia, sans-serif;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #FF00FF;
            }
            QPushButton:pressed {
                background-color: #FF00FF;
            }
            QHBoxLayout QPushButton {
                margin-left: 6px;
            }
        """)

        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText('Ask about the video summary...')
        layout.addWidget(self.user_input)

        self.send_btn = QPushButton('Send')
        self.send_btn.clicked.connect(self.send_message)
        layout.addWidget(self.send_btn)

        self.setLayout(layout)

    def send_message(self):
        user_message = self.user_input.text()
        if not user_message:
            return

        self.chat_display.append(f"You: {user_message}")
        self.user_input.clear()

        self.chat_history.append({"role": "user", "content": user_message})

        try:
            response = self.groq_client.chat.completions.create(
                messages=[
                    {"role": "system", "content": f"You are an AI assistant discussing a video summary. The summary is: {self.summary}"}
                ] + self.chat_history,
                model="llama3-8b-8192",
                temperature=0.7
            )

            ai_response = response.choices[0].message.content
            self.chat_display.append(f"AI: {ai_response}")
            self.chat_history.append({"role": "assistant", "content": ai_response})
        except Exception as e:
            self.chat_display.append(f"Error: {str(e)}")

class ModernYouTubeTranscriptApp(QWidget):
    def __init__(self, groq_client):
        super().__init__()
        self.groq_client = groq_client
        self.initUI()

    def initUI(self):
        # Window setup
        self.setWindowTitle('MoonAI v.1.0.0')
        self.setGeometry(100, 100, 800, 600)

        # Default Theme
        self.current_theme = 'Light'
        self.apply_theme(self.current_theme)

        # Main layout
        main_layout = QVBoxLayout()

        # Menu Bar
        self.menu_bar = QMenuBar()
        settings_menu = QMenu("Settings", self)

        # Theme Selector
        theme_menu = QMenu("Themes", self)
        themes = ['Light', 'Dark', 'Cafe']
        for theme in themes:
            theme_menu.addAction(theme, lambda checked, t=theme: self.change_theme(t))
        settings_menu.addMenu(theme_menu)

        self.menu_bar.addMenu(settings_menu)
        main_layout.setMenuBar(self.menu_bar)

        # Logo Image
        logo_label = QLabel()
        pixmap = QPixmap("MoonLogo.png")
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            logo_label.setPixmap(scaled_pixmap)
            logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            main_layout.addWidget(logo_label)
        else:
            print("Failed to load MoonChatbot.png")

        # Card-like frame
        card_frame = QFrame()
        card_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                padding: 20px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }
        """)
        card_layout = QVBoxLayout(card_frame)

        # Title
        title_label = QLabel('YouTube Transcript Analyzer')
        title_label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #2c3e50;
                margin-bottom: 15px;
                text-align: center;
            }
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(title_label)

        # URL Input Layout
        url_layout = QHBoxLayout()
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText('Enter YouTube Video URL')
        self.url_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #d1d8e0;
                border-radius: 6px;
                font-size: 14px;
            }
        """)
        url_layout.addWidget(self.url_input)

        # Download Button
        self.download_btn = QPushButton('Download Transcript')
        self.download_btn.setStyleSheet("""
            QPushButton {
                background-color: #525aff;
                color: white;
                border: none;
                padding: 10px 15px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        self.download_btn.clicked.connect(self.download_transcript)
        url_layout.addWidget(self.download_btn)
        card_layout.addLayout(url_layout)

        # Transcript Display
        self.transcript_display = QTextEdit()
        self.transcript_display.setStyleSheet("""
            QTextEdit {
                border: 1px solid #d1d8e0;
                border-radius: 6px;
                padding: 10px;
                margin-top: 10px;
                margin-bottom: 10px;
            }
        """)
        card_layout.addWidget(self.transcript_display)

        # Copy Transcript Button
        
        

        # Summarize Button
        self.summarize_btn = QPushButton('Summarize Transcript')
        self.summarize_btn.setStyleSheet("""
            QPushButton {
                background-color: #546373;
                color: white;
                border: none;
                padding: 10px 15px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #6d8196;
            }
        """)
        self.summarize_btn.clicked.connect(self.summarize_transcript)
        card_layout.addWidget(self.summarize_btn)

        # Copy Summary Button
        self.copy_summary_btn = QPushButton("Copy Summary")
        self.copy_summary_btn.setToolTip("Copy Summary to Clipboard")
        self.copy_summary_btn.setIcon(QIcon("Paste.png"))
        self.copy_summary_btn
        self.copy_summary_btn.setStyleSheet("""
            QPushButton {
                background-color: #e9ecef;
                border: none;
                padding: 8px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #ced4da;
            }
        """)
        self.copy_summary_btn.clicked.connect(self.copy_summary)
        card_layout.addWidget(self.copy_summary_btn)

        # Chat Button
        self.chat_btn = QPushButton("")
        self.chat_btn.setIcon(QIcon("MoonChatbot.png"))
        self.chat_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                
                border: none;
                padding: 15px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: white;
            }
        """)
        self.chat_btn.setIconSize(QSize(100, 100))  # Adjust icon size as needed
        self.chat_btn.setFixedSize(120, 120)
        self.chat_btn.clicked.connect(self.open_chat)
        card_layout.addWidget(self.chat_btn)

        # Status Bar
        self.status_bar = QStatusBar()
        self.status_bar.setStyleSheet("""
            QStatusBar {
                color: #6c757d;
                font-style: italic;
            }
        """)
        card_layout.addWidget(self.status_bar)

        # Add card to main layout
        main_layout.addWidget(card_frame)
        self.setLayout(main_layout)

    def apply_theme(self, theme):
        if theme == 'Light':
            self.setStyleSheet("""
                QWidget {
                    background: #f5f7fa;
                    color: #333;
                    font-family: Georgia, sans-serif;
                }
            """)
        elif theme == 'Dark':
            self.setStyleSheet("""
                QWidget {
                    background: #2c3e50;
                    color: #ecf0f1;
                    font-family: Georgia, sans-serif;
                }
            """)
        elif theme == 'Cafe':
            self.setStyleSheet("""
                QWidget {
                    background: #d7ccc8;
                    color: #4e342e;
                    font-family: Georgia, serif;
                }
            """)

    def change_theme(self, theme):
        self.current_theme = theme
        self.apply_theme(theme)

    def download_transcript(self):
        video_url = self.url_input.text()
        if not video_url:
            self.status_bar.showMessage('Please enter a video URL')
            return

        try:
            video_id = extract_video_id(video_url)
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            transcript_text = '\n'.join([entry['text'] for entry in transcript])
            self.transcript_display.setPlainText(transcript_text)
            self.status_bar.showMessage('Transcript downloaded successfully')
        except Exception as e:
            self.transcript_display.setPlainText(f'Error: {str(e)}')
            self.status_bar.showMessage('Failed to download transcript')

    def summarize_transcript(self):
        transcript = self.transcript_display.toPlainText()
        if not transcript:
            self.status_bar.showMessage('No transcript to summarize')
            return

        try:
            response = self.groq_client.chat.completions.create(
                messages=[{
                    "role": "user",
                    "content": f"Summarize this transcript in clear bullet points:\n\n{transcript}"
                }],
                model="llama3-8b-8192",
                temperature=0.3
            )

            summary = response.choices[0].message.content

            # Convert Markdown-style bold to HTML (if needed)
            formatted_summary = summary.replace("**", "<b>").replace("**", "</b>")

            # Format the summary with HTML for bold text and line breaks
            formatted_summary = "<b>Summary:</b><br>" + formatted_summary.replace("\n", "<br>")

            self.transcript_display.setHtml(formatted_summary)
            self.status_bar.showMessage('Transcript summarized')
        except Exception as e:
            self.transcript_display.setPlainText(f'Summarization error: {str(e)}')
            self.status_bar.showMessage('Failed to summarize transcript')

    

    def copy_summary(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.transcript_display.toPlainText())  # Adjust if summary is displayed elsewhere
        self.status_bar.showMessage('Summary copied to clipboard')

    def open_chat(self):
        summary = self.transcript_display.toPlainText()
        if not summary:
            self.status_bar.showMessage('No summary to discuss')
            return

        chat_dialog = ChatDialog(self.groq_client, summary)
        chat_dialog.exec()

def main():
    GROQ_API_KEY = "YOUR_API_KEY"


    app = QApplication(sys.argv)

    groq_client = groq.Client(api_key=GROQ_API_KEY)

    main_window = ModernYouTubeTranscriptApp(groq_client)
    main_window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()

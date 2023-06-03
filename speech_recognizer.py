import sqlite3
import uuid

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import (QApplication, QLabel, QProgressDialog,
                             QPushButton, QTabWidget, QVBoxLayout, QWidget)

from ai_evaluation import parse_and_evaluate_conversation
from ai_response import create_and_play_ai_response
from random_pm_question import generate_random_question as generate_question
from user_speech_to_text import transcribe_speech


#
class CurrentConversationTab(QWidget):
    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window

        self.layout = QVBoxLayout(self)

        self.label = QLabel("Hello and welcome to the interview")
        self.start_button = QPushButton("Start")
        self.stop_button = QPushButton("Stop")
        self.ai_response_button = QPushButton("Generate AI Response")
        self.transcribe_button = QPushButton("Transcribe Speech")
        self.conversation_display = QWebEngineView()

        # Initialize with an empty HTML document
        self.conversation_display.setHtml("<html><body></body></html>")

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.start_button)
        self.layout.addWidget(self.stop_button)
        self.layout.addWidget(self.ai_response_button)
        self.layout.addWidget(self.transcribe_button)
        self.layout.addWidget(self.conversation_display)

        self.ai_response_button.hide()
        self.transcribe_button.hide()
        self.conversation_display.hide()

        self.start_button.clicked.connect(self.main_window.start_main)
        self.stop_button.clicked.connect(self.main_window.stop_main)
        self.ai_response_button.clicked.connect(self.main_window.ai_response)
        self.transcribe_button.clicked.connect(
            self.main_window.transcribe_speech)

        self.setLayout(self.layout)


class PastConversationsTab(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)


class MainWindow (QWidget): 
    def __init__(self, main_function):
        super().__init__()
        self.resize(800, 600)
        self.main_function = main_function
        self.run_main = False
        self.conversation = []
        self.starting_question = ""
        self.conversation_id = ""
        self.setWindowTitle("Interview Practice")

        self.tab_widget = QTabWidget()
        self.layout = QVBoxLayout(self)

        self.current_conversation_tab = CurrentConversationTab(self)
        self.past_conversations_tab = PastConversationsTab()

        self.tab_widget.addTab(
            self.current_conversation_tab, "Current Conversation")
        self.tab_widget.addTab(
            self.past_conversations_tab, "Past Conversations")

        self.layout.addWidget(self.tab_widget)
        self.setLayout(self.layout)

    # All your MainWindow methods follow here...

# This method is called when the start button is clicked
    def start_main(self):
        self.run_main = True  # We start our conversation

        # create a random unique ID for the conversation
        self.conversation_id = str(uuid.uuid4())

        # We show the buttons for the AI response and speech transcription
        self.current_conversation_tab.ai_response_button.show()
        self.current_conversation_tab.transcribe_button.show()
        # We show the conversation display
        self.current_conversation_tab.conversation_display.show()

        # We initialize a new conversation
        self.conversation, self.starting_question = self.main_function()
        self.current_conversation_tab.label.setText(
            self.starting_question)  # We set the label to the first question

        self.ai_response()  # We generate an AI response to the first question

    # This method is called when the stop button is clicked

    def stop_main(self):
        self.run_main = False  # We stop our conversation
        self.current_conversation_tab.label.setText(
            "Hello and welcome to the interview")  # We reset the label
        self.conversation = []  # We reset the conversation
        self.starting_question = ""  # We reset the starting question
        self.conversation_id = ""  # We reset the conversation ID

        # we remove the buttons for the AI response and speech transcription
        self.current_conversation_tab.ai_response_button.hide()
        self.current_conversation_tab.transcribe_button.hide()

        # clear the converstaion display
        self.current_conversation_tab.conversation_display.clear()
        self.current_conversation_tab.conversation_display.hide()

    # This method is called when the "Generate AI Response" button is clicked

    def ai_response(self):
        if self.run_main:  # We generate an AI response only if a conversation is active
            # Create a QProgressDialog
            progress = QProgressDialog(
                "Generating AI response...", None, 0, 0, self)
            # Set the progress dialog to modal mode
            progress.setWindowModality(Qt.WindowModal)
            # Show the progress dialog
            progress.show()
            QApplication.processEvents()
            ai_text_response, path_to_audio = create_and_play_ai_response(
                self.conversation)
            # Close the progress dialog
            progress.cancel()
            print("Interviewer: ", ai_text_response)
            print("path to audio: ", path_to_audio)
            insert_message(self.conversation_id, len(
                self.conversation), "assistant", ai_text_response)
            self.add_message_to_display("blue", "AI", ai_text_response)

            # We add the AI response to the conversation display

    # This method is called when the "Transcribe Speech" button is clicked

    def transcribe_speech(self):
        if self.run_main:  # We transcribe speech only if a conversation is active
            response = transcribe_speech()  # We transcribe the user's speech
            if response is not None:
                # We add the user response to the conversation
                self.conversation.append({"role": "user", "content": response})
                insert_message(self.conversation_id, len(
                    self.conversation), "user", response)  # We add the user response to the database

                # We add the user response to the conversation display
                self.add_message_to_display("red", "User", response)

                # We evaluate the user response
                score, qualitative_feedback = parse_and_evaluate_conversation(
                    self.conversation)

                # We add the evaluation to the conversation display
                self.add_message_to_display(
                    "Green", "Evaluation", f"Score: {score}")
                self.add_message_to_display(
                    "Green", "Evaluation", f"Qualitative Feedback: {qualitative_feedback}")

    def add_message_to_display(self, color, role, message):
        # Format the message as an HTML string
        html_message = f"""
            <div style='margin-top: 0; margin-bottom: 10px;'>
                <p style='color: {color}; margin: 0; font-weight: bold;'>{role}</p>
                <p style='margin-top: 2px;'>{message}</p>
            </div>
        """
        # Insert the HTML string into the current page
        self.current_conversation_tab.conversation_display.page().runJavaScript(f"""
            var body = document.querySelector('body');
            var div = document.createElement('div');
            div.innerHTML = `{html_message}`;
            body.appendChild(div);
        """)


def insert_message(conversation_id, message_id, role, content):
    conn = sqlite3.connect('conversations.db')
    c = conn.cursor()

    c.execute('''
        INSERT INTO messages(conversation_id, message_id, role, content)
        VALUES (?, ?, ?, ?)
    ''', (conversation_id, message_id, role, content))

    conn.commit()
    conn.close()

# We define our main function that initializes a new conversation
def create_conversation():
    print("Welcome to the negotiation practice program!")
    starting_question = generate_question()
    print(starting_question)

    starting_prompt = [{"role": "system", "content": f"Your name is Yarrow and you are interviewing the candidate for an engineering position at a tech company. Your responses wi The candidate's name is Brooks. Respond as though you are the interviewer and the candidate is the interviewee. Be extremely critical of the candidate's answers. The first question you should ask the candidate is: {starting_question}"},
                       {"role": "user", "content": "Hi, my name is Brooks, I'm excited to be here today. Let's get started."}]
    return starting_prompt, starting_question


# If this script is being run directly, we create a QApplication and our MainWindow
if __name__ == "__main__":
    # We create a QApplication, which is necessary for any PyQt5 application
    app = QApplication([])

    with open('style.qss', 'r') as file:
        app.setStyleSheet(file.read())

    # We create our MainWindow, passing in our create conversation function
    win = MainWindow(create_conversation)
    win.show()  # We show our MainWindow
    app.exec()  # We start the event loop of our application

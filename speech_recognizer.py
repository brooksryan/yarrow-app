import sys
import uuid
import sqlite3

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QTextEdit, QProgressDialog
from PyQt5.QtCore import Qt
from random_pm_question import generate_random_question as generate_question
from ai_analysis import create_and_play_ai_response
from user_speech_to_text import transcribe_speech


# We create a MainWindow class that inherits from QWidget which is a base class for all user interface objects, or "widgets".
class MainWindow(QWidget):
    def __init__(self, main_function):  # Here we initialize our MainWindow object
        super().__init__()  # We call the initializer of QWidget class

        # We assign our main function to a class variable, so we can use it later
        self.main_function = main_function
        
        # This boolean will represent whether our conversation is active
        self.run_main = False
        
        # This will hold our conversation
        self.conversation = []
        
        # This will hold the starting question
        self.starting_question = ""

        self.conversation_id = ""

        # We set the title of the main window
        self.setWindowTitle("Interview Practice")

        # We create a vertical layout that we will add our widgets to
        self.layout = QVBoxLayout()
        # We create a label
        self.label = QLabel("Hello and welcome to the interview")
        # We create a start button
        self.start_button = QPushButton("Start")
        # We create a stop button
        self.stop_button = QPushButton("Stop")
        # We create a button that will trigger the AI response
        self.ai_response_button = QPushButton("Generate AI Response")
        # We create a button that will trigger speech transcription
        self.transcribe_button = QPushButton("Transcribe Speech")
        # Create a QTextEdit widget to display the conversation
        self.conversation_display = QTextEdit()
        # Set the widget to read-only so it can't be edited by the user
        self.conversation_display.setReadOnly(True)

        # We add our widgets to the layout
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.start_button)
        self.layout.addWidget(self.stop_button)
        # add the buttons for the AI response and speech transcription
        self.layout.addWidget(self.ai_response_button)
        self.layout.addWidget(self.transcribe_button)
        # We add the conversation display to the layout
        self.layout.addWidget(self.conversation_display)

        # We hide the buttons for the AI response and speech transcription
        self.ai_response_button.hide()
        self.transcribe_button.hide()
        self.conversation_display.hide()

        # We connect our buttons to their respective methods
        self.start_button.clicked.connect(self.start_main)
        self.stop_button.clicked.connect(self.stop_main)
        self.ai_response_button.clicked.connect(self.ai_response)
        self.transcribe_button.clicked.connect(self.transcribe_speech)

        # We set the layout of the main window to our created layout
        self.setLayout(self.layout)

    # This method is called when the start button is clicked
    def start_main(self):
        self.run_main = True  # We start our conversation

        #create a randon unique ID for the conversation
        self.conversation_id = str(uuid.uuid4())

        self.ai_response_button.show() # We show the buttons for the AI response and speech transcription
        self.transcribe_button.show() 
        self.conversation_display.show() # We show the conversation display

        self.conversation, self.starting_question = self.main_function()  # We initialize a new conversation
        self.label.setText(self.starting_question)  # We set the label to the first question
        
        # We add the buttons for the AI response and speech transcription

        


    # This method is called when the stop button is clicked
    def stop_main(self):
        self.run_main = False  # We stop our conversation
        self.label.setText("Hello and welcome to the interview")  # We reset the label
        self.conversation = []  # We reset the conversation
        self.starting_question = ""  # We reset the starting question
        self.conversation_id = "" # We reset the conversation ID
        # we remove the buttons for the AI response and speech transcription
        self.ai_response_button.hide()
        self.transcribe_button.hide()
        self.conversation_display.hide()

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
            ai_text_response, path_to_audio = create_and_play_ai_response(self.conversation)
            # Close the progress dialog
            progress.cancel()
            print("Interviewer: ", ai_text_response)
            print("path to audio: ", path_to_audio)
            self.conversation.append({"role": "assistant", "content": ai_text_response})
            insert_message(self.conversation_id, len(self.conversation), "assistant", ai_text_response)
            # We add the AI response to the conversation display
            self.conversation_display.append(f"AI: {ai_text_response}")

    # This method is called when the "Transcribe Speech" button is clicked
    def transcribe_speech(self):
        if self.run_main:  # We transcribe speech only if a conversation is active
            response = transcribe_speech()
            if response is not None:
                self.conversation.append({"role": "user", "content": response})
                insert_message(self.conversation_id, len(
                    self.conversation), "user", response)
                # We add the user response to the conversation display
                self.conversation_display.append(f"User: {response}")


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

    starting_prompt = [{"role": "system", "content": f"Your name is Yarrow and you are interviewing the candidate for a product management position at a tech company. Your responses wi The candidate's name is Brooks. Respond as though you are the interviewer and the candidate is the interviewee. Be extremely critical of the candidate's answers. The first question you should ask the candidate is: {starting_question}"},
                       {"role": "user", "content": "Hi, my name is Brooks, I'm excited to be here today. Let's get started."}]
    return starting_prompt, starting_question


# If this script is being run directly, we create a QApplication and our MainWindow
if __name__ == "__main__":
    # We create a QApplication, which is necessary for any PyQt5 application
    app = QApplication([])
    # We create our MainWindow, passing in our create conversation function
    win = MainWindow(create_conversation)
    win.show()  # We show our MainWindow
    app.exec()  # We start the event loop of our application


from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt
import sys

import pyaudio
import sqlite3
from random_pm_question import generate_random_question as generate_question
from ai_analysis import create_and_play_ai_response
from user_speech_to_text import transcribe_speech

def create_GUI(main_function):
    app = QApplication([])

    window = QWidget()
    window.setWindowTitle("Interview Practice")

    layout = QVBoxLayout()

    welcome_label = QLabel("Hello and welcome to the interview")
    layout.addWidget(welcome_label)

    run_main = False

    def start_main():
        nonlocal run_main
        run_main = True
        main(run_main)

    def stop_main():
        nonlocal run_main
        run_main = False

    start_button = QPushButton('Start')
    start_button.clicked.connect(start_main)
    layout.addWidget(start_button)

    stop_button = QPushButton('Stop')
    stop_button.clicked.connect(stop_main)
    layout.addWidget(stop_button)

    window.setLayout(layout)
    window.show()

    sys.exit(app.exec())

def insert_message(conversation_id, message_id, role, content):
    conn = sqlite3.connect('conversations.db')
    c = conn.cursor()

    c.execute('''
        INSERT INTO messages(conversation_id, message_id, role, content)
        VALUES (?, ?, ?, ?)
    ''', (conversation_id, message_id, role, content))

    conn.commit()
    conn.close()


def main(run_main):
    if run_main:

        print("Welcome to the negotiaton practice program!")

        # create starting question
        starting_question = generate_question()
        print(starting_question)

        while run_main:

            # ------ INTERVIEWING AI ------ #

            # This is the prompt that the AI will use to start the conversation. It can be changed to anything you want. Currently it is set to introduce the AI and ask the user to tell them about their work experience.
            conversation = [
                {"role": "system", "content": f"Your name is Yarrow and you are interviewing the candidate for a product management position at a tech company. Your responses wi The candidate's name is Brooks. Respond as though you are the interviewer and the candidate is the interviewee. Be extremely critical of the candidate's answers. The first question you should ask the candidate is: {starting_question}"},
                {"role": "user", "content": "Hi, my name is Brooks, I'm excited to be here today. Let's get started."},
            ]

            # In the future I want to improve the AI prompting or spawn a secondary AI to continuously evaluate the user's responses

            while True:
                print("starting loop")
                ai_text_response, path_to_audio = create_and_play_ai_response(
                    conversation)
                print("Interviewer: ", ai_text_response)
                print("path to audio: ", path_to_audio)

                if "[satisfied]" in ai_text_response:
                    ai_text_response = ai_text_response.replace(
                        "[satisfied]", "").strip()
                    break
                
                conversation.append(
                    {"role": "assistant", "content": ai_text_response})
                
                insert_message("interview", len(conversation),
                               "assistant", ai_text_response)

                response = transcribe_speech()

                if response is None:
                    continue

                conversation.append({"role": "user", "content": response})
                insert_message("interview", len(
                    conversation), "user", response)
                print(conversation)

        pass
    run_main = False
if __name__ == "__main__":
    create_GUI(main)

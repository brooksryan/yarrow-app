import sqlite3

def create_table():
    conn = sqlite3.connect('conversations.db') # Creates a database file named 'conversations.db' if it doesn't exist
    c = conn.cursor()

    # Create table named 'messages' if it doesn't exist
    c.execute('''
        CREATE TABLE IF NOT EXISTS messages(
            conversation_id TEXT,
            message_id INTEGER,
            role TEXT,
            content TEXT
        )
    ''')

    conn.commit()
    conn.close()

create_table()
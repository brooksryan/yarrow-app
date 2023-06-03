import sqlite3

import pandas as pd

# Establish a connection to the SQLite database
conn = sqlite3.connect('conversations.db')

# Define a SQL query to get all user-assistant pairs from the messages table
query = '''
    SELECT
        a.conversation_id,
        a.content AS Question,
        b.content AS Answer
    FROM
        messages AS a
    JOIN
        messages AS b
    ON
        a.conversation_id = b.conversation_id
    WHERE
        a.conversation_id != 'interview' AND
        a.role = 'assistant' AND
        b.role = 'user' AND
        b.message_id = a.message_id + 1
'''

# Execute the SQL query and fetch the data into a DataFrame
df = pd.read_sql_query(query, conn)

# Write the DataFrame to a CSV file
df.to_csv('questions_and_answers.csv', index=False)

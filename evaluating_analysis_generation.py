import csv
import datetime

import pandas as pd

# Assuming your refactored script is saved in a file named ai_evaluation.py
import ai_evaluation

# Read the CSV file
# df = pd.read_csv("evaluator_test_datasets\questions_and_answers.csv") # full dataset
df = pd.read_csv("evaluator_test_datasets\questions_and_answers copy.csv") # small dataset

# Prepare a list to store the results
results = []

# Iterate through the rows in the dataframe
for i, row in df.iterrows():
    question = row["Question"]
    answer = row["Answer"]

    # Prepare the conversation based on question and answer
    conversation = [{"role": "assistant", "content": question},
                    {"role": "user", "content": answer}]

    try:
        # Evaluate the conversation
        score, feedback = ai_evaluation.parse_and_evaluate_conversation (
            conversation)
        cannot_parse = ""
        
        if score == -1:
            print("error parsing conversation")
            cannot_parse = True

    except Exception as e:
        # If an error occurs while evaluating the conversation, set score and feedback to None and note the error
        score, feedback = None, None
        cannot_parse = f"Error occurred while parsing AI response: {str(e)}"

    # Append the results to the results list
    results.append([question, answer, score, feedback, cannot_parse])

# create string for folder path to save results current datetime
todays_date = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
csv_save_location = "evaluation_tests/" + todays_date + "_results.csv"
text_save_location = "evaluation_tests/" + todays_date + "_results_analysis.txt"

# Write the results to a new CSV file
with open(csv_save_location, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Question", "Answer", "Score",
                    "Feedback", "Cannot be Parsed"])
    writer.writerows(results)

#load the csv I just created and count the number of rows with a score of -1
df = pd.read_csv(csv_save_location)

cannot_parse_count = str(df[df['Score'] == -1].shape[0])

message_to_save = f'''
    results for test: {csv_save_location} \nNumber of rows with 'Cannot be Parsed':{cannot_parse_count}
    '''

with open(text_save_location, "w") as f:
    f.write(message_to_save)

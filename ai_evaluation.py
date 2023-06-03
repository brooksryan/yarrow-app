# takes in a conversation and evaluates the users most recent response. The file needs to parse the conversation to extract the most recent user response, and the question asked of the user. Then, the file needs to evaluate the user response and return a boolean value indicating whether the user response was good or bad.

import json

import openai

# test conversation
sample_conversation = [{"role": "system", "content": "Your name is Yarrow and you are interviewing the candidate for a engineering position at a tech company. Your responses wi The candidate's name is Brooks. Respond as though you are the interviewer and the candidate is the interviewee. Be extremely critical of the candidate's answers. The first question you should ask the candidate is: heyo"},
                       {"role": "user", "content": "Hi, my name is Brooks, I'm excited to be here today. Let's get started."},
                       {"role": "system", "content": "What do you see as a Product Manager’s main role within product development?"},
                       {"role": "user", "content": "I think you're a piece of shit and you shouldn't have a job"}]


# takes in dictionary and takes the last two items in the dictionary and parses into a string
def parse_conversation_into_string(conversation):

    # takes the last two items in the conversation list and concatenates them into a string with the format question:content
    concatenated_string_of_conversation = "Interviewer:" + \
        conversation[-2]["content"] + "\n" + \
        "Candidate:" + conversation[-1]["content"]

    return concatenated_string_of_conversation


def create_conversation_with_expected_outputs_from_user(system_prompt, conversation_analysis_pairs):
    # The initial system prompt
    conversation = [{"role": "system", "content": system_prompt}]

    # Iterate through the user/assistant pairs
    for conversation, analysis in conversation_analysis_pairs:
        # Add user response
        conversation.append({"role": "user", "content": conversation})

        # Add assistant response
        conversation.append(
            {"role": "assistant", "content": analysis})

    return conversation


# analyzes cadidate answers
def analyze_candidate_answer(text_to_evaluate):
    prompt = '''AI Personality: Critical Analyst
    I'm going to give you a series of questions along with the interviewee's answers. For each pair, rate the answer on a scale from 1 (poor) to 5 (excellent), providing a brief qualitative feedback for each score. The criteria for evaluation should include the following: relevance of the response to the question, depth and quality of the response, clarity and coherence of the response, and the level of detail provided. In your qualitative feedback, provide a critical analysis of the strengths and weaknesses of the interviewee's response.
    !important: Always format your response as a JSON object with attributes exactly as show below:  
    
    ```json
    {
        "score": 5,
        "qualitative_feedback": "The candidate showed excellent problem-solving and interpersonal skills, demonstrating their ability to resolve team conflicts effectively."
    } 
    ```
    
    Here are two example interview questions and responses, as well as two example outputs: 
    Input:
    Interviewer: Can you tell us about a time when you had to deal with a difficult team member?
    Candidate: In my previous job, I had a team member who often missed deadlines. I sat down with him to understand his challenges, and we worked out a schedule that was more manageable for him. This improved our team's productivity.
    Output:
    
    ```json
    {
        "score": 5,
        "qualitative_feedback": "The candidate showed excellent problem-solving and interpersonal skills, demonstrating their ability to resolve team conflicts effectively."
    }
    ```

    Input:
    Interviewer: What interests you about this position?
    Candidate: Honestly, I just need a job and the salary for this position is quite attractive.
    Output:
    ```json
    {
        "score": 1,
        "qualitative_feedback": "The response lacks enthusiasm and a genuine interest in the position or the company. It's crucial for a candidate to be motivated by more than just a paycheck."
    }
    ```

    '''

    conversation = [{"role": "system", "content": prompt},
                    {"role": "user", "content": text_to_evaluate}]

    # print the conversation
    print("~~~ this is the conversation ~~~ \n",
          conversation, "\n ~~~ end conversation ~~~")
    # print length of conversation
    print("~~~ this is the length of the conversation ~~~ \n", len(
        conversation), "\n ~~~ end length of conversation ~~~")

    # send the conversation to GPT-3
    retry_counter = 0
    while True:
        try:
            res = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=conversation
            )
            gpt3_response = res['choices'][0]['message']['content'].strip()
            break

        except openai.error.RateLimitError as e:
            print("RateLimitError: error with gpt3 response")
            print("retrying...")
            retry_counter += 1
            if retry_counter > 10:
                print("retry limit exceeded")
                gpt3_response = {"score": -1, "qualitative_feedback": e}
                return gpt3_response
            continue

    # convert the response to a JSON object

    print(
        f"~~~ this is the gpt response ~~~ \n {gpt3_response}) \n ~~~ end gpt response ~~~")

    print("\n this is the tpye of the gpt3 response: ", type(gpt3_response))

    # convert the response to a JSON object
    try:
        gpt3_response = json.loads(gpt3_response)

    except TypeError as error:
        print("TypeError: error parsing gpt3 response")
        gpt3_response = {"score": -1, "qualitative_feedback": error}
        return gpt3_response

    except Exception as error:
        print("Generic error: error parsing gpt3 response")
        gpt3_response = {"score": -1, "qualitative_feedback": error}
        return gpt3_response

    # return the response
    return gpt3_response


# takes in a conversation and returns a score and qualitative feedback
def parse_and_evaluate_conversation(conversation):
    evaluated_response = analyze_candidate_answer(
        parse_conversation_into_string(conversation))
    score = evaluated_response["score"]
    print(score)
    qualitative_feedback = evaluated_response["qualitative_feedback"]
    return score, qualitative_feedback


# if run as main test
if __name__ == "__main__":
    # parse_conversation_into_string(sample_conversation) # test parse_conversation_into_string
    print(analyze_candidate_answer(parse_conversation_into_string(
        sample_conversation)))  # test analyze_candidate_answer

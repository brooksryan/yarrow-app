# takes in a conversation and evaluates the users most recent response. The file needs to parse the conversation to extract the most recent user response, and the question asked of the user. Then, the file needs to evaluate the user response and return a boolean value indicating whether the user response was good or bad.

import openai

sample_conversation = [{"role": "system", "content": "Your name is Yarrow and you are interviewing the candidate for a product management position at a tech company. Your responses wi The candidate's name is Brooks. Respond as though you are the interviewer and the candidate is the interviewee. Be extremely critical of the candidate's answers. The first question you should ask the candidate is: heyo"},
                       {"role": "user", "content": "Hi, my name is Brooks, I'm excited to be here today. Let's get started."},
                       {"role": "system", "content": "What do you see as a Product Manager’s main role within product development?"},
                       {"role": "user", "content": "I think you're a piece of shit and you shouldn't have a job"}]

def parse_conversation_into_string(conversation):

    #takes the last two items in the conversation list and concatenates them into a string with the format question:content
    concatenated_string_of_conversation = "Interviewer:" + conversation[-2]["content"] + "\n" + "Candidate:" + conversation[-1]["content"]
    
    return concatenated_string_of_conversation



def analyze_candidate_answer(text_to_evaluate):
    prompt = '''AI Personality: Critical Analyst
    I'm going to give you a series of questions along with the interviewee's answers. For each pair, rate the answer on a scale from 1 (poor) to 5 (excellent), providing a brief qualitative feedback for each score. The criteria for evaluation should include the following: relevance of the response to the question, depth and quality of the response, clarity and coherence of the response, and the level of detail provided. In your qualitative feedback, provide a critical analysis of the strengths and weaknesses of the interviewee's response.
    Format your response as a JSON object with attributes "score:" and "qualitative_feedback:" for each question. Here are two example interview questions and responses, as well as two example outputs: 
    Input:
    Interviewer: Can you tell us about a time when you had to deal with a difficult team member?
    Candidate: In my previous job, I had a team member who often missed deadlines. I sat down with him to understand his challenges, and we worked out a schedule that was more manageable for him. This improved our team's productivity.
    Output:
    {
        "score": 5,
        "qualitative_feedback": "The candidate showed excellent problem-solving and interpersonal skills, demonstrating their ability to resolve team conflicts effectively."
    }
    
    Input:
    Interviewer: What interests you about this position?
    Candidate: Honestly, I just need a job and the salary for this position is quite attractive.
    Output:
    {
        "score": 1,
        "qualitative_feedback": "The response lacks enthusiasm and a genuine interest in the position or the company. It's crucial for a candidate to be motivated by more than just a paycheck."
    }
    '''

    conversation = [{"role": "system", "content": prompt},{"role": "user", "content": text_to_evaluate}]

    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation
    )
    gpt3_response = res['choices'][0]['message']['content'].strip()

    # convert the response to a JSON object
    gpt3_response = eval(gpt3_response)

    return gpt3_response

def parse_and_evaluate_conversation(conversation):
    evaluated_response = analyze_candidate_answer(parse_conversation_into_string(conversation))
    score = evaluated_response["score"]
    qualitative_feedback = evaluated_response["qualitative_feedback"]
    return score, qualitative_feedback


# if run as main test
if __name__ == "__main__":
    parse_conversation_into_string(sample_conversation)
    print(analyze_candidate_answer(parse_conversation_into_string(sample_conversation)))
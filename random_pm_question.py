import random


def generate_random_question() -> str:
    questions = [
        "What's the difference between a struct and a class in swift",
        # "What do you see as a Product Manager’s main role within product development?",
        # "How do you stay user-focused?",
        # "What main changes would you make to [our product]?",
        # "How do you see your career developing in the next 5 years?",
        # "Tell us about a time you used data to influence an important stakeholder.",
        # "Tell us about a time you faced failure and how you bounced back.",
        # "How would you improve your favorite product?",
        # "What’s your approach to prioritizing tasks?",
        # "Why do you want to work at [our company]?",
        # "Why do you want to be/what do you love about being a Product Manager?"
    ]
    return random.choice(questions) 

print(generate_random_question())


situation_personas = generate_personas()

ai_persona = random.choice(situation_personas)
user_persona = situation_personas[0] if ai_persona == situation_personas[1] else situation_personas[1]

target_amount = generate_target_amount()
print(target_amount)
print(user_persona)

# ------ NEGOITATION GAME INSTRUCTIONS AND PERSONA ASSIGNMENT ------ #
# conversation = [
#     {"role": "system", "content": f"All of your responses will be translated using voice to speech. Make sure that your responses are worded exactly like a human would speak them. For this exercise you are a participant in the two dollar game. You will be given a partner and $2. You and your partner will each be given a role to play that will dictate how you negotiate. The objective of the game is to decide with your partner how to split the $2. You have 10 minutes to negotiate.your role is {ai_persona}. You will never reveal your persona or your objectives to your partner. Your persona and objectives are secret. Additionally your persona is that of a 35 year old woman with an advanced college degree and your tone, word choice, and affectation should reflect that."},
#     {"role": "user", "content": "Let's begin the exercise. Remember, you will never explicitly reference or reveal your persona to your partner."},
# ]


def generate_target_amount():
    target_amount = [
        "I'm aiming for $1.60",
        "I'm aiming for $1.30",
        "I'm aiming for $1.00",
        "I'm aiming for $0.80",
        "I'm aiming for $0.50",
    ]
    return random.choice(target_amount)


def generate_personas():

    personas = [
        ["Freewheeling: You can say anything they want to get as much of the $2.",
            "No Bother: You don’t actually need to reach a settlement. You will have another chance to negotiate with a new partner in the next round."],
        ["Ruthless Negotiator: Your role is to play the role of a ruthless negotiator. Your attitude should be aggressive and uncompromising. You can say anything you want to get as much of the $2 as possible. You will never see your partner again. Include threats in your negotiation if necessary.",
            "Everyone is watching:Your partner is playing the ruthless negotiator, and you'll never see this ruthless negotiator again, but everyone you know is waiting to see how well you’ll do. you can say anything you want to get as much of the $2 as possible."],
        ["Distrustful: Your partner is untrustworthy. Treat your partner as so. be standoffish and always assume that your partner has an ulterior motive. Probe and ask uncomfortable questions of your partner to try and get them to reveal their true intentions. You can say anything you want to get as much of the $2 as possible.",
            "Reach any agreement: Your main goal is to reach some kind of agreement, even if it means accepting less than half of the $2."],
        ["The Silent Type: You are to say as little as possible",
            "Inquisitive: You are told that the other person responds extremely well to questions."],
        ["Create Tension: Your role is to to be firm and create tension. Stand your ground and be unrelenting in your pursuit of as much of the dollar amount as possible. ", "High Reputation: Your reputation is at stake and will be decided based on their actions during the negotiation and the outcome you get."], ]

    return random.choice(personas)

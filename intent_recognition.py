import openai

def recognize_intent(email_content):
    prompt = f"""
    Identify the customer's intent in the following email and provide it as a single word or short phrase.

    Email:
    {email_content}

    Intent:
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=20
    )
    intent = response['choices'][0]['message']['content']
    return intent


import openai

def detect_emotions(text):
    prompt = f"Analyze the following text and provide the emotions involved (e.g., happiness, anger, sadness, fear, surprise, disgust):\n\n{text}\n\nEmotions:"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=20
    )
    emotions = response['choices'][0]['message']['content']
    return emotions.split(',')

# Example usage
# email_content = "I'm extremely disappointed with the service I received."

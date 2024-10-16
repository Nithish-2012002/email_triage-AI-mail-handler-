import openai
from google.cloud import translate_v2 as translate

# Detect Language
def detect_language(text):
    prompt = f"Detect the language of the following text :\n\n{text}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=5
    )
    language = response['choices'][0]['message']['content']
    return language

# Translate Text
def translate_text(text, dest_language='en'):
    try:
        translate_client = translate.Client()
        result = translate_client.translate(text, target_language=dest_language)
        return result['translatedText']
    except Exception as e:
        return f"Error translating text: {e}"


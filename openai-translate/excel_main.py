import pandas as pd
import openai
import json
from datetime import datetime

# Initialize OpenAI API (replace 'your-api-key' with your actual API key)
openai.api_key = 'sk-proj-U0Hcuszuv8bwBgzqHcVyT3BlbkFJwZywdlOm8m49pG6ZIiSq'

# Load the Excel file
file_path = 'input.xlsx'
df = pd.read_excel(file_path)

# Function to translate text using OpenAI
def translate_text(text, target_language):
    prompt = f"Translate this text to {target_language}: {text}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000,
        temperature=0.5
    )
    translated_text = response.choices[0].message['content'].strip()
    return translated_text

# Dictionary of target languages and their codes

languages = {
    "Catalan": "ca",
    "Arabic": "ar",
    "Dutch": "nl",
    "French": "fr",
    "German": "de",
    "Portuguese": "pt",
    "Italian": "it",
    "Romansh": "rm",
    "Spanish": "es",
    "Chinese": "zh",
    "Vietnamese": "vi",
    "Korean": "ko",
    "Amharic": "am",
    "Hindi": "hi",
    "English": "en",
    "Standard Arabic": "ar"
}

# Initialize a dictionary to store the translations
translations = {}

# Translate the 'Title' and 'Description' columns for each language
for language, code in languages.items():
    translations[code] = {
        'Title': df['Title'].apply(lambda x: translate_text(x, language)).tolist(),
        'Description': df['Description'].apply(lambda x: translate_text(x, language)).tolist()
    }

# Generate the filename with the current datetime
current_datetime = datetime.now().strftime('%Y%m%d_%H%M%S')
output_file_path = f'json/translations_{current_datetime}.json'
with open(output_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(translations, json_file, ensure_ascii=False, indent=4)

print(f"Translation completed. The translated data is saved as {output_file_path}")

import pandas as pd
import openai
import json
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()
# Initialize OpenAI API (replace 'your-api-key' with your actual API key)
openai.api_key = os.getenv('OPENAI_API_KEY')

# Load the Excel file
file_path = 'Device-Reasons.xlsx'
df = pd.read_excel(file_path)

# Function to translate text using OpenAI
def translate_text(text, target_language):
    prompt = f"Translate the following text to {target_language} without any explanations or additional information: {text}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that provides direct translations."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000,
        temperature=0.5
    )
    translated_text = response.choices[0].message['content'].strip()
    return translated_text

# Dictionary of target languages and their codes
languages = {
    "Dutch": "nl",
    "French": "fr",
    "German": "de",
    "Italian": "it",
    "Spanish": "es",
    "Portuguese": "pt"
}

# Initialize a dictionary to store translations for each language
translations = {lang_code: {} for lang_code in languages.values()}

# Translate each Title and Description
for idx, row in df.iterrows():
    titleKey = row['Code']
    # descriptionKey = row['Descritpion Code']
    title = row['Value']
    # description = row['Description']
    if 'en' not in translations:
        translations['en'] = {}

    translations['en'][titleKey] = title

    for language, lang_code in languages.items():
        translated_title = translate_text(title, language)
        #translated_description = translate_text(description, language)

        translations[lang_code][f'{titleKey}'] = translated_title
        #translations[lang_code][f'{descriptionKey}'] = translated_description

# Save the translations to separate JSON files for each language
for lang_code, translation in translations.items():
    with open(f'json/DSR/{lang_code}.json', 'w', encoding='utf-8') as json_file:
        json.dump(translation, json_file, ensure_ascii=False, indent=4)

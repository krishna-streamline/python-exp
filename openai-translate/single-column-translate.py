import pandas as pd
import openai
import os
from dotenv import load_dotenv
import json

# OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')
# Load the Excel file
df = pd.read_excel('Localization-master-sheet.xlsx', header=None)

# Extract the single column of strings
strings = df[0].tolist()
# print(df[0].tolist())


# Languages for translation
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
    "Standard Arabic": "ar"
}

# Function to translate text using GPT-3.5-turbo
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

# Function to translate a list of strings
def translate_strings(strings):
    translations = {lang: [] for lang in languages.keys()}
    translations["English"] = strings

    for string in strings:
        for lang in languages.keys():
            translated_text = translate_text(string, lang)
            translations[lang].append(translated_text)

    return translations

# Translate the strings
translated_strings = translate_strings(strings)

# Save to Excel file
with pd.ExcelWriter('translations.xlsx', engine='xlsxwriter') as writer:
    for lang, translation in translated_strings.items():
        df_translation = pd.DataFrame(translation, columns=[lang])
        df_translation.to_excel(writer, sheet_name=lang, index=False)

print("Translations saved to translations.xlsx")

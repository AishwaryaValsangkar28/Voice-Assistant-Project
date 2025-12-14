import whisper
from googletrans import Translator

# Load Whisper model (small is accurate+fast)
model = whisper.load_model("small")

# # Step 1: Ask for audio file path
# audio_path = input("Enter the path to your audio file (e.g. lecture.mp3): ")

# DEV: Hard-coded path
audio_path = r"C:\Users\valsa\OneDrive\Desktop\pruefungstraining_1_hoeren_a1_erwachsene-v2 - Trim.mp4"

print("\n audio File found")

# PROD: User input
# audio_path = input("Enter the path to your audio file: ").strip().strip('"')


# Step 2: Transcribe audio
print("\nTranscribing audio... Please wait.")
result = model.transcribe(audio_path)

original_text = result["text"]
detected_lang = result["language"]

print("\n--- Original Transcription ---")
print(f"(Detected language: {detected_lang})")
print(original_text)

# Step 3: Ask for target language
target_lang = input("\nEnter the language you want to translate into (e.g. 'en' for English, 'fr' for French): ")

# Step 4: Translate using googletrans
translator = Translator()
translation = translator.translate(original_text, src=detected_lang, dest=target_lang)

# Step 5: Show results
print("\n--- Translated Text ---")
print(f"(Translated from {detected_lang} to {target_lang})")
print(translation.text)

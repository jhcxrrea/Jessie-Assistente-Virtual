import pyttsx3

def print_available_voices():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    for idx, voice in enumerate(voices):
        print(f"Voz {idx + 1}:")
        print(f" - ID: {voice.id}")
        print(f" - Nome: {voice.name}")
        print(f" - Idioma: {voice.languages[0]}")
        print(f" - Gênero: {voice.gender}")
        print(f" - Idade: {voice.age}")
        print("\n")

print_available_voices()

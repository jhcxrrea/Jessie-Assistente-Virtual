import time
import speech_recognition as sr
import pyttsx3
from gtts import gTTS
import webbrowser
import sys
import os
import requests
from playsound import playsound
from hugchat import hugchat
from hugchat.login import Login
from modules.get_env import print_env
import tkinter as tk
from tkinter import scrolledtext
import threading
from datetime import datetime
from googletrans import Translator
import random
import sympy as sp

# Initialize global variables for latency and history
latency_info = {
    'gTTS': 0.0,
    'pyttsx3': 0.0,
    'Speech Recognition': 0.0,
    'Weather Request': 0.0,
    'Command Processing': 0.0
}
history = []
commands_history = []
assistant_thread = None
stop_event = threading.Event()
assistant_ready = False

# Function to speak using gTTS with pyttsx3 fallback
def speak(text):
    global latency_info
    try:
        start_time = time.time()
        if not isinstance(text, str):
            text = str(text)
        tts = gTTS(text=text.strip(), lang='pt', slow=False)
        tts.save("response.mp3")
        playsound("response.mp3")
        os.remove("response.mp3")
        end_time = time.time()
        latency_info['gTTS'] = end_time - start_time
    except Exception as e:
        print(f"Erro no gTTS: {e}. Usando pyttsx3 como fallback.")
        speak_pyttsx3(text)

# Fallback function to speak using pyttsx3
def speak_pyttsx3(text, voice_id=None):
    global latency_info
    try:
        start_time = time.time()
        engine = pyttsx3.init()
        engine.setProperty('rate', 210)
        engine.setProperty('volume', 1.0)

        voices = engine.getProperty('voices')
        if voice_id is not None and 0 <= voice_id < len(voices):
            engine.setProperty('voice', voices[voice_id].id)
        else:
            for voice in voices:
                if "female" in voice.name.lower():
                    engine.setProperty('voice', voice.id)
                    break

        engine.say(text)
        engine.runAndWait()
        end_time = time.time()
        latency_info['pyttsx3'] = end_time - start_time
    except Exception as e:
        print(f"Erro no pyttsx3: {e}")

# Function to listen to user input
def listen():
    global latency_info
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("Diga algo...")
        audio = r.listen(source, phrase_time_limit=5)
        try:
            start_time = time.time()
            statement = r.recognize_google(audio, language='pt-BR')
            end_time = time.time()
            latency_info['Speech Recognition'] = end_time - start_time
            print(f"Você disse: {statement}\n")
            history.append(f"Você disse: {statement}")
            return statement.lower()
        except sr.UnknownValueError:
            print("Não entendi o que você disse...")
            speak("Desculpe, não entendi o que você disse.")
            return None
        except sr.RequestError:
            print("Não foi possível acessar o serviço de reconhecimento de voz.")
            speak("Não foi possível acessar o serviço de reconhecimento de voz.")
            return None

# Function to create a chatbot session
def create_chatbot_session():
    try:
        env_vars = print_env(['pass', 'email'])
        senha = env_vars['pass']
        email = env_vars['email']

        sign = Login(email, senha)
        cookies = sign.login()

        cookie_path_dir = "./cookies_snapshot"
        sign.saveCookiesToDir(cookie_path_dir)

        chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
        return chatbot
    except Exception as e:
        print(f"Ocorreu um erro durante o login: {e}")
        speak("Ocorreu um erro durante o login no chatbot. Verifique suas credenciais e tente novamente.")
        return None

# Function to search and play a video or music on YouTube
def play_youtube(query):
    url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
    webbrowser.open(url)
    speak(f"Ok mestre, abrindo a busca por '{query}' no YouTube.")
    commands_history.append(f"Played YouTube search for '{query}'")

# função para lidar com a entrada do usuário após o comando "tocar música"
def handle_music_request():
    speak("Por favor, diga o nome da música que você deseja tocar.")
    music_query = listen()  # Obtenha a consulta de música do usuário
    if music_query:
        play_youtube(music_query)


# Function to open specific websites
def open_website(url):
    webbrowser.open(url)
    speak(f"Ok mestre, abrindo")
    commands_history.append(f"Opened website '{url}'")

# Function to get the weather forecast (specific example)
def get_weather():
    global latency_info
    city = "Ananindeua"
    url = f"https://wttr.in/{city}?format=%c+%t"
    try:
        start_time = time.time()
        response = requests.get(url)
        end_time = time.time()
        latency_info['Weather Request'] = end_time - start_time
        if response.status_code == 200:
            return response.text.strip()
        else:
            return "Não foi possível obter a previsão do tempo no momento."
    except requests.RequestException:
        return "Não foi possível obter a previsão do tempo no momento."

# Function to get the current time in different cities
def get_world_time(city):
    cities = {
        "nova york": "America/New_York",
        "londres": "Europe/London",
        "tokyo": "Asia/Tokyo"
    }
    if city.lower() in cities:
        timezone = cities[city.lower()]
        url = f"http://worldtimeapi.org/api/timezone/{timezone}"
        try:
            response = requests.get(url)
            data = response.json()
            current_time = data['datetime']
            return f"A hora atual em {city} é {current_time}."
        except requests.RequestException:
            return "Não foi possível obter a hora mundial."
    else:
        return "Cidade não suportada."

# Function to get the dollar exchange rate
def get_dollar_rate():
    try:
        response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
        data = response.json()
        rate = data['rates']['BRL']
        return f"A cotação do dólar é {rate:.2f} reais."
    except requests.RequestException:
        return "Não foi possível obter a cotação do dólar."

# Function to get the definition of a word
def get_definition(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    try:
        response = requests.get(url)
        data = response.json()
        definition = data[0]['meanings'][0]['definitions'][0]['definition']
        return f"A definição de '{word}' é: {definition}"
    except (requests.RequestException, KeyError):
        return "Não foi possível obter a definição da palavra."

# Function to generate a random number
def generate_random_number():
    return f"O número aleatório gerado é {random.randint(1, 100)}."

# Function to create a note
def create_note(note_text):
    global history
    with open("notes.txt", "a") as file:
        file.write(note_text + "\n")
    history.append(f"Nota criada: {note_text}")
    speak("Nota criada com sucesso.")

# Function to convert units
def convert_units(command):
    try:
        if "celsius" in command and "fahrenheit" in command:
            celsius = float(command.split("celsius")[0].strip())
            fahrenheit = celsius * 9/5 + 32
            return f"{celsius} graus Celsius é igual a {fahrenheit:.2f} graus Fahrenheit."
        elif "fahrenheit" in command and "celsius" in command:
            fahrenheit = float(command.split("fahrenheit")[0].strip())
            celsius = (fahrenheit - 32) * 5/9
            return f"{fahrenheit} graus Fahrenheit é igual a {celsius:.2f} graus Celsius."
        else:
            return "Comando de conversão não reconhecido."
    except ValueError:
        return "Valor inválido para conversão."
    
# Function to calculate expressions using sympy
def calcular(expression):
    try:
        # Remove "calcular" do início e espaços extras
        expression = expression.lower().replace("calcular", "").strip()
        # Substitua '*' por ' * ' para garantir que a multiplicação seja corretamente identificada
        expression = expression.replace('*', ' * ')
        # Use sympy para simplificar e calcular a expressão
        expr = sp.sympify(expression)
        result = sp.N(expr)  # Calcula o resultado numérico
        # Formate o resultado com 2 casas decimais
        formatted_result = f"{result:.2f}"
        return f"O resultado é: {formatted_result}"
    except sp.SympifyError:
        return "Erro na análise da expressão. Verifique a sintaxe."
    except Exception as e:
        return f"Erro ao calcular a expressão: {e}"

# Dictionary of commands
commands = {

    "desligar": lambda: (speak("Até mais mestre! Desligando."), root.destroy(), sys.exit()),
    "adeus": lambda: (speak("Até logo! Foi um prazer."), root.destroy(), sys.exit()),
    "hora": lambda: speak(time.strftime("%H:%M")),
    "data": lambda: speak(time.strftime("%d/%m/%Y")),
    "quem é você": lambda: speak("Olá, eu sou a Jessie, seu assistente pessoal!"),
    "meu nome é jessie": lambda: speak("Ah, você também se chama Jessie? Que coincidência! O meu criador se inspirou na grandiosa mulher que ele tem."),
    "abrir youtube": lambda: open_website("https://www.youtube.com"),
    "abrir spotify": lambda: open_website("https://open.spotify.com"),
    "tocar música": handle_music_request,
    "previsão do tempo": lambda: speak(get_weather()),
    "reproduzir música": lambda: play_youtube("música"),
    "reproduzir vídeo": lambda: play_youtube("vídeo"),
    "abrir google": lambda: open_website("https://www.google.com"),
    "abrir amazon": lambda: open_website("https://www.amazon.com.br"),
    "pesquisar": lambda query: webbrowser.open(f"https://www.google.com/search?q={query.replace(' ', '+')}"),
    "notícias": lambda: open_website("https://news.google.com"),
    "clima": lambda: speak(get_weather()),
    "definir lembrete": lambda: speak("Por favor, diga o lembrete que você deseja definir."),
    "calcular": lambda expression: speak(calcular(expression)),
    "cotação do dólar": lambda: speak(get_dollar_rate()),
    "hora mundial": lambda city: speak(get_world_time(city)),
    "criar nota": lambda note: create_note(note.replace("criar nota", "").strip()),
    "converter": lambda query: speak(convert_units(query)),
    "jessie": lambda: speak("Sim, mestre? Como posso ajudar você?")
}

# Function to update the GUI with new information
def update_gui():
    global latency_info, history, commands_history, assistant_ready

    # Update latency info
    latency_label.config(text=f"gTTS: {latency_info['gTTS']:.2f}s | "
                              f"pyttsx3: {latency_info['pyttsx3']:.2f}s | "
                              f"Speech Recognition: {latency_info['Speech Recognition']:.2f}s | "
                              f"Weather Request: {latency_info['Weather Request']:.2f}s | "
                              f"Command Processing: {latency_info['Command Processing']:.2f}s")
    
    # Update status message
    status_message = "Carregando" if not assistant_ready else "Pode Falar!"
    status_label.config(text=status_message, fg="red" if not assistant_ready else "green")
    
    # Update history and commands history
    history_text.config(state=tk.NORMAL)
    history_text.delete(1.0, tk.END)
    history_text.insert(tk.END, "\n".join(history))
    history_text.see(tk.END)  # Scroll to the end to show the latest messages
    history_text.config(state=tk.DISABLED)

    commands_text.config(state=tk.NORMAL)
    commands_text.delete(1.0, tk.END)
    commands_text.insert(tk.END, "\n".join(commands_history))
    commands_text.see(tk.END)  # Scroll to the end to show the latest messages
    commands_text.config(state=tk.DISABLED)

    root.after(1000, update_gui)

# Function to stop the assistant and clean up resources
def stop_assistant():
    global stop_event
    stop_event.set()  # Signal the thread to stop

    if assistant_thread and assistant_thread.is_alive():
        assistant_thread.join()  # Wait for the thread to finish

    root.quit()  # Close the GUI

# Function to start the assistant and GUI
def start_assistant():
    global assistant_ready
    print("Iniciando o assistente...")
    chatbot = create_chatbot_session()

    if not chatbot:
        print("Não foi possível iniciar o assistente. Verifique os logs para mais informações.")
        speak("Não foi possível iniciar o assistente.")
        return

    # Welcome message
    welcome_message = "Olá! Eu sou a Jessie, seu assistente virtual. Como posso ajudar você hoje?"
    speak(welcome_message)
    history.append(f"Assistente: {welcome_message}")

    assistant_ready = True  # Set assistant to ready state
    while not stop_event.is_set():
        command = listen()
        if command:
            start_time = time.time()
            # Process command
            found_command = False
            for key in commands:
                if key in command:
                    found_command = True
                    if key == "pesquisar":
                        query = command.replace(key, "").strip()
                        commands[key](query)
                    elif key == "calcular":
                        expression = command.replace(key, "").strip()
                        commands[key](expression)
                    elif key == "traduzir para":
                        query = command.replace(key, "").strip()
                        commands[key](query)
                    elif key == "converter":
                        query = command.replace(key, "").strip()
                        commands[key](query)
                    elif key == "criar nota":
                        note = command.replace(key, "").strip()
                        commands[key](note)
                    elif key == "definir lembrete":
                        reminder = command.replace(key, "").strip()
                        commands[key](reminder)
                    elif key == "hora mundial":
                        city = command.replace(key, "").strip()
                        commands[key](city)
                    else:
                        commands[key]()
                    latency_info['Command Processing'] = time.time() - start_time
                    break

            if not found_command:
                try:
                    response = chatbot.chat(command)
                    speak(response)
                    history.append(f"Assistente: {response}")
                except Exception as e:
                    response = f"Ocorreu um erro ao processar o comando: {e}"
                    speak(response)
                    history.append(f"Assistente: {response}")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Jessie - Assistente Virtual")
    root.geometry("800x600")
    root.configure(bg="#121212")  # Dark background color
    root.resizable(True, True)

    # Defina o ícone da janela
    root.iconbitmap("C:/Users/corre/OneDrive/Área de Trabalho/CODE/projetos/Karol Assistente Virtual/Jessie Assistente Virtual(CONCLUIDO)/jessie.ico")  # Substitua pelo caminho do seu arquivo .ico

    # Create widgets with updated styles
    frame = tk.Frame(root, padx=20, pady=20, bg="#1e1e1e")
    frame.pack(fill=tk.BOTH, expand=True)

    # Status message at the top, centered
    status_label = tk.Label(frame, text="Assistente pronto para ouvir!", font=("Roboto", 14, "bold"), fg="green", bg="#1e1e1e")
    status_label.grid(row=0, column=0, columnspan=2, pady=10, sticky="n")

    latency_label = tk.Label(frame, text="Latência", font=("Roboto", 10, "normal"), bg="#1e1e1e", fg="#d1d1d1")
    latency_label.grid(row=1, column=0, columnspan=2, pady=5, sticky="n")

    history_text = scrolledtext.ScrolledText(frame, wrap=tk.WORD, height=15, width=90, state=tk.DISABLED, bg="#2e2e2e", fg="#d1d1d1", font=("Roboto", 12))
    history_text.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

    commands_text = scrolledtext.ScrolledText(frame, wrap=tk.WORD, height=7, width=90, state=tk.DISABLED, bg="#2e2e2e", fg="#d1d1d1", font=("Roboto", 12))
    commands_text.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(2, weight=1)
    frame.rowconfigure(3, weight=1)

    # Bind the window close event to the stop_assistant function
    root.protocol("WM_DELETE_WINDOW", stop_assistant)

    # Start GUI update loop
    root.after(1000, update_gui)

    # Run assistant in a separate thread
    assistant_thread = threading.Thread(target=start_assistant)
    assistant_thread.start()

    # Start GUI main loop
    root.mainloop()

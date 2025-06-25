import requests
from config import BASE_PROMPT

# Обработка запроса
def ask_ollama(prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "mistral",
            "prompt": BASE_PROMPT + prompt,
            "stream": False
        }
    )
    if response.status_code != 200:
            return f"Error: {response.status_code} - {response.text}"
    return response.json()["response"]

# Проверка состояния AI
def ollama_online():
    try:
        response = requests.get("http://localhost:11434")
        return response.status_code == 200
    
    except requests.exceptions.ConnectionError:
        return False

# Разбиение из-за ограничений дискорда
def split_message(text, max_lenght=2000):
    return [text[i:i+max_lenght] for i in range(0, len(text), max_lenght)]
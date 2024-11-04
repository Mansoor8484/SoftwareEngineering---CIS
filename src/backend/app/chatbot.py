import requests
from config import Config

class Chatbot:
    def __init__(self):
        self.api_key = Config.ASSISTANT_API_KEY
        self.base_url = "https://api.ollama.com/chat"  # Adjust as needed

    def get_response(self, user_message):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "input": user_message
        }

        try:
            response = requests.post(self.base_url, headers=headers, json=payload)
            response.raise_for_status()
            chatbot_response = response.json().get('output')
            return chatbot_response
        except requests.exceptions.RequestException as e:
            return f"Error communicating with the chatbot service: {str(e)}"

    # Set Environment Variables in Terminal: export ASSISTANT_API_KEY='your_actual_api_key'

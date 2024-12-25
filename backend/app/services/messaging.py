import os
import requests
from slack_sdk import WebClient
from dotenv import load_dotenv

load_dotenv()

class SlackIntegration:
    def __init__(self):
        self.token = os.environ.get("YOUR_SLACK_BOT_TOKEN")
        if self.token is None:
            raise ValueError("YOUR_SLACK_BOT_TOKEN environment variable not set.")
        self.client = WebClient(token=self.token)  # Initialize the Slack client here
        self.last_error = None

    def send_message(self, channel_id, message):
        try:
            result = self.client.chat_postMessage(channel=channel_id, text=message)
            return result.data
        except Exception as e:
            self.last_error = str(e)
            return None

    def fetch_conversation(self, channel_id):
        try:
            result = self.client.conversations_history(channel=channel_id, limit=10)
            messages = result.get("messages", [])
            return "\n".join(msg.get("text", "") for msg in messages)
        except Exception as e:
            self.last_error = str(e)
            return "", 500

class WhatsAppIntegration:
    def __init__(self):
        self.base_url = "https://graph.facebook.com/v12.0/"
        self.token = "YOUR_WHATSAPP_API_TOKEN"

    def send_message(self, phone_number_id, recipient, message):
        # Implement WhatsApp message sending logic (using the Facebook Graph API)
        pass

    def fetch_conversation(self, thread_id):
        # Simulate fetching WhatsApp conversation
        return "Sample WhatsApp conversation for thread ID: " + thread_id

class TeamsIntegration:
    def __init__(self):
        self.webhook_url = "YOUR_TEAMS_WEBHOOK_URL"

    def send_message(self, message):
        headers = {"Content-Type": "application/json"}
        payload = {"text": message}
        response = requests.post(self.webhook_url, json=payload, headers=headers)
        return response.json()

    def fetch_conversation(self, team_id):
        # Simulate fetching Teams conversation
        return "Sample Teams conversation for team ID: " + team_id
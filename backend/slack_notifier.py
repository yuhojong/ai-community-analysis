from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import os

class SlackNotifier:
    def __init__(self, token: str):
        self.client = WebClient(token=token)

    def post_message(self, channel_id: str, text: str):
        try:
            response = self.client.chat_postMessage(
                channel=channel_id,
                text=text
            )
            return response
        except SlackApiError as e:
            print(f"Error posting message: {e.response['error']}")
            return None

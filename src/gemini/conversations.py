from google.generativeai import ChatSession, GenerativeModel
from pymongo.database import Database

from src.database.character import Character
from src.database.user import User


class Conversation:
    def __init__(
            self,
            author_id: int,
            character: Character
    ):
        self.author_id: int = author_id

        self.character: Character = character

        self.chat: ChatSession = self.setup_chat()

    def ask(self, text: str) -> str:
        self.chat.send_message(text)

        return self.chat.last.text

    def notify(self, habit_title: str) -> str:
        self.chat.send_message()  # TODO: use the notify prompt here

        return self.chat.last.text

    def setup_chat(self) -> ChatSession:
        # Set up the model
        generation_config = {
            "temperature": 0.9,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048,
        }

        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_NONE"
            },
        ]

        # noinspection PyTypeChecker
        model = GenerativeModel(
            model_name="gemini-pro",
            generation_config=generation_config,
            safety_settings=safety_settings
        )

        # noinspection PyTypeChecker
        conversation = model.start_chat(
            history=[
                {
                    "role": "user",
                    "parts": self.character.initial_prompt
                },
                {
                    "role": "model",
                    "parts": "知道了！"
                }
            ]
        )  # TODO: Implement the prompting here based on the characters and improve prompt handling.

        return conversation


class ConversationManager:
    def __init__(self, database: Database):
        self.database: Database = database

        self.conversations: dict[int, Conversation] = {}

    def close_conversation(self, user_id: int):
        if user_id not in self.conversations:
            return

        del self.conversations[user_id]

    def get_conversation(self, user_id: int) -> Conversation:
        if user_id in self.conversations:
            return self.conversations[user_id]

        user_settings = User.find_one(self.database, user_id=user_id)
        character = Character.find_one(self.database, character_id=user_settings.selected_character_id)

        self.conversations[user_id] = Conversation(user_id, character)

        return self.conversations[user_id]

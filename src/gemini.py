from google.generativeai import GenerativeModel


class Gemini:
    def __init__(self, api_key: str):
        self.api_key: str = api_key

    @staticmethod
    def setup_model() -> GenerativeModel:
        generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }

        # noinspection PyTypeChecker
        model = GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config,
        )

        return model

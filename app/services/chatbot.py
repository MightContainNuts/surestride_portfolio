import os
from langchain_community.chat_models import ChatopenAI
from dotenv import load_dotenv

class LangChainHandler:

    def __init__(self, llm):
        load_dotenv()
        self.llm = ChatopenAI(
            model_name="gpt-3.5-turbo",
            temperature=0,
            openai_api_key=os.environ.get("OPENAI_API_KEY"),
        )

    def handle_message(self, message):
        # Process the message using the LLM
        response = self.llm.generate_response(message)
        return response
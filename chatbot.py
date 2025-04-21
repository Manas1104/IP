from google.cloud import dialogflow_v2 as dialogflow
import os
import uuid

# ======== SETUP AUTHENTICATION ========
GOOGLE_AUTH_PATH = r"C:\Users\manas\Downloads\manas-vlav-a3997f0be8e2.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_AUTH_PATH

# ======== ChatBot Base Class ========
class ChatBot:
    def __init__(self, name="AI Bot"):
        self.name = name

    def get_response(self, user_input):
        raise NotImplementedError("Subclasses should implement this method.")

# ======== Dialogflow ChatBot Class ========
class DialogflowChatBot(ChatBot):
    def __init__(self, project_id, language_code='en', name="Dialogflow Assistant"):
        super().__init__(name)
        self.project_id = project_id
        self.session_id = str(uuid.uuid4())  # Unique session for context tracking
        self.language_code = language_code
        self.session_client = dialogflow.SessionsClient()
        self.session = self.session_client.session_path(project_id, self.session_id)
        self.history = []

    def get_response(self, user_input):
        from google.cloud.dialogflow_v2.types import TextInput, QueryInput

        text_input = TextInput(text=user_input, language_code=self.language_code)
        query_input = QueryInput(text=text_input)

        try:
            response = self.session_client.detect_intent(session=self.session, query_input=query_input)
            reply = response.query_result.fulfillment_text

            # Save history
            self.history.append({'user': user_input, 'bot': reply})
            return reply if reply else "Sorry, I didn't get that."

        except Exception as e:
            return f"Error: {str(e)}"

# ======== Example Usage ========
if __name__ == "__main__":
    PROJECT_ID = "manas-vlav"
    bot = DialogflowChatBot(project_id=PROJECT_ID)
    print(f"{bot.name} is ready to chat!")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            print("Goodbye!")
            break
        response = bot.get_response(user_input)
        print(f"{bot.name}: {response}")

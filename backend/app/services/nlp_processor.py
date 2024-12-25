import openai

class NLPProcessor:
    def __init__(self, api_key):
        openai.api_key = api_key

    def extract_key_points(self, text):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",  # Use "gpt-3.5-turbo" if that's your plan
                messages=[
                    {"role": "system", "content": "You are an assistant that extracts key points from text."},
                    {"role": "user", "content": f"Extract key points from the following text: {text}"}
                ],
                max_tokens=300
            )
            return response["choices"][0]["message"]["content"].strip()
        except openai.error.OpenAIError as e:
            return {"error": str(e)}
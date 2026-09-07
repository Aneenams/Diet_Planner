# pip install -U google-genai

import os
from google import genai
from google.genai import types

# pip install -U google-genai

# Load API Key from environment or define directly
# GOOGLE_API_KEY ="AQ.A1Ho-"
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

def analyze_food(image):
    if not image:
        return {"error": "No image provided"}

    # Initialize Client
    client = genai.Client(api_key=GOOGLE_API_KEY)

    # Read image binary data and grab mime-type (defaults to image/jpeg)
    image_bytes = image.read()
    # mimetype = getattr(image, "contenttype", "image/jpeg")
    mime_type = image.content_type

    prompt = (
        "You are a clinical nutritionist. Identify the food in the image, estimate the "
        "average calories, and determine the meal_type (breakfast, lunch, snack, or dinner) "
        "based on standard consumption patterns."
    )

    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=[
                prompt,
                types.Part.from_bytes(data=image_bytes, mime_type=mime_type),
            ],
            config=types.GenerateContentConfig(
                system_instruction="You are a clinical nutritionist. Return ONLY JSON.",
                response_mime_type="application/json",
                response_schema={
                    "type": "OBJECT",
                    "properties": {
                        "foodname": {"type": "STRING"},
                        "averagecalorie": {"type": "NUMBER"},
                        "mealtype": {"type": "STRING"},
                    },
                    "required": ["foodname", "averagecalorie", "mealtype"],
                },
            ),
        )

        # Automatically parsed output dictionary when responsemime_type is JSON
        return response.parsed

    except Exception as e:
        return {"error": str(e)}
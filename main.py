import os
from pydantic import BaseModel, Field
from typing import List
from groq import Groq
import instructor
from dotenv import load_dotenv

load_dotenv()

class Character(BaseModel):
    name: str
    fact: List[str] = Field(..., description="A list of facts about the subject")

client = Groq(
    api_key=os.environ.get('GROQ_API_KEY'),
)

client = instructor.from_groq(client, mode=instructor.Mode.TOOLS)

while True:
    user_input = input("Enter name(type 'quit' to exit): ")

    if user_input.lower() == 'quit':
        print("Goodbye!")
        break

    try:
        resp = client.chat.completions.create(
            model="mixtral-8x7b-32768", 
            messages=[
                {"role": "user", "content": user_input}, 
            ],
            response_model=Character, 
        )

        response_json = resp.model_dump_json(indent=2)

        if response_json:
            print(response_json)
        else:
            print("No response received.")

    except Exception as e:
        print(f"An error occurred: {e}")



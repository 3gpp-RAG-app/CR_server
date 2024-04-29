from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

client = OpenAI()
client.api_key = os.getenv("OPENAI_API_KEY")


def generate_response(query, ret_list):
    
    references = "\n".join([f"spec number: {ret[2]},\n CR number: {ret[3]}, \n status: {ret[5]}, CR summary: {ret[8]}" for ret in ret_list])

    completion = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[
            {
                "role": "system",
                "content": f'You are a 3GPP specialized assistant, you have access to 3gpp CR database, you search in the provided retrivals from the database and answers to the user only based on the provided reference.' 
                            f'If the answer can not be found in the given reference. respond "I could not find an answer."'
                            f'Here is the reference between brackets:[{references}].',
            },
            {"role": "user", "content": query},
        ],
        temperature=0.2,
        max_tokens=3000,
    )

    response_message = completion.choices[0].message

    return response_message.content

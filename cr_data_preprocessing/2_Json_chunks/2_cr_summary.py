import os
from dotenv import load_dotenv
import requests
import openai
import json
from openai import OpenAI

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")


client = OpenAI()

"""This code loads the project JSONs from their directory
It imports the metadata from each, and passes it to a generation function that will generate CR summaries.
It then inserts the summaries into the JSON."""


def load_json(json_path):

    with open(json_path, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
    return data


def process_json_files(directory_path):
    for filename in os.listdir(directory_path):
        if filename.lower().endswith(".json"):
            json_path = os.path.join(directory_path, filename)
            print(f"{filename} is processing")

            json_data = load_json(json_path)

            metadata = json_data.get("Metadata", {})
            titles = json_data.get("titles_list", [])

            cr_summary = ""
            for key, value in metadata.items():
                cr_summary += f"{key}: {value}\n"

            cr_summary += "\nTitles:\n"
            for title in titles:

                if isinstance(title, dict):
                    title = str(title)
                cr_summary += title + "\n"

            summary = []

            response = generate_sammury(cr_summary)

            summary.append(response)

            json_data["summary"] = summary

            with open(
                json_path.replace(".json", "_with_summary.json"), "w"
            ) as output_file:
                json.dump(json_data, output_file)


def generate_sammury(text):

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {
                "role": "system",
                "content": """
                    You are a 3GPP Change Request summarizer.
                    Users will provide you with information about a change request,
                    and your task is to generate a concise paragraph that accurately describes the provided change request.
                """,
            },
            {"role": "user", "content": text},
        ],
        temperature=0,
        max_tokens=3000,
    )

    response_message = completion.choices[0].message

    return response_message.content


json_directory = ""
process_json_files(json_directory)

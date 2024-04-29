import os
from dotenv import load_dotenv
import requests
import openai
import json
import pandas as pd
from openai import OpenAI

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")


client = OpenAI()

'''This code loads JSONs, loads summaries, and sends them to an embedding function,
which produces the vector representation from the summary.
It then inserts the embeddings into the JSON.'''


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

            titles = json_data.get("titles_list", [])
            summary = json_data.get("summary", [])

            embeddings = []
            clauses = "Changes have been made to: "
            for title_obj in titles:

                if isinstance(title_obj, dict):

                    clauses += next(iter(title_obj.values()))
                else:
                    clauses += str(title_obj)
            for item in summary:

                combined_text = item + "\n" + clauses

                emb = get_openai_embeddings(combined_text)
                embeddings.append(emb)

                json_data["embeddings"] = embeddings

                with open(
                    json_path.replace(".json", "_with_embeddings.json"), "w"
                ) as output_file:
                    json.dump(json_data, output_file)
                    print(f"{filename} processed")




def get_openai_embeddings(input_text):

    url = "https://api.openai.com/v1/embeddings"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_api_key}",
    }

    data = {
        "input": input_text,
        "model": "text-embedding-3-large",
    }

    response = requests.post(url, headers=headers, json=data)
    response_json = response.json()
    if "data" in response_json:
      
        first_data_item = response_json["data"][0]
        embeddings = first_data_item.get("embedding", [])
    else:
        embeddings = []
    print(len(embeddings))

    return embeddings


json_directory = ""
process_json_files(json_directory)

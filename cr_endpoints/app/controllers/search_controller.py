from pymilvus import Collection
from openai import OpenAI
import os
from typing import Dict

import torch
import numpy as np
from transformers import AutoModel, AutoTokenizer


from dotenv import load_dotenv

load_dotenv()

client = OpenAI()
OPENAI_ENGINE = "text-embedding-3-large"
client.api_key = os.getenv("OPENAI_API_KEY")

search_latency_fmt = "search latency = {:.4f}s"
num_entities, dim = (3000, 8)

collection = Collection("CR")
collection.load()


def embed(text):
    response = client.embeddings.create(
        input=text, model=OPENAI_ENGINE
    )  
    return response.data[0].embedding


def search(user_input, filters=None):
    search_params = {"metric_type": "L2"}

    results = collection.search(
        data=[embed(user_input)],
        anns_field="embedings",
        param=search_params,
        limit=6,
        output_fields=["id", "spec", "cr_number", "impacted_version","status", "title", "source", "cr_summary"],
        filter=filters
    )

    ret = []
    for hit in results[0]:
        row = [
            hit.score,
            hit.entity.get("id"),
            hit.entity.get("spec"),
            hit.entity.get("cr_number"),
            hit.entity.get("impacted_version"),
            hit.entity.get("status"),
            hit.entity.get("title"),
            hit.entity.get("source"),
            hit.entity.get("cr_summary")
        ]
        ret.append(row)

    ret.sort(key=lambda x: x[0])

    return ret




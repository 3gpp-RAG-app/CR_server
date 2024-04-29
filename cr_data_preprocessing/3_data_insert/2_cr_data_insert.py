import json
import os
from pymilvus import Collection, connections, utility
from config import HOST, MILVUS_PORT, MILVUS_PORT,MILVUS_USER, MILVUS_PASSWORD

connections.connect(
    "default", host=HOST, port=MILVUS_PORT, user=MILVUS_USER, password=MILVUS_PASSWORD
)
collection = Collection('CR')
print('collection loaded')


def load_json(json_path):
    with open(json_path, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
    return data


def process_json_files(directory_path):
    counter = 0
    for filename in os.listdir(directory_path):
        if filename.lower().endswith(".json"):
            json_path = os.path.join(directory_path, filename)

            json_data = load_json(json_path)
            metadata = json_data.get('Metadata', {})
            embeddings = json_data.get("embeddings", [])
            summary = json_data.get('summary', [])

            for text in summary:
                cr_summary = text
            for emb in embeddings:
                emb=emb
            
            spec = metadata.get('spec', '')
            cr_number = metadata.get('CR', '')
            revision = metadata.get('revision', '')
            impacted_version = metadata.get('Impacted Version', '')
            target_release = metadata.get('Target Release', '')
            status = metadata.get('CR status at WG', '')
            title = metadata.get('Title', '')
            source = metadata.get('Source to WG', '')

            entity = [
                        [counter],
                        [spec],
                        [cr_number],
                        [revision],
                        [impacted_version],
                        [target_release],
                        [status],
                        [title],
                        [source],
                        [emb],
                        [cr_summary],
                    ]
            counter += 1
            collection.insert(entity)
            collection.flush()
            print(
                f"inserted {counter} from {filename} \nembeddings list len is {len(embeddings)}"
             )
                   
               
                
            collection.release()


if __name__ == "__main__":
    process_json_files("")

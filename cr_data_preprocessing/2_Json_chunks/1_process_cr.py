import json
import re
import os
from bs4 import BeautifulSoup
from langchain_text_splitters import (
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter,
)
import nltk


"""This code processes a directory where Change Requests (CRs) in .md format are located. It parses the table
using HTML parsing, and the changes clauses based on markdown headers if they exit in the file.
It produces a JSON that contains the CR metadata and the body of the CR (the changed clauses)."""


def process_file(file_path):

    with open(file_path, "r", encoding="utf-8") as file:
        document = file.read()

        headers_to_split_on = [
            ("#", "Header 1"),
            ("##", "Header 2"),
            ("###", "Header 3"),
            ("####", "Header 4"),
            ("#####", "Header 5"),
            ("######", "Header 6"),
            ("#######", "Header 7"),
            ("########", "Header 8"),
        ]
        splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
        header_splits = splitter.split_text(document)

        titles_list = []
        content_list = []
        data_dict = {}

        table_match = re.search(r"<table\b[^>]*>(.*?)</table>", document, re.DOTALL)
        if table_match:
            table_content = table_match.group(1)
            soup = BeautifulSoup(table_content, "html.parser")
            rows = soup.find_all("tr")

            for row in rows:
                cells = row.find_all(["td", "th"])
                for i in range(0, len(cells), 2):
                    if i + 1 < len(cells):
                        key = cells[i].text.strip().rstrip(":")
                        value = cells[i + 1].text.strip()
                        data_dict[key] = value

        for i, item in enumerate(header_splits, start=0):
            headers = item.metadata
            contents = item.page_content.strip()
            tokens = nltk.word_tokenize(contents)

            if headers:
                titles_list.append(headers)
                content_list.append(contents)

        split_info = {
            "Metadata": data_dict,
            "titles_list": titles_list,
            "contents_list": content_list,
        }

        base_name = os.path.splitext(os.path.basename(markdown_file))[0]
        output_file = os.path.join(f"{base_name}.json")

        with open(output_file, "w", encoding="utf-8") as json_file:
            json.dump(split_info, json_file, ensure_ascii=False, indent=2)

        print(f"Saved splits to a single JSON file: {output_file}.")


file_path = ""
process_file(file_path)

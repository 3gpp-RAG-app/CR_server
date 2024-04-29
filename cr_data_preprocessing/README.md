# 3GPP CRs Data Preparation And Data Insert

The data preparation process refers to extracting relevant pieces of text from the source file format DOCX while preserving basic layout elements such as headers and tables.

The extracted text is then used to generate source data embeddings representations.

The output of the preparation process is project own file format as JSON, containing metadata, a content list, original text content, and embeddings.

These JSON files are then used to execute data insertion while maintaining the relational structure of the text chunks.

## Introduction of the repository

### 1_docx_conversion

the folder contains Bash scripts used to convert the docx file to html file and markdown file.

- **to_html.sh**
  This shell script utilizes the pandoc command-line tool for converting docx to html format, since html format can be easily used to extract metadata from the table of the data.

- **to_mkd.sh**
  This shell script utilizes the pandoc command-line tool for converting docx to markdown format, since markdown format can be easily used to recoganise different sections based on hearders of the changed content in CRs.

### 2_Json_chunks

This folder contains Python scripts used to split the markdown file based on headers to create context-aware text chunks (paragraph level).

Subsequently, it generates and inserts the corresponding embeddings into the same JSON file.

It also includes a script that utilizes fixed-size recursive chunking with overlapping. This is useful in cases where chunk sizes are more relevant than individual topic sizes.

- **1_process_cr.py**
  This Python script utilizes BeautifulSoup to extract metadata from .html.Then it uses MarkdownHeaderTextSplitter to split Markdown files based on specified headers and produced titles_list and content_list. The final splited json file include: Metadata, titles_list and contents_list.

- **2_cr_summary.py**
  This code loads the project JSONs from their directory. It imports the metadata from each, and passes it to a generation function that will generate CR summaries.It then inserts the summaries into the JSON.

- **3_cr_embed.py**
  This code loads JSONs, loads summaries, and sends them to an embedding function,which produces the vector representation from the summary.It then inserts the embeddings into the JSON.

### 3_data_insert

- **1_create_cr_collection.py**
  The code establishes a connection to Milvus, defines a collection schema with various fields(which will be used as relational database for improving accuracy of similar search), creates a collection, and sets up an index for efficient search operations.

- **2_cr_data_insert.py**
  The code connects to a Milvus collection, processes JSON files, extracts metadata and embeddings, constructs entities, and inserts them into the collection while printing progress and metadata information.

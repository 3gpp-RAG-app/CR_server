import time
import json

import numpy as np
from pymilvus import (
    connections,
    utility,
    FieldSchema,
    CollectionSchema,
    DataType,
    Collection,
)
from config import HOST, MILVUS_PORT, MILVUS_PORT,MILVUS_USER, MILVUS_PASSWORD

fmt = "\n=== {:30} ===\n"
search_latency_fmt = "search latency = {:.4f}s"
num_entities, dim = 3000, 8

print(fmt.format("start connecting to Milvus"))
connections.connect(
    "default", host=HOST, port=MILVUS_PORT, user=MILVUS_USER, password=MILVUS_PASSWORD
)

fields = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True),
    FieldSchema(
        name="spec",
        dtype=DataType.VARCHAR,
        max_length=300,
        default_value="Unknown",
    ),
    FieldSchema(
        name="cr_number",
        dtype=DataType.VARCHAR,
        max_length=600,
        default_value="Unknown",
    ),
    FieldSchema(
        name="revision",
        dtype=DataType.VARCHAR,
        max_length=600,
        default_value="Unknown",
    ),

    FieldSchema(
        name="impacted_version",
        dtype=DataType.VARCHAR,
        max_length=600,
        default_value="Unknown",
    ),
    FieldSchema(
        name="target_release",
        dtype=DataType.VARCHAR,
        max_length=600,
        default_value="Unknown",
    ),
    FieldSchema(
        name="status",
        dtype=DataType.VARCHAR,
        max_length=600,
        default_value="Unknown",
    ),
    FieldSchema(
        name="title",
        dtype=DataType.VARCHAR,
        max_length=600,
        default_value="Unknown",
    ),
    FieldSchema(
        name="source",
        dtype=DataType.VARCHAR,
        max_length=600,
        default_value="Unknown",
    ),

    FieldSchema(name="embedings", dtype=DataType.FLOAT_VECTOR, dim=3072),
    FieldSchema(
        name="cr_summary",
        dtype=DataType.VARCHAR,
        max_length=65000,
        default_value="Unknown",
    )
]

schema = CollectionSchema(
    fields=fields,
    description="this v0.1 database covers cr test content",
    enable_dynamic_field=True,
)

collection_name = "CR"
collection = Collection(
    name=collection_name, schema=schema, using="default", shards_num=2
)
index_params = {
    "index_type": "IVF_FLAT",
    "metric_type": "L2",
    "params": {"nlist": 1024},
}
collection.create_index(field_name="embedings", index_params=index_params)

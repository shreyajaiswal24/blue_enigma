#!/usr/bin/env python3
from pinecone import Pinecone
import config
import time

pc = Pinecone(api_key=config.PINECONE_API_KEY)

# Delete existing index if it exists
if config.PINECONE_INDEX_NAME in pc.list_indexes().names():
    print(f"Deleting existing index: {config.PINECONE_INDEX_NAME}")
    pc.delete_index(config.PINECONE_INDEX_NAME)
    time.sleep(5)  # Wait for deletion

print("Index deleted successfully. You can now run pinecone_upload.py")
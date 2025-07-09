import hashlib
import json
import os

INDEX_PATH = "index.json"

def hash_url(url):
    return hashlib.sha256(url.encode()).hexdigest()

def load_index():
    if not os.path.exists(INDEX_PATH):
        return {}
    with open(INDEX_PATH, 'r') as f:
        return json.load(f)

def save_index(index):
    with open(INDEX_PATH, 'w') as f:
        json.dump(index, f, indent=2)

def is_duplicate(url, index):
    return hash_url(url) in index

def add_to_index(url, data, index):
    index[hash_url(url)] = data

#!/usr/bin/env python3

import os
import re
import time
import json
import socket
import requests
from dotenv import load_dotenv
from parser import parse_status_block
from elasticsearch import Elasticsearch

load_dotenv()

HA_URL = os.getenv("HA_URL", "http://localhost:8123/api/hassio/addons/a0d7b954_wireguard/logs")
TOKEN = os.getenv("HA_TOKEN")
ES_HOST = os.getenv("ES_HOST", "http://localhost:9200")
ES_USER = os.getenv("ES_USER", "wireguard_writer")
ES_PASS = os.getenv("ES_PASS", "changeme")

headers = {"Authorization": f"Bearer {TOKEN}"}
es = Elasticsearch(ES_HOST, basic_auth=(ES_USER, ES_PASS), verify_certs=False)

def ship_to_es(json_obj):
    index_name = f"wireguard-logs-{time.strftime('%Y.%m.%d')}"
    for peer in json_obj.get("peers", []):
        doc = {
            "addon": json_obj.get("addon"),
            "timestamp": json_obj.get("timestamp"),
            "interface": json_obj.get("interface"),
            "peer": peer
        }
        es.index(index=index_name, document=doc)

def fetch_and_ship():
    resp = requests.get(HA_URL, headers=headers)
    if resp.status_code != 200:
        print("Failed to fetch logs:", resp.status_code, resp.text)
        return

    raw = resp.text
    # Split into blocks (each begins with INFO: Requesting current status)
    blocks = raw.split("INFO: Requesting current status from WireGuard...")
    blocks = [b.strip() for b in blocks if b.strip()]

    for block in blocks:
        parsed = parse_status_block(block)
        print(json.dumps(parsed, indent=2))  # optional for debugging
        ship_to_es(parsed)

if __name__ == "__main__":
    fetch_and_ship()
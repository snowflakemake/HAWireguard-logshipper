import re
import time
import json

def parse_status_block(block: str):
    lines = [l.strip() for l in block.splitlines() if l.strip()]
    result = {
        "addon": "wireguard",
        "timestamp": None,
        "interface": {},
        "peers": []
    }
    peer = None

    for line in lines:
        # Timestamp line
        if line.startswith("[") and "Requesting current status" in line:
            ts_match = re.match(r"\[(\d+:\d+:\d+)\]", line)
            if ts_match:
                # Today’s date + time (approx)
                result["timestamp"] = time.strftime("%Y-%m-%dT") + ts_match.group(1) + time.strftime("%z")

        elif line.startswith("interface:"):
            result["interface"]["name"] = line.split(":", 1)[1].strip()

        elif line.startswith("public key:"):
            result["interface"]["public_key"] = line.split(":", 1)[1].strip()

        elif line.startswith("listening port:"):
            result["interface"]["port"] = int(line.split(":", 1)[1].strip())

        elif line.startswith("peer:"):
            if peer:
                result["peers"].append(peer)
            peer = {"public_key": line.split(":", 1)[1].strip()}

        elif line.startswith("endpoint:") and peer is not None:
            peer["endpoint"] = line.split(":", 1)[1].strip()

        elif line.startswith("allowed ips:") and peer is not None:
            peer["allowed_ips"] = line.split(":", 1)[1].strip()

        elif line.startswith("latest handshake:") and peer is not None:
            peer["latest_handshake"] = line.split(":", 1)[1].strip()

        elif line.startswith("transfer:") and peer is not None:
            m = re.search(r"([\d\.]+\s+\w+) received, ([\d\.]+\s+\w+) sent", line)
            if m:
                peer["transfer"] = {"received": m.group(1), "sent": m.group(2)}

        elif line.startswith("persistent keepalive:") and peer is not None:
            peer["keepalive"] = line.split(":", 1)[1].strip()

    if peer:
        result["peers"].append(peer)

    return result
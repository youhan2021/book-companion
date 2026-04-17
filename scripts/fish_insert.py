#!/usr/bin/env python3
"""
插入摸鱼内容 - 无参数调用，输出符合最小字数要求的内容
"""

import json
import os
import sys

QUEUE_FILE = os.path.expanduser("~/.hermes/fish_queue.json")
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_FILE = os.path.join(SKILL_DIR, "config.env")

MIN_CHARS = 100


def get_config():
    if os.path.exists(CONFIG_FILE):
        for line in open(CONFIG_FILE):
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                k, v = line.split('=', 1)
                if k.strip() == 'FISH_MIN_CHARS':
                    return int(v.strip())
    return MIN_CHARS


def main():
    min_chars = get_config()

    if not os.path.exists(QUEUE_FILE):
        return

    with open(QUEUE_FILE) as f:
        data = json.load(f)

    if not data.get("active") or not data.get("queue"):
        return

    output = []
    total = 0

    while data["queue"] and total < min_chars:
        item = data["queue"].pop(0)
        output.append(item)
        total += len(item)

    if output:
        with open(QUEUE_FILE, 'w') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print('\n'.join(output))


if __name__ == "__main__":
    main()

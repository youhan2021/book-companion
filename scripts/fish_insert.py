#!/usr/bin/env python3
"""
插入摸鱼内容 - 无参数调用
直接输出下一条内容（由调用者决定是否发送）
"""

import json
import os
import sys
from datetime import datetime, timezone

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUEUE_FILE = os.path.join(SKILL_DIR, "fish_queue.json")
CONFIG_FILE = os.path.join(SKILL_DIR, "config.env")

MIN_CHARS = 100


def get_config():
    config = {"FISH_MIN_CHARS": str(MIN_CHARS)}
    if os.path.exists(CONFIG_FILE):
        for line in open(CONFIG_FILE):
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                k, v = line.split('=', 1)
                config[k.strip()] = v.strip()
    return config


def main():
    if not os.path.exists(QUEUE_FILE):
        return

    with open(QUEUE_FILE) as f:
        data = json.load(f)

    if not data.get("queue"):
        return

    config = get_config()
    min_chars = int(config.get("FISH_MIN_CHARS", MIN_CHARS))

    output = []
    total = 0

    while data["queue"] and total < min_chars:
        item = data["queue"].pop(0)
        output.append(item)
        total += len(item)

    if output:
        data["last_sent_at"] = datetime.now(timezone.utc).isoformat()
        with open(QUEUE_FILE, 'w') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print('\n'.join(output))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
插入摸鱼内容 - 无参数调用
直接输出下一条内容（由 agent 通过 session_search 判断是否应该发送）
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
    if os.path.exists(CONFIG_FILE):
        for line in open(CONFIG_FILE):
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                k, v = line.split('=', 1)
                if k.strip() == 'FISH_MIN_CHARS':
                    return int(v.strip())
    return MIN_CHARS


def get_last_sent_at():
    """从队列文件读取上次发送时间，返回 UTC datetime 或 None"""
    if not os.path.exists(QUEUE_FILE):
        return None
    with open(QUEUE_FILE) as f:
        data = json.load(f)
    ts = data.get("last_sent_at")
    if ts:
        return datetime.fromisoformat(ts.replace("Z", "+00:00"))
    return None


def set_last_sent_now():
    """将当前 UTC 时间写入队列文件的 last_sent_at"""
    if not os.path.exists(QUEUE_FILE):
        return
    with open(QUEUE_FILE) as f:
        data = json.load(f)
    data["last_sent_at"] = datetime.now(timezone.utc).isoformat()
    with open(QUEUE_FILE, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def main():
    min_chars = get_config()

    if not os.path.exists(QUEUE_FILE):
        return

    with open(QUEUE_FILE) as f:
        data = json.load(f)

    if not data.get("queue"):
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
        set_last_sent_now()
        print('\n'.join(output))


if __name__ == "__main__":
    main()

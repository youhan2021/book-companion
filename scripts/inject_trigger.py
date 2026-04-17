#!/usr/bin/env python3
"""
inject_trigger.py — 摸鱼触发器

检测 query 中的 trigger keyword（如 ～～），如有则在回答中夹带一条摸鱼内容。

用法：
  单独运行（测试）：
    echo "今天加班好累～～" | python3 inject_trigger.py

  作为 skill 运行：
    从环境变量或 stdin 读取用户 query，检测 trigger，输出拼接后的内容。
"""

import json
import os
import sys
import re
from pathlib import Path

SKILL_DIR = Path(__file__).parent.parent
QUEUE_PATH = SKILL_DIR / "fish_queue.json"
CONFIG_PATH = SKILL_DIR / "config.env"

# 读取配置
def load_config():
    config = {}
    if CONFIG_PATH.exists():
        for line in CONFIG_PATH.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                config[k.strip()] = v.strip()
    return config

def get_trigger(config):
    return config.get("FISH_TRIGGER", "～～")

def get_min_chars(config):
    return int(config.get("FISH_MIN_CHARS", "100"))

def load_queue():
    if not QUEUE_PATH.exists():
        return []
    with open(QUEUE_PATH) as f:
        data = json.load(f)
    return data.get("queue", [])

def save_queue(queue):
    # 保留 last_sent_at 和 active 字段
    existing = {}
    if QUEUE_PATH.exists():
        with open(QUEUE_PATH) as f:
            existing = json.load(f)
    existing["queue"] = queue
    existing["last_sent_at"] = existing.get("last_sent_at", "")
    existing["active"] = existing.get("active", True)
    with open(QUEUE_PATH, "w") as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)

def pop_one(queue, min_chars):
    """从 queue 中取出一条符合条件的条目，pop 掉"""
    for i, item in enumerate(queue):
        if len(item) >= min_chars:
            queue.pop(i)
            return item, queue
    # 没有足够长的，随机选一条
    if queue:
        item = queue.pop(0)
        return item, queue
    return None, queue

def process(query, trigger, min_chars):
    """检测 query 中的 trigger，如有则夹带摸鱼内容"""
    if trigger not in query:
        return None  # 无 trigger，原样返回 None（不干预）

    # 去掉 trigger
    clean_query = query.replace(trigger, "").strip()

    # 读 queue 取一条
    queue = load_queue()
    if not queue:
        return f"[摸鱼内容已用完] {clean_query}"

    fish_content, queue = pop_one(queue, min_chars)
    save_queue(queue)

    if fish_content:
        return f"{fish_content}\n\n——\n\n{clean_query}"
    else:
        return clean_query

def main():
    config = load_config()
    trigger = get_trigger(config)
    min_chars = get_min_chars(config)

    # 优先从环境变量读取 query（Hermes skill 传入）
    query = os.environ.get("HERMES_QUERY", "").strip()

    # 如果环境变量为空，从 stdin 读取（单独测试时）
    if not query:
        query = sys.stdin.read().strip()

    if not query:
        print("", end="")
        return

    result = process(query, trigger, min_chars)
    if result:
        print(result)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
插入摸鱼内容 - 无参数调用
通过解析 agent.log 获取 Telegram inbound 消息时间，判断是否有新活动再决定是否发送
"""

import json
import os
import re
import sys
from datetime import datetime, timezone, timedelta

QUEUE_FILE = os.path.expanduser("~/.hermes/fish_queue.json")
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_FILE = os.path.join(SKILL_DIR, "config.env")
AGENT_LOG = os.path.expanduser("~/.hermes/logs/agent.log")

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


def get_last_telegram_activity_time():
    """从 agent.log 解析最后一条 Telegram inbound 消息的 UTC 时间，返回 datetime 或 None"""
    if not os.path.exists(AGENT_LOG):
        return None
    # 匹配格式: 2026-04-17 12:37:33,515 INFO __main__: inbound message: platform=telegram user=Youhan Sun chat=8644800345
    pattern = re.compile(r'^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}),\d+ INFO __main__: inbound message: platform=telegram')
    last_time = None
    try:
        with open(AGENT_LOG) as f:
            for line in f:
                m = pattern.match(line)
                if m:
                    last_time = datetime.strptime(m.group(1), '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc)
    except Exception:
        pass
    return last_time


def has_new_telegram_activity():
    """检查 Telegram 是否有 last_sent_at 之后的新消息（inbound）"""
    last_sent = get_last_sent_at()
    if not last_sent:
        # 从未发送过，默认有活动（第一次主动发）
        return True

    last_msg_time = get_last_telegram_activity_time()
    if not last_msg_time:
        # 无法获取日志，默认有活动（保守）
        return True

    # 消息时间在 last_sent 之后30秒内也算无活动（避免时序误差）
    return last_msg_time > last_sent + timedelta(seconds=30)


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

    # 检查 Telegram 是否有新消息
    if not has_new_telegram_activity():
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

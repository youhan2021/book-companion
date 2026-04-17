#!/usr/bin/env python3
"""
摸鱼内容插入脚本
每次调用：从队列顺序获取内容，持续取直到总字数超过 FISH_MIN_CHARS

用法:
  python3 fish_insert.py                    # 插入摸鱼内容
  python3 fish_insert.py config get <key>   # 读取配置
  python3 fish_insert.py config set <key> <value>  # 设置配置
"""

import json
import subprocess
import sys
import os

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
QUEUE_SCRIPT = os.path.join(SKILL_DIR, "fish_queue.py")
CONFIG_FILE = os.path.join(os.path.dirname(SKILL_DIR), "config.env")


def load_config():
    """加载配置"""
    defaults = {"FISH_MIN_CHARS": 100}
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    try:
                        defaults[key.strip()] = int(value.strip())
                    except ValueError:
                        pass
    return defaults


def save_config(data):
    """保存配置"""
    with open(CONFIG_FILE, 'w') as f:
        f.write("# book-companion 配置文件\n")
        f.write(f"FISH_MIN_CHARS={data.get('FISH_MIN_CHARS', 100)}\n")


def get_next():
    """从队列获取下一条"""
    r = subprocess.run(["python3", QUEUE_SCRIPT, "next"],
                       capture_output=True, text=True)
    return r.stdout.strip()


def get_content(min_chars):
    """持续取直到总字数超过 min_chars"""
    result = []
    total = 0
    while total < min_chars:
        item = get_next()
        if not item:
            break
        result.append(item)
        total += len(item)
    return "\n\n".join(result)


def cmd_config(args):
    """config 命令"""
    if len(args) < 2:
        print("用法: fish_insert.py config get|set <key> [value]")
        return
    cfg = load_config()
    op, key = args[0], args[1]
    if op == "get":
        print(cfg.get(key, "未找到"))
    elif op == "set" and len(args) > 2:
        try:
            cfg[key] = int(args[2])
            save_config(cfg)
            print(f"{key} = {cfg[key]}")
        except ValueError:
            print("无效的值")
    else:
        print(f"未知命令: {op}")


def main():
    args = sys.argv[1:]

    # config 命令
    if args and args[0] == "config":
        cmd_config(args[1:])
        return

    # 无参数：直接输出摸鱼内容
    cfg = load_config()
    content = get_content(cfg.get("FISH_MIN_CHARS", 100))
    if content:
        print(content)


if __name__ == "__main__":
    main()

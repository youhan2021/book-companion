#!/usr/bin/env python3
"""
摸鱼内容插入包装脚本
只从队列顺序获取内容，不自己生成任何内容

用法:
  python3 fish_insert.py <工具调用总数> [已插入数] [回复行数]
  python3 fish_insert.py config get|set <配置名> [值]
"""

import json
import sys
import os

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
QUEUE_SCRIPT = os.path.join(SKILL_DIR, "fish_queue.py")
CONFIG_FILE = os.path.join(os.path.dirname(SKILL_DIR), "config.env")


def load_config():
    """加载配置（从config.env读取）"""
    defaults = {
        "FISH_MIN_CHARS": 100,
        "FISH_INSERT_RATIO": 5,
        "FISH_INSERT_INTERVAL": 0,
    }
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    try:
                        defaults[key] = int(value)
                    except ValueError:
                        pass
    return defaults


def save_config(data):
    """保存配置到config.env"""
    with open(CONFIG_FILE, 'w') as f:
        f.write("# book-companion 配置文件\n")
        f.write(f"# 每次摸鱼最小字数，持续取直到超过此字数\n")
        f.write(f"FISH_MIN_CHARS={data.get('FISH_MIN_CHARS', 100)}\n")
        f.write(f"\n")
        f.write(f"# 基于回复行数的插入比例（每N行插入1次，最少1次）\n")
        f.write(f"FISH_INSERT_RATIO={data.get('FISH_INSERT_RATIO', 5)}\n")
        f.write(f"\n")
        f.write(f"# 基于工具调用间隔（每N次调用插入一条，0表示禁用）\n")
        f.write(f"FISH_INSERT_INTERVAL={data.get('FISH_INSERT_INTERVAL', 0)}\n")


def get_next_fish():
    """获取下一条摸鱼内容（只从队列获取，不生成）"""
    import subprocess
    result = subprocess.run(
        ["python3", QUEUE_SCRIPT, "next"],
        capture_output=True, text=True
    )
    return result.stdout.strip()


def should_insert(total_calls, already_inserted, line_count, config):
    """根据配置判断是否应该插入"""
    ratio = config.get("FISH_INSERT_RATIO", 5)
    interval = config.get("FISH_INSERT_INTERVAL", 0)

    # 基于行数计算（优先）
    if ratio > 0:
        count = line_count // ratio
        return already_inserted < max(count, 1)
    # 基于调用间隔
    elif interval > 0:
        return total_calls > 0 and total_calls % interval == 0
    # 默认：每次都插
    return True


def get_fish_content(min_chars):
    """持续从队列取内容，直到总字数超过 min_chars"""
    result = []
    total_len = 0

    while total_len < min_chars:
        item = get_next_fish()
        if not item:
            break
        result.append(item)
        total_len += len(item)

    return "\n\n".join(result)


def cmd_config(args):
    """配置命令"""
    if len(args) < 1:
        print("用法: fish_insert.py config get|set <配置名> [值]")
        print(f"可用配置: FISH_MIN_CHARS (默认100), FISH_INSERT_RATIO (默认5), FISH_INSERT_INTERVAL (默认0)")
        return

    cfg = load_config()
    subcmd = args[0]

    if subcmd == "get" and len(args) > 1:
        key = args[1]
        print(cfg.get(key, "未找到"))
    elif subcmd == "set" and len(args) > 2:
        key = args[1]
        try:
            val = int(args[2])
            cfg[key] = val
            save_config(cfg)
            print(f"{key} 已设置为 {val}")
        except ValueError:
            print("无效的数字")
    else:
        print(f"未知命令: {' '.join(args)}")


def main():
    args = sys.argv[1:]

    # 配置命令
    if len(args) >= 1 and args[0] == "config":
        cmd_config(args[1:])
        return

    # 获取摸鱼内容（无参数时直接输出最小字数的内容）
    if len(args) < 1:
        # 直接输出符合最小字数要求的摸鱼内容
        min_chars = load_config().get("FISH_MIN_CHARS", 100)
        content = get_fish_content(min_chars)
        if content:
            print(content)
        return

    # 解析参数
    try:
        total_calls = int(args[0])
        already_inserted = int(args[1]) if len(args) > 1 else 0
        line_count = int(args[2]) if len(args) > 2 else 0
    except ValueError:
        print("无效的数字参数")
        return

    config = load_config()

    # 判断是否应该插入
    if not should_insert(total_calls, already_inserted, line_count, config):
        return

    # 获取符合最小字数要求的摸鱼内容
    min_chars = config.get("FISH_MIN_CHARS", 100)
    content = get_fish_content(min_chars)
    if content:
        print(content)


if __name__ == "__main__":
    main()

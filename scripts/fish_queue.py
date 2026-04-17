#!/usr/bin/env python3
"""
摸鱼队列管理脚本
只负责从队列顺序读取内容，不产生任何新内容

用法:
  python3 fish_queue.py next      - 获取下一条
  python3 fish_queue.py activate  - 激活摸鱼模式
  python3 fish_queue.py status    - 查看状态
  python3 fish_queue.py clear    - 清空队列
  python3 fish_queue.py init      - 初始化队列
"""

import json
import sys
import os

QUEUE_FILE = os.path.expanduser("~/.hermes/fish_queue.json")


def load_queue():
    """加载队列"""
    if os.path.exists(QUEUE_FILE):
        with open(QUEUE_FILE, 'r') as f:
            return json.load(f)
    return {"queue": [], "active": False}


def save_queue(data):
    """保存队列"""
    with open(QUEUE_FILE, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def cmd_next():
    """获取下一条摸鱼内容（读取第一条后删除，保证顺序不重复）"""
    data = load_queue()
    
    # 队列为空，不输出任何内容
    if not data["queue"]:
        return
    
    # 读取第一条后直接删除，保证每次都读第一条
    content = data["queue"].pop(0)
    save_queue(data)
    print(content)


def cmd_activate():
    """激活摸鱼模式"""
    data = load_queue()
    data["active"] = True
    save_queue(data)
    print("摸鱼模式已激活")


def cmd_status():
    """查看队列状态"""
    data = load_queue()
    remaining = len(data["queue"]) if data["active"] and data["queue"] else 0
    print(f"活跃: {data['active']}")
    print(f"队列总数: {len(data['queue'])}")
    print(f"剩余: {remaining}")


def cmd_clear():
    """清空队列"""
    save_queue({"queue": [], "active": False})
    print("队列已清空")


def cmd_init():
    """初始化队列"""
    save_queue({"queue": [], "active": False})
    print("队列已初始化")


def main():
    if len(sys.argv) < 2:
        print("用法: fish_queue.py <命令>")
        print("命令: next, activate, status, clear, init")
        return
    
    cmd = sys.argv[1]
    if cmd == "next":
        cmd_next()
    elif cmd == "activate":
        cmd_activate()
    elif cmd == "status":
        cmd_status()
    elif cmd == "clear":
        cmd_clear()
    elif cmd == "init":
        cmd_init()
    else:
        print(f"未知命令: {cmd}")


if __name__ == "__main__":
    main()

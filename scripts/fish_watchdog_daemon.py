#!/usr/bin/env python3
"""
摸鱼看门狗守护进程
每隔 INTERVAL 秒自动插入摸鱼内容到当前对话，防止我遗漏时补发。

用法:
  python3 fish_watchdog_daemon.py start   # 后台启动
  python3 fish_watchdog_daemon.py stop    # 停止
  python3 fish_watchdog_daemon.py status  # 查看状态
"""

import sys
import os
import time
import signal
import json
import subprocess
from pathlib import Path

SKILL_DIR = Path(__file__).parent.parent
QUEUE_FILE = Path.home() / ".hermes/fish_queue.json"
PID_FILE = Path.home() / ".hermes/fish_watchdog.pid"
INTERVAL = 120  # 默认2分钟


def get_fish_content():
    """获取摸鱼内容"""
    result = subprocess.run(
        [sys.executable, str(SKILL_DIR / "scripts" / "fish_insert.py")],
        capture_output=True, text=True, timeout=10
    )
    return result.stdout.strip()


def send_fish(content):
    """通过 send_message 发送摸鱼内容到 origin"""
    if not content:
        return
    import urllib.request
    # 调用 Hermes MCP 工具接口
    # 注意：这需要 Hermes 运行在本地且有 send_message 可用
    # 备用方案：写入一个待发送队列，由主会话处理
    pending = Path.home() / ".hermes/fish_pending.txt"
    with open(pending, "w") as f:
        f.write(content)


def daemon_loop(interval):
    """主循环"""
    while True:
        try:
            # 检查队列是否活跃
            if QUEUE_FILE.exists():
                with open(QUEUE_FILE) as f:
                    data = json.load(f)
                if not data.get("active"):
                    time.sleep(interval)
                    continue

            content = get_fish_content()
            if content:
                send_fish(content)
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 已发送摸鱼内容: {content[:50]}...")
        except Exception as e:
            print(f"Watchdog error: {e}")

        time.sleep(interval)


def start_daemon(interval=INTERVAL):
    """后台启动守护进程"""
    # 检查是否已在运行
    if PID_FILE.exists():
        try:
            pid = int(PID_FILE.read_text())
            os.kill(pid, 0)
            print(f"Watchdog already running (PID {pid})")
            return
        except (ValueError, ProcessLookupError):
            PID_FILE.unlink()

    pid = os.fork()
    if pid == 0:
        # 子进程：脱离控制终端
        os.setsid()
        signal.signal(signal.SIGTERM, lambda *_: sys.exit(0))
        sys.stdin.close()
        sys.stdout.close()
        sys.stderr.close()

        daemon_loop(interval)
    else:
        PID_FILE.write_text(str(pid))
        print(f"Watchdog started (PID {pid}), interval={interval}s")


def stop_daemon():
    """停止守护进程"""
    if not PID_FILE.exists():
        print("Watchdog not running")
        return
    try:
        pid = int(PID_FILE.read_text())
        os.kill(pid, signal.SIGTERM)
        PID_FILE.unlink()
        print("Watchdog stopped")
    except ProcessLookupError:
        PID_FILE.unlink()
        print("Watchdog not running")


def status():
    """查看状态"""
    if PID_FILE.exists():
        try:
            pid = int(PID_FILE.read_text())
            os.kill(pid, 0)
            print(f"Watchdog running (PID {pid})")
            return
        except ProcessLookupError:
            pass
    print("Watchdog not running")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    if cmd == "start":
        interval = int(sys.argv[2]) if len(sys.argv) > 2 else INTERVAL
        start_daemon(interval)
    elif cmd == "stop":
        stop_daemon()
    elif cmd == "status":
        status()
    else:
        print(__doc__)

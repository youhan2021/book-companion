#!/bin/bash
# 摸鱼看门狗 - OpenClaw 版本
# 使用 OpenClaw 的消息接口发送摸鱼内容
# 仅在 OpenClaw 环境下使用

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
QUEUE_FILE="$HOME/.hermes/fish_queue.json"
LOG="$HOME/.hermes/fish_watchdog.log"
INTERVAL=120

log_msg() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG"
}

# 检查是否在 OpenClaw 环境
is_openclaw() {
    [ -d "$HOME/.openclaw" ] || [ -n "$(which openclaw 2>/dev/null)" ]
}

# 检查队列是否活跃
is_active() {
    if [ ! -f "$QUEUE_FILE" ]; then
        return 1
    fi
    python3 -c "import json,sys; d=json.load(open('$QUEUE_FILE')); sys.exit(0 if d.get('active') else 1)" 2>/dev/null
}

# 发送摸鱼内容（写入待发队列，由主会话处理）
send_fish() {
    local content="$1"
    local pending="$HOME/.hermes/fish_pending.txt"
    echo "$content" >> "$pending"
}

# 主循环
main() {
    while true; do
        if is_active; then
            content=$(cd "$SKILL_DIR" && python3 scripts/fish_insert.py 2>/dev/null)
            if [ -n "$content" ]; then
                send_fish "$content"
                log_msg "已发送摸鱼内容: ${content:0:50}..."
            fi
        fi
        sleep "$INTERVAL"
    done
}

case "$1" in
    start)
        if is_openclaw; then
            nohup "$0" run >> "$LOG" 2>&1 &
            echo "Watchdog started (PID $!)"
        else
            echo "OpenClaw not detected, skipping"
        fi
        ;;
    run)
        main
        ;;
    stop)
        pkill -f "fish_watchdog.sh.*run" 2>/dev/null
        echo "Watchdog stopped"
        ;;
    status)
        if pgrep -f "fish_watchdog.sh.*run" > /dev/null; then
            echo "Watchdog running"
        else
            echo "Watchdog not running"
        fi
        ;;
    *)
        echo "Usage: fish_watchdog.sh {start|stop|status}"
        ;;
esac

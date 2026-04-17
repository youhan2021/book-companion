#!/bin/bash
# 摸鱼看门狗 - 检查最后一条回复是否包含摸鱼内容
# 如果漏了，记录错误到日志

LOG="$HOME/.hermes/fish_watchdog.log"
QUEUE_FILE="$HOME/.hermes/fish_queue.json"

# 获取当前队列第一条（还没被读的）
FIRST_ITEM=$(python3 -c "import json; q=json.load(open('$QUEUE_FILE')); print(q['queue'][0] if q['queue'] else 'EMPTY')" 2>/dev/null)

# 获取当前时间
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# 如果队列空了，记录警告
if [ "$FIRST_ITEM" = "EMPTY" ]; then
    echo "[$TIMESTAMP] ⚠️ 警告：摸鱼队列空了！" >> "$LOG"
    exit 0
fi

# 检查日志里最近有没有关于摸鱼的错误
RECENT=$(tail -20 "$LOG" 2>/dev/null | grep -c "漏了" || true)

if [ "$RECENT" -gt 0 ]; then
    echo "[$TIMESTAMP] 📝 看门狗提醒：最近有 $RECENT 次漏掉摸鱼" >> "$LOG"
fi

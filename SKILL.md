---
name: book-companion
description: 摸鱼skill - 插入古典中文摘录到对话中
---

# book-companion

两个功能：**添加内容** 和 **发出内容**。

## 添加内容

从 URL 提取文本填充队列（添加前清空旧队列）：
```bash
python3 scripts/add_from_url.py <URL>
```

## 发出内容

运行脚本输出摸鱼内容（由调用者判断是否发送）：
```bash
python3 scripts/fish_insert.py
```

## 管理队列

```bash
python3 scripts/fish_queue.py status   # 查看状态
python3 scripts/fish_queue.py clear    # 清空队列
```

## 配置

`config.env`（技能根目录）：
```
FISH_MIN_CHARS=100
```

## 队列文件

`~/.hermes/skills/leisure/book-companion/fish_queue.json`

格式：`{"queue": [...], "last_sent_at": "ISO时间"}`

## 定时发出内容

通过 cron 触发，参考以下 prompt 创建 agent cron job。

## cron 创建 prompt

**添加内容：**
```
Run book-companion skill: add content from <URL> to the queue.
```

**创建 cron（每5分钟，有新对话才发）：**
```
Create a book-companion cron job: run the `book-companion` skill every 5 minutes. Before running, use session_search to check if there is any Telegram user message since the queue's last_sent_at. Only run the skill's fish_insert.py if there is new Telegram activity. If there is no new activity, respond with exactly [SILENT]. Name it `book-companion-runner`, deliver to origin.
```

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

运行脚本输出摸鱼内容：
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
ACTIVITY_LOG=/home/ubuntu/.hermes/logs/agent.log
```

## 队列文件

`fish_queue.json`（技能根目录下）

格式：`{"queue": [...], "last_sent_at": "ISO时间"}`

## 活动检测设计（重要）

**不要在脚本里检测 Telegram 活动**，因为：
- `session_search` 在 cron 隔离环境里看不到 Telegram DM 会话
- `gateway.log` 只记录 bot → user 的 outbound 消息，没有 user → bot 的 inbound
- `agent.log` 有 inbound 记录，但路径可能因部署而异

正确做法：活动检测逻辑写在 **cron prompt** 里，脚本只负责输出。

## cron 创建 prompt

**添加内容：**
```
Run book-companion skill: add content from <URL> to the queue.
```

**创建 cron（每5分钟，有新对话才发）：**
```
Create a book-companion cron job: every 5 minutes, (1) read last_sent_at from the queue file at /home/ubuntu/.hermes/skills/leisure/book-companion/fish_queue.json, (2) check the log at /home/ubuntu/.hermes/logs/agent.log for the latest Telegram inbound message (grep "inbound message: platform=telegram"), (3) only run "python3 scripts/fish_insert.py" in the skill directory if there is a message newer than last_sent_at + 30s, (4) if no new activity respond with exactly [SILENT]. Name it book-companion-runner, deliver to origin.
```

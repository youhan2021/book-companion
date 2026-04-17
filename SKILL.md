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

`~/.hermes/fish_queue.json`

格式：`{"queue": [...], "last_sent_at": "ISO时间"}`

## 定时发出内容

通过 cron 触发，参考 README 中的 prompt 创建 agent cron job。

---

## README prompt 模板

**添加内容：**
```
Run book-companion skill: add content from <URL> to the queue.
```

**创建 cron（每5分钟，有新对话才发）：**
```
Create a book-companion cron job: run the `book-companion` skill every 5 minutes, but first use session_search to check if there is any new Telegram user message since the queue's last_sent_at. Only send content if there is new conversation activity. Name it `book-companion-runner`, deliver to origin.
```

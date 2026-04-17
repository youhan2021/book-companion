# book-companion 读书陪伴技能

> 📚 Insert classical Chinese text excerpts into your conversations

两个功能：**添加内容** 和 **定时发出内容**。

---

**Jump to: [English](#-english) | [中文](#-中文)**

---

## 🇺🇸 English

### Two Functions

**1. Add Content** — Fill the queue from a URL (clears old queue first)

```
Run book-companion skill: add content from https://www.purepen.com/sgyy/001.htm to the queue.
```

**2. Scheduled Output** — Create a cron job to trigger skill output automatically

```
Create a book-companion cron job: every 5 minutes:
1. Read last_sent_at from ~/.hermes/skills/leisure/book-companion/fish_queue.json
2. Check the log file configured in config.env (ACTIVITY_LOG) for the latest Telegram inbound message time (grep "inbound message: platform=telegram")
3. Only run "python3 scripts/fish_insert.py" in the skill directory if there is a Telegram message after last_sent_at + 30 seconds
4. If no new activity, respond with exactly [SILENT]
Name it `book-companion-runner`, deliver to origin.
```

### Config

`config.env` (skill root directory):
```
FISH_MIN_CHARS=100
ACTIVITY_LOG=/home/ubuntu/.hermes/logs/agent.log
```

---

## 🇨🇳 中文

### 两个功能

**1. 添加内容** — 从 URL 提取文本填充队列（添加前清空旧队列）

```
运行 book-companion skill：从 https://www.purepen.com/sgyy/001.htm 添加内容到队列。
```

**2. 定时发出内容** — 让 agent 创建 cron job，定时触发 skill 输出内容

```
创建 book-companion 的 cron job：每5分钟执行以下步骤：
1. 从 ~/.hermes/skills/leisure/book-companion/fish_queue.json 读取 last_sent_at
2. 检查 config.env 中配置的 ACTIVITY_LOG 文件，用 grep 查找最新的 Telegram inbound 消息时间（"inbound message: platform=telegram"）
3. 只有当 Telegram 消息时间晚于 last_sent_at + 30秒 时，才运行 skill 目录下的 "python3 scripts/fish_insert.py"
4. 如果没有新活动，回复 exactly [SILENT]
名称为 book-companion-runner，投递到 origin。
```

### 配置

`config.env`（技能根目录）:
```
FISH_MIN_CHARS=100
ACTIVITY_LOG=/home/ubuntu/.hermes/logs/agent.log
```

---

## 📝 License | 许可证

MIT

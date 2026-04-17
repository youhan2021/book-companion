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
Run book-companion skill: add content from https://www.136book.com/santiheji/fqlrcvw/ to the queue.
```

**2. Scheduled Output** — Create a cron job to trigger skill output automatically

```
Create a book-companion cron job: run the `book-companion` skill every 5 minutes, but first check Telegram conversation history with `session_search`. Only send content if there has been new conversation activity since the last send. Name it `book-companion-runner`, deliver to origin.
```

### Config

`config.env` (skill root directory):
```
FISH_MIN_CHARS=100
```

---

## 🇨🇳 中文

### 两个功能

**1. 添加内容** — 从 URL 提取文本填充队列（添加前清空旧队列）

```
运行 book-companion skill：从 https://www.136book.com/santiheji/fqlrcvw/ 添加内容到队列。
```

**2. 定时发出内容** — 让 agent 创建 cron job，定时触发 skill 输出内容

```
创建 book-companion 的 cron job：每5分钟自动运行 `book-companion` skill，但先通过 `session_search` 查询 Telegram 对话历史，只有在上次发送后有新对话活动时才发送内容，名称为 `book-companion-runner`，投递到 origin。
```

### 配置

`config.env`（技能根目录）:
```
FISH_MIN_CHARS=100
```

---

## 📝 License | 许可证

MIT

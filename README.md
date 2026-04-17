# book-companion 读书陪伴技能

> 📚 Load this skill to inject reading excerpts into every reply

---

**Jump to: [English](#-english) | [中文](#-中文)**

---

## 🇺🇸 English

### How It Works

**Load the skill** → Every reply automatically includes a passage from the queue.

**Unload / turn off** → Tell the agent to stop.

### Activate

```
Load book-companion skill
```

→ Agent calls `fish_insert.py` before every reply, concatenating a passage to the response.

### Deactivate

```
Turn off book-companion
```

→ Agent stops injecting content. Skill remains loaded but idle.

### Add Content

Fill the queue from a URL (clears old queue first):

```
Run book-companion skill: add content from https://www.purepen.com/sgyy/001.htm to the queue.
```

### Config

`config.env` (skill root directory):
```
FISH_MIN_CHARS=300
FISH_TRIGGER=～～
```

### Manage Queue

```bash
python3 scripts/fish_queue.py status   # view queue
python3 scripts/fish_queue.py clear    # clear queue
```

---

## 🇨🇳 中文

### 工作原理

**加载 skill** → 每条回复自动夹带一条队列中的内容。

**关闭** → 告诉 agent 停掉即可。

### 开启摸鱼

```
加载 book-companion
```

→ Agent 每次回复前调用 `fish_insert.py`，把摸鱼内容拼入回答。

### 关闭摸鱼

```
关掉摸鱼
```

→ Agent 停止夹带，skill 仍加载但不执行注入。

### 添加内容

从 URL 提取文本填充队列（添加前清空旧队列）：

```
运行 book-companion skill：从 https://www.purepen.com/sgyy/001.htm 添加内容到队列。
```

### 配置

`config.env`（技能根目录）:
```
FISH_MIN_CHARS=300
FISH_TRIGGER=～～
```

### 管理队列

```bash
python3 scripts/fish_queue.py status   # 查看队列
python3 scripts/fish_queue.py clear    # 清空队列
```

---

## 📝 License | 许可证

MIT

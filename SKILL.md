---
name: book-companion
description: 摸鱼skill - 加载后每条回复自动夹带摸鱼内容
---

# book-companion

加载此 skill = 开启摸鱼模式。每条回复前自动从队列取出一条内容拼入回答。

**关闭：** 告诉用户"关掉摸鱼"即可。

## 队列内容（当前）

`fish_queue.json` — 队列文件，位于技能根目录。

## 配置

`config.env`（技能根目录）：
```
FISH_MIN_CHARS=300
FISH_TRIGGER=～～
```

## 脚本说明

### fish_insert.py
每次运行从队列 pop 一条内容输出。**由 agent 在回复前调用**，不是定时执行。

### fish_queue.py
队列管理工具：
```bash
python3 scripts/fish_queue.py status   # 查看队列状态
python3 scripts/fish_queue.py clear    # 清空队列
```

### add_from_url.py
从 URL 提取文本填充队列（添加前清空旧队列）：
```bash
python3 scripts/add_from_url.py <URL>
```

## 使用方式

**开启摸鱼（每条回复都带）：**
```
加载 book-companion
```
→ agent 每次回复前自动调用 `fish_insert.py`，把内容拼入回答。

**关闭摸鱼：**
```
关掉摸鱼
```
→ agent 停止夹带，skill 仍加载但不再执行注入。

---

⚠️ 注意：skill 加载依赖 agent 配合执行脚本。如果 agent 跳过或不听话，用法会不稳定。

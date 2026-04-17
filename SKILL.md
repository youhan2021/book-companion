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

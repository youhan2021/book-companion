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

运行脚本输出一句队列内容：
```bash
python3 scripts/fish_insert.py
```

## 激活（只需一次）

```bash
python3 scripts/fish_queue.py activate
```

## 配置

`config.env`（技能根目录）：
```
FISH_MIN_CHARS=100
```

## 队列文件

`~/.hermes/fish_queue.json`

格式：`{"queue": [...], "active": bool}`

---

## 定时发出内容

让 agent 创建 cron job，参考 README 中的 prompt。

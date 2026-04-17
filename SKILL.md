---
name: book-companion
description: 摸鱼skill - 插入古典中文摘录到对话中
---

# book-companion

管理一个古典中文文本摘录队列，每次调用 `fish_insert.py` 从队列顺序读取内容输出。

## 快速开始

```bash
# 激活
python3 scripts/fish_queue.py activate

# 添加内容（先清空旧队列）
python3 scripts/add_from_url.py <URL>

# 手动插入
python3 scripts/fish_insert.py
```

## 队列管理

| 命令 | 说明 |
|------|------|
| `fish_queue.py activate` | 激活摸鱼模式 |
| `fish_queue.py status` | 查看队列状态 |
| `fish_queue.py clear` | 清空队列 |
| `fish_queue.py init` | 初始化队列 |

## 配置

`config.env`（技能根目录）:
```
FISH_MIN_CHARS=100
```

## 队列文件

`~/.hermes/fish_queue.json`

格式：`{"queue": [...], "active": bool}`

## Cron 集成

在 Hermes 中创建 cronjob，定时调用 `fish_insert.py` 并将输出作为回复一部分：

```
Every response must start by inserting 摸鱼 content.
Run: cd ~/.hermes/skills/leisure/book-companion && python3 scripts/fish_insert.py
and paste the output as the first part of your reply.
Never skip this.
```

用 `cronjob(action='create', ...)` 创建定时任务，附载 book-companion skill。

## 内容来源

使用 `add_from_url.py` 从 URL 提取内容填充队列。添加前会清空旧队列。

---
name: book-companion
description: 摸鱼skill - 加载后每条回复自动夹带摸鱼内容
---

# book-companion

加载此 skill = 开启摸鱼模式。每条回复前自动从队列取出一条内容拼入回答。

## 用法

| 命令 | 效果 |
|------|------|
| `加载 book-companion` | 开启摸鱼（队列已有内容自动复用） |
| `加载 book-companion，从 <url> 添加内容` | 清空队列 → 加载 url 内容 → 开启摸鱼 |
| `加载 <url> 内容到摸鱼队列` | 仅加载内容，不开启摸鱼 |
| `关闭 book-companion` | 关闭摸鱼，skill 保留在内存中 |

## 配置

`config.env`（技能根目录）：
```
FISH_MIN_CHARS=300
```

## 队列文件

`fish_queue.json` — 位于技能根目录，加载 skill 后队列内容持久化。

## 脚本说明

### fish_insert.py
每次运行从队列 pop 一条内容输出。**由 agent 在回复前调用**，不是定时执行。

### fish_queue.py
```bash
python3 scripts/fish_queue.py status   # 查看队列状态
python3 scripts/fish_queue.py clear    # 清空队列
```

### add_from_url.py
从 URL 提取文本填充队列（添加前清空旧队列）：
```bash
python3 scripts/add_from_url.py <URL>
```

---

⚠️ 注意：skill 依赖 agent 主动调用脚本，偶尔可能跳过，不保证 100% 稳定。

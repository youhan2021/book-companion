---
name: book-companion
description: 摸鱼skill - 加载后每条回复自动夹带摸鱼内容
---

# book-companion

**激活条件（自动加载）：** 当用户说"开始摸鱼"、"开始 book companion"、"start book companion"时，必须立即执行 `skill_view("book-companion")` 加载此 skill，然后按下方流程执行。

## 命令

| 命令 | 效果 |
|------|------|
| `开始摸鱼` / `开始 book companion` / `start book companion` | **立即加载 skill**，每条回复夹带一条内容 |
| `开始摸鱼 <url>` / `开始 book companion <url>` | 清空队列 → 加载 url 内容 → 开启摸鱼 |
| `摸鱼内容 <url>` / `load book from <url>` | 仅加载 url 内容到队列 |
| `结束摸鱼` / `stop book companion` | 关闭摸鱼 |

## 流程（每次回复前必须执行）

1. 加载 skill：`skill_view("book-companion")`
2. 运行 `cd /home/ubuntu/.hermes/skills/leisure/book-companion && python3 scripts/fish_insert.py`
3. 将脚本输出**拼接**在回复正文**之前**
4. 如果队列为空，先运行 `add_from_url.py` 加载默认内容

## 配置

`config.env`（技能根目录）：
```
FISH_MIN_CHARS=300
```

## 脚本说明

### fish_insert.py
每次运行从队列 pop 一条内容输出。

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

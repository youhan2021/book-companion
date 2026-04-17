---
name: book-companion
description: 摸鱼skill - 加载后每条回复自动夹带摸鱼内容
---

# book-companion

## 激活条件

当用户说"开始摸鱼"、"开始 book companion"、"start book companion"时，**必须立即**执行：

1. `skill_view("book-companion")` 加载此 skill
2. 运行 `cd /home/ubuntu/.hermes/skills/leisure/book-companion && python3 scripts/fish_insert.py`
3. 将脚本输出**拼接在回复正文之前**
4. 然后再处理用户的其他问题

## 强制约束（每次说话后必须执行）

**在处理用户任何其他问题之前**，必须先执行注入：

```
cd /home/ubuntu/.hermes/skills/leisure/book-companion && python3 scripts/fish_insert.py
```

将输出拼接到回复最前面，**不要在注入内容之前添加任何文字或解释**。

如果用户没有说"开始摸鱼"或类似激活语，跳过注入。

## 命令

| 命令 | 效果 |
|------|------|
| `开始摸鱼` / `开始 book companion` / `start book companion` | **立即加载 skill 并执行注入**，之后每句话都先注入 |
| `开始摸鱼 <url>` / `start book companion <url>` | 清空队列 → 加载 url 内容 → 开启摸鱼 |
| `摸鱼内容 <url>` / `load book from <url>` | 仅加载 url 内容到队列 |
| `结束摸鱼` / `stop book companion` | 关闭摸鱼 |

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

⚠️ 强制执行：注入必须每次都做，不允许跳过。

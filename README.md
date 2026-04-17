# book-companion 读书陪伴技能

> 📚 Inject reading excerpts into every reply — load once, enjoy forever

---

**Jump to: [🇺🇸 English](#-english) | [🇨🇳 中文](#-中文)**

---

## 🇺🇸 English

### What It Does

Load this skill → Every reply automatically includes a passage from the queue. No triggers, no cron — just load and go.

### Installation

```bash
cd ~/.hermes/skills/leisure
git clone https://github.com/youhan2021/book-companion.git
cd book-companion
git remote set-url origin https://<YOUR_TOKEN>@github.com/youhan2021/book-companion.git
```

### Setup

```bash
cd book-companion
cp config.env.example.txt config.env
```

Optionally fill the queue with content from a URL:
```bash
python3 scripts/add_from_url.py https://www.purepen.com/sgyy/001.htm
```

### Usage

| Command | Effect |
|---------|--------|
| `Load book-companion` | Start mò yú — every reply gets a passage |
| `Load book-companion, add from <url>` | Clear queue → load url → start mò yú |
| `Add <url> to mò yú queue` | Load content only, no mò yú |
| `Turn off book-companion` | Stop injecting, skill stays in memory |

### Config

`config.env`:
```
FISH_MIN_CHARS=300
```

### Manage Queue

```bash
python3 scripts/fish_queue.py status   # view queue
python3 scripts/fish_queue.py clear    # clear queue
```

---

## 🇨🇳 中文

### 功能说明

加载此 skill → 每条回复自动夹带一条队列中的内容。不需要触发词，不需要定时任务，加载就能用。

### 安装方法

```bash
cd ~/.hermes/skills/leisure
git clone https://github.com/youhan2021/book-companion.git
cd book-companion
git remote set-url origin https://<YOUR_TOKEN>@github.com/youhan2021/book-companion.git
```

### 初始化

```bash
cd book-companion
cp config.env.example.txt config.env
```

可选：先用 URL 填充队列内容：
```bash
python3 scripts/add_from_url.py https://www.purepen.com/sgyy/001.htm
```

### 用法

| 命令 | 效果 |
|------|------|
| `加载 book-companion` | 开启摸鱼，每条回复都夹带一条内容 |
| `加载 book-companion，从 <url> 添加内容` | 清空队列 → 加载 url 内容 → 开启摸鱼 |
| `加载 <url> 内容到摸鱼队列` | 仅加载内容，不开启摸鱼 |
| `关闭 book-companion` | 停止夹带，skill 保留在内存中 |

### 配置

`config.env`:
```
FISH_MIN_CHARS=300
```

### 管理队列

```bash
python3 scripts/fish_queue.py status   # 查看队列状态
python3 scripts/fish_queue.py clear    # 清空队列
```

---

## 📝 License | 许可证

MIT

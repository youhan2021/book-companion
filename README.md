# book-companion 读书陪伴技能

> 📚 Inject reading excerpts into every reply — load once, enjoy forever

---

**Jump to: [🇺🇸 English](#-english) | [🇨🇳 中文](#-中文)**

---

## 🇺🇸 English

### What It Does

Load this skill → Every reply automatically includes a passage from the queue.

### Installation

```
Run book-companion skill: install from https://github.com/youhan2021/book-companion.git
```

### Setup

```
Run book-companion skill: setup config
```

### Commands

| Prompt | Effect |
|---------|--------|
| `start book companion` | Start mò yú — every reply gets a passage |
| `start book companion <url>` | Clear queue → load url → start mò yú |
| `load book from <url>` | Load content to queue only, no mò yú |
| `stop book companion` | Stop injecting |

### Config

`config.env`:
```
FISH_MIN_CHARS=300
```

### Manage Queue

```
Run book-companion skill: show queue status
```

```
Run book-companion skill: clear queue
```

---

## 🇨🇳 中文

### 功能说明

加载此 skill → 每条回复自动夹带一条队列中的内容。

### 安装

```
运行 book-companion skill：从 https://github.com/youhan2021/book-companion.git 安装
```

### 初始化

```
运行 book-companion skill：初始化配置
```

### 命令

| 指令 | 效果 |
|------|------|
| `开始摸鱼` | 开启摸鱼，每条回复夹带一条内容 |
| `开始摸鱼 <url>` | 清空队列 → 加载 url 内容 → 开启摸鱼 |
| `摸鱼内容 <url>` | 仅加载 url 内容到队列 |
| `结束摸鱼` | 关闭摸鱼 |

### 配置

`config.env`:
```
FISH_MIN_CHARS=300
```

### 管理队列

```
运行 book-companion skill：查看队列状态
```

```
运行 book-companion skill：清空队列
```

---

## 📝 License | 许可证

MIT

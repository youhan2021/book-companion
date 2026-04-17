# book-companion 读书陪伴技能

> 📚 Insert classical Chinese text excerpts into your conversations

两个功能：**添加内容** 和 **定时发出内容**。

---

**Jump to: [English](#-english) | [中文](#-中文)**

---

## 🇺🇸 English

### 两个功能

**1. 添加内容** — 从 URL 提取文本填充队列（添加前清空旧队列）
```bash
python3 scripts/add_from_url.py <URL>
```

**2. 定时发出内容** — 通过 cron 定时触发
```python
cronjob(
    action='create',
    prompt='Run book-companion skill and output the content.',
    schedule='*/5 * * * *',
    name='fish-watchdog',
    deliver='origin',
    skills=['book-companion']
)
```

### 激活（只需一次）
```bash
python3 scripts/fish_queue.py activate
```

### 配置

`config.env`（技能根目录）:
```
FISH_MIN_CHARS=100
```

---

## 🇨🇳 中文

### 两个功能

**1. 添加内容** — 从 URL 提取文本填充队列（添加前清空旧队列）
```bash
python3 scripts/add_from_url.py <URL>
```

**2. 定时发出内容** — 通过 cron 定时触发
```python
cronjob(
    action='create',
    prompt='Run book-companion skill and output the content.',
    schedule='*/5 * * * *',
    name='fish-watchdog',
    deliver='origin',
    skills=['book-companion']
)
```

### 激活（只需一次）
```bash
python3 scripts/fish_queue.py activate
```

### 配置

`config.env`（技能根目录）:
```
FISH_MIN_CHARS=100
```

---

## 📝 License | 许可证

MIT

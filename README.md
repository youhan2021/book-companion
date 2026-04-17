# book-companion 读书陪伴技能

> 📚 Insert classical Chinese text excerpts into your conversations

**book-companion** manages a queue of classical Chinese text excerpts. Call `fish_insert.py` and paste the output into your replies.

---

**Jump to: [English](#-english) | [中文](#-中文)**

---

## 🇺🇸 English

### Installation

```bash
git clone https://github.com/youhan2021/book-companion.git
# Copy to: ~/.hermes/skills/book-companion/
```

### Setup

```bash
cd ~/.hermes/skills/book-companion

# Activate
python3 scripts/fish_queue.py activate

# Add content from URL (clears old queue first)
python3 scripts/add_from_url.py <URL>

# Manual insert
python3 scripts/fish_insert.py
```

### Queue Management

```bash
python3 scripts/fish_queue.py status      # View status
python3 scripts/fish_queue.py clear       # Clear queue
python3 scripts/fish_queue.py deactivate  # Turn off
```

### Configuration

Edit `config.env` in skill root:
```env
FISH_MIN_CHARS=100      # Min characters per insert
```

### Cron Integration

Create a cronjob that inserts 摸鱼 content on a schedule. The prompt is fully customizable:

```
Every response must start by inserting 摸鱼 content.
Paste the output as the first part of your reply.
Never skip this.
```

In Hermes, use:
```python
cronjob(
    action='create',
    prompt='Your custom prompt here...',
    schedule='*/2 * * * *',
    name='fish-watchdog',
    deliver='origin',
    skills=['book-companion']
)
```

---

## 🇨🇳 中文

### 安装

```bash
git clone https://github.com/youhan2021/book-companion.git
# 复制到: ~/.hermes/skills/book-companion/
```

### 快速开始

```bash
cd ~/.hermes/skills/book-companion

# 激活
python3 scripts/fish_queue.py activate

# 从 URL 添加内容（先清空旧队列）
python3 scripts/add_from_url.py <URL>

# 手动插入
python3 scripts/fish_insert.py
```

### 队列管理

```bash
python3 scripts/fish_queue.py status      # 查看状态
python3 scripts/fish_queue.py clear       # 清空队列
python3 scripts/fish_queue.py deactivate  # 关闭
```

### 配置

编辑技能根目录 `config.env`：
```env
FISH_MIN_CHARS=100      # 每次插入最小字数
```

### Cron 集成

创建 cronjob，定时插入摸鱼内容。prompt 可完全自定义：

```
每次回复必须首先插入摸鱼内容。
将输出作为回复正文的第一部分。
永不跳过。
```

在 Hermes 中使用：
```python
cronjob(
    action='create',
    prompt='你的自定义 prompt...',
    schedule='*/2 * * * *',
    name='fish-watchdog',
    deliver='origin',
    skills=['book-companion']
)
```

---

## 📝 License | 许可证

MIT

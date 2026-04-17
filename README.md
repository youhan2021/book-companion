# book-companion 摸鱼技能

> 🐟 A leisure reading companion skill — automatically inserts classical Chinese text excerpts between your conversations

**book-companion** is a skill for Hermes Agent that manages a reading queue of classical Chinese texts. After activation, every reply will automatically include excerpts from the queue, creating a meditative "摸鱼" (slacking) experience woven into your work sessions.

---

## 📦 Installation | 安装

### From GitHub

```bash
cd ~/.hermes/skills/leisure
git clone https://github.com/owner/repo.git
```

### Manual Setup

```bash
# 1. Create the skill directory
mkdir -p ~/.hermes/skills/leisure/book-companion

# 2. Copy all files from this repo into that directory
# 3. The queue file will be created automatically at:
~/.hermes/fish_queue.json
```

---

## 🚀 Quick Start | 快速开始

### Activate the Skill

```bash
cd ~/.hermes/skills/leisure/book-companion
python3 scripts/fish_queue.py activate
```

### Add Content from URL | 从 URL 添加内容

```bash
# Supported sites: 笔趣阁 (various), purepen.com
python3 scripts/add_from_url.py <URL>
```

Example:
```bash
python3 scripts/add_from_url.py https://www.purepen.com/huagong/
```

⚠️ Adding new content **clears the existing queue** first.

---

## 📖 Usage | 使用方法

### Insert Fish Content | 插入摸鱼内容

The skill is called automatically by Hermes Agent on every reply. To manually trigger an insert:

```bash
python3 scripts/fish_insert.py
```

This outputs the next excerpt from the queue (or multiple excerpts until the minimum character count is reached).

### Manage the Queue | 管理队列

```bash
# View status
python3 scripts/fish_queue.py status

# Get next item (reads and removes it)
python3 scripts/fish_queue.py next

# Clear the queue
python3 scripts/fish_queue.py clear

# Deactivate fish mode
python3 scripts/fish_queue.py deactivate
```

### Configuration | 配置

Edit `scripts/config.env`:

```env
FISH_MIN_CHARS=100      # Minimum characters per insert (default: 100)
FISH_INSERT_RATIO=5     # Insert once per N lines of reply (default: 5)
```

Or use the config command:

```bash
python3 scripts/fish_insert.py config get FISH_MIN_CHARS
python3 scripts/fish_insert.py config set FISH_MIN_CHARS 200
```

---

## 🔧 How It Works | 工作原理

```
User Message
    │
    ▼
Hermes loads book-companion skill
    │
    ▼
[Rule 0 - Iron Rule]
Every reply MUST start by inserting fish content
    │
    ▼
fish_insert.py reads from ~/.hermes/fish_queue.json
    │
    ▼
Loops until total characters >= FISH_MIN_CHARS (default 100)
    │
    ▼
Output is pasted directly into the reply body
```

---

## 📁 File Structure | 文件结构

```
book-companion/
├── SKILL.md                          # Skill definition & rules
├── README.md                         # This file
├── config.env                        # Global config
├── config.env.example.txt            # Config template
└── scripts/
    ├── fish_insert.py                # Core insert logic
    ├── fish_queue.py                 # Queue management
    ├── add_from_url.py               # URL content extractor
    ├── fish_watchdog.sh              # Watchdog monitor (optional)
    └── config.env                    # Runtime config
```

---

## ⚙️ Queue File | 队列文件

**Location:** `~/.hermes/fish_queue.json`

**Format:**
```json
{
  "queue": [
    "First excerpt...",
    "Second excerpt...",
    "Third excerpt..."
  ],
  "active": true
}
```

Each `fish_queue.py next` call removes the first item permanently.

---

## ⚠️ Important Rules | 重要规则

1. **Rule 0 (Iron Rule):** Every reply MUST insert fish content first — never skip
2. **Queue only:** Content comes strictly from the queue — never generate content
3. **Clear on add:** Adding new content clears the existing queue
4. **Sequential read:** Items are read in order — no random

---

## 🔍 Troubleshooting | 故障排除

**Q: Nothing happens when I call `fish_insert.py`**
A: Check that `~/.hermes/fish_queue.json` exists and has items:
```bash
python3 scripts/fish_queue.py status
```

**Q: Queue is empty**
A: Add content from a URL:
```bash
python3 scripts/add_from_url.py <novel_url>
```

**Q: Character count too low**
A: Increase `FISH_MIN_CHARS` in `scripts/config.env`

---

## 📝 License

MIT — use freely, modify as needed.

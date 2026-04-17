# book-companion 读书陪伴技能

> 📚 A reading companion skill — insert classical Chinese text excerpts into your conversations

**book-companion** is a skill that manages a reading queue of classical Chinese texts. It can insert excerpts from the queue into your conversations, serving as a meditative reading companion. While 摸鱼 (slacking) is one popular use case, it's equally great for language learning, cultural exploration, or simply enjoying classical literature in daily chat.

---

## 📦 Installation (OpenClaw)

```bash
# Via git clone
git clone https://github.com/owner/repo.git

# Or manually copy this directory into your OpenClaw skills folder:
# ~/.openclaw/skills/book-companion/
```

---

## 🚀 Quick Start

### Activate

```bash
cd ~/.openclaw/skills/book-companion
python3 scripts/fish_queue.py activate
```

### Add Content from URL

```bash
python3 scripts/add_from_url.py <URL>
```

Supported sites: 笔趣阁 (various mirrors), purepen.com

Example:
```bash
python3 scripts/add_from_url.py https://www.purepen.com/huagong/
```

> ⚠️ Adding new content **clears the existing queue** first.

### Manual Insert

```bash
python3 scripts/fish_insert.py
```

---

## 📖 Usage

### Queue Management

```bash
python3 scripts/fish_queue.py status    # View status
python3 scripts/fish_queue.py next     # Get next item (removes it)
python3 scripts/fish_queue.py clear     # Clear queue
python3 scripts/fish_queue.py deactivate  # Turn off
```

### Configuration

Edit `scripts/config.env`:

```env
FISH_MIN_CHARS=100      # Min characters per insert (default: 100)
FISH_INSERT_RATIO=5     # Insert once per N lines (default: 5)
```

Or via command:

```bash
python3 scripts/fish_insert.py config get FISH_MIN_CHARS
python3 scripts/fish_insert.py config set FISH_MIN_CHARS 200
```

---

## 🔧 How It Works

```
User Message
    │
    ▼
Skill loaded → every reply inserts a classical Chinese excerpt
    │
    ▼
fish_insert.py reads from ~/.hermes/fish_queue.json
    │
    ▼
Loops until characters >= FISH_MIN_CHARS (default 100)
    │
    ▼
Output pasted into reply body
```

---

## 📁 File Structure

```
book-companion/
├── SKILL.md                    # Skill definition & rules
├── README.md                   # This file
├── config.env                  # Global config
└── scripts/
    ├── fish_insert.py          # Core insert logic
    ├── fish_queue.py           # Queue management
    ├── add_from_url.py         # URL content extractor
    └── config.env             # Runtime config
```

---

## ⚙️ Queue File

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

Each `next` call permanently removes the first item.

---

## ⚠️ Rules

1. **Rule 0:** Every reply inserts fish content first — never skip
2. **Queue only:** Content comes strictly from the queue — never generate
3. **Clear on add:** Adding new content clears the existing queue
4. **Sequential read:** Items are read in order — no random

---

## 🔍 Troubleshooting

**Q: Nothing happens when I call `fish_insert.py`**
A: Check the queue exists and has items:
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

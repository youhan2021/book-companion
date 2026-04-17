# book-companion 读书陪伴技能

> 📚 A reading companion skill — insert classical Chinese text excerpts into your conversations

**book-companion** is a skill that manages a reading queue of classical Chinese texts. It inserts excerpts from the queue into your conversations, serving as a meditative reading companion. While 摸鱼 (slacking) is one popular use case, it's equally great for language learning, cultural exploration, or simply enjoying classical literature in daily chat.

---

**Jump to: [English](#-english) | [中文](#-中文)**  

---

## 🇺🇸 English

### 🇺🇸 Installation (OpenClaw)

```bash
git clone https://github.com/youhan2021/book-companion.git
# Or manually copy to: ~/.openclaw/skills/book-companion/
```

### 🇺🇸 Adding to Your Agent Prompt

After installation, add this to your OpenClaw/Hermes system prompt:

```
Load the book-companion skill for every reply. Every response must start by inserting
classical Chinese text excerpts from ~/.hermes/fish_queue.json using:
  cd ~/.openclaw/skills/book-companion && python3 scripts/fish_insert.py

Rules:
- Always insert fish content FIRST before any other action
- Queue is at ~/.hermes/fish_queue.json
- Never generate content yourself — only from queue
```

### 🇺🇸 Quick Start

**Activate:**
```bash
cd ~/.openclaw/skills/book-companion
python3 scripts/fish_queue.py activate
```

**Add content from URL:**
```bash
python3 scripts/add_from_url.py <URL>
```
> ⚠️ Adding new content **clears the existing queue** first.

**Manual insert:**
```bash
python3 scripts/fish_insert.py
```

### 🇺🇸 Queue Management

```bash
python3 scripts/fish_queue.py status      # View status
python3 scripts/fish_queue.py next        # Get next item (removes it)
python3 scripts/fish_queue.py clear       # Clear queue
python3 scripts/fish_queue.py deactivate  # Turn off
```

### 🇺🇸 Configuration

Edit `config.env` in the skill root directory:
```env
FISH_MIN_CHARS=100      # Min characters per insert (default: 100)
```

Or via command:
```bash
python3 scripts/fish_insert.py config get FISH_MIN_CHARS
python3 scripts/fish_insert.py config set FISH_MIN_CHARS 200
```

### 🇺🇸 How It Works

```
User Message → Skill in prompt → Inserts classical Chinese excerpt
                    ↓
            fish_insert.py reads ~/.hermes/fish_queue.json
                    ↓
            Loops until characters >= FISH_MIN_CHARS (default 100)
                    ↓
            Output pasted into reply body
```

### 🇺🇸 File Structure

```
book-companion/
├── SKILL.md                    # Skill definition & rules
├── README.md                   # This file
├── config.env                  # Global config
└── scripts/
    ├── fish_insert.py          # Core insert logic
    ├── fish_queue.py           # Queue management
    └── add_from_url.py         # URL content extractor
```

### 🇺🇸 Queue File

**Location:** `~/.hermes/fish_queue.json`

**Format:**
```json
{
  "queue": ["First excerpt...", "Second excerpt..."],
  "active": true
}
```

Each `next` call permanently removes the first item.

### 🇺🇸 Rules

1. **Rule 0:** Every reply inserts fish content first — never skip
2. **Queue only:** Content comes strictly from the queue — never generate
3. **Clear on add:** Adding new content clears the existing queue
4. **Sequential read:** Items are read in order — no random

### 🇺🇸 Troubleshooting

**Q: Nothing happens when calling `fish_insert.py`**
A: Check queue status:
```bash
python3 scripts/fish_queue.py status
```

**Q: Queue is empty**
A: Add content from URL:
```bash
python3 scripts/add_from_url.py <novel_url>
```

**Q: Character count too low**
A: Increase `FISH_MIN_CHARS` in `config.env`

---

## 🇨🇳 中文

### 🇨🇳 安装 (OpenClaw)

```bash
git clone https://github.com/youhan2021/book-companion.git
# 或手动复制到: ~/.openclaw/skills/book-companion/
```

### 🇨🇳 添加到 Agent Prompt

安装完成后，将以下内容添加到你的 OpenClaw/Hermes 系统提示词中：

```
Load the book-companion skill for every reply. Every response must start by inserting
classical Chinese text excerpts from ~/.hermes/fish_queue.json using:
  cd ~/.openclaw/skills/book-companion && python3 scripts/fish_insert.py

规则：
- 所有其他操作之前，必须首先插入摸鱼内容
- 队列文件位于 ~/.hermes/fish_queue.json
- 严禁自行生成内容 — 仅从队列读取
```

### 🇨🇳 快速开始

**激活技能：**
```bash
cd ~/.openclaw/skills/book-companion
python3 scripts/fish_queue.py activate
```

**从 URL 添加内容：**
```bash
python3 scripts/add_from_url.py <URL>
```
> ⚠️ 添加新内容会先清空现有队列。

**手动插入：**
```bash
python3 scripts/fish_insert.py
```

### 🇨🇳 队列管理

```bash
python3 scripts/fish_queue.py status      # 查看状态
python3 scripts/fish_queue.py next       # 获取下一条（读取后删除）
python3 scripts/fish_queue.py clear       # 清空队列
python3 scripts/fish_queue.py deactivate  # 关闭摸鱼模式
```

### 🇨🇳 配置

编辑技能根目录的 `config.env`：
```env
FISH_MIN_CHARS=100      # 每次插入最小字数（默认100）
```

或通过命令：
```bash
python3 scripts/fish_insert.py config get FISH_MIN_CHARS
python3 scripts/fish_insert.py config set FISH_MIN_CHARS 200
```

### 🇨🇳 工作原理

```
用户消息 → 技能在prompt中 → 插入古文摘录
                    ↓
         fish_insert.py 读取 ~/.hermes/fish_queue.json
                    ↓
         循环直到总字数 >= FISH_MIN_CHARS（默认100）
                    ↓
         输出直接粘贴到回复正文
```

### 🇨🇳 文件结构

```
book-companion/
├── SKILL.md                    # 技能定义与规则
├── README.md                   # 本文件
├── config.env                  # 全局配置
└── scripts/
    ├── fish_insert.py          # 核心插入逻辑
    ├── fish_queue.py           # 队列管理
    └── add_from_url.py         # URL 内容提取
```

### 🇨🇳 队列文件

**位置：** `~/.hermes/fish_queue.json`

**格式：**
```json
{
  "queue": ["第一条摘录...", "第二条摘录..."],
  "active": true
}
```

每次 `next` 调用会永久删除第一条。

### 🇨🇳 规则

1. **规则0：** 每条回复必须先插入摸鱼内容——永不跳过
2. **仅从队列获取：** 内容严格来自队列，不自行生成
3. **添加时清空：** 添加新内容会清空现有队列
4. **顺序读取：** 按顺序读取，不随机

### 🇨🇳 故障排除

**Q: 调用 `fish_insert.py` 后没反应**
A: 检查队列状态：
```bash
python3 scripts/fish_queue.py status
```

**Q: 队列为空**
A: 从 URL 添加内容：
```bash
python3 scripts/add_from_url.py <小说URL>
```

**Q: 字数不够**
A: 在 `config.env` 中调高 `FISH_MIN_CHARS`

---

## 📝 License | 许可证

MIT — use freely, modify as needed. | MIT — 自由使用，随意修改。

---

*Jump to: [🇺🇸 English](#-english) | [🇨🇳 中文](#-中文)*

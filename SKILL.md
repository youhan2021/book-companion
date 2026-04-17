---
name: book-companion
description: 摸鱼skill - 激活摸鱼队列，每次回复自动插入摸鱼内容
---

# book-companion

激活摸鱼队列后，每次回复都会按顺序插入摸鱼内容。

## 持久化机制

`activate` 时会将铁则写入 `~/.hermes/fish_queue.json` 的 `_system_reminder` 字段，该字段在队列文件中永久存在。每次会话启动时 Hermes 会读取此字段，使约束深入系统层面而非仅存在于 SKILL.md。

## 核心规则（最高优先级）

0. **【铁则-最重要】每次回复的第二步 = 插入摸鱼内容** — 不可遗漏！不可跳过！不可先用浏览器！不可先搜索！不可先做其他任何事！流程必须是：
   - **第一步（最先）**：执行用户请求的所有工具调用（搜索、浏览网页、终端命令等）
   - **第二步（之后）**：调用 `fish_insert.py`，获取摸鱼内容并插入回复
   - **第三步（最后）**：在摸鱼内容之后，给出分析/结论

### 自动执行触发机制（无条件执行）

**触发条件：收到用户消息的同一时刻，无条件立即执行！**

```
伪代码：
if 用户发送了任何消息:
    # 第一步：先执行所有工具调用
    DO: 执行搜索、终端命令、浏览器等所有需要的工具

    # 第二步：获取摸鱼内容（必须在工具调用之后、结论之前）
    DO: cd ~/.hermes/skills/leisure/book-companion && python3 scripts/fish_insert.py
    OUTPUT = 获取的摸鱼内容

    # 把 OUTPUT 粘贴到回复正文（必须！工具输出≠回复正文）
    返回: 第一步的工具结果 + "\n" + OUTPUT + "\n" + 本次回复的分析/结论

    # 禁止任何其他行为！
    禁止在第二步之前给出任何分析结论
```

**第二步必须同时满足两个条件：**
1. 调用 `cd ~/.hermes/skills/leisure/book-companion && python3 scripts/fish_insert.py`
2. 把输出内容原封不动地粘贴到回复正文

**缺一不可！工具调用≠回复正文！工具输出是单独显示的，只有粘贴到正文中才生效！**

⚠️ **绝对禁止在第二步之前给出任何分析结论！包括：**
- ❌ 读文件 / 读 SKILL.md
- ❌ 分析问题原因
- ❌ 搜索
- ❌ 打开浏览器
- ❌ 调用任何工具
- ❌ 先给出任何结论或判断

⚠️ **即使消息只有一个字 "hi"，也必须在所有工具调用完成后第二步插入摸鱼！**

### 输出要求（必须做到）

**`fish_insert.py` 的输出必须作为回复正文的一部分出现，不能只是 tool call 的返回值！**

正确做法：把输出内容复制/粘贴到回复正文中，放在最前面。
错误做法：只调用工具，tool 输出单独显示，用户看不到。
1. **摸鱼内容必须严格从队列获取** — 绝不自己生成任何内容
2. **添加时清空** — 使用 add_from_url.py 添加新内容时，先清空旧队列
3. **顺序读取** — 队列按顺序读取，不随机

## 工作流程（每次回复必须执行）

**⚠️ 触发时机：所有工具调用完成后、给出分析结论之前！**

1. **第一步（最先）**：执行用户请求的所有工具调用（搜索、浏览网页、终端命令等）
2. **第二步（之后）**：立即调用 `cd ~/.hermes/skills/leisure/book-companion && python3 scripts/fish_insert.py`，把输出插入到回复正文
3. **第三步（最后）**：在摸鱼内容之后，给出本次回复的分析/结论

**关键点：摸鱼插入在工具调用之后、结论之前。终端输出 ≠ 回复正文，必须手动把摸鱼内容粘贴到正文！**

## 摸鱼字数规则

每次调用 `fish_insert.py`（无参数）时，持续从队列取内容，直到**总字数超过 `FISH_MIN_CHARS`（默认100字）**。即每次摸鱼至少100字，不够就继续从队列取下一条拼接。

## 网站编码和处理方式

### 编码检测顺序
```
utf-8 → gb2312 → gbk → gb18030 → utf-8 (errors=replace)
```

### HTML 正文提取
| 网站 | 标签 | 处理 |
|------|------|------|
| purepen.com | `<pre>` | 长文本按 `。！？` 分句 |
| 一般笔趣阁 | `<p>` / `<div id=content>` | 段落提取 |

### 反爬警告
- ❌ 99csw.com — Cloudflare 保护
- ❌ piaotia.com — Cloudflare 保护
- ✅ purepen.com — 可直接抓取（GB2312）
- ⚠️ 笔趣阁系 — 搜索功能常坏，尝试直接猜 book ID

### curl 测试命令
```bash
curl -s -L -A "Mozilla/5.0" "URL" | iconv -f gb2312 -t utf-8 2>/dev/null | head -20
```

## 脚本说明

### fish_queue.py - 队列管理
```bash
python3 ~/.hermes/skills/leisure/book-companion/scripts/fish_queue.py next      # 获取下一条（读取后删除）
python3 ~/.hermes/skills/leisure/book-companion/scripts/fish_queue.py activate  # 激活摸鱼模式
python3 ~/.hermes/skills/leisure/book-companion/scripts/fish_queue.py status    # 查看状态
python3 ~/.hermes/skills/leisure/book-companion/scripts/fish_queue.py clear     # 清空队列
python3 ~/.hermes/skills/leisure/book-companion/scripts/fish_queue.py init       # 初始化队列
```

### add_from_url.py - 添加内容
```bash
python3 ~/.hermes/skills/leisure/book-companion/scripts/add_from_url.py <URL>
# 添加前会先清空旧队列，保证下一条一定是最新内容
```

### fish_insert.py - 插入内容
```bash
# 无参数：获取符合最小字数要求的摸鱼内容（供我直接调用）
python3 ~/.hermes/skills/leisure/book-companion/scripts/fish_insert.py

# 有参数：判断是否应该插入并输出
python3 ~/.hermes/skills/leisure/book-companion/scripts/fish_insert.py <总调用数> <已插入数> <回复行数>

# 配置查看/设置
python3 ~/.hermes/skills/leisure/book-companion/scripts/fish_insert.py config get <配置名>
python3 ~/.hermes/skills/leisure/book-companion/scripts/fish_insert.py config set <配置名> <值>
```

## 配置项

| 配置 | 默认值 | 说明 |
|------|--------|------|
| FISH_MIN_CHARS | 100 | 每次摸鱼最小字数，持续取直到超过此字数 |

## 内容来源

用户通过 add_from_url.py 提供URL，脚本从URL提取内容填充队列。

## 队列文件

`~/.hermes/fish_queue.json`

队列结构：`{"queue": [...], "active": bool}`，无 index 字段，next 命令 pop(0) 读取第一条后删除。

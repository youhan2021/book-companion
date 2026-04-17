---
name: book-companion
description: 摸鱼skill - 激活摸鱼队列，每次回复自动插入摸鱼内容
---

# book-companion

激活摸鱼队列后，每次回复都会按顺序插入摸鱼内容。

## 核心规则（最高优先级）

0. **【铁则-最重要】每次回复的第一步 = 插入摸鱼内容** — 不可遗漏！不可跳过！不可先用浏览器！不可先搜索！不可先做其他任何事！流程必须是：
   - **第一步（最先）**：调用 `fish_insert.py`，获取摸鱼内容并插入回复
   - **第二步（之后）**：再执行用户请求（搜索、浏览网页、代码等）
   - **第三步（最后）**：确认本次回复已包含摸鱼内容

### 自动执行触发机制（无条件执行）

**触发条件：收到用户消息的同一时刻，无条件立即执行！**

```
伪代码：
if 用户发送了任何消息:
    立即执行: cd ~/.hermes/skills/leisure/book-companion && python3 scripts/fish_insert.py
    把输出插入回复最前面
    然后才能做其他任何事情
```

⚠️ **绝对禁止在摸鱼插入之前执行任何操作！包括：**
- ❌ 读文件 / 读 SKILL.md
- ❌ 分析问题原因
- ❌ 搜索
- ❌ 打开浏览器
- ❌ 调用任何工具

⚠️ **即使消息只有一个字 "hi"，也必须先插入摸鱼！**
1. **摸鱼内容必须严格从队列获取** — 绝不自己生成任何内容
2. **添加时清空** — 使用 add_from_url.py 添加新内容时，先清空旧队列
3. **顺序读取** — 队列按顺序读取，不随机

## 工作流程（每次回复必须执行）

**⚠️ 触发时机：收到用户消息的第一刻，立即执行摸鱼插入，永远在所有分析/调试行为之前！**

1. **第一步（最先）**：立即调用 `cd ~/.hermes/skills/leisure/book-companion && python3 scripts/fish_insert.py`，把输出插入到回复最前面
2. **第二步（之后）**：搜索、浏览网页、读文件、代码分析等操作
3. **第三步（最后）**：确认本次回复已包含摸鱼内容

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
| FISH_INSERT_RATIO | 5 | 每N行插入1次，最少1次（优先于INTERVAL） |
| FISH_INSERT_INTERVAL | 0 | 每N次工具调用插入一条（0表示禁用） |

## 内容来源

用户通过 add_from_url.py 提供URL，脚本从URL提取内容填充队列。

## 队列文件

`~/.hermes/fish_queue.json`

队列结构：`{"queue": [...], "active": bool}`，无 index 字段，next 命令 pop(0) 读取第一条后删除。

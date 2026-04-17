#!/usr/bin/env python3
"""
从URL获取古文内容并填充摸鱼队列

用法:
  python3 add_from_url.py <URL>
"""

import sys
import os
import urllib.request
import json
import re

# 添加skill目录到路径
SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SKILL_DIR)

from fish_queue import load_queue, save_queue

def fetch_page(url):
    """获取页面内容"""
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        raw = resp.read()
        # 尝试多种编码
        for enc in ("utf-8", "gb2312", "gbk", "gb18030"):
            try:
                return raw.decode(enc)
            except (UnicodeDecodeError, LookupError):
                continue
        # 最后 fallback
        return raw.decode("utf-8", errors="replace")

def extract_text(html):
    """从HTML中提取古文段落"""
    import re
    # 移除script和style标签
    html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
    html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL)
    
    texts = []
    
    # 先尝试提取<pre>标签中的内容（纯文学网站常用）
    pre_matches = re.findall(r'<pre[^>]*>(.*?)</pre>', html, re.DOTALL)
    for pre in pre_matches:
        text = re.sub(r'<[^>]+>', '', pre)
        text = text.replace('&nbsp;', ' ').replace('\xa0', ' ')
        text = text.strip()
        if len(text) > 50:
            # 按句号拆分
            sentences = re.split(r'([。！？])', text)
            for i in range(0, len(sentences) - 1, 2):
                s = (sentences[i] + sentences[i + 1]).strip()
                s = re.sub(r'\s+', ' ', s)
                if len(s) > 10:
                    texts.append(s)
    
    # 再提取<p>标签中的内容
    paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', html, re.DOTALL)
    for p in paragraphs:
        text = re.sub(r'<[^>]+>', '', p)
        text = text.strip()
        if len(text) > 10:
            texts.append(text)
    
    return texts

def main():
    if len(sys.argv) < 2:
        print("用法: python3 add_from_url.py <URL>")
        return
    
    url = sys.argv[1]
    print(f"正在获取页面: {url}")
    
    try:
        html = fetch_page(url)
        texts = extract_text(html)
        print(f"提取到 {len(texts)} 段文本")
        
        if not texts:
            print("未提取到内容")
            return
        
        data = load_queue()
        
        # 先清空旧内容，保证下一条一定是最新内容
        data["queue"] = []
        
        for text in texts:
            data["queue"].append(text)
        
        data["active"] = True
        save_queue(data)
        
        print(f"已添加 {len(texts)} 句到摸鱼队列")
        print(f"队列总数: {len(data['queue'])}")
        
    except Exception as e:
        print(f"错误: {e}")

if __name__ == "__main__":
    main()

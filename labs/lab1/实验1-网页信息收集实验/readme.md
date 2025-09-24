# Lab 1: Web-Info Collection Agent  
&gt; 2025 Fall · PKU AI-Enabled Programming  
&gt; Author: [@Pan-Yunze](https://github.com/Pan-Yunze) | ID: 2023141530019

---

## 🎯 Purpose  
1. Master the **LangGraph ReAct** pattern to build a reliable LLM-powered agent.  
2. Understand **HTTP + HTML basics** and implement two missing tools (`get_webpage_info`, `analyze_webpage`).  
3. Enforce a **“must-call-tool”** policy so the model never hallucinates web data.

---

## 🧱 Agent Architecture

```text
agent.py → create LLM → bind tools → ReAct-Agent → chat loop

| Module         | What it does                                                                     |
| -------------- | -------------------------------------------------------------------------------- |
| **LLM init**   | `ChatOpenAI(model='deepseek-chat', base_url='https://api.deepseek.com')`         |
| **Prompt**     | Lists 3 tools + hard rule: *“Any web-related request MUST call a tool”*.         |
| **ReAct loop** | `create_react_agent(llm, tools, prompt, debug=True)`                             |
| **Guard**      | If keywords like `网页｜html｜meta` trigger but no tool used → reject & ask for URL. |

##🌐 HTTP & HTML Primer
| Layer    | Key Points                                                                               |
| -------- | ---------------------------------------------------------------------------------------- |
| **HTTP** | Req-Line + Headers + Body → Resp-Line (status) + Headers + HTML bytes                    |
| **HTML** | `<html>` → `<head>` (meta, title, canonical) + `<body>` (header/nav/main/article/footer) |
| **DOM**  | Nested tags → tree; CSS selectors style it; depth = longest parent chain                 |

🔧 Tool Cheat-Sheet
表格
复制
Tool	In one sentence	How
search_subdomains	Grab sub-domains from Bing	Query domain:example.com, scrape <h2><a href="">, extract urlparse(link).netloc
get_webpage_info	Get “ID card” of a page	requests → status code; BeautifulSoup → <title>, <meta>, <link rel="canonical">
analyze_webpage	Give the page a “health check”	Parse DOM → total / unique tags, max depth, <main> → <article> → <body> fallback, count h1-3/p & links, 200-char snippet
💻 Implementation Highlights
1️⃣ get_webpage_info
Python
复制
resp  = requests.get(url, timeout=10)
soup  = BeautifulSoup(resp.text, 'lxml')

data = {
    "normalized_url": f"{parsed.scheme}://{parsed.netloc}{parsed.path}",
    "http_status"   : resp.status_code,
    "title"         : soup.title.string or "N/A",
    "description"   : soup.find("meta", attrs={"name":"description"})["content"] or "",
    "meta"          : {m.get("name") or m.get("property"): m["content"]
                       for m in soup.find_all("meta") if m.get("content")}
}
2️⃣ analyze_webpage
Python
复制
tags = soup.find_all(True)
data = {
    "dom_summary": {
        "total_tags"  : len(tags),
        "unique_tags" : len({t.name for t in tags}),
        "max_depth"   : max(len(list(t.parents)) for t in tags)
    },
    "main_content_strategy": "<main> → <article> → <body>",
    "important_node_count" : len(soup.find_all(["h1","h2","h3","p"])),
    "link_count"           : len(soup.find_all("a", href=True)),
    "main_text_snippet"    : main_text[:200]
}
🕹️ Quick Start
bash
复制
# 1. clone & install
git clone https://github.com/YOUR_ID/web-info-agent.git
cd web-info-agent
pip install -r requirements.txt

# 2. add key (or export it)
export OPENAI_API_KEY="sk-xxx"

# 3. run
python agent.py
Example chats
复制
>> 搜索 qq.com 的子域名
['https://im.qq.com', 'https://mail.qq.com', ...]

>> 获取网页信息 https://www.baidu.com
HTTP 200 | 标题: 百度一下，你就知道 | description: 全球领先的中文搜索引擎 ...

>> 分析网页结构 https://www.baidu.com
DOM 节点 634 个，深度 15，主内容区<body>，重要节点 68，链接 43 ...
📊 Fun Facts
百度首页没有 <main> / <article>，主内容策略被迫回退到 <body>。
部分站点（im.qq.com）返回 403，但 Server 头仍暴露 nginx。
Bing 子域名列表每次略有不同，与 Cookie 会话有关。
📁 File Map
复制
web-info-agent/
├─ agent.py          # 主入口（LLM + ReAct loop）
├─ tools/
│  └─ web_tools.py   # 三个工具的实现
├─ requirements.txt  # 依赖
└─ README.md         # this file
"""
简化的网页信息收集工具
"""

import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib.request import urlopen
from langchain_core.tools import tool
from datetime import datetime
import json
from uuid import uuid4

@tool
def search_subdomains(domain: str) -> list[str]:
    """搜索指定域名的子域名
    
    Args:
        domain (str): 要搜索的主域名，例如 "qq.com"
    
    Returns:
        list[str]: 子域名列表
    """
    try:
        print(f"正在搜索 {domain} 的子域名...")
        #定义请求头，绕过反爬机制
        headers = {
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 Edg/90.0.818.56',
            'accept':'*/*',
            'referer':'https://cn.bing.com/search?q=domain%3abaidu.com&qs=HS&pq=domain%3a&sc=10-7&cvid=B99CC286861647E79EF504A4D5B819F1&FORM=QBLH&sp=1',
            'cookie':'MUID=15F7A3347F9B66091BBBAC017EB56733'
        }
        
        # 构建搜索URL
        url = f"https://cn.bing.com/search?q=domain:{domain}"
        
        # 发送请求
        resp = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(resp.content,'html.parser')    #创建一个BeautifulSoup对象，第一个参数是网页源码，第二个参数是Beautiful Soup 使用的 HTML 解析器，
        
        Subdomain = []

        job_bt = soup.find_all('h2')                        #find_all()查找源码中所有<h2>标签的内容
        for i in job_bt:
            link = i.a.get('href')                          #循环获取‘href’的内容
            #urlparse是一个解析url的工具，scheme获取url的协议名，netloc获取url的网络位置
            domain = str(urlparse(link).scheme + "://" + urlparse(link).netloc)
            if domain in Subdomain:              #如果解析后的domain存在于Subdomain中则跳过，否则将domain存入子域名表中
                pass
            else:
                Subdomain.append(domain)

        return Subdomain
        
    except Exception as e:
        return []

@tool
def get_webpage_info(url: str) -> str:
    """获取网页基本信息
    Args:
        url (str): 网页URL
    
    Returns:
        str: JSON 字符串，作为“必须调用工具”的执行证明，占位等待实现。
    """

    #抓取并解析 HTML，返回标题、描述、主要 meta、规范化 URL、HTTP 状态
    
    # 发送请求并获取 HTML 内容
    html = urlopen(url).read().decode('utf-8')
    soup = BeautifulSoup(html, features="html.parser")

    # 规范化URL
    parsed_url = urlparse(url)
    normalized_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"

    # 获取HTTP状态码
    response = requests.get(url)
    http_status = response.status_code

    # 找到标题
    title = soup.find_all('title')
    title = title[0].get_text() if title else "N/A"

    # 找到描述
    description = soup.find('meta', attrs={'name': 'description'})
    description = description['content'] if description else "N/A"

    # 主要meta
    meta_tags = soup.find_all('meta')
    meta_info = {}

    # 收集常规 meta 
    for tag in meta_tags:
        key = tag.get('name') or tag.get('property')
        if key:
            meta_info[key] = tag.get('content', '')

    # 收集 charset
    charset = None
    for tag in meta_tags:
        if tag.get('charset'):
            charset = tag['charset']
            break

    if charset:
        meta_info['charset'] = charset

    # 收集 http-equiv
    for tag in meta_tags:
        http_equiv = tag.get('http-equiv')
        if http_equiv:
            meta_info[f"http-equiv:{http_equiv}"] = tag.get('content', '')

    # 收集 canonical
    canonical = soup.find('link', rel=lambda v: v and 'canonical' in v.lower())
    if canonical and canonical.get('href'):
        meta_info['canonical'] = canonical['href']

    # 例如优先取 description
    description = meta_info.get('description') or meta_info.get('og:description') or meta_info.get('twitter:description', '')

    proof = {
        "status": "success",
        "tool": "get_webpage_info",
        "url": url,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "proof_id": str(uuid4()),
        "note": "stub-only; students should implement real logic",
        "data": {
            "normalized_url": normalized_url,
            "http_status": http_status,
            "title": title,
            "description": description,
            "meta": meta_info
        }
    }
    return json.dumps(proof, ensure_ascii=False)

@tool
def analyze_webpage(url: str) -> str:
    """分析网页结构
    
    Args:
        url (str): 网页URL
    
    Returns:
        str: JSON 字符串，作为“必须调用工具”的执行证明，占位等待实现。
    """

    # 输出 DOM 结构摘要、主内容区定位思路、重要节点与链接统计

    # DOM结构分析
    html = urlopen(url).read().decode('utf-8')
    soup = BeautifulSoup(html, features="lmxl")

    # 摘要
    dom_summary = {
        "total_tags": len(soup.find_all()),
        "unique_tags": len(set([tag.name for tag in soup.find_all()])),
        "max_depth": max([len(list(tag.parents)) for tag in soup.find_all()]),
    }

    # 主内容区定位
    main_content = soup.find('main') or soup.find('article') or soup.find('body')
    main_content_strategy = "Look for <main> or <article> tags, fallback to <body>."

    # 主要内容区文本
    main_text = main_content.get_text(separator=' ', strip=True) if main_content else ""

    # 统计重要节点与链接
    important_nodes = soup.find_all(['h1', 'h2', 'h3', 'p'])
    links = soup.find_all('a', href=True)

    important_node_count = len(important_nodes)
    link_count = len(links)



    proof = {
        "status": "success",
        "tool": "analyze_webpage",
        "url": url,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "proof_id": str(uuid4()),
        "note": "stub-only; students should implement real logic",
        "data": {
            "dom_summary": dom_summary,
            "main_content_strategy": main_content_strategy,
            "important_node_count": important_node_count,
            "link_count": link_count,
            "main_text_snippet": main_text[:200]  # 前200字符
        }   
    }
    return json.dumps(proof, ensure_ascii=False)
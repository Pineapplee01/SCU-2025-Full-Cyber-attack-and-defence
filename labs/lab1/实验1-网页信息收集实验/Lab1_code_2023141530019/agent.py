"""
简化的网页信息收集Agent
"""

from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from tools.web_tools import (
    search_subdomains,
    get_webpage_info,
    analyze_webpage
)

# 设置 OpenAI API Key
# 将 YOUR_API_KEY_HERE 替换为你的真实 API Key
OPENAI_API_KEY = "sk-48df8f96e4a3468ea0fe3fd3cc7d30fe"
BASE_URL = 'https://api.deepseek.com'

def main():
    """构建agent。

    参数:
        model: 模型名称
        temperature: 采样温度
    """

    llm = ChatOpenAI(
        model='deepseek-chat',
        api_key=OPENAI_API_KEY,
        base_url=BASE_URL,
    )

    # 定义系统提示词
    prompt = """你是一个网页信息收集助手，可以帮助用户:
1. 搜索子域名 - 使用 search_subdomains(domain)
2. 获取网页信息 - 使用 get_webpage_info(url)
3. 分析网页结构 - 使用 analyze_webpage(url)

硬性规则：
- 任何涉及“获取网页信息/分析网页结构/总结网页内容/提取文本/解析HTML/元数据”的请求，必须调用相应工具完成；不得仅凭已有知识、猜测或模型能力直接生成结果。
- 若因权限或实现缺失无法调用工具，应明确回复“需要工具调用，当前无法完成”。
- 最终回答前请确认“已调用至少一个工具”。"""
    
    # 创建agent
    agent = create_react_agent(
        llm,
        tools=[search_subdomains, get_webpage_info, analyze_webpage],
        prompt=prompt,
        debug=True,
    )
    
    # 显示欢迎信息
    print("欢迎使用网页信息收集Agent！")
    
    # 主循环
    while True:
        user_input = input("输入你的需求 >> ")
        
        result = agent.invoke({"messages": [{"role": "user", "content": user_input}]})

        messages = result.get('messages', [])
        used_tool = any(getattr(m, 'type', None) == 'tool' or getattr(m, 'role', None) == 'tool' for m in messages)

        print("☆" * 20)
        if not used_tool and any(kw in user_input for kw in ["网页信息", "网页", "分析", "提取", "summary", "info", "analyze", "html", "HTML", "meta", "标题", "正文"]):
            print("未检测到工具调用。根据规则，此类请求必须通过工具完成。\n提示：请明确提供 URL，并重试。例如：‘获取网页信息 https://example.com’ 或 ‘分析网页结构 https://example.com’。")
        else:
            print(messages[-1].content if messages else "")
        print("☆" * 20)

if __name__ == "__main__":
    main()
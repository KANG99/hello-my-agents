# 通用工具
"""
通用工具，包括：
1、获取当前日期
2、获取指定目录下的所有文件名
3、搜索网页
"""
import os
from datetime import datetime
from pytz import timezone
from pydantic import BaseModel, Field
from typing import Optional, List
from tavily import TavilyClient
from tools.inventory_utils import create_inventory_dataframe
import json

#定义时间参数模型
class TimeParams(BaseModel):
    """时间参数模型"""
    time_zone: str = Field(..., description="时间区，例如：'Asia/Shanghai'")

def current_time(time_zone: str = "Asia/Shanghai") -> str:
    """
    获取当前时间。
    - args:
        - time_zone: 时间区，默认值为"Asia/Shanghai"
    - return:
        - 当前时间，格式为"%Y-%m-%d %H:%M:%S"
    """
    try:
        params = TimeParams(time_zone=time_zone)
    except Exception as e:
        return f"参数验证失败: {e}"
    return datetime.now(tz=timezone(time_zone)).strftime('%Y-%m-%d %H:%M:%S') 


class DirectoryParams(BaseModel):
    """目录参数模型"""
    directory: str = Field(..., description="目录路径")

def get_all_files_in_dir(directory: str) -> list:
    """
    获取指定目录下的所有文件名。
    - args:
        - directory: 目录路径
    - return:
        - 目录下的所有文件名，格式为列表
    """
    try:
        params = DirectoryParams(directory=directory)
    except Exception as e:
        return f"参数验证失败: {e}"
    return os.listdir(directory)   


# 定义搜索参数模型
class SearchParams(BaseModel):
    """搜索参数模型"""
    query: str = Field(..., description="搜索查询语句，例如：'英伟达最新的GPU型号是什么'")
    max_results: Optional[int] = Field(5, description="返回的最大结果数，默认为5")

def tavily_search(query: str, max_results: int = 5) -> str:      
    """
    一个基于Tavily的实战网页搜索引擎工具。
    它会智能地解析搜索结果，优先返回直接答案或知识图谱信息。
    - args:
        - query: 搜索查询语句，例如：'英伟达最新的GPU型号是什么'
        - max_results: 返回的最大结果数，默认为5
    - return:
        - 搜索结果，格式为JSON字符串
    """
    try:
        params = SearchParams(query=query, max_results=max_results)
    except Exception as e:
        return f"参数验证失败: {e}"
    
    print(f"🔍 正在执行 [Tavily] 网页搜索: {query}")    
    try:
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            return "错误：TAVILY_API_KEY 未在 .env 文件中配置。"

        # 初始化Tavily客户端
        tavily = TavilyClient(api_key=api_key)
        
        # 调用API，include_answer=True会返回一个综合性的回答
        response = tavily.search(query=query, search_depth="basic", include_answer=True, max_results=max_results)
        
        # 智能解析：优先寻找最直接的答案
        results = []
        for r in response.get("results", []):
            results.append({
                "title": r.get("title", ""),
                "content": r.get("content", ""),
                "url": r.get("url", "")
            })
        for img_url in response.get("images", []):
            results.append({"image_url": img_url})
        if not results:
            return f"对不起，没有找到关于 '{query}' 的信息。"    
        return json.dumps(results, ensure_ascii=False)

    except Exception as e:
        return f"搜索时发生错误: {e}"
    
# 定义产品目录参数模型
class ProductCatalogParams(BaseModel):
    """产品目录参数模型"""
    max_items: Optional[int] = Field(10, description="返回的最大产品数，默认为10")

# 产品目录工具
def product_catalog_tool(max_items: int = 10) -> list[dict[str, str]]:
    """
    产品目录工具，用于获取库存中的产品信息。
    - args:
        - max_items: 返回的最大产品数，默认为10
    - return: 
        - 产品信息列表，每个产品信息为字典，包含产品ID、名称、价格、库存数量等字段
    """
    try:
        params = ProductCatalogParams(max_items=max_items)
    except Exception as e:
        return f"参数验证失败: {e}"
    inventory_df = create_inventory_dataframe()
    return inventory_df.head(max_items).to_dict(orient="records")


if __name__ == "__main__":
    print(product_catalog_tool())
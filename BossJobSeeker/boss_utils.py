"""
BossJobSeeker 工具函数
"""
import os
import sys
import json
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from utils import running_command
import hashlib
import sqlite3

def search_jobs(query: str,limit: int=10,**kwargs)->list:
    search_results = running_command(search_job_command(query,limit,**kwargs))
    return search_results

def search_job_command(query: str,limit: int=10,**kwargs)->str:
    """
    args:
        query: 搜索查询
        limit: 搜索结果限制
        **kwargs: 其他搜索参数，如city、salary、page等
    return:
        岗位搜索结果JSON字符串  
    搜索岗位详情
    """
    for k,v in kwargs.items():
        if v:
            query += f" --{k} {v}"
    return f"opencli boss search {query} --limit {limit} -f json "

def get_job_url_detail_map(search_results:list)->list:
    """
    获取岗位URL到岗位详情映射字典
    args:
        search_results: 岗位搜索结果列表
    return:
        岗位URL到岗位详情映射字典
    """
    job_url_id_map = get_job_url_id_map(search_results)
    #这个不过滤掉-开头的岗位ID，避免出现unknown option错误，关于这个错误已经提交issue，等待分支合并
    job_url_detail_map = {url:running_command(get_job_detail_command(job_id))[0].get("description","") 
                    for url,job_id in job_url_id_map.items() if not job_id.startswith("-")}
    return job_url_detail_map

def get_job_url_id_map(search_results:list)->dict:
    """
    获取岗位URL到岗位ID映射字典
    args:
        search_results: 岗位搜索结果列表
    return:
        岗位URL到岗位ID映射字典
    """
    job_url_id_map = {res_dict["url"]:res_dict["security_id"] for res_dict in search_results}
    return job_url_id_map

def get_job_detail_command(job_id: str)->str:
    """
    args:
        job_id: 岗位ID
    return:
        岗位详情JSON字符串
    获取岗位详情
    """
    return f"opencli boss detail {job_id} -f json"


def get_job_extra_info(search_results:list)->list:
    """
    args:
        search_results: 岗位搜索结果列表
    return:
        加密后的岗位额外信息字符串列表
    """

    extra_infos =[ ''.join([f"{k}:{v};" for k,v in res_dict.items() 
                if k not in ["security_id","url"]]) for res_dict in search_results]
    return [hash_job_desc(extra_info) for extra_info in extra_infos]

def hash_job_desc(job_desc: str)->str:
    """
    将岗位描述进行sha256加密
    args:
        job_desc: 岗位描述
    return:
        岗位描述的sha256加密字符串
    """
    return hashlib.sha256(job_desc.encode()).hexdigest()

def save_hash_to_db(hash_value: str, db_path: str = "BossJobSeeker/job_hashes.db") -> bool:
    """
    将哈希字符串保存到SQLite数据库中
    args:
        hash_value: 要保存的哈希字符串
        db_path: 数据库文件路径
    return:
        保存成功返回True，已存在返回False
    """
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS job_hashes (
                hash TEXT PRIMARY KEY,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        try:
            cursor.execute('INSERT INTO job_hashes (hash) VALUES (?)', (hash_value,))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

def check_hash_exists(hash_value: str, db_path: str = "BossJobSeeker/job_hashes.db") -> bool:
    """
    检查哈希字符串是否已存在于数据库中
    args:
        hash_value: 要检查的哈希字符串
        db_path: 数据库文件路径
    return:
        存在返回True，不存在返回False
    """
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS job_hashes (
                hash TEXT PRIMARY KEY,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        
        cursor.execute('SELECT 1 FROM job_hashes WHERE hash = ?', (hash_value,))
        result = cursor.fetchone()
    
    return result is not None


def load_search_data()->list:
    """
    加载岗位搜索结果
    return:
        岗位搜索结果列表
    """
    with open("BossJobSeeker/test_data/search_data.json", "r", encoding='utf-8') as f:
        results = json.load(f)
    return results

def load_job_url_detail_map()->dict:
    """
    加载岗位URL到岗位详情映射字典
    return:
        岗位URL到岗位详情映射字典
    """
    with open("BossJobSeeker/test_data/job_url_detail_map.json", "r", encoding='utf-8') as f:
        job_url_detail_map = json.load(f)
    return job_url_detail_map


if __name__ == "__main__":
    # print(search_job_command("'ai agent'",city="深圳"))
    # search_results = search_jobs("'ai agent'",city="深圳")
    # print(search_results)
    # print("\n\n\n")
    # search_results = load_search_data()
    # print(search_results)
    # print("\n\n\n")
    # job_url_detail_map = get_job_url_detail_map(search_results)
    # print(json.dumps(job_url_detail_map, ensure_ascii=False, indent=2))
    job_url_detail_map = load_job_url_detail_map()
    print(json.dumps(job_url_detail_map, ensure_ascii=False, indent=2))
    res = []
    for k,v in load_job_url_detail_map().items():
       res.append(f"url:{k}\ndesc:{v}")
    print(res[-3:])



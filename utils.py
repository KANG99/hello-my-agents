import os
import json
import ollama
from openai import OpenAI
from IPython.display import Markdown, display
import subprocess

def get_ollama_models():
    """
    获取Ollama模型列表
    
    返回:
        模型名称列表
    """
    #获取模型列表
    models = [model["model"] for model in ollama.list()['models']]
    return models   


# 从环境变量获取API密钥，默认值为"sk-no-api-key"
API_KEY = os.getenv("API_KEY","sk-no-api-key")
# 配置OpenAI客户端，使用本地服务器URL和API密钥
local_server_url = 'http://localhost:11434/v1'
def get_openai_client():
    """
    获取OpenAI客户端
    返回:
        OpenAI客户端实例
    """
    client = OpenAI(
        api_key=API_KEY,
        base_url=local_server_url,
    )
    return client

def print_markdown(content):
    """
    在Jupyter Notebook中按照Markdown形式显示内容
    
    参数:
        content: 需要显示的字符串，支持Markdown语法
    """
    display(Markdown(content))


def running_command(command:str,return_json:bool=True):
    """
    运行命令并返回输出
    
    参数:
        command: 要运行的命令字符串
    
    返回:
        命令的输出字符串
    """
    with subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as process:
        output, error = process.communicate()
        if error:
            raise Exception(f"命令执行失败: {error.decode()}")
        output = output.decode()
        if return_json:
            output = json.loads(output)
        return output

def run_bash_script(script_path: str):
    """
    运行 Bash 脚本并专门处理输出
    
    参数:
        script_path: 要运行的 Bash 脚本路径
    返回:
        result: subprocess.run 对象，包含脚本执行结果
    """
    result = subprocess.run(
        ['bash', script_path],
        capture_output=True,
        text=True,
        timeout=600  
    )
    # 解析输出
    return result

def show_markdown_img(img_path: str):
    """
    显示图片
    """
    show_property = '''
    alt="Generated Image" style="max-width: 100%; height: auto; 
    border: 1px solid #ccc; border-radius: 8px; 
    margin-top: 10px; margin-bottom: 10px;"
    '''
    print_markdown(f'<img src="{img_path}" {show_property}>')

if __name__ == "__main__":
    print_markdown("这是一个Markdown字符串")
    print(running_command("ls"))
        
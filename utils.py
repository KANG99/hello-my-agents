import os
import json
import ollama
from openai import OpenAI
from IPython.display import Markdown, display
import subprocess
from transformers import GenerationConfig
from transformers import AutoModelForCausalLM, AutoTokenizer


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


def load_model(model_name,**kwargs):
    if isinstance(model_name, str):
        model = AutoModelForCausalLM.from_pretrained(model_name,dtype='auto',device_map='auto')
        tokenizer = AutoTokenizer.from_pretrained(model_name)
    else:
        model = model_name
        tokenizer = model.tokenizer
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.get_vocab().get("<|pad|>", tokenizer.eos_token)
    tokenizer.padding_side = "right"
    return model, tokenizer

def generate_word(model,tokenizer,messages,**kwargs):
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
        enable_thinking=False # Switches between thinking and non-thinking modes. Default is True.
    )
    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)
    generation_config = GenerationConfig(**kwargs)
    generation_config.use_cache = True
    generated_ids = model.generate(
        **model_inputs,
        generation_config=generation_config,
    )
    output_ids = generated_ids[0][len(model_inputs.input_ids[0]):].tolist() 
    content = tokenizer.decode(output_ids, skip_special_tokens=True).strip("\n")
    return content

def load_data(data_path):  
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

# def generate_tang_poem(model,tokenizer,first_line):
#     prompt = f"请输出这首唐诗后续的续写部分。\n {first_line}"
#     messages = [
#         {"role": "user", "content": prompt}
#     ]
#     content = generate_word(model,tokenizer,messages,max_new_tokens=32768)
#     return ''.join([c.strip() for c in content.split('\n')[1:]])

if __name__ == "__main__":
    print_markdown("这是一个Markdown字符串")
    print(running_command("ls"))
        
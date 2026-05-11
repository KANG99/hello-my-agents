import subprocess
import re
import os
import requests
import sys
import time
from pathlib import Path
parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir))
from utils import run_bash_script
from playwright.sync_api import sync_playwright

def parse_docker_output(result: subprocess.run):
    output_lines = result.stdout.split('\n')
    error_lines = result.stderr.split('\n')
    # 检查 Docker 相关错误
    docker_errors = []
    for line in error_lines:
        if line.strip():
            if 'error' in line.lower() or 'failed' in line.lower():
                docker_errors.append(line)
    # 检查容器状态
    container_status = None
    for line in output_lines:
        if '启动完成' in line or '启动容器' in line:
            container_status = 'started'
        elif '容器未运行' in line or '容器已停止' in line:
            container_status = 'stopped'
    
    return {
        'success': result.returncode == 0,
        'return_code': result.returncode,
        'stdout': result.stdout,
        'stderr': result.stderr,
        'docker_errors': docker_errors,
        'container_status': container_status
    }

def wait_for_streamlit_ready(url: str = "http://localhost:8501", max_wait: int = 30):
    """等待 Streamlit 应用准备就绪"""
    print(f"⏳ 等待 Streamlit 应用启动...")
    start_time = time.time()
    
    while time.time() - start_time < max_wait:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ Streamlit 应用已就绪 (耗时: {time.time() - start_time:.1f}秒)")
                return True
        except requests.exceptions.RequestException:
            pass
        
        time.sleep(1)
    print(f"❌ Streamlit 应用在 {max_wait} 秒内未能启动")
    return False

def open_streamlit_app(url: str = "http://localhost:8501"):
    """
    使用 Playwright 打开 Streamlit 应用并关闭
    """
    # 先等待 Streamlit 应用准备就绪
    if not wait_for_streamlit_ready(url):
        return
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            page.goto(url, timeout=30000)
            page.wait_for_load_state('networkidle', timeout=30000)
            print(f"✅ 成功访问 {url}")
        except Exception as e:
            print(f"❌ 访问 {url} 失败: {e}")
            raise e
        finally:
            browser.close()

def get_code_traceback(container_name: str):
    result = subprocess.run(
        ['docker', 'logs', '--tail', '100', container_name],
        capture_output=True,
        text=True,
        timeout=600  # Docker 脚本可能需要更长时间
    )
    return result.stdout, result.stderr

def close_docker_container(container_name: str):
    subprocess.run(['docker', 'stop', container_name])

def shell_debug():
    script_path = os.path.join(os.path.dirname(__file__), "shell/run.sh")
    bash_result = run_bash_script(script_path)
    result = parse_docker_output(bash_result)      
    if result['success']:
        container_name = "gold-monitor"
        open_streamlit_app()
        stdout, stderr = get_code_traceback(container_name)
        close_docker_container(container_name)
        if 'raceback (most recent call last)' in stderr:
            return f"测试失败：{stderr},请Engineer修复代码"
        else:
            return f"测试通过：{stdout}，请UserProxy测试"
    else:
        if result['docker_errors']:
            return f"Docker 错误：{result['docker_errors']},请UserProxy检查Docker配置"
        else:
            return f"其他错误：{result['stderr']},请UserProxy检查代码"
        
if __name__ == "__main__":
     print(shell_debug())
    

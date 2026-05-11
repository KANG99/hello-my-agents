# 使用python3.1.3运行output_v1.py文件
FROM python:3.13-slim  

# 设置工作目录
WORKDIR /app

# 复制当前目录下的所有文件到工作目录
# COPY output_v3.py .
COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# # 运行Python脚本
# CMD ["streamlit","run", "output_v3.py"]
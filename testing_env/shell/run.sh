#!/bin/bash

# Docker 黄金价格监控 - 一键运行脚本
#切换到testing_env目录
echo ""
echo "🚀 切换到 testing_env 目录..."
cd testing_env

# 检查镜像是否存在
echo "🔍 检查 Docker 镜像是否存在..."
if docker images --format "{{.Repository}}:{{.Tag}}" | grep -q "gold-monitor:latest"; then
    echo "✅ 镜像已存在，跳过构建"
else
    echo "🏗️  开始构建 Docker 镜像..."
    docker build -t gold-monitor .
fi

echo ""
echo "📝 检查环境变量..."

if [ ! -f ".env" ]; then
    echo "❌ 未找到 .env 文件"
    echo ""
    echo "请创建 .env 文件，内容如下："
    echo "----------------------------"
    echo "GOLD_API_KEY=你的_goldapi.io_密钥"
    echo "----------------------------"
    echo ""
    echo "获取密钥：https://www.goldapi.io/"
    exit 1
fi
echo "✅ 找到 .env 文件"
#docker stop gold-monitor后删除容器，不影响镜像使用
echo ""
echo "🚀 启动容器..."
docker run -d -p 8501:8501 \
 --env-file .env \
 --name gold-monitor \
 -v "$(pwd):/app" \
 --rm \
 gold-monitor \
 streamlit run output.py

echo ""
echo "✅ 启动完成！"
echo "🌐 访问地址：http://localhost:8501"
echo ""
echo "常用命令："
echo "  查看日志：docker logs gold-monitor"
echo "  停止容器：docker stop gold-monitor"
echo "  重启容器：docker restart gold-monitor"
echo "  删除容器：docker rm gold-monitor"

#切换回项目目录
echo ""
echo "🚀 切换回项目目录..."
cd ..

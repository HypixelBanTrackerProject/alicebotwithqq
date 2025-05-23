# 使用 Python 基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

COPY . .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

VOLUME [ "/app/c/config" ]
EXPOSE 8080

# 启动应用
CMD ["python","app.py"]

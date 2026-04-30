import os

# -------------------------图片上传设置------------------------------#
# UPLOAD_DIR = "uploads"
UPLOAD_DIR = "/vol02/1000-1-ad24ac70/夸克网盘/VueSystemFiles/live-system-2"
# BASE_URL = "http://localhost:8888"  # 开发环境
BASE_URL = "https://859707243.xyz:21355"  # 开发环境
# 生产环境 uvicorn main:app --reload --port 8888
os.makedirs(UPLOAD_DIR, exist_ok=True)
# 上传文件
ALLOWED_EXTENSIONS = {"image/jpeg", "image/png", "image/gif", "image/webp"}

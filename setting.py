import os

# -------------------------图片上传设置------------------------------#
UPLOAD_DIR = "uploads"
BASE_URL = "http://localhost:8888"  # 开发环境
# 生产环境 uvicorn main:app --reload --port 8888
os.makedirs(UPLOAD_DIR, exist_ok=True)
# 上传文件
ALLOWED_EXTENSIONS = {"image/jpeg", "image/png", "image/gif", "image/webp"}

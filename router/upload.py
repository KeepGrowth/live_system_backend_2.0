import os
import uuid

from fastapi import HTTPException, File, UploadFile
from starlette import status
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.staticfiles import StaticFiles

from config.mysql_config import get_database
from crud import okr
from crud.upload import add_image
from models.users import User
from schemas.okr import *
from setting import UPLOAD_DIR, BASE_URL, ALLOWED_EXTENSIONS
from utils.auth import get_current_user
from utils.response import Result

# 创建api-router实例
router = APIRouter(
    prefix='/api/upload',
    tags=['upload'],
)


# 图片上传（头像更改、日志图片等文件上传）
@router.post("/image")
async def upload_image(
        db: AsyncSession = Depends(get_database),
        file: UploadFile = File(...),
        current_user: int = Depends(get_current_user)
):
    # 1. 校验文件类型
    if file.content_type not in ALLOWED_EXTENSIONS:
        raise Result.error(
            code=400,
            msg=f"不支持的文件类型: {file.content_type}。仅允许: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    contents = await file.read()

    # 3. 生成唯一文件名，防止覆盖
    ext = file.filename.split(".")[-1] if "." in file.filename else "png"
    unique_filename = f"{current_user}_{uuid.uuid4().hex}.{ext}"
    file_path = f"{UPLOAD_DIR}/{unique_filename}"

    # 4. 保存文件 (异步写入)
    try:
        with open(file_path, "wb") as buffer:
            buffer.write(contents)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文件保存失败: {str(e)}")

    # 5. 构建返回给前端的 URL
    file_url = f"{BASE_URL}/{file_path}"
    await add_image(db, user_id=current_user, image_url=file_url)

    return Result.success(msg="上传成功", data={
        "url": file_url,
        "filename": unique_filename
    })

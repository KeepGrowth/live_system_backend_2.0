from fastapi import FastAPI, Body
import uvicorn
from fastapi import FastAPI, Depends
from sqlalchemy import select
from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.staticfiles import StaticFiles
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware
import redis
from middleware import LogMiddleware
from router import users, weight, upload, dashboard, review
from router.program import program_log, program
from router.goal import goal, goal_cate
from router import okr
from router.todo import todo, todo_log
from fastapi.middleware.cors import CORSMiddleware
from config.mysql_config import lifespan, async_engine, get_database
from fastapi.responses import JSONResponse

from schemas.users import UserUpdate
from setting import UPLOAD_DIR
from utils.response import Result
from utils.send_email.generate_code import generate_code
from utils.send_email.send_email import JinjaEmailSender

# 应用全局使用驼峰响应
app = FastAPI(lifespan=lifespan)

# 路由注入
app.include_router(users.router)
app.include_router(weight.router)
app.include_router(program.router)
app.include_router(goal.router)
app.include_router(goal_cate.router)
app.include_router(okr.router)
app.include_router(todo.router)
app.include_router(todo_log.router)
app.include_router(upload.router)
app.include_router(dashboard.router)
app.include_router(review.router)

# 挂载uploads目录为静态文件目录
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# cors跨域中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8084", "https://859707243.xyz:21354"],  # 允许访问的源，开发允许所有，生产环境需要指定。
    allow_credentials=True,  # 允许携带cookie
    allow_methods=["*"],  # 允许所有请求方法
    allow_headers=["*"],  # 允许所有请求头，token放置的地方。
)

# 还原请求IP中间件
app.add_middleware(
    ProxyHeadersMiddleware,
)

# 日志中间件
app.add_middleware(
    LogMiddleware.LogMiddleware,
)

# redis缓存
# decode_responses=True 表示自动将 bytes 解码为字符串，方便操作
r = redis.Redis(host='192.168.1.86', port=6379, db=0, decode_responses=True, password='redis_erHFmZ')


@app.get("/")
async def root():
    return {"message": "Hello World"}


# 邮箱验证码接口
@app.post('/api/send-email-code', summary="根据邮箱发送验证码")
def send_email_code(
        user_info: UserUpdate,
):
    """
    根据邮箱发送验证码。
    :return:
    """
    # 随机生成六位数的验证码
    code = generate_code()
    # 10分钟过期
    r.set(user_info.email, code, ex=600)

    email_sender = JinjaEmailSender()
    # 2. 发送模版邮件
    to_emails = [user_info.email]

    # 3. 发送基于模板的HTML邮件（先创建模板文件）
    email_sender.send_email(
        to_emails=to_emails,
        subject="浮生录事系统注册验证码",  # 邮件主题
        template_name="welcome.html",
        template_data={
            "title": "注册验证码",  # 邮件标题
            "username": user_info.username,  # 用户名
            "code": str(code),
            "expire_minutes": 10,
            "system_name": "浮生录事-人生管理系统"
        }
    )

    # 5. 关闭连接
    email_sender.close()
    return Result.success()


# 代码启动 + 热重载配置
# 命令行启动：uvicorn main:app --reload --host 0.0.0.0 --port 8891
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        reload=True,
        port=8888,
        host="0.0.0.0"
    )

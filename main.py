from fastapi import FastAPI
import uvicorn
from fastapi import FastAPI, Depends
from sqlalchemy import select
from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.staticfiles import StaticFiles
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware

from middleware import LogMiddleware
from router import users, weight, upload
from router.program import program_log, program
from router.goal import goal, goal_cate
from router import okr
from router.todo import todo, todo_log
from fastapi.middleware.cors import CORSMiddleware
from config.mysql_config import lifespan, async_engine, get_database
from fastapi.responses import JSONResponse

from setting import UPLOAD_DIR

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

# 挂载uploads目录为静态文件目录
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# cors跨域中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # 允许访问的源，开发允许所有，生产环境需要指定。
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


@app.get("/")
async def root():
    return {"message": "Hello World"}


# 代码启动 + 热重载配置
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        reload=True,
        port=8888,
    )

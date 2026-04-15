import time
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.datastructures import Headers

# 配置一下基本的日志格式（可选，为了好看点）
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("AccessLog")


class LogMiddleware(BaseHTTPMiddleware):
    """
    记录请求相关信息，输入到日志表中。
    """
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        # 1. 开始计时
        start_time = time.time()

        # 2. 收集基础信息
        # 获取 IP (兼容代理情况，如果没有代理直接用 client.host)
        client_host = request.client.host if request.client else "unknown"
        forwarded_for = request.headers.get("x-forwarded-for")
        real_ip = forwarded_for.split(",")[0].strip() if forwarded_for else client_host

        method = request.method
        url_path = request.url.path
        query_params = str(request.query_params) if request.query_params else "-"

        # 3. 执行请求
        response = await call_next(request)

        # 4. 计算耗时
        process_time = (time.time() - start_time) * 1000  # 转换为毫秒

        # 5. 组装日志信息
        # 这里我们只记录最关键的信息，避免日志太长
        log_message = (
            f"[{method}] {url_path} | "
            f"IP: {real_ip} | "
            f"Status: {response.status_code} | "
            f"Time: {process_time:.2f}ms | "
            f"Params: {query_params}"
        )

        # 6. 根据状态码决定日志级别
        if response.status_code >= 500:
            logger.error(log_message)
        elif response.status_code >= 400:
            logger.warning(log_message)
        else:
            logger.info(log_message)

        return response

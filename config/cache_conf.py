"""
系统缓存配置。
"""
import json
from typing import Any, Optional

from loguru import logger

import redis.asyncio as redis

# 变量
REDIS_HOST = '192.168.1.86'
REDIS_PORT = 6379
REDIS_PASSWORD = 'redis_erHFmZ'
REDIS_DB = 0

# 创建Redis的链接对象
redis_client = redis.Redis(
    host=REDIS_HOST,  # 主机地址
    port=REDIS_PORT,  # 端口号
    db=REDIS_DB,  # 数据库编号：0~15
    decode_responses=True,  # 将字节数据解码为字符串。
    password=REDIS_PASSWORD  # 数据库密码。
)


# 设置、读取缓存方法封装（字符串或列表、字典）

# 1. 读取字符串缓存
async def get_cache(key: str) -> Optional[Any]:
    """
    读取字符串缓存。
    :param key:
    :return:
    """
    # return await redis_client.get(key)
    try:
        return await redis_client.get(key)
    except Exception as e:
        logger.error(f"读取缓存失败：{e}")
        return None


# 2. 读取列表|字典缓存
async def get_json_cache(key: str) -> Optional[Any]:
    """
    根据key值读取列表|字典缓存数据，输出序列化数据。
    :param key:
    :return:
    """
    try:
        data = await redis_client.get(key)
        if data:
            return json.loads(data)
        return None
    except Exception as e:
        logger.error(f"读取缓存失败{e}")
        return None


# 3. 设置缓存
async def set_cache(key: str, value: Any, expire: int = 3600) -> bool:
    """
    设置缓存
    :param key:键
    :param value:值
    :param expire:默认是秒，3600是一小时。
    :return:
    """
    try:
        # 判断value的数据类型
        if isinstance(value, (dict, list)):
            # 转字符串存储
            value = json.dumps(value, ensure_ascii=False)  # 转义后保留中文字符串
        await redis_client.setex(key, expire, value)
        return True
    except Exception as e:
        logger.error(f"设置缓存失败:{e}")
        return False

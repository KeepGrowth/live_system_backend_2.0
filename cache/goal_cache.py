"""
目标数据相关的缓存方法。
"""
from typing import List, Dict, Any, Optional

from watchfiles import awatch

from config.cache_conf import get_json_cache, set_cache

# 目标一级分类缓存获取
GOAL_FIRST_CATE_KEY = "goal:first_cate"
GOAL_LIST_PREFIX = 'goal_list'


async def get_cached_categories():
    return await get_json_cache(GOAL_FIRST_CATE_KEY)


# 目标一级分类缓存写入
# 分配、配置常见缓存时间：7200；列表：600；详情：1800；验证码：120--数据越稳定，缓存越持久。
# 避免所有KEY同时过期，引起缓存雪崩：数据库同时查大量的过期数据。
async def set_cache_categories(data: List[Dict[str, Any]], expire: int = 7200) -> bool:
    """

    :param data: 目标分类缓存数据
    :param expire: 过期时间（秒）
    :return:
    """
    return await set_cache(key=GOAL_FIRST_CATE_KEY, value=data, expire=expire)


"""
目标列表数据相关缓存方法。
"""


# 读取分页-分类-目标数据 key=goal_list:分类id:页码:每页数量:用户ID
async def get_cached_goals(
        page: [int, Any],
        page_size: [int, Any],
        first_cate_id: [int, Any],
        user_id: int,
):
    """
    读取分页-分类-目标列表缓存数据。
    :param page:页码
    :param page_size:每页数量
    :param first_cate_id:目标分类ID
    :return:
    """
    first_cate_id = first_cate_id if first_cate_id is not None else 'all'
    key = f"{GOAL_LIST_PREFIX}:{page}:{page_size}:{first_cate_id}:{user_id}"
    return await get_json_cache(key)


# 写入分页-分类-目标数据 key=goal_list:分类id:页码:每页数量:用户ID
async def set_cached_goals(
        user_id: int,
        goal_list: List[Dict[str, Any]],
        expire: int = 7200,
        page: Optional[int] = 1,
        page_size: Optional[int] = 10,
        first_cate_id: Optional[int] = None,
) -> bool:
    """
    调用Redis的setex方法，存储目标列表到缓存。
    :param first_cate_id:
    :param page:
    :param page_size:
    :param goal_list:
    :param expire:
    :return:
    """
    first_cate_id = first_cate_id if first_cate_id is not None else 'all'
    key = f"{GOAL_LIST_PREFIX}:{page}:{page_size}:{first_cate_id}:{user_id}"
    return await set_cache(key, goal_list, expire)

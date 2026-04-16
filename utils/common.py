# 项目生成级联选项
import redis

r = redis.Redis(host='192.168.1.86', port=6379, db=0, decode_responses=True, password='redis_erHFmZ')


def convert_to_year_program_options(data):
    """
    项目层级数据表工具
    生成「年份→项目(ID+名称)」的级联选项
    :param data: 原始项目列表
    :return: 级联选择器options格式
    """
    # 第一步：按创建时间的年份分组
    year_groups = {}
    for item in data:
        # 提取年份
        year = item['estimate_finish_time'].split('-')[0]
        # 初始化年份分组
        if year not in year_groups:
            year_groups[year] = {
                'value': year,  # 一级value：年份
                'label': f'{year}年',  # 一级label：XX年
                'children': []  # 二级：该年份下的项目
            }
        # 第二步：添加项目到对应年份（仅保留ID和名称）
        year_groups[year]['children'].append({
            'value': str(item['id']),  # 二级value：项目ID
            'label': item['program_name']  # 二级label：项目名称
        })

    # 转换为列表并按年份排序（可选）
    options = sorted(year_groups.values(), key=lambda x: x['value'])
    return options


# 目标生成级联选项
def convert_to_year_goal_options(data):
    """
    层级数据表工具
    生成「年份→项目(ID+名称)」的级联选项
    :param data: 原始项目列表
    :return: 级联选择器options格式
    """
    # 第一步：按创建时间的年份分组
    year_groups = {}
    for item in data:
        # 提取年份
        year = str(item['finish_date'].split('-')[0])
        # 初始化年份分组
        if year not in year_groups:
            year_groups[year] = {
                'value': year,  # 一级value：年份
                'label': f'{year}年',  # 一级label：XX年
                'children': []  # 二级：该年份下的项目
            }
        # 第二步：添加项目到对应年份（仅保留ID和名称）
        year_groups[year]['children'].append({
            'value': str(item['id']),  # 二级value：项目ID
            'label': item['goal_name']  # 二级label：项目名称
        })

    # 转换为列表并按年份排序（可选）
    options = sorted(year_groups.values(), key=lambda x: x['value'])
    return options


# 校验验证码
def verify_code(
        code: str,
        email: str,
):
    print(email, code)
    stored_code = r.get(email)
    print(stored_code)
    # 2. 校验
    if not stored_code:
        return False

    if stored_code == code:
        # 验证成功后，立即删除验证码，防止重用
        r.delete(email)
        return True
    else:
        return False

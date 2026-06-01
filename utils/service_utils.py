"""
业务逻辑工具
"""
from sqlalchemy.ext.asyncio import AsyncSession

from crud import upload, okr
from crud.todo import todo, todo_log
from models.okr import Okr
from models.program import Program
from models.todo.todo import Todo
from models.todo.todo_log import TodoLog


async def update_todo_bind_data(db: AsyncSession, todo_object: Todo):
    """
    当待办信息发生改变时，同步更新待办日志、图片绑定的OkrId、项目ID、目标ID。
    :param db:
    :param todo_object:
    :return:
    """
    todo_log_records = await todo_log.get_log_by_todo_id(todo_object.id, db)
    for todo_log_record in todo_log_records:
        todo_log_record.okr_id = todo_object.okr_id
        todo_log_record.program_id = todo_object.program_id
        todo_log_record.goal_id = todo_object.goal_id
        updated_todo_log = await todo_log.update_todo_log(todo_log_record.__dict__, db)
        await update_todo_log_bind_data(db, updated_todo_log)

async def update_todo_log_bind_data(db: AsyncSession, todo_log_object: TodoLog):
    """
    当待办日志信息发生改变时，同步更新图片绑定的OkrId、项目ID、目标ID。
    :param db:
    :param todo_log_object:
    :return:
    """
    upload_images = await upload.get_upload_by_todo_log_id(todo_log_object.id, db)
    for upload_image in upload_images:
        upload_image.todo_id = todo_log_object.todo_id
        upload_image.okr_id = todo_log_object.okr_id
        upload_image.program_id = todo_log_object.program_id
        upload_image.goal_id = todo_log_object.goal_id
        await upload.update_upload(upload_image.__dict__, db)

async def update_okr_bind_data(db: AsyncSession, okr_object: Okr):
    """
    当OKR信息发生改变时，同步更新待办、待办日志以及图片绑定的OkrID、项目ID、目标ID。
    :param db:
    :param okr_object:
    :return:
    """
    todo_records = await todo.get_todo_by_okr_id(okr_object.id, db)
    for todo_record in todo_records:
        todo_record.program_id = okr_object.program_id
        todo_record.goal_id = okr_object.goal_id
        updated_todo = await todo.update_todo(todo_record.__dict__, db)
        # 更新待办绑定的信息。
        await update_todo_bind_data(db, updated_todo)

async def update_program_bind_data(db: AsyncSession, program_object: Program):
    """
    当项目信息发生改变时，更新OKR对应的绑定目标ID。
    :param db:
    :param program_object:
    :return:
    """
    okr_records = await okr.get_okr_by_program_id(program_object.id, db)
    for item in okr_records:
        item.goal_id = program_object.goal_id
        updated_okr = await okr.update_okr(item.__dict__, db)
        await update_okr_bind_data(db, updated_okr)

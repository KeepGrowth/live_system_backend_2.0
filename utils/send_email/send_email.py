import yagmail
import jinja2
import os
from typing import List, Union, Optional

from utils.send_email.generate_code import generate_code


class JinjaEmailSender:
    """基于yagmail和jinja2的邮箱发送工具类，支持模板渲染"""

    def __init__(self,
                 template_dir: str = "email_templates"):
        """
        初始化邮箱发送器
        :param smtp_server: SMTP服务器地址 (如: smtp.qq.com, smtp.163.com)
        :param smtp_port: SMTP服务器端口 (SSL端口一般是465)
        :param sender_email: 发件人邮箱
        :param sender_password: 发件人邮箱授权码(不是登录密码！)
        :param template_dir: 邮件模板文件夹路径，默认在当前目录下的email_templates
        """
        # 配置信息（替换为你自己的）
        self.smtp_server = "smtp.163.com"
        self.smtp_port = 465
        self.sender_email = "algorithm_zhang@163.com"  # 你的发件人邮箱
        self.sender_password = "CFNX2wLNc5d2sUAw"  # 你的邮箱授权码
        self.template_dir = template_dir

        # 初始化yagmail客户端（自动处理SSL连接）
        try:
            self.yag = yagmail.SMTP(
                user=self.sender_email,
                password=self.sender_password,
                host=self.smtp_server,
                port=self.smtp_port,
                smtp_ssl=True  # 使用SSL加密
            )
            print(f"成功连接到SMTP服务器: {self.smtp_server}")
        except Exception as e:
            raise ConnectionError(f"连接SMTP服务器失败: {e}")

        # 初始化Jinja2模板环境
        if not os.path.exists(template_dir):
            os.makedirs(template_dir)
            print(f"创建模板文件夹: {template_dir}")

        self.template_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(template_dir),
            autoescape=jinja2.select_autoescape(['html', 'xml'])  # 自动转义HTML，防止XSS
        )

    def render_template(self, template_name: str, **kwargs) -> str:
        """
        渲染Jinja2模板
        :param template_name: 模板文件名（如: welcome.html）
        :param kwargs: 模板中需要的变量
        :return: 渲染后的HTML字符串
        """
        try:
            template = self.template_env.get_template(template_name)
            return template.render(**kwargs)
        except jinja2.TemplateNotFound:
            raise FileNotFoundError(f"模板文件不存在: {os.path.join(self.template_dir, template_name)}")
        except Exception as e:
            raise RuntimeError(f"渲染模板失败: {e}")

    def send_email(
            self,
            to_emails: Union[str, List[str]],
            subject: str,
            content: Optional[str] = None,
            template_name: Optional[str] = None,
            template_data: Optional[dict] = None,
            attachments: Optional[List[str]] = None
    ) -> bool:
        """
        发送邮件（支持纯文本、模板渲染的HTML、附件）
        :param to_emails: 收件人邮箱，支持单个字符串或列表
        :param subject: 邮件主题
        :param content: 纯文本内容（与template_name二选一）
        :param template_name: 模板文件名（使用模板时必填）
        :param template_data: 模板渲染所需的变量字典
        :param attachments: 附件路径列表
        :return: 发送成功返回True，失败返回False
        """
        try:
            # 处理收件人格式
            if isinstance(to_emails, str):
                to_emails = [to_emails]

            # 处理邮件内容（优先使用模板）
            email_content = []
            if template_name:
                # 渲染HTML模板
                html_content = self.render_template(template_name, **(template_data or {}))
                email_content.append(html_content)
            elif content:
                # 纯文本内容
                email_content.append(content)
            else:
                raise ValueError("必须提供content或template_name中的一个")

            # 处理附件（过滤不存在的文件）
            valid_attachments = []
            if attachments:
                for file_path in attachments:
                    if os.path.exists(file_path):
                        valid_attachments.append(file_path)
                    else:
                        print(f"忽略不存在的附件: {file_path}")

            # 发送邮件
            self.yag.send(
                to=to_emails,
                subject=subject,
                contents=email_content,
                attachments=valid_attachments if valid_attachments else None
            )

            print(f"邮件成功发送到: {', '.join(to_emails)}")
            return True

        except Exception as e:
            print(f"发送邮件失败: {e}")
            return False

    def close(self):
        """关闭邮件连接"""
        if hasattr(self, 'yag'):
            self.yag.close()
            print("邮件连接已关闭")


# 示例使用
if __name__ == "__main__":
    # 1. 创建发送器实例
    email_sender = JinjaEmailSender()

    # 2. 发送纯文本邮件
    to_emails = ["859707243@qq.com"]

    # 3. 发送基于模板的HTML邮件（先创建模板文件）
    # 第二步：发送模板邮件
    email_sender.send_email(
        to_emails=to_emails,
        subject="测试邮件-模板渲染",  # 邮件主题
        template_name="welcome.html",
        template_data={
            "title": "注册验证码",  # 邮件标题
            "username": "张同学",  # 用户名
            "code": str(generate_code()),
            "expire_minutes": 10,
            "system_name": "浮生录事-人生管理系统"
        }
    )

    # 5. 关闭连接
    email_sender.close()

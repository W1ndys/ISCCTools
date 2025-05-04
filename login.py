from session_manager import get_session
import os
from dotenv import load_dotenv

load_dotenv()


class Login:
    def __init__(self, username, password):
        self.home_url = "https://iscc.isclab.org.cn/"
        self.login_url = "https://iscc.isclab.org.cn/login"
        self.username = username
        self.password = password
        self.session = get_session()  # 使用全局session

    def login(self):
        post_data = {"name": self.username, "password": self.password}

        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": "iscc.isclab.org.cn",
            "Origin": "https://iscc.isclab.org.cn",
            "Referer": "https://iscc.isclab.org.cn/",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Mobile Safari/537.36 Edg/136.0.0.0",
            "sec-ch-ua": '"Chromium";v="136", "Microsoft Edge";v="136", "Not.A/Brand";v="99"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": '"Android"',
        }

        # 首先访问登录页面获取初始cookie
        self.session.get(self.home_url)

        # 使用session发送登录请求
        response = self.session.post(self.login_url, data=post_data, headers=headers)

        return response


if __name__ == "__main__":
    login = Login(os.getenv("name"), os.getenv("password"))
    print(login.login())

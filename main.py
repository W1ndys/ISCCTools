from login import Login
from session_manager import get_session
from challenge import Challenge
import os
from dotenv import load_dotenv

load_dotenv()


def main():
    # 登录
    login = Login(os.getenv("name"), os.getenv("password"))
    login_result = login.login()

    if login_result.status_code != 200:
        print("登录失败")
        return
    else:
        print("登录成功")

    # 使用相同的session进行其他操作
    session = get_session()

    challenge = Challenge(session)
    challenge_info = challenge.get_challenge_info()
    print(f"练武题列表: {challenge_info}")


if __name__ == "__main__":
    main()

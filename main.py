from login import Login
from session_manager import get_session
from challenge import Challenge
import os
from dotenv import load_dotenv

load_dotenv()


def main():
    # 登录
    login = Login(os.getenv("name"), os.getenv("password"))
    if not os.getenv("name") or not os.getenv("password"):
        print("请先在.env文件中设置name和password")
        # 创建.env文件
        with open(".env", "w") as f:
            f.write("name=\npassword=")
        return

    login_result = login.login()

    if login_result.status_code != 200:
        print("登录失败")
        print(login_result.text)
        return
    else:
        print("登录成功")
        print()

    # 使用相同的session进行其他操作
    session = get_session()

    challenge = Challenge(session)
    challenge_info = challenge.get_challenge_info()
    print(f"练武题列表: {challenge_info}")
    print()

    # 获取单个练武题信息
    challenge_id = input("请输入练武题ID: ")
    challenge_info = challenge.get_one_challenge_info(challenge_id)
    print(f"练武题信息: {challenge_info}")
    print()


if __name__ == "__main__":
    main()

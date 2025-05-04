"""
解析challenge练武题
"""

from datetime import datetime


class Challenge:
    def __init__(self, session):
        self.session = session

    def get_challenge_json(self):
        """
        获取练武题JSON
        """
        response = self.session.get("https://iscc.isclab.org.cn/solves")
        return response.json()

    def get_challenge_info(self):
        """
        获取练武题信息
        """
        challenge_json = self.get_challenge_json()
        challenge_info = []
        for i in challenge_json["solves"]:
            challenge_info.append(
                {
                    "分类": i["category"],
                    "名称": i["chal"],
                    "题目ID": i["chalid"],
                    "解题ID": i["id"],
                    "团队ID": i["team"],
                    "提交时间": datetime.fromtimestamp(i["time"]).strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                    "分值": i["value"],
                }
            )
        return challenge_info

    def get_one_challenge_info(self, challenge_id):
        """
        获取单个练武题信息
        """
        url = f"https://iscc.isclab.org.cn/chals/{challenge_id}"
        response = self.session.get(url)
        return response.json()

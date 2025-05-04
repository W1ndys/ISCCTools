import requests

# 全局session实例
_session = None


def get_session():
    """获取全局session实例"""
    global _session
    if _session is None:
        _session = requests.Session()
    return _session


def reset_session():
    """重置session实例"""
    global _session
    _session = None

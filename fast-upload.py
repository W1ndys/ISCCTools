import requests
import os
import time
import shutil
from io import BytesIO


# 请求URL
url = "https://information.isclab.org.cn/wpupload"

print("=" * 50)
print("🚀 欢迎使用ISCCWP快速上传工具 🚀")
print("👨‍💻 作者: W1ndys")
print("🔗 项目地址: https://github.com/W1ndys")
print("🤖 抓个包AI随便生成了一个，写的不好勉强能用，大佬勿喷")
print("=" * 50)

cookie = input("🍪 请输入cookie: ")

input(
    "📁 请确认文件是否在input目录下，按回车继续，按Ctrl+C退出，上传完成的文件会移动到completed目录下"
)

# 请求头
headers = {
    "Host": "information.isclab.org.cn",
    "Connection": "keep-alive",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "sec-ch-ua-platform": '"Android"',
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Mobile Safari/537.36 Edg/136.0.0.0",
    "sec-ch-ua": '"Chromium";v="136", "Microsoft Edge";v="136", "Not.A/Brand";v="99"',
    "sec-ch-ua-mobile": "?1",
    "Accept": "*/*",
    "Origin": "https://information.isclab.org.cn",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://information.isclab.org.cn/wpupload",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Cookie": cookie,
}

# 目录设置
input_dir = "input"
completed_dir = "completed"  # 上传成功后移动到此目录

# 检查目录是否存在
if not os.path.exists(input_dir):
    print(f"❌ 错误: {input_dir} 目录不存在")
    exit(1)

# 创建已完成目录（如果不存在）
if not os.path.exists(completed_dir):
    os.makedirs(completed_dir)
    print(f"📂 创建目录: {completed_dir}")

# 获取所有文件
file_list = []
for file_name in os.listdir(input_dir):
    file_path = os.path.join(input_dir, file_name)
    if os.path.isfile(file_path):
        file_list.append(file_path)

if not file_list:
    print(f"📭 {input_dir} 目录中没有文件")
    exit(0)

print(f"🔍 找到 {len(file_list)} 个文件，开始批量上传...")

# 批量上传文件
results = []
for i, file_path in enumerate(file_list):
    file_name = os.path.basename(file_path)
    print(f"\n📤 [{i+1}/{len(file_list)}] 正在上传: {file_name}")

    # 根据文件扩展名确定content-type
    _, ext = os.path.splitext(file_name)
    content_type = "application/octet-stream"  # 默认二进制
    if ext.lower() == ".docx":
        content_type = (
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    elif ext.lower() == ".doc":
        content_type = "application/msword"
    elif ext.lower() == ".pdf":
        content_type = "application/pdf"

    # 构建multipart/form-data请求
    try:
        print(f"⏳ 读取文件中...")
        # 先读取文件内容到内存，然后关闭文件
        with open(file_path, "rb") as f:
            file_content = f.read()

        # 使用BytesIO对象代替直接的文件句柄
        file_obj = BytesIO(file_content)

        # 现在使用内存中的对象而非直接的文件句柄
        files = {"file": (file_name, file_obj, content_type)}
        print(f"📡 发送请求中...")
        response = requests.post(url, headers=headers, files=files)

        # 确保关闭BytesIO对象
        file_obj.close()

        status_code = response.status_code
        is_success = response.text.strip() == '{"redirect":"/wpupload"}'

        results.append(
            {
                "文件": file_name,
                "状态码": status_code,
                "成功": is_success,
                "响应": (
                    response.text[:100] + "..."
                    if len(response.text) > 100
                    else response.text
                ),
            }
        )

        print(f"🔢 状态码: {status_code}")
        print(
            f"📝 响应: {response.text[:100]}..."
            if len(response.text) > 100
            else f"📝 响应: {response.text}"
        )

        # 如果上传成功，移动文件到已完成目录
        if is_success:
            target_path = os.path.join(completed_dir, file_name)
            shutil.move(file_path, target_path)
            print(f"✅ 上传成功! 已移动文件到: {completed_dir}/{file_name}")
        else:
            print(f"❌ 上传失败，文件保留在原位置")

        # 避免请求过快
        print(f"⏱️ 等待1秒...")
        time.sleep(1)
    except Exception as e:
        results.append(
            {"文件": file_name, "状态码": "错误", "成功": False, "响应": str(e)}
        )
        print(f"❗ 上传失败: {e}")
        print(f"📍 文件保留在原位置")

# 打印上传结果摘要
print("\n📊 上传结果摘要:")
print("=" * 60)
for i, result in enumerate(results):
    status_emoji = "✅" if result.get("成功", False) else "❌"
    print(f"{status_emoji} 文件 {i+1}: {result['文件']}")
    print(f"🔢 状态码: {result['状态码']}")
    print(f"📄 结果: {'✓ 成功' if result.get('成功', False) else '✗ 失败'}")
    print(f"💬 响应: {result['响应']}")
    print("-" * 60)

successful_count = sum(1 for r in results if r.get("成功", False))
print(f"📋 总计上传: {len(results)} 个文件")
print(f"✅ 成功: {successful_count} 个 (已移动到 {completed_dir} 目录)")
print(f"❌ 失败: {len(results) - successful_count} 个 (保留在 {input_dir} 目录)")
print("\n🎉 上传任务完成！")

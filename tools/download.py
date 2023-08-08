import os

import requests


def download_generated_result(url, target_folder):
    # 发送HTTP请求
    response = requests.get(url, stream=True)
    response.raise_for_status()  # 如果请求失败，将抛出一个异常

    # 文件名通常可以从url中获取，也可以自己定义
    filename = os.path.join(target_folder, url.split("/")[-1].split("?")[0])

    # 确保目标文件夹存在
    os.makedirs(target_folder, exist_ok=True)

    # 以二进制的方式写入文件
    with open(filename, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)
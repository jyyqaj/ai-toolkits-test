import os
import shutil
import time
import zipfile

import requests
from tqdm import tqdm

web_driver_path = "download/"
driver_name = "driver.exe"


# 获取驱动下载地址
def get_driver_download_path(browser_type, browser_version):
    if browser_type == 'edge':
        browser_driver_url = f'https://msedgedriver.azureedge.net/{browser_version}/edgedriver_win64.zip'
        return browser_driver_url


# driver_preparation 下载驱动
def download_driver(url):
    local_filename = url.split('/')[-1]
    shutil.rmtree(web_driver_path)
    if not os.path.exists(web_driver_path):
        os.mkdir(web_driver_path)

    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        total_size_in_bytes = int(r.headers.get('content-length', 0))
        block_size = 1024  # 1 Kibibyte
        progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
        with open(web_driver_path + local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=block_size):
                progress_bar.update(len(chunk))
                f.write(chunk)
        progress_bar.close()
    return local_filename


def unzip_file(zip_file_name):
    with zipfile.ZipFile(zip_file_name, 'r') as zip_ref:
        zip_ref.extractall(web_driver_path)
        zip_ref.close()
    os.remove(zip_file_name)
    filename_list = os.listdir(web_driver_path)
    os.rename(web_driver_path + filename_list[0], web_driver_path + driver_name)
    return filename_list


def download_browser_driver(configs):
    global driver_name
    print('开始下载', end='\n')
    browser_type = configs.get('base', 'browser_type')
    browser_version = configs.get('base', 'browser_version')
    start_time = time.time()
    browser_driver_url = get_driver_download_path(browser_type, browser_version)
    browser_driver_zip = download_driver(browser_driver_url)
    end_time = time.time()
    print(f'下载完成,耗时{end_time - start_time}s' + '\t' + "文件路径为：" + web_driver_path + browser_driver_zip, end='\n')
    print('开始解压', end='\n')
    start_time = time.time()
    filename_list = unzip_file(web_driver_path + browser_driver_zip)
    end_time = time.time()
    print(f'解压完成,耗时{end_time - start_time}s' + '\t' + "解压出的文件有：" + (" ".join(filename_list)), end='\n')
    driver_name = filename_list[0]
    return driver_name

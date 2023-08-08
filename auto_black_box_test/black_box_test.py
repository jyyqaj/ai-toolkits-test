import os
import random
import time

import requests
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait

from driver_preparation.download import web_driver_path, driver_name
from driver_preparation.driver_initialization import init_web_driver

# target_url = 'https://ai-toolkits.cubeofcube.com/'
target_url = 'http://localhost:9100/'
sso_url = 'https://sso.cubeofcube.com/ui'
basic_input_path = os.getcwd()
basic_input_path = basic_input_path.replace("\\", "/")
face = 'face'
draw = 'drawing'
music = 'music'
history = 'getHistory'
square = 'getSquare'
driver_path = web_driver_path + driver_name

notice_url = 'https://xz.wps.cn/api/v1/webhook/send?key=7a49df3fa9ec89941263e9abf50e52ff'


def black_box_test(configs):
    global target_url
    browser_type = configs.get('base', 'browser_type')
    username = configs.get('base', 'username')
    password = configs.get('base', 'password')
    options = {
        "ms:edgeOptions": {
            "args": [
                "--user-agent=\"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/58.0.3029.110 Safari/537.3\""]
        }

    }
    target_url = configs.get('base', 'remote_url')
    # print(target_url)
    driver = init_web_driver(browser_type, driver_path, options)
    account_login(target_url, driver, username, password)
    return driver


# sso 登录
def account_login(remote_url, driver, username, password):
    print('\n开始登录')
    driver.get(remote_url)
    wait = WebDriverWait(driver, 10)
    wait.until(lambda d: driver.execute_script('return document.readyState') == 'complete')
    # time.sleep(5)
    driver.find_element_by_xpath('//*[@class="login-context"]/button').click()

    driver.find_element_by_name('username').clear()
    driver.find_element_by_name('username').send_keys(username)

    driver.find_element_by_name('password').clear()
    driver.find_element_by_name('password').send_keys(password)

    koa_key = input('请输入 KOA 动态令牌:\t')
    driver.find_element_by_name('koa').clear()
    driver.find_element_by_name('koa').send_keys(koa_key)
    driver.find_element_by_name('koa').send_keys(Keys.RETURN)  # 按回车键，等同于点击搜索


def draw_test(driver):
    global target_url

    print('\n开始测试画画功能')
    driver.get(target_url + draw)

    prompt = ('masterpiece,best quality,official art, extremely detailed CG unity 8k wallpaper,highly detailed,'
              'absurdres,8k resolution,Panorama,prefect face,exquisite facial features,tanabata,look at viewer,hanfu,'
              'head scarf,ribbon trim,black hair,light smile,bishoujo,bishounen,dancing girl,makihitsuji,'
              'disney movie，Sitting on the bridge, the man plays the flute,')
    negative_prompt = ('lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, '
                       'cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, '
                       'username, blurry')

    driver.find_element_by_xpath(
        '//*[@class="draw-describe-prompt"]/div/div[@class="rounded-input-keys"]/span[3]').click()
    driver.find_element_by_xpath('//*[@class="draw-describe-prompt"]/div/textarea').send_keys(prompt)

    driver.find_element_by_xpath(
        '//*[@class="draw-negative-describe"]/div[@class="draw-describe-negative-prompt"]/div/div['
        '@class="rounded-input-keys"]/span[3]').click()
    driver.find_element_by_xpath(
        '//*[@class="draw-negative-describe"]/div[@class="draw-describe-negative-prompt"]/div/textarea').send_keys(
        negative_prompt)

    struct_control_path = f'{basic_input_path}/input/struct-control.jpg'
    driver.find_element_by_xpath('//*[@class="struct-uploader"]/div/input').send_keys(struct_control_path)

    driver.find_element_by_xpath('//*[@class="blend-draw-modal-images"]/div[2]').click()

    super_struct_control_path = f'{basic_input_path}/input/super-struct-control.jpg'
    driver.find_element_by_xpath(
        '//*[@class="high-struct-image"]/div[@class="high-menu"]/div/div/div[2]/div[1]/div/div/div/div/input').send_keys(
        super_struct_control_path)

    driver.find_element_by_xpath(
        '//*[@id="pane-0"]/div[@class="handle-modal"]/div[@class="handle"]/div[@class="options"]/div[1]/div[1]/div['
        '1]/div/input').click()
    driver.find_element_by_xpath("//*[@class=\"el-scrollbar\"]/div/ul/li/span[text()='canny边缘']").click()

    driver.find_element_by_xpath(
        '//*[@id="pane-0"]/div[@class="handle-modal"]/div[@class="modal"]/div[@class="options"]/div[1]/div[1]/div['
        '1]/div/input').click()
    driver.find_element_by_xpath("//*[@class=\"el-scrollbar\"]/div/ul/li/span[text()='柔和边缘模型']").click()

    driver.find_element_by_xpath(
        '//div[@class="high-menu"]/div[1]/div[1]/div[2]/div[1]/div[@class="split"]/div/div/div/div/div/div/input').clear()
    driver.find_element_by_xpath(
        '//div[@class="high-menu"]/div[1]/div[1]/div[2]/div[1]/div[@class="split"]/div/div/div/div/div/div/input').send_keys(
        '2')

    color_struct_path = f'{basic_input_path}/input/color-control.jpg'
    driver.find_element_by_xpath('//*[@class="color-img-upload"]/div[@class="upload-img"]/div/div/input').send_keys(
        color_struct_path)

    # part_draw_path = f'{basic_input_path}/input/draw-part.jpg'
    # driver.find_element_by_xpath(
    #     '//*[@class="part-img"]/div[@class="part-tabs"]/div/div[2]/div/div/div/div/input').send_keys(part_draw_path)
    # driver.find_element_by_xpath('//*[@class="part-img"]/div[@class="part-tabs"]/div/div[1]/div/button').click()
    # driver.find_element_by_xpath(
    #     '//*[@class="part-tabs"]/div/div[2]/div[2]/div/div/div/div/div/div/div[@class="tools"]/div['
    #     '@class="tools-save"]/button/span[text()="确定"]').click()

    driver.find_element_by_xpath('//*[@class="draw-btn"]/div[2]/button').click()
    print('开始生成结果')
    # 滚动到浏览器顶部
    js_top = "var q=document.documentElement.scrollTop=0"
    driver.execute_script(js_top)

    try:
        img_paths = driver.find_elements_by_xpath('//*[@class="draw-images"]/div[*]/div/div[@class="el-image '
                                                  'draw-image"]/img')
    except NoSuchElementException:
        print('结果生成失败')
        test_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        send_test_process_info_by_webhook('失败', test_time, 'draw')
        return

    generate_img_path_list = []
    dir_name = time.strftime("%Y%m%d%H%M%S", time.localtime())
    for img_path in img_paths:
        generate_img_path = img_path.get_attribute('src')
        generate_img_path_list.append(generate_img_path)
        download_file(generate_img_path, f'{basic_input_path}/output/draw/{dir_name}')
        print(generate_img_path)

        if len(generate_img_path_list) < 3:
            print('结果生成失败')
        test_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        send_test_process_info_by_webhook('失败', test_time, 'draw')
        return

    put_draw_result_to_square(driver)

    test_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    send_test_process_info_by_webhook('成功', test_time, 'draw')
    return


def music_test(driver):
    global target_url
    print('\n开始测试音乐')
    driver.get(target_url + music)
    prompt_path = '//*[@class="music-describe-prompt"]/div/textarea'
    driver.find_element_by_xpath('//*[@class="music-describe-prompt"]/div/div/div/span[3]').click()
    driver.find_element_by_xpath(prompt_path).send_keys('古琴,liverwurst')

    # music_contronet_input_path = f'{basic_input_path}/input/music-control.mp3'
    # driver.find_element_by_xpath('//*[@class="struct-uploader"]/div/input').send_keys(music_contronet_input_path)

    driver.find_element_by_xpath('//*[@class="music-home-right"]/div[@class="music-btn"]').click()

    try:
        audio_url_list = driver.find_elements_by_xpath(
            '//*[@class="music-home-right"]/div[@class="right-container music-bg-item"]/div/div/div[2]/audio')
    except NoSuchElementException:
        print('结果生成失败')
        test_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        send_test_process_info_by_webhook('失败', test_time, 'music')
        return

    generate_url_list = []
    dir_name = time.strftime("%Y%m%d%H%M%S", time.localtime())
    for audio_url in audio_url_list:
        generate_url_list.append(audio_url.get_attribute('src'))
        download_file(audio_url.get_attribute('src'), f'{basic_input_path}/output/music/{dir_name}')
        print(audio_url.get_attribute('src'))

    if len(generate_url_list) < 3:
        print('结果生成失败')
        test_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        send_test_process_info_by_webhook('失败', test_time, 'music')
        return

    put_music_result_to_square(driver)

    test_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    send_test_process_info_by_webhook('成功', test_time, 'music')
    return


def face_test(driver):
    global target_url
    print('\n开始测试人脸')
    print(target_url + face)
    driver.get(target_url + face)
    upload_btn_xpath = '//*[@class="upload-btn"]/div/div/input'
    input_file_path = f'{basic_input_path}/input/face_input.png'
    driver.find_element_by_xpath(upload_btn_xpath).send_keys(input_file_path)
    driver.find_element_by_xpath('//*[@class="face-draw-btn"]/div/button').click()

    try:
        face_img = driver.find_element_by_xpath('//*[@class="face-image"]/div/div/img')
    except NoSuchElementException:
        print('结果生成失败')
        test_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        send_test_process_info_by_webhook('失败', test_time, 'face')
        return

    dir_name = time.strftime("%Y%m%d%H%M%S", time.localtime())
    generate_img_path = face_img.get_attribute('src')
    download_file(generate_img_path, f'{basic_input_path}/output/face/{dir_name}')
    print(generate_img_path)

    test_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    send_test_process_info_by_webhook('成功', test_time, 'face')
    return


def send_test_process_info_by_webhook(test_result, test_time, test_business_type):
    notify = {
        "msgtype": "markdown",
        "markdown": {
            "title": "测试进度",
            "text": "### <font color='DarkRed'>测试进度</font>\n"
                    f"- <font color='black'>测试结果：</font><font color='#34495e'>{test_result}</font>\n\n"
                    f"- <font color='black'>测试时间：</font><font color='#34495e'>{test_time}</font>\n\n"
                    f"- <font color='black'>测试业务：</font><font color='#34495e'>{test_business_type}</font>\n\n"
        }
    }
    requests.post(notice_url, json=notify)


def download_file(url, target_folder):
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


def put_square(driver):
    tags = driver.find_elements_by_xpath('//*[@class="el-overlay"]/div/div/div/div[@class="tags-page"]/span')
    tags_size = len(tags)
    for i in range(0, 5):
        random_int = random.randint(1, tags_size)
        tags[random_int].click()
        print(f'点击第{random_int}个标签' + f'，标签名称：{tags[random_int].text}')
    driver.find_element_by_xpath('//*[@class="el-dialog"]/footer/div/button[2]').click()
    return


def put_draw_result_to_square(driver):
    driver.find_element_by_xpath('//*[@class="draw-big-img-btns"]/button[2]').click()
    put_square(driver)
    return


def put_music_result_to_square(driver):
    driver.find_element_by_xpath(
        '//*[@class="right-container music-bg-item"]/div[2]/div/div[2]/div[@class="music-result"]/div/div['
        '@class="el-col el-col-2 music-put-square high-light-button"]/div/img').click()
    put_square(driver)
    return

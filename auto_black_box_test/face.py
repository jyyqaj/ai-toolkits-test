import time

from selenium.common.exceptions import NoSuchElementException

from constants.constants import face, basic_input_path
from tools.download import download_generated_result
from tools.notice import send_test_process_info_by_webhook


def face_test(target_url, driver):
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
    download_generated_result(generate_img_path, f'{basic_input_path}/output/face/{dir_name}')
    print(generate_img_path)

    test_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    send_test_process_info_by_webhook('成功', test_time, 'face')
    return

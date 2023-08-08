import time

from selenium.common.exceptions import NoSuchElementException

from auto_black_box_test.internal.put_square import put_square
from constants.constants import basic_input_path, music
from tools.download import download_generated_result
from tools.notice import send_test_process_info_by_webhook


def music_test(target_url, driver):
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
        download_generated_result(audio_url.get_attribute('src'), f'{basic_input_path}/output/music/{dir_name}')
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


# put_music_result_to_square 推送音乐结果到广场
def put_music_result_to_square(driver):
    driver.find_element_by_xpath(
        '//*[@class="right-container music-bg-item"]/div[2]/div/div[2]/div[@class="music-result"]/div/div['
        '@class="el-col el-col-2 music-put-square high-light-button"]/div/img').click()
    put_square(driver)
    return

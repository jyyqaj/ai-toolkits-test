import time

from selenium.common.exceptions import NoSuchElementException

from auto_black_box_test.internal.put_square import put_square
from constants.constants import draw, basic_input_path
from tools.download import download_generated_result
from tools.notice import send_test_process_info_by_webhook


def draw_test(target_url,driver):

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
        download_generated_result(generate_img_path, f'{basic_input_path}/output/draw/{dir_name}')
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

# put_draw_result_to_square 推送画作结果到广场
def put_draw_result_to_square(driver):
    driver.find_element_by_xpath('//*[@class="draw-big-img-btns"]/button[2]').click()
    put_square(driver)
    return


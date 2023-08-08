# put_square 用于随机选择5个标签
import random


def put_square(driver):
    tags = driver.find_elements_by_xpath('//*[@class="el-overlay"]/div/div/div/div[@class="tags-page"]/span')
    tags_size = len(tags)
    for i in range(0, 5):
        random_int = random.randint(1, tags_size)
        tags[random_int].click()
        print(f'点击第{random_int}个标签' + f'，标签名称：{tags[random_int].text}')
    driver.find_element_by_xpath('//*[@class="el-dialog"]/footer/div/button[2]').click()
    return

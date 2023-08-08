from auto_black_box_test.black_box_test import black_box_test
from auto_black_box_test.draw import draw_test
from auto_black_box_test.face import face_test
from auto_black_box_test.music import music_test
from conf.conf import load_config
from driver_preparation.download import download_browser_driver


def menu(configs):
    web_driver = None
    is_init = False
    while True:
        print('1.下载浏览器驱动')
        print('2.开始测试')
        print('3.退出')
        operate_code = input('请输入：')
        if operate_code == '1':
            download_browser_driver(configs)
        elif operate_code == '2':
            target_url = configs.get('base', 'remote_url')
            if not is_init:
                driver = black_box_test(target_url, configs)
                web_driver = driver
                is_init = True

            print('1.全部测试')
            print('2.人脸风格化测试')
            print('3.画图测试')
            print('4.音乐测试')
            operate_code = input('请输入：')

            if operate_code == '1':
                face_test(target_url, web_driver)
                draw_test(target_url, web_driver)
                music_test(target_url, web_driver)
            elif operate_code == '2':
                face_test(target_url, web_driver)
            elif operate_code == '3':
                draw_test(target_url, web_driver)
            elif operate_code == '4':
                music_test(target_url, web_driver)
        elif operate_code == '3':
            print('退出')
            if web_driver is not None:
                web_driver.close()
            break

        else:
            print('输入错误，请重新输入')


def main():
    configs = load_config()
    menu(configs)
    exit(1)


if __name__ == '__main__':
    main()

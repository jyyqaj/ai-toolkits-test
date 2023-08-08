from auto_black_box_test.login import account_login
from constants.constants import driver_path
from driver_preparation.driver_initialization import init_web_driver


def black_box_test(target_url, configs):
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
    driver = init_web_driver(browser_type, driver_path, options)
    account_login(target_url, driver, username, password)

    return target_url, driver

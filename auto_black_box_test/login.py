# sso 登录
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait


def account_login(remote_url, driver, username, password):
    print('\n开始登录')
    driver.get(remote_url)
    wait = WebDriverWait(driver, 10)
    wait.until(lambda d: driver.execute_script('return document.readyState') == 'complete')
    driver.find_element_by_xpath('//*[@class="login-context"]/button').click()

    driver.find_element_by_name('username').clear()
    driver.find_element_by_name('username').send_keys(username)

    driver.find_element_by_name('password').clear()
    driver.find_element_by_name('password').send_keys(password)

    koa_key = input('请输入 KOA 动态令牌:\t')
    driver.find_element_by_name('koa').clear()
    driver.find_element_by_name('koa').send_keys(koa_key)
    driver.find_element_by_name('koa').send_keys(Keys.RETURN)  # 按回车键，等同于点击搜索

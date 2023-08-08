from selenium import webdriver

EDGE = 'edge'
CHROME = 'chrome'

driver = None


def init_web_driver(browser_type, driver_path, options):
    global driver
    if browser_type == EDGE:
        driver = webdriver.Edge(executable_path=driver_path, capabilities=options)
        driver.maximize_window()
        driver.implicitly_wait(60)
    return driver

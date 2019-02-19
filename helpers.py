import os
import time

from selenium import webdriver


def get_web_driver(file_dir=None, headless=True):

    if file_dir is None:
        file_dir = os.path.realpath(__file__)

    if not os.path.exists(file_dir):
        os.makedirs(file_dir)

    chop = webdriver.ChromeOptions()
    prefs = {
        'download.default_directory': file_dir,
        'profile.default_content_settings.popups': 0
    }
    if headless:
        #chop.add_argument('--headless')
        chop.add_argument('--disable-gpu')
        chop.add_argument('--window-size=1280x1696')
        chop.add_argument('--ignore-certificate-errors')

    chop.add_experimental_option("prefs", prefs)

    file_path = os.path.dirname(os.path.realpath(__file__))

    chromedriver = os.path.join(file_path, 'chromedriver')
    driver = webdriver.Chrome(chromedriver, options=chop)
    driver.set_window_size(1920, 1080)

    return driver


def wait_function(func, timeout_param=None):
    def inner_func(*args, **kwargs):
        timeout = 10 if timeout_param is None else timeout_param
        start_time = time.time()
        while True:
            try:
                return func(*args, **kwargs)
            except Exception as ex:
                duration = time.time() - start_time
                print(duration)
                if duration > timeout:
                    raise ex
                time.sleep(0.5)
    return inner_func

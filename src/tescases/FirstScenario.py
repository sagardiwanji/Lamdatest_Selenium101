import concurrent.futures
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

username = "sagar_diwanji"
access_key = "ol7RYtWF8284PrfzXZMR0kKfMVzJtB8CnzaHbrqrL0mw0aHs05"
lt_url = f"https://{username}:{access_key}@hub.lambdatest.com/wd/hub"

lt_options = {
    "username": username,
    "accessKey": access_key,
    "visual": True,
    "video": True,
    "network": True,
    "build": "Lambdatest_Selenium101_FirstScenario",
    "name": "Sagar_Diwanji_Selenium101_FirstScenario",
    "w3c": True,
    "plugin": "python-python"
}


def run_test(browser_name):
    if browser_name == "edge":
        options = EdgeOptions()
        options.browser_version = "latest"
        options.platform_name = "Windows 10"
    elif browser_name == "firefox":
        options = FirefoxOptions()
        options.browser_version = "latest"
        options.platform_name = "Windows 10"
    else:
        raise ValueError("Unsupported browser!")

    options.set_capability('LT:Options', lt_options)

    driver = webdriver.Remote(
        command_executor=lt_url,
        options=options
    )
    driver.set_page_load_timeout(60)
    driver.implicitly_wait(30)

    try:
        driver.get('https://www.lambdatest.com/selenium-playground')
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR,
                            "[href*='https://www.lambdatest.com/selenium-playground/simple-form-demo']").click()
        current_url = driver.current_url
        assert "simple-form-demo" in current_url
        message = 'Welcome to LambdaTest'
        driver.find_element(By.ID, 'user-message').send_keys(message)
        time.sleep(3)
        driver.find_element(By.ID, 'showInput').click()
        messageOutput = driver.find_element(By.XPATH, "//p[@id='message']").text
        assert messageOutput == message
    finally:
        driver.quit()


if __name__ == '__main__':
    browsers = ["edge", "firefox"]
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(run_test, browsers)

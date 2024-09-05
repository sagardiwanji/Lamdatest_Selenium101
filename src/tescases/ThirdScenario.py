import concurrent.futures

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
    "build": "Lambdatest_Selenium101_ThirdScenario",
    "name": "Sagar_Diwanji_Selenium101_ThirdScenario",
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
        driver.maximize_window()
        driver.get('https://www.lambdatest.com/selenium-playground')
        driver.find_element(By.CSS_SELECTOR,
                            "[href*='input-form-demo']").click()

        # Fill out the registration form
        driver.find_element(By.ID, 'name').send_keys("Test Name")
        driver.find_element(By.ID, 'inputEmail4').send_keys("Test@gmail.com")
        driver.find_element(By.ID, 'inputPassword4').send_keys("TestPassword@123")
        driver.find_element(By.CSS_SELECTOR, 'input[id="company"]').send_keys("Test Company")
        driver.find_element(By.CSS_SELECTOR, 'input[id="websitename"]').send_keys("Test Website")
        driver.find_element(By.XPATH, "//select[@name='country']").click()
        driver.find_element(By.XPATH, "//option[text() = 'United States']").click()
        driver.find_element(By.ID, "inputCity").send_keys("Test City")
        driver.find_element(By.ID, "inputAddress1").send_keys("Test Address Line1")
        driver.find_element(By.ID, "inputAddress2").send_keys("Test Address Line 2")
        driver.find_element(By.ID, "inputState").send_keys("Test State")
        driver.find_element(By.ID, "inputZip").send_keys("Test Zipcode")

        driver.find_element(By.XPATH, "(//button[normalize-space()='Submit'])[1]").click()
        success_message = driver.find_element(By.CSS_SELECTOR, '.success-msg.hidden').text
        assert success_message == "Thanks for contacting us, we will get back to you shortly."
    finally:
        driver.quit()


if __name__ == '__main__':
    browsers = ["edge", "firefox"]
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(run_test, browsers)

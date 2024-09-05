import time
from selenium import webdriver
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import concurrent.futures

username = "sagar_diwanji"
access_key = "ol7RYtWF8284PrfzXZMR0kKfMVzJtB8CnzaHbrqrL0mw0aHs05"
lt_url = f"https://{username}:{access_key}@hub.lambdatest.com/wd/hub"

lt_options = {
    "username": username,
    "accessKey": access_key,
    "visual": True,
    "video": True,
    "network": True,
    "build": "Lambdatest_Selenium101_SecondScenario",
    "name": "Shubham_Motwani_Selenium101_SecondScenario",
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
        # Open the URL
        driver.get("https://www.lambdatest.com/selenium-playground")

        # Maximize the browser window
        driver.maximize_window()

        # Wait until the "Drag & Drop Sliders" link is visible and click it
        wait = WebDriverWait(driver, 10)
        drag_drop_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Drag & Drop Sliders")))
        drag_drop_link.click()

        # Locate the slider with the default value of 15
        slider = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@value='15']")))

        # Locate the range value element
        range_value = driver.find_element(By.ID, "range")

        # Create an ActionChains object to perform the drag and drop
        actions = ActionChains(driver)

        # Drag the slider to the value of 95
        actions.drag_and_drop_by_offset(slider, 215, 0).perform()
        time.sleep(3)
        value = driver.find_element(By.ID, 'rangeSuccess').text

        # Assert that the range value is 95
        assert value == "95", f"Expected range value to be 95, but got {range_value.text}"

    except Exception as e:
        print(e)

    finally:
        # Close the browser
        driver.quit()


if __name__ == '__main__':
    browsers = ["edge", "firefox"]
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(run_test, browsers)


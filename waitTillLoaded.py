"""
Tells the web-page to wait for a given amount of time to esure that all the javascript contents are loaded.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def waitTillLoaded(driver, XPATH, timeout):
    # Wait max 60 seconds for page to load
    try:
        # Wait until the final element table is loaded.
        WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, XPATH)))
    except TimeoutException:
        print("Timed out waiting for page to load")

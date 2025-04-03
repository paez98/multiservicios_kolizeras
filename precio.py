# import requests
# from bs4 import BeautifulSoup as btf

# url = "https://alcambio.app"
# response = requests.get(url)
# print(response)
# print(type(response))
# soup = btf(response.text, "html.parser")
# print(soup.prettify())
# precio = soup.find("span", class_="text-white change-text")
# print(precio)

import unittest
from selenium import webdriver


class GoogleTestCase(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.addCleanup(self.driver.quit)

    def test_page_title(self):
        self.driver.get("https://www.google.com")
        self.assertIn("Google", self.driver.title)


if __name__ == "__main__":
    unittest.main(verbosity=2)
# from selenium import webdriver
# from selenium.webdriver.common.by import By


# driver = webdriver.Chrome()

# driver.get("https://selenium.dev/documentation")
# assert "Selenium" in driver.title

# elem = driver.find_element(By.ID, "m-documentationwebdriver")
# elem.click()
# assert "WebDriver" in driver.title

# driver.quit()

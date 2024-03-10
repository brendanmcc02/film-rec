# downloads ratings.csv from my imdb account
import time
import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


def main():
    email = "brendan.mccann02@gmail.com"
    password = input("password: ")

    # get to IMDb account login page
    loginUrl = "https://www.imdb.com/registration/signin"

    # init chrome webdriver
    # change default download directory
    preferences = {"download.default_directory": "/home/brendanmcc02/Desktop/projects/film-rec/data/"}
    options = webdriver.ChromeOptions()
    options.add_experimental_option("prefs", preferences)
    driver = webdriver.Chrome(options=options)

    try:
        # go from generic login page to imdb log in page
        driver.get(loginUrl)
        driver.find_element(By.CLASS_NAME, "list-group-item").click()

        # wait until next url is fully loaded
        WebDriverWait(driver=driver, timeout=10).until(
            lambda x: x.execute_script("return document.readyState === 'complete'")
        )

        # input email, password, and click 'sign in'
        driver.find_element(By.ID, "ap_email").send_keys(email)
        driver.find_element(By.ID, "ap_password").send_keys(password)
        driver.find_element(By.ID, "signInSubmit").click()

        # wait until next url is fully loaded
        WebDriverWait(driver=driver, timeout=10).until(
            lambda x: x.execute_script("return document.readyState === 'complete'")
        )

        # download ratings.csv
        driver.get("https://www.imdb.com/user/ur95934592/ratings/export")

        # wait until download is done
        WebDriverWait(driver=driver, timeout=10).until(
            lambda x: x.execute_script("return document.readyState === 'complete'")
        )

        time.sleep(3)  # sometimes the above wait doesn't work, so wait extra time as caution

        driver.close()  # close the driver
    except selenium.common.exceptions.NoSuchElementException:
        print("couldn't find element in html")
    except selenium.common.exceptions.TimeoutException:
        print("web driver timed out. check email and password are correct, and that URLs are correct.")
    except FileNotFoundError:
        print("file not found. ratings.csv most likely not downloaded fully/correctly")


if __name__ == "__main__":
    main()

import time
import urllib.request
from bs4 import BeautifulSoup as bs
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


def main():
    loginUrl = "https://www.imdb.com/registration/signin"

    html = requests.get(loginUrl)
    soup = bs(html.text, 'html.parser')
    imdbLoginUrl = soup.find('a', class_='list-group-item')

    if imdbLoginUrl:
        imdbLoginUrl = imdbLoginUrl.get('href')
    else:
        print("login url not found.")
        return

    # email = input("email: ")
    email = "brendan.mccann02@gmail.com"
    password = input("password: ")

    options = webdriver.ChromeOptions()
    prefs = {"download.default_directory": "/home/brendanmcc02/Desktop/projects/film-rec/data/"}
    options.add_experimental_option("prefs", prefs)

    # initialize the Chrome driver
    driver = webdriver.Chrome(options=options)
    driver.get(imdbLoginUrl)
    driver.find_element("id", "ap_email").send_keys(email)
    driver.find_element("id", "ap_password").send_keys(password)
    driver.find_element("id", "signInSubmit").click()

    WebDriverWait(driver=driver, timeout=10).until(
        lambda x: x.execute_script("return document.readyState === 'complete'")
    )
    error_message = "Incorrect username or password."
    # get the errors (if there are)
    errors = driver.find_elements("css selector", ".flash-error")
    # print the errors optionally
    # for e in errors:
    #     print(e.text)
    # if we find that error message within errors, then login is failed
    if any(error_message in e.text for e in errors):
        print("[!] Login failed")
    else:
        print("[+] Login successful")

    # download ratings.csv
    driver.get("https://www.imdb.com/user/ur95934592/ratings/export")

    time.sleep(100)

    # close the driver
    driver.close()


if __name__ == "__main__":
    main()

# https://www.imdb.com/ap/signin  # =>  request url

from selenium import webdriver
import time

# https://stackoverflow.com/a/27760083
def scroll_all_the_way_down(driver):
    SCROLL_PAUSE_TIME = 0.5
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def fetch_likes_list(username):
    driver = webdriver.Firefox()
    driver.get("https://soundcloud.com/" + username + "/likes")

    scroll_all_the_way_down(driver)

    title_elements = driver.find_elements_by_class_name('soundTitle__title')
    links = [title.get_attribute("href") for title in title_elements]

    driver.close()
    return links

print(fetch_likes_list("djmcmostowiak"))

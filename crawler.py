"""

"""

import os
import json
import re
import time
import requests
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs


def get_chapters(base_url, driver):
    """Gets a list of all chapters from the webpage."""
    driver.get(base_url)
    # chapters = driver.find_elements(By.XPATH, value="//a[@href]")
    chapters = driver.find_elements_by_xpath("//a[@href]")
    chapters = [x.get_attribute("href") for x in chapters if "chapter" in x.get_attribute("href")]    
    return chapters

def get_images(chapter_url, driver):
    """Gets a list of all image links from the webpage."""
    driver.get(chapter_url)
    imgs = driver.find_elements_by_tag_name("img")
    imgs = [x.get_attribute("src") for x in imgs]
    return imgs


def parse_chapter_name(chapter_url):
    """Parses the manga name from the url. Assumes the name is between the last two forward slashes."""
    index_st = len(chapter_url) - chapter_url[len(chapter_url)-2::-1].index("/") - 1
    index_en = len(chapter_url) - 1

    return chapter_url[index_st:index_en]

def crawler():

    PATH = r"C:\Program Files\Mozilla Firefox\geckodriver.exe"
    driver = webdriver.Firefox(executable_path=PATH)
    base_url = "https://spyxmanga.com/"
    
    # Get list of chapters
    chapters = get_chapters(base_url, driver)

    # For each chapter, get list of all images
    for chap in chapters:
        chap_name = parse_chapter_name(chap)
        chap_name = Path(chap_name + "/")
        if not chap_name.is_dir():
            chap_name.mkdir(parents=True, exist_ok=True)
            driver.switch_to.new_window('tab')
            imgs = get_images(chap, driver)

            # For each image, save images to folder. Increment images by "x_of_y.jpg"
            i = 0
            for img in imgs:
                r = requests.get(img, allow_redirects=True)
                open(f"./{chap_name}/{i}_of_{len(imgs)-1}.jpg","wb").write(r.content)
                i += 1
        driver.close()
    driver.quit()

if __name__ == "__main__":
    crawler()

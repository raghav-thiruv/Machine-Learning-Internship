""" Scrapes the [ Tapas ] forum for data and organizes said data in a csv """

from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd


class Scraper:
    def __init__(self, csvpath, numposts=-1, driverpath="C:\\Users\\"
                                                        "besar\\Documents\\"
                                                        "chromedriver_win32\\"
                                                        "chromedriver.exe"):
        self.BASE_URL = "https://forums.tapas.io/"
        self._driverpath = driverpath
        self._numposts = numposts
        self._csvpath = csvpath

    @property
    def baseurl(self):
        return self.BASE_URL

    @property
    def numposts(self):
        return self._numposts

    @property
    def csvpath(self):
        return self._csvpath

    @property
    def driverpath(self):
        return self._driverpath

    def scrape(self):
        """ Executes the scrape and stores the collected data """
        browser = self.browser_setup()

        browser.get(self.baseurl)

        browser.find_element_by_xpath('//*[@id="ember878"]/a[1]').click()

        categories_urls = [category.get_attribute("href") for
                           category in
                           browser.find_elements_by_xpath('//*/section/div/a')[
                           1:]]

        data = []
        for category_url in categories_urls:
            browser.get(category_url)
            self.scroll(browser)
            a_tags = browser.find_elements_by_css_selector("a.title")
            titles = [tag.text for tag in a_tags[:self.numposts]]
            urls = [tag.get_attribute("href") for
                    tag in a_tags[:self.numposts]]
            for title, url in zip(titles, urls):
                browser.get(url)
                replies_views = self.get_topic_replies_and_views(browser)
                soup = self.get_topic_soup(browser)
                comments = self.get_comments(soup)
                data.append({"Title": title,
                             "Category": self.get_topic_category(soup),
                             "Date": self.get_post_date(soup),
                             "Likes": self.get_likes(soup),
                             "Num Replies": replies_views[0],
                             "Num Views": replies_views[1],
                             "Original Post": comments[0],
                             "Comments": comments[1:]
                             })

        browser.close()
        self.to_csv(data, self._csvpath)

    def browser_setup(self):
        """ Sets up browser and options """
        opts = Options()
        opts.headless = True
        browser = webdriver.Chrome(self.driverpath, options=opts)
        return browser

    def scroll(self, browser):
        """ Determines scroll execution """
        self.infinite_scroll(browser) if self.numposts == -1 else \
            self.controlled_scroll(browser, self.numposts)

    @staticmethod
    def to_csv(data, path):
        """ Produces csv file from data """
        pd.DataFrame(data).to_csv(path, encoding='utf-8')

    @staticmethod
    def controlled_scroll(browser, post_num):
        """ Limits scroll to match preferred # of posts to gather """
        for i in range(int(post_num / (1079 / 35))):  # 35range -> 1079posts
            browser.execute_script("window.scrollTo"
                                   "(0,document.body.scrollHeight)")
            time.sleep(1)

    @staticmethod
    def infinite_scroll(browser):
        """ Scrolls down until end and allows the page to buffer """
        while True:
            former_height = browser.execute_script("return document.body"
                                                   ".scrollHeight")
            browser.execute_script("window.scrollTo"
                                   "(0,document.body.scrollHeight)")
            time.sleep(1)
            current_height = browser.execute_script("return document.body"
                                                    ".scrollHeight")
            if former_height == current_height:
                break

    @staticmethod
    def get_topic_soup(browser):
        """ Gets page HTML as a BeautifulSoup object """
        while (browser.execute_script(
                "window.scrollTo(0,document.body.scrollHeight)")):
            pass
        return BeautifulSoup(browser.page_source, 'html.parser')

    @staticmethod
    def get_topic_category(topic_soup):
        """ Gets the category of the topic """
        topic_category = topic_soup.find("span",
                                         {"class": "badge-category"
                                                   " clear-badge"})
        return topic_category.get_text()

    @staticmethod
    def get_topic_replies_and_views(browser):
        """ Gets the replies and views of the topic """
        try:
            browser.find_element_by_class_name("map")
            numbers = browser.find_elements_by_class_name("number")
            return [numbers[i].text for i in range(2)]
        except NoSuchElementException:
            return ["Map Unavailable", "Map Unavailable"]

    @staticmethod
    def get_comments(topic_soup):
        """ Gets the comments of the topic """
        post_stream = topic_soup.find("div", {"class": "post-stream"})
        post_divs = post_stream.find_all("div",
                                         {"class": ["topic-post clearfix"
                                                    " topic-owner regular",
                                                    "topic-post clearfix"
                                                    " regular"]})

        return ["Aberrant HTML"] if len(post_divs) == 0 else \
            [post_divs[i].find("div", {"class": "cooked"}).text.strip() for
             i in range(len(post_divs))]

    @staticmethod
    def get_post_date(topic_soup):
        """ Gets the original post date """
        try:
            return topic_soup.find("span", {"class": "relative-date"})["title"]
        except KeyError:
            return topic_soup.find("a",
                                   {"class": "widget-link start-date"}).text

    @staticmethod
    def get_likes(topic_soup):
        """ Gets the like count """
        try:
            return topic_soup.find("button", {
                "class": "widget-button like-count highlight-action"}).text. \
                replace(" Likes", "").replace(" Like", "")
        except AttributeError:
            return "0"


if __name__ == '__main__':
    Scraper("TestCSV.csv", 1000).scrape()

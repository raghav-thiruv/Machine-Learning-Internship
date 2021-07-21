import requests
from bs4 import BeautifulSoup
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options


def scrape_tutorial():
    BASE_URL = "https://forums.t-nation.com/"

    """ With BeautifulSoup """
    page = requests.get(BASE_URL)
    soup = BeautifulSoup(page.content, "html.parser")

    # print(soup.prettify())

    # print(soup.find_all("span"))

    titles = [title.text for title in soup.find_all("span") if "\n" not in
              title.text]

    titles = []
    for title in soup.find_all("span"):
        if "\n" not in title.text:
            titles.append(title.text)

    print(titles)

    # print(soup.find_all("a"))
    urls = [url["href"] for url in soup.find_all("a") if "/c/" in url["href"]]
    print(urls)

    """ Check if same amount of titles and urls """
    assert len(urls) == len(titles)

    first_topic_titles = []
    for url in urls:
        page = requests.get(BASE_URL + url)
        soup = BeautifulSoup(page.content, "html.parser")
        cls = "title raw-link raw-topic-link"
        first_topic_titles.append(soup.find("a", class_=cls).text)

    print(first_topic_titles)

    """ With Selenium """
    PATH = 'C:\\Users\\besar\\Documents\\gecko' \
           'driver-v0.29.1-win64\\geckodriver.exe'

    opts = Options()
    opts.headless = True
    assert opts.headless
    browser = Firefox(options=opts,
                      executable_path=PATH)
    browser.get(BASE_URL)

    tags = browser.find_elements_by_class_name("category-title-link")
    titles_urls = [[tag.text, tag.get_attribute("href")] for tag in tags]
    print(titles_urls)

    first_topics = []
    for title_url in titles_urls:
        browser.get(title_url[1])
        first_topics.append(browser.
                            find_element_by_class_name("link-top-line").text)

    print(first_topics)

    browser.close()


if __name__ == '__main__':
    scrape_tutorial()
